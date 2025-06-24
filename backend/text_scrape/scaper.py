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
    gray_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2GRAY) #turn to nparray and use grayscale
    _, thresh = cv2.threshold(gray_img, 240, 255, cv2.THRESH_BINARY_INV) #mask to filter out background and content, The background becomes black and the other becomes lighter
    boundaries, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #find the outline of blobs. Basically use countour and find the image boundaries and map the image in that way
    regions = [] #to save the actual coordiantes of waht we think is an image
    
    for cnt in boundaries: #go through and find iamges and ignore punctuations. 
        x, y, w, h = cv2.boundingRect(cnt)
        if w*h >= min_area:
            regions.append((x, y, w, h))
    return regions
def has_page_number_started(ocr_data, page_num):
    """
    Check if we've reached actual content by looking for "Page X" or similar patterns
    """
    if not ocr_data or 'text' not in ocr_data:
        return False
        
    full_text = ' '.join([text.strip() for text in ocr_data['text'] if text.strip()])
    
    # Look for patterns that indicate actual content has started
    content_patterns = [
        rf'\bpage\s+{page_num}\b',
        r'\bchapter\s+\d+',
        r'\bsection\s+\d+',
        r'\b\d+\.\d+\b',  # Section numbers like 1.1, 2.3, etc.
        r'\bfigure\s+\d+',
        r'\btable\s+\d+'
    ]
    
    for pattern in content_patterns:
        if re.search(pattern, full_text, re.IGNORECASE):
            return True
    
    # Also check if we have substantial text content (not just title pages)
    words = [word.strip() for word in ocr_data['text'] if word.strip() and len(word.strip()) > 2]
    if len(words) > 20:  # Substantial content usually means we're past title pages
        return True
        
    return False
                            
#to find the captions we get an image and then we look use euclidean distance of the blob to find the nearest 'figure' description. None if there is
def extract_all_captions(ocr_data, word_limit=50):
    captions = []
    if not ocr_data or 'text' not in ocr_data: 
        print("nothing in this yawn")
        return captions
    n = len(ocr_data['text'])
    print(f"processing {n} elements")
    # group words by line
    lines = {}
    for i in range(n):
        line = ocr_data['line_num'][i]
        lines.setdefault(line, []).append(i)
    for line_num, idxs in lines.items():
        words = [ocr_data['text'][i].strip() for i in idxs]
        line_text = ' '.join(w for w in words if w)
        print(f'line: {line_num}, text: {line_text}')
        if re.search(r"\b(?:figure|fig)\s*\.?\s*\d+", line_text, re.IGNORECASE):
            print(f"Found figure caption at line {line_num}")
            # record bbox center of this line
            xs = [ocr_data['left'][i] for i in idxs]
            ys = [ocr_data['top'][i] for i in idxs]
            ws = [ocr_data['width'][i] for i in idxs]
            hs = [ocr_data['height'][i] for i in idxs]
            cx = int(np.mean([x + w/2 for x,w in zip(xs,ws)]))
            cy = int(np.mean([y + h/2 for y,h in zip(ys,hs)]))
            # capture following words up to limit
            start = idxs[0]
            end = min(idxs[-1] + word_limit, n)
            caption_words = [ocr_data['text'][j] for j in range(start, end)]
            caption_text = ' '.join(w for w in caption_words if w)
            caption_entry = {'center':(cx,cy),'line_text':(caption_words), 'text':caption_text}
            captions.append(caption_entry)
            print("these are the captions:", caption_text)
    return captions

def match_caption_to_region(captions, region):
    if not captions:
        return "Nothing found"
    x, y, w, h = region
    rx, ry = x + w/2, y + h/2
    dists = [((rx - cx)**2 + (ry - cy)**2, cap['text']) for cap in captions for cx, cy in [cap['center']]]
    dists.sort(key=lambda t: t[0])
    print(dists)
    return dists[0][1]

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


def process_pdf_file(file, text_pointer, image_pointer, existing_ids, seen_hashes, img_counter, j_file, context_overlap=True):
    doc = fitz.open(file)
    base = os.path.splitext(os.path.basename(file))[0]
    txt_path = os.path.join(text_pointer, base + ".txt")
    with open(txt_path, 'w', encoding='utf-8') as tf:
        for page_num, page in enumerate(doc, start=1):
            pil_img, _ = extract_page_image(page)
            full_text, ocr_data = ocr_page_text(pil_img)
            tf.write(f"\n\n--- Page {page_num} ---\n{full_text}")
            regions = detect_image_regions(pil_img)
            captions = extract_all_captions(ocr_data)
            print('this is caption:', captions)
            for bbox in regions:
                img_id = f"IMG_{img_counter:06d}"; img_counter += 1
                img_bytes = save_image(pil_img, bbox, image_pointer, img_id, seen_hashes)
                if not img_bytes:
                    continue
                context_text = match_caption_to_region(captions, bbox) if context_overlap else ""
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
    from pathlib import Path
    import shutil
    base = os.path.dirname(__file__)
    src = os.path.abspath(os.path.join(base, '..', 'file_sources'))
    txt_out = os.path.abspath(os.path.join(base, '..', 'test_text'))
    img_out = os.path.abspath(os.path.join(base, '..', 'test_images'))
    tj = os.path.abspath(os.path.join(base, '..', 'test_tracker.json'))
    cf = os.path.abspath(os.path.join(base, '..', 'test_counter.txt'))
    shutil.rmtree(txt_out, ignore_errors=True)
    shutil.rmtree(img_out, ignore_errors=True)
    if os.path.exists(tj): os.remove(tj)
    if os.path.exists(cf): os.remove(cf)
    os.makedirs(txt_out, exist_ok=True)
    os.makedirs(img_out, exist_ok=True)
    tracker = []
    existing = set()
    counter = 0
    seen = set()
    for pdf in Path(src).glob('*.pdf'):
        doc = fitz.open(str(pdf))
        base_name = pdf.stem
        for i in range(1, min(20, len(doc)) + 1):
            pil_img, _ = extract_page_image(doc[i-1])
            text, ocr_data = ocr_page_text(pil_img)
            open(os.path.join(txt_out, f"{base_name}.txt"), 'a').write(f"\n\n--- Page {i} ---\n{text}")
            regions = detect_image_regions(pil_img)
            captions = extract_all_captions(ocr_data)
            for bbox in regions:
                img_id = f"IMG_{counter:06d}"; counter += 1
                img_bytes = save_image(pil_img, bbox, img_out, img_id, seen)
                if not img_bytes: continue
                context = match_caption_to_region(captions, bbox)
                print(context)
                save_tracker_entry(tracker, img_id, context, existing)
        doc.close()
    with open(tj, 'w') as f:
        json.dump(tracker, f, indent=4)
    open(cf, 'w').write(str(counter))
    print(f"Test complete. Text: {txt_out}, Images: {img_out}, Tracker: {tj}")
def main():
    files = get_paths()
    #extract_file_info_for_db(files)
    #extract_text_images_from_pdfs(files, into = 'text_files', other = 'image_storage', json_path = 'tracker.json', c = 'counter.txt', context_overlap = True )
    test_first_20_pages_from_file_sources()

if __name__ == "__main__":
    main()



    


