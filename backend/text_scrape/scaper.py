import fitz 
import os
from datetime import datetime
from backend.database import SessionLocal, Textbook  # adjust import path as needed
from backend.database import Body  # assuming Body enum/model is also defined
from sqlalchemy.orm import Session


extensions_allowed = [".pdf", ".epub", ".docx", ".txt"]
files = [] 
def get_paths (folder_name = 'file_sources'): #iterating over the paths 
    dir = os.path.dirname(__file__)
    folder_path = os.path.abspath(os.path.join(dir, "..", "file_sources"))
    for file in os.listdir(folder_path):
        if any(file.lower().endswith(ext) for ext in extensions_allowed):
            path = os.path.join(folder_path, file)
            files.append(path)
    return files #returns list of paths

if __name__ == "__main__":
    files = get_paths()
    for f in files:
        print(f"{f}")


def extract_file_info_for_db(files):
   db: Session = SessionLocal()
   for path in files: 
    file_name = os.path.basename(path)
    size = os.path.getsize(file_name)
    split_title = path.split('--')
    title = split_title[0].strip().lower()
    author = split_title[1].strip()
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



    


