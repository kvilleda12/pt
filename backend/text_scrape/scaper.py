import os
import fitz
from datetime import datetime
from backend.database.database import SessionLocal, Textbook, Body # adjust import path as needed



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
    author = split_title[1].strip() if len(split_title) > 1 else "unknown"
    part_id = 'm'  # default = misc
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



def main():
    files = get_paths()
    for f in files:
        print("Found file:", f)
    extract_file_info_for_db(files)

if __name__ == "__main__":
    main()



    


