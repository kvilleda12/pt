import os
import fitz
import io
from datetime import datetime
from backend.database.database import SessionLocal, Textbook, Body # adjust import path as needed
import json
import hashlib
import pytesseract
from PIL import Image
import re
import cv2
import numpy as np


extensions_allowed = [".pdf", ".epub", ".docx", ".txt"]

#convert all the files in file_sources into a readable file list
def get_paths (folder_name = 'file_sources'): #iterating over the paths 
    dir = os.path.dirname(__file__)
    folder_path = os.path.abspath(os.path.join(dir, "..", "file_sources"))
    files = [] 
    for f in os.listdir(folder_path):
        if any(f.lower().endswith(ext) for ext in extensions_allowed):
            path = os.path.join( folder_path, f)
            files.append(path)
    return files #returns list of paths

#to get the information necessary for the datable. We only actually want to store the names for resource referencing
def extract_file_info_for_db(files):
   db =  SessionLocal()
   for path in files: 
    #file_name = os.path.basename(path)
    size = os.path.getsize(path)

    split_title = path.split('--')

    title = split_title[0].strip().lower()
    fp = '/users/kevinvilleda/pt/backend/file_sources/'
    title, _ext = os.path.splitext(os.path.basename(fp))#remove the path from the file``
    author = split_title[1].strip() if len(split_title) > 1 else "unknown"
    part_id = 'e'  # default = everything
    title_keywords = {
            'neck': 'n',
            'chest': 'c',
            'head': 'h',
            'arms': 'a',
            'legs': 'l',
            'shoulders': 's',
            'back': 'b'
        }
    for keyword, pid in title_keywords.items():
       if keyword in title: 
          part_id = pid
          break 
    new_t = Textbook(
       textbook_name= title, 
       author = author,
       size = size ,
       date_added = datetime.utcnow(),
       where = 'Annas',
       part_id = part_id, 
    )
    db.add(new_t)
   db.commit() 
   db.close()
   print("files processed")


#find the images within a page   
def extract_page_image(page, dpi=300):
    pix = page.get_pixmap(dpi=dpi)
    img_bytes = pix.tobytes("png")
    pil_img = Image.open(io.BytesIO(img_bytes))
    return pil_img, img_bytes

#get all the text out of the image. Will be used to convert pdf test into a txt file
def ocr_page_text(pil_img):
    full_text = pytesseract.image_to_string(pil_img)
    ocr_data = pytesseract.image_to_data(pil_img, output_type=pytesseract.Output.DICT)
    return full_text, ocr_data

#find the image regions within a page. So we can find the captions afterwards. 
def detect_image_regions(pil_img, min_area=5000):
    open_cv_image = np.array(pil_img)
    # Convert RGB to BGR
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
    
    # Use an adaptive threshold for better results on varied backgrounds
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    regions = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        aspect_ratio = w / float(h) if h > 0 else 0

        # Filter based on area and aspect ratio
        if area > min_area and (0.1 < aspect_ratio < 10.0):
             regions.append((x, y, w, h))
             
    return regions
def has_content_started(ocr_data, page_num, total_pages):
    """
    Check if we've reached the main content of the book.
    """
    if not ocr_data or 'text' not in ocr_data:
        return False

    full_text = ' '.join([text.strip() for text in ocr_data['text'] if text.strip()])

    # If we are very deep into the book, it's safe to assume content has started.
    # This avoids issues with OCR failing on a single content page.
    if page_num > 25 or page_num > total_pages * 0.15:
        return True

    # Look for patterns that indicate actual content has started
    content_patterns = [
        rf'\b(page|pg\.?)\s+{page_num}\b', # "Page 5" or "pg. 5"
        r'\bchapter\s+\d+',
        r'\bsection\s+\d+',
        r'\b(figure|fig|table)\s+\d+',
        r'introduction' # The word "Introduction" is a strong signal
    ]

    for pattern in content_patterns:
        if re.search(pattern, full_text, re.IGNORECASE):
            return True

    # Check for substantial text content (avoids sparse title pages)
    words = [word for word in ocr_data['text'] if len(word.strip()) > 2]
    if len(words) > 50:
        return True

    return False
                            
