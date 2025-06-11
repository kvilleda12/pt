import os
import fitz
import io
from datetime import datetime
from backend.database.database import SessionLocal, Textbook, Body # adjust import path as needed
import json
import hashlib


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


#getting images and text from sources. 
def extract_text_images_from_pdf(files, into='text_files', other='image_storage', json_path='tracker.json', c='counter.txt', context_overlap=True):
    # Set up paths
    base_dir = os.path.dirname(__file__)
    text_pointer = os.path.abspath(os.path.join(base_dir, '..', into))
    image_pointer = os.path.abspath(os.path.join(base_dir, '..', other))
    j_p = os.path.abspath(os.path.join(base_dir, '..', json_path))
    counter_pointer = os.path.abspath(os.path.join(base_dir, '..', c))

    os.makedirs(text_pointer, exist_ok=True)
    os.makedirs(image_pointer, exist_ok=True)

    j_file = []
    existing_ids = set()
    if os.path.exists(j_p):
        with open(j_p, 'r', encoding='utf-8') as json_file:
            try:
                existing_entries = json.load(json_file)
                existing_ids = {entry['id'] for entry in existing_entries}
                j_file.extend(existing_entries)  # preserve previous entries
            except json.JSONDecodeError:
                print("error. Can't find json")
    img_counter = 0


    if os.path.exists(counter_pointer):
        with open(counter_pointer, 'r') as f:
            img_counter = int(f.read().strip() or 0)

    seen_hashes = set()

    for file in files:
        document = fitz.open(file)
        base, _ext = os.path.splitext(os.path.basename(file))
        txt_name = base + ".txt"
        txt_path = os.path.join(text_pointer, txt_name)

        # Save PDF text to .txt file
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            for page in document:
                text = page.get_text()
                txt_file.write(text + '\n\n')

        # Gather image references
        image_refs = []
        for page_num, page in enumerate(document, start=1):
            for img in page.get_images(full=True):
                xref = img[0]
                image_refs.append((page_num, xref))

        # Skip first and last 10 images
        usable_images = image_refs[10:-10]

        for page_num, xref in usable_images:
            page = document[page_num - 1]
            img_id = f"IMG_{img_counter:06d}"
            img_counter += 1

            try:
                pix = fitz.Pixmap(document, xref) #make sure its rgb
                if pix.n != 3:
                    pix = fitz.Pixmap(fitz.csRGB, pix)

                # Compute hash to detect duplicates
                img_bytes = pix.tobytes()
                img_hash = hashlib.md5(img_bytes).hexdigest()

                if img_hash in seen_hashes:
                    print(f" duplicate: {img_id}")
                    continue
                seen_hashes.add(img_hash)

                # Save image
                img_filename = f"{img_id}.png"
                img_path = os.path.join(image_pointer, img_filename)
                pix.save(img_path)
                pix = None

            except Exception as e:
                print(f"failed to save {img_id}: {e}")
                continue

            #to get context
            context_text = ''
            if context_overlap:
                try:
                    image_rect = fitz.Rect(fitz.Pixmap(document, xref).irect)
                    blocks = page.get_text('dict')['blocks']
                    context_lines = []
                    for tb in blocks:
                        if tb.get("type") == 0 and "bbox" in tb:
                            text_rect = fitz.Rect(tb["bbox"])
                        if image_rect.intersects(text_rect) or image_rect.is_near(text_rect, 100):  # Adjust 100 as needed
                            context_lines.append(tb["text"].strip())

                    context_text = "\n\n".join(context_lines)
                except Exception as e: 
                    print(" no context for {img_id}: e")
                    context_text = ""

            if img_id not in existing_ids:
                j_file.append({
                    'id': img_id,
                    'context': context_text
                })

        document.close()

    # Save context JSON
    with open(j_p, 'w', encoding='utf-8') as json_file:
        json.dump(j_file, json_file, indent=4)

    # Update counter
    with open(counter_pointer, 'w', encoding='utf-8') as update:
        update.write(str(img_counter))

    print(f"saved '{into}', images to '{other}', and context JSON to '{json_path}'.")


def main():
    files = get_paths()
    #extract_file_info_for_db(files)
    extract_text_images_from_pdf(files, into = 'text_files', other = 'image_storage', json_path = 'tracker.json', c = 'counter.txt', context_overlap = True )

if __name__ == "__main__":
    main()



    


