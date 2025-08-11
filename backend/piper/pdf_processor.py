import os
import fitz
import io
import json
import hashlib
import pytesseract
import cv2
import re
import numpy as np
import shutil
from PIL import Image
from sqlalchemy.orm import Session

from .config import IMAGE_STORAGE_DIR, CAPTIONS_JSON_PATH, PROCESSED_ARCHIVE_DIR
from backend.database.database import SessionLocal, Image as DBImage, Research_paper, Textbook

# Helpers
def extract_page_image(page, dpi=200):
    pix_img = page.get_pixmap(dpi=dpi)
    return Image.open(io.BytesIO(pix_img.tobytes("png")))

def ocr_page_text(processed_img):
    return pytesseract.image_to_data(processed_img, output_type=pytesseract.Output.DICT)

def detect_image_regions(processed_img, min_area=5000):
    open_cv_image = np.array(processed_img)
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    grayscale = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(grayscale, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    regions = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w * h > min_area and (0.1 < w / float(h) < 10.0 if h > 0 else 0):
            regions.append((x, y, w, h))
    return regions

def extract_all_captions(ocr_dict):
    captions = []
    if not ocr_dict or 'text' not in ocr_dict: return captions
    lines = {}
    for i in range(len(ocr_dict['text'])):
        key = (ocr_dict['block_num'][i], ocr_dict['line_num'][i])
        if key not in lines: lines[key] = []
        lines[key].append(i)
    for idxs in lines.values():
        line_text = ' '.join(ocr_dict['text'][i] for i in idxs if ocr_dict['text'][i].strip()).strip()
        if re.search(r"^(figure|fig|chart|table)\s*[\d\.\-A-Za-z]+[:\.]?", line_text, re.IGNORECASE):
            x_coords = [ocr_dict['left'][i] for i in idxs]
            y_coords = [ocr_dict['top'][i] for i in idxs]
            captions.append({'center': (sum(x_coords)/len(x_coords), sum(y_coords)/len(y_coords)), 'text': line_text})
    return captions

def match_caption_to_region(captions, region):
    if not captions: return "No caption found"
    x_img, y_img, w_img, h_img = region
    center_x_img, bottom_y_img = x_img + w_img / 2, y_img + h_img
    best_match, min_dist = None, float('inf')
    for caption in captions:
        center_x_cap, center_y_cap = caption['center']
        if center_y_cap > bottom_y_img:
            distance = np.sqrt((2 * (center_x_img - center_x_cap))**2 + (center_y_cap - bottom_y_img)**2)
            if distance < min_dist:
                min_dist, best_match = distance, caption['text']
    return best_match if best_match else "No caption found"

def save_image_file(processed_img, bbox, out_dir, img_id, seen_hashes):
    x, y, w, h = bbox
    if w < 50 or h < 50: return None, None
    crop = processed_img.crop((x, y, x + w, y + h)).convert('L')
    buf = io.BytesIO()
    crop.save(buf, format='PNG')
    img_bytes = buf.getvalue()
    hsh = hashlib.md5(img_bytes).hexdigest()
    if hsh in seen_hashes: return None, None
    seen_hashes.add(hsh)
    file_name = f"{img_id}.png"
    path = os.path.join(out_dir, file_name)
    crop.save(path)
    return img_bytes, file_name

# --- Main Processing Function ---
def process_pdf_file(pdf_path: str, source_type: str):
    #Processes a single PDF file to extract images, save them to the DB, and update captions.json
    db = SessionLocal()
    seen_hashes = set()
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    record = None
    if source_type == 'paper':
        record = db.query(Research_paper).filter(Research_paper.paper_name == base_name).first()
    elif source_type == 'textbook':
        record = db.query(Textbook).filter(Textbook.textbook_name == base_name).first()

    if not record:
        print(f"⚠️ Could not find DB record for '{base_name}'. Aborting processing.")
        db.close()
        return

    record_id = record.id if source_type == 'paper' else record.textbook_id
    print(f"\n🔬 Processing {source_type}: {base_name}")
    
    try:
        doc = fitz.open(pdf_path)
        new_captions = []
        for page_num, page in enumerate(doc, start=1):
            processed_img = extract_page_image(page)
            ocr_dict = ocr_page_text(processed_img)
            regions = detect_image_regions(processed_img)
            if not regions: continue
            
            captions = extract_all_captions(ocr_dict)
            for i, bbox in enumerate(regions):
                img_id = f"img_{source_type}_{record_id}_{page_num}_{i+1}"
                img_bytes, file_name = save_image_file(processed_img, bbox, IMAGE_STORAGE_DIR, img_id, seen_hashes)
                if not img_bytes: continue
                
                db_image = DBImage(id=img_id, size=len(img_bytes), file_name=file_name, page=page_num, has_context=True)
                if source_type == 'paper': db_image.paper_id = record_id
                else: db_image.textbook_id = record_id
                db.add(db_image)

                caption_text = match_caption_to_region(captions, bbox)
                new_captions.append({'id': img_id, 'caption': caption_text})
                if caption_text == "No caption found": db_image.has_context = False
                print(f"  -> Processed image {file_name}")
        
        db.commit()

        if new_captions:
            all_captions = []
            if os.path.exists(CAPTIONS_JSON_PATH):
                with open(CAPTIONS_JSON_PATH, 'r') as f:
                    try: all_captions = json.load(f)
                    except json.JSONDecodeError: pass
            all_captions.extend(new_captions)
            with open(CAPTIONS_JSON_PATH, 'w') as f:
                json.dump(all_captions, f, indent=4)
        
        shutil.move(pdf_path, os.path.join(PROCESSED_ARCHIVE_DIR, os.path.basename(pdf_path)))
        print(f"🗄️ Moved '{os.path.basename(pdf_path)}' to archive.")
    except Exception as e:
        print(f"‼️ Failed to process {os.path.basename(pdf_path)}: {e}")
        db.rollback()
    finally:
        db.close()