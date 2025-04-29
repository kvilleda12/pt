import os
import fitz
import io
from datetime import datetime
from backend.database.database import SessionLocal, Textbook, Body # adjust import path as needed
import json


extensions_allowed = [".pdf", ".epub", ".docx", ".txt"]

def get_paths (folder_name = 'file_sources'): #iterating over the paths 
    dir = os.path.dirname(__file__)
    folder_path = os.path.abspath(os.path.join(dir, "..", "file_sources"))
    files = [] 
    for f in os.listdir(folder_path):
        if any(f.lower().endswith(ext) for ext in extensions_allowed):
            path = os.path.join( folder_path, f)
            files.append(path)
    return files #returns list of paths

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
   #extracting text from the pdf. Now to save the pdf in the actualy text 
def extract_text_images_from_pdf(files, into = 'text_files', other = 'image_storage', json_path = 'tracker.json', context_overlap = True): 
    #making sure we point to text_files

    base_dir = os.path.dirname(__file__) #go into the directory of where scaper is at
    text_pointer = os.path.abspath(os.path.join(base_dir,'..', into)) #redirect to the backend and then make sure we are appending it to text_files which is in oru arg
    image_pointer = os.path.abspath(os.path.join('image_storage'))
    j_p = os.path.abspath(os.path.join(base_dir, '..', json_path))

    os.makedirs(text_pointer, exist_ok = True) #make sure it exist
    os.makedirs(image_pointer, exist_ok = True)

    j_file = []
    img_counter = 0

    for file in files: 
        document = fitz.open(file)
        
        #write a txt path for this file
        base, _ext = os.path.splitext(os.path.basename(file))

        txt_name = base +".txt"

        txt_path = os.path.join(text_pointer, txt_name)
        txt_file = open(txt_path, 'w', encoding = 'utf-8')
        if file.contain('.pdf)'):
            for page_num, page in enumerate(document, start = 1):
                text = page.get_text() 
                txt_file.write(text)
                txt_file.write('\n\n')
                #to extract the images
                blocks = page.get_text('dict')['blocks'] #each page is basically seperated into blocks
                #we want to look for teh blocks that contain nubmers because images converted to numbers
                for block in blocks: 
                    if block.get('type') != 1: 
                        continue
                    img_id = f"IMG_{img_counter:06d}"
                    img_counter +=1 
                    pic = fitz.Pixmap(document, block['Image'])
                    img_filename = f"{img_id}.png"
                    img_path = os.path.absjoin(image_pointer, img_filename)
                    pic.save(img_path)
                    pic = None

                    context_text = ''
                    if context_overlap: 
                        y0, y1 = block['bbox'][1], block['bbox'][3]
                        context_lines = [] 
                        for text_block in blocks: 
                            if  text_block.get('type') != 0:
                                continue
                            text_block_y0, text_block_y1 = text_block['bbox'][1], text_block['bbox'][3]
                            if not (text_block_y1 < y0 or text_block_y0 > y1): 
                                context_lines.append(text_block['text'].strip())


                

            
                




                 
        print("succesful: {txt_path}")


def main():
    files = get_paths()
    for f in files:
        print("Found file:", f)
    #extract_file_info_for_db(files)
    extract_text_images_from_pdf(files, into = 'text_files')

if __name__ == "__main__":
    main()



    


