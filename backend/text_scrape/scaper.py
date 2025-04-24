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
    fp = '/users/kevinvilleda/pt/backend/file_sources/'
    title, _ext = os.path.splitext(os.path.basename(fp))#remove the path from the file``
    author = split_title[1].strip() if len(split_title) > 1 else "unknown"
    part_id = 'e'  # default = misc
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
def extract_text_from_pdf(files, into = 'text_files'): 
    #making sure we point to text_files
    base_dir = os.path.dirname(__file__) #go into the directory of where scaper is at
    to = os.path.abspath(os.path.join(base_dir,'..', into)) #redirect to the backend and then make sure we are appending it to text_files which is in oru arg
    os.makedirs(to, exist_ok = True) #make sure it exist

    for file in files: 
        document = fitz.open(file)
        
        #write a txt path for this file
        base, _ext = os.path.splitext(os.path.basename(file))
        txt_name = base +".txt"
        txt_path = os.path.join(to, txt_name)
        with open (txt_path, 'w', encoding = 'utf-8') as txt_file:
           for page_num in range(len(document)):
              page = document.load_page(page_num)
              text = page.get_text() 
              txt_file.write(text)
              txt_file.write('\n\n')
        print("succesful: {txt_path}")
    
         
      

#what I need to do now is to take out teh certian parts of teh title out
   #then I need to actualyl extract out the text from teh pdfs 
   

def main():
    files = get_paths()
    for f in files:
        print("Found file:", f)
    #extract_file_info_for_db(files)
    extract_text_from_pdf(files, into = 'text_files')

if __name__ == "__main__":
    main()



    