#to find the captions we get an image and then we look use euclidean distance of the blob to find the nearest 'figure' description. None if there is
def extract_all_captions(ocr_data, word_limit=50):
    captions = []
    if not ocr_data or 'text' not in ocr_data:
        return captions

    n = len(ocr_data['text'])
    
    # Pre-group words by their block and line numbers for better context
    lines = {}
    for i in range(n):
        block_num = ocr_data['block_num'][i]
        line_num = ocr_data['line_num'][i]
        if (block_num, line_num) not in lines:
            lines[(block_num, line_num)] = []
        lines[(block_num, line_num)].append(i)

    for (block_num, line_num), idxs in lines.items():
        line_text = ' '.join(ocr_data['text'][i] for i in idxs if ocr_data['text'][i].strip()).strip()

        # Improved Regex:
        # - Handles "Figure", "Fig", "Chart", "Table"
        # - More flexible with spacing and punctuation
        match = re.search(r"^(?:figure|fig|chart|table)\s*[\d\.\-A-Za-z]+[:\.]?", line_text, re.IGNORECASE)
        
        if match:
            # We found a potential caption start
            
            # --- Better Bounding Box Calculation ---
            # Get the bounding box of the entire matched line
            x_coords = [ocr_data['left'][i] for i in idxs]
            y_coords = [ocr_data['top'][i] for i in idxs]
            w_coords = [ocr_data['width'][i] for i in idxs]
            h_coords = [ocr_data['height'][i] for i in idxs]
            
            x, y = min(x_coords), min(y_coords)
            w = max(x_coords) + max(w_coords) - x
            h = max(y_coords) + max(h_coords) - y

            # Use the center of this more accurate bounding box
            center_x = x + w / 2
            center_y = y + h / 2

            # --- Full Caption Text Aggregation ---
            # Start with the current line
            full_caption_text = [line_text]
            
            # Look ahead for subsequent lines that are part of the same caption
            # (This is a simplified lookahead, more advanced logic could be added)
            
            # For now, we'll just use a word limit from the start of the caption
            start_index = idxs[0]
            words = []
            for i in range(start_index, min(start_index + word_limit, n)):
                 words.append(ocr_data['text'][i])
            
            final_caption = ' '.join(words).strip()


            captions.append({
                'center': (center_x, center_y),
                'text': final_caption,
                'bbox': (x, y, w, h) # Store for debugging
            })
    return captions

def match_caption_to_region(captions, region):
    if not captions:
        return "No caption found"

    x_img, y_img, w_img, h_img = region
    center_x_img = x_img + w_img / 2
    bottom_y_img = y_img + h_img

    best_match = None
    min_dist = float('inf')

    for caption in captions:
        center_x_cap, center_y_cap = caption['center']

        # Prioritize captions that are BELOW the image
        if center_y_cap > bottom_y_img:
            # Calculate a weighted distance
            # Give much more weight to horizontal distance to favor vertical alignment
            dx = (center_x_img - center_x_cap)
            dy = (center_y_cap - bottom_y_img) # Distance from bottom of image to top of caption
            
            # Weighted Euclidean distance
            distance = np.sqrt((2 * dx)**2 + dy**2) # Weight horizontal distance more

            if distance < min_dist:
                min_dist = distance
                best_match = caption['text']

    return best_match if best_match else "No caption found"

def save_image(pil_img, bbox, out_dir, img_id, seen_hashes):
    x, y, w, h = bbox
    crop = pil_img.crop((x, y, x+w, y+h))
    
    # Filter out single-letter image crops (previous working version)
    try:
        letter_text = pytesseract.image_to_string(crop, config='--psm 10').strip()
        if len(letter_text) == 1 and re.match(r'^[A-Za-z0-9]$', letter_text):
            print(f"Skipping letter-only crop for {img_id}: '{letter_text}'")
            return None
    except Exception:
        pass

    # Optional whitespace filter
    try:
        gray = crop.convert('L')
        arr = np.array(gray)
        white_thresh = 240
        white_pixels = np.sum(arr >= white_thresh)
        total = arr.size
        if white_pixels / total > 0.4:
            print(f"Skipping mostly-white crop for {img_id}")
            return None
    except Exception:
        pass
    crop = crop.convert('L')
    # Duplicate check & save
    buf = io.BytesIO()
    crop.save(buf, format='PNG')
    img_bytes = buf.getvalue()
    hsh = hashlib.md5(img_bytes).hexdigest()
    if hsh in seen_hashes:
        print(f"Skipping duplicate: {img_id}")
        return None
    seen_hashes.add(hsh)

    fname = f"{img_id}.png"
    path = os.path.join(out_dir, fname)
    crop.save(path)
    print(f"Saved image region: {fname}")
    return img_bytes


def save_tracker_entry(j_file, img_id, context_text, existing_ids):
    entry_context = context_text if context_text else "No caption found"
    if img_id not in existing_ids:
        j_file.append({'id': img_id, 'context': entry_context})


def process_pdf_file(file, text_pointer, image_pointer, existing_ids, seen_hashes, img_counter, j_file, context_overlap=True, page_limit = None):
    doc = fitz.open(file)
    base = os.path.splitext(os.path.basename(file))[0]
    txt_path = os.path.join(text_pointer, base + ".txt")
    content_has_begun = False
    with open(txt_path, 'w', encoding='utf-8') as tf:
        for page_num, page in enumerate(doc, start=1):
            print(f"\n--- Analyzing Page {page_num} of {len(doc)} ---")
            pil_img, _ = extract_page_image(page)
            full_text, ocr_data = ocr_page_text(pil_img)
            if not content_has_begun:
                if has_content_started(ocr_data, page_num, len(doc)):
                    print(f"*** Content detected on page {page_num}. Starting extraction. ***")
                    content_has_begun = True
                else:
                    print(f"Skipping page {page_num} (likely front matter).")
                    continue # Skip to the next page
            tf.write(f"\n\n--- Page {page_num} ---\n{full_text}")
            regions = detect_image_regions(pil_img)
            captions = extract_all_captions(ocr_data)
            print(f"Page {page_num}: Found {len(regions)} potential image regions.")
            print(f"Page {page_num}: Found {len(captions)} potential captions.")
            if captions:
                for i, cap in enumerate(captions):
                    print(f"  - Caption {i}: '{cap['text'][:50]}...' at {cap['center']}")
            for bbox in regions:
                img_id = f"IMG_{img_counter:06d}"; img_counter += 1
                img_bytes = save_image(pil_img, bbox, image_pointer, img_id, seen_hashes)
                if not img_bytes:
                    continue
                context_text = match_caption_to_region(captions, bbox)
                if context_text == "No caption found":
                    print(f"!! Failed to find caption for image {img_id} at {bbox}")
                save_tracker_entry(j_file, img_id, context_text, existing_ids)
    doc.close()
    return img_counter

def extract_text_images_from_pdfs(files, into='text_files', other='image_storage', json_path='tracker.json', c='counter.txt', context_overlap=True):
    base_dir = os.path.dirname(__file__)
    text_pointer = os.path.abspath(os.path.join(base_dir, '..', into))
    image_pointer = os.path.abspath(os.path.join(base_dir, '..', other))
    j_p = os.path.abspath(os.path.join(base_dir, '..', json_path))
    counter_pointer = os.path.abspath(os.path.join(base_dir, '..', c))
    os.makedirs(text_pointer, exist_ok=True); os.makedirs(image_pointer, exist_ok=True)
    j_file = []; existing_ids = set()
    if os.path.exists(j_p):
        with open(j_p, 'r', encoding='utf-8') as jf: data = json.load(jf); existing_ids = {e['id'] for e in data}; j_file.extend(data)
    img_counter = 0
    if os.path.exists(counter_pointer): img_counter = int(open(counter_pointer).read().strip() or 0)
    for f in files:
        img_counter = process_pdf_file(f, text_pointer, image_pointer, existing_ids, seen_hashes=set(), img_counter=img_counter, j_file=j_file, context_overlap=context_overlap)
    with open(j_p, 'w', encoding='utf-8') as jf: json.dump(j_file, jf, indent=4)
    open(counter_pointer, 'w').write(str(img_counter))
    print(f"Saved text to '{into}', images to '{other}', and context JSON to '{json_path}'.")

def test_first_20_pages_from_file_sources():
    """
    Sets up a clean test environment and runs the full extraction and
    captioning process on the first 20 pages of each PDF found in
    the file_sources directory.
    """
    from pathlib import Path
    import shutil

    print("--- STARTING TEST: Processing first 20 pages of each PDF ---")

    # 1. Setup test directories and paths
    base = os.path.dirname(__file__)
    src_dir = os.path.abspath(os.path.join(base, '..', 'file_sources'))
    txt_out_dir = os.path.abspath(os.path.join(base, '..', 'test_text'))
    img_out_dir = os.path.abspath(os.path.join(base, '..', 'test_images'))
    tracker_json_path = os.path.abspath(os.path.join(base, '..', 'test_tracker.json'))

    # 2. Clean up previous test runs
    shutil.rmtree(txt_out_dir, ignore_errors=True)
    shutil.rmtree(img_out_dir, ignore_errors=True)
    if os.path.exists(tracker_json_path):
        os.remove(tracker_json_path)

    # 3. Recreate test directories
    os.makedirs(txt_out_dir, exist_ok=True)
    os.makedirs(img_out_dir, exist_ok=True)

    # 4. Initialize tracking variables
    j_file_data = []
    existing_ids = set()
    img_counter = 0
    seen_hashes = set()

    # 5. Loop through PDFs and process the first 20 pages of each
    pdf_files = list(Path(src_dir).glob('*.pdf'))
    if not pdf_files:
        print("No PDF files found in 'file_sources' directory. Test cannot run.")
        return

    for pdf_path in pdf_files:
        print(f"\n>>> Processing test file: {pdf_path.name}")
        # Call the main processing function, but with a page limit!
        img_counter = process_pdf_file(
            file=str(pdf_path),
            text_pointer=txt_out_dir,
            image_pointer=img_out_dir,
            existing_ids=existing_ids,
            seen_hashes=seen_hashes,
            img_counter=img_counter,
            j_file=j_file_data,
            page_limit=20  # <-- The crucial argument for the test
        )

    # 6. Save the final results of the test run
    with open(tracker_json_path, 'w', encoding='utf-8') as f:
        json.dump(j_file_data, f, indent=4)

    print("\n--- TEST COMPLETE ---")
    print(f"Total images extracted: {len(j_file_data)}")
    print(f"Test text files saved to: '{txt_out_dir}'")
    print(f"Test images saved to: '{img_out_dir}'")
    print(f"Test tracker JSON saved to: '{tracker_json_path}'")
def main():
    files = get_paths()
    #extract_file_info_for_db(files)
    #extract_text_images_from_pdfs(files, into = 'text_files', other = 'image_storage', json_path = 'tracker.json', c = 'counter.txt', context_overlap = True )
    test_first_20_pages_from_file_sources()

if __name__ == "__main__":
    main()
