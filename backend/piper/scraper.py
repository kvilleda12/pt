import os
import requests
import fitz
import re
import time
import json
import shutil
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from semanticscholar import SemanticScholar
from .config import (
    LABELS_TO_SCRAPE, TEXTBOOK_QUERIES, SOURCES_PER_LABEL,
    FILE_SOURCES_DIR, TEXT_FILES_DIR, REQUESTS_HEADERS, REQUESTS_TIMEOUT, SKIPPED_SOURCES_JSON_PATH
)
from .database_manager import add_paper_to_db, add_textbook_to_db
from .pdf_processor import process_pdf_file

def is_source_reliable_llm(title: str, author: str, publisher:str) -> bool:
    #check with ollama to see if a textbook is good or bad. This prompt works very well. I made mistral make up its own guidelines before this and this is 
    #what it came up with
    ollama_api_url = "http://localhost:11434/api/generate"
    prompt = f""" 
    You are an expert academic librarian specializing in physical therapy. Your task is to evaluate the reliability of a textbook based on the criteria below

    Use the following criteria in your evaluation and examine the:
    1. Publisher: Reputable publishers often have rigorous editorial processes and high standards for their books. is the publisher {publisher} reputable?
    2. Authors: Check the credentials and reputation of the author(s. Are they experts in the field they're writing about? Do they have relevant degrees, research experience, or 
        professional practice? is the author {author} accredited and reputable in this field
    3. Peer Review: Many textbooks go through a peer review process where other scholars in the same field evaluate and provide feedback on the content before publication. This can help 
    ensure accuracy and depth
    4. Content and Title: Does the title "{title}" suggest a credible, well-structured textbook?
    5. Publication date: More recent editions may incorporate the latest research and 
    developments in the field, although older editions might still be valuable for certain 
    subjects.
    6. Reader Reviews: Check online reviews from other readers or instructors who have used the 
    book in the past. This can give you an idea of how useful and engaging the book is.

    Based on these factors, is the following textbook a credible source for a professional or student?
    Respond with only one word: 'yes' or 'no'.

    Title: "{title}"
    Author: "{author}"
    publisher:"{publisher}"
    """
    payload = {"model": "mistral", "prompt": prompt, "stream": False}
    try:
        print(f" LLm Validating: '{title}'...")
        response = requests.post(ollama_api_url, json=payload, timeout=90)
        response.raise_for_status()
        llm_response_text = response.json().get("response", "").strip().lower()
        print(f"Mistral Response: '{llm_response_text}'")
        return 'yes' in llm_response_text
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect")
        return False
    except Exception as e:
        print(f"error occured: {e}")
        return False

#helper to check if a pdf has images that way we know exacty where to send it to
def has_images(pdf_path: str) -> bool:
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            if page.get_images(full=True):
                doc.close()
                return True
        doc.close()
        return False
    except Exception as e:
        print(f"Could not check for images in {os.path.basename(pdf_path)}: {e}")
        return False

#this will setup a temporary browser for us to bypass the human verification check
def download_file(url: str, destination_folder: str, filename: str) -> str | None:
    """
    Handles downloading by opening a browser, waiting for manual human
    verification, and then programmatically clicking the download button.
    """
    temp_download_dir = os.path.join(os.path.dirname(destination_folder), 'browser_downloads')
    os.makedirs(temp_download_dir, exist_ok=True)

    options = ChromeOptions()
    prefs = {"download.default_directory": temp_download_dir}
    options.add_experimental_option("prefs", prefs)

    driver = None
    try:
        print(f"⬇️ Opening stealth browser for: {filename}")
        driver = uc.Chrome(options=options)
        driver.get(url)

        # 1. The script pauses, waiting for you to solve the human check.
        input(">>> Please solve the human verification check in the browser, then press Enter in this terminal to continue...")

        # =========================================================
        # NEW: The program now takes over to click the download button.
        # =========================================================
        print("... Human check complete. Searching for the download button...")
        try:
            # We wait up to 30 seconds for a button with text like "Download" to appear and be clickable.
            download_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Download')]"))
            )
            print("... Download button found. Clicking now.")
            download_button.click()
        except Exception as button_error:
            print(f"❌ Could not find or click the download button. Error: {button_error}")
            raise # Raise the error to be caught by the main try/except block
        # =========================================================

        # 3. The script waits for the download to finish.
        print("... Waiting for download to finish ...")
        download_wait_time = 300
        time_waited = 0
        downloaded_file_path = os.path.join(temp_download_dir, filename)

        while not os.path.exists(downloaded_file_path) and time_waited < download_wait_time:
            time.sleep(1)
            time_waited += 1

        if os.path.exists(downloaded_file_path):
            final_path = os.path.join(destination_folder, filename)
            shutil.move(downloaded_file_path, final_path)
            print(f"✅ Download complete and file moved to: {final_path}")
            return final_path
        else:
            print("❌ Download timed out or file was not found.")
            return None

    except Exception as e:
        print(f"❌ An error occurred during the browser download: {e}")
        return None
    finally:
        if driver:
            driver.quit()
        if os.path.exists(temp_download_dir):
            shutil.rmtree(temp_download_dir)

 # 1. <input type="search" name="q" placeholder="Title, author, DOI, ISBN, MD5, …" value="physical therapy" class="js-slash-focus js-search-main-input grow bg-black/6.7 px-2 py-1 mr-2 rounded">
            #to find the text books -><main class  = "main"> --> form action = "/search" ... --> <div class = "flex w-full ---> "min-w-[0] w-full ---> div class "mb-4" m -->
            #go into the search settings incase the link above doesn't work and we have to go ahead and edit 
            #<div aria-labelledby = "search settintgs"

            #div id = "aarecord list"
            #div class   = " h-[110]px flex flex-col justify center"
            #<a = href = the link that we want to access the textbook we must click on this link


            #to extract the title its in this line: <h3 class="max-lg:line-clamp-[2] lg:truncate leading-[1.2] lg:leading-[1.35] text-md lg:text-xl font-bold">Guccione's Geriatric Physical Therapy</h3>
            #publisher is on this line: <div class="truncate leading-[1.2] lg:leading-[1.35] max-lg:text-xs">Elsevier, 4</div>
            #author is in this class. 

            #the script we need has to access all tehse things so it can be even quixker to pull the information from the site

            # we find the path we need to download here: <h3 class="mt-4 mb-1 text-xl font-bold">🐢 Slow downloads</h3>
            #then we enter this path: <ul class="list-inside mb-4 ml-1">
              #<li class="list-disc">Option #1: <a href="/slow_download/ba3e8aa2517f9625835ac61aba40b72b/0/0" rel="noopener noreferrer nofollow" class="js-download-link">Slow Partner Server #1</a> (slightly faster but with waitlist)</li>
             #our download link is in the link above and it is the link we are supposed to get



def download_textbooks():
#uses the console in annas archive to look for the specific textbooks we need
    print("\n--- Searching for Textbooks on Anna's Archive ---")
    
    skipped_hashes = set()
    if os.path.exists(SKIPPED_SOURCES_JSON_PATH):
        with open(SKIPPED_SOURCES_JSON_PATH, 'r') as f:
            try: skipped_hashes = set(json.load(f))
            except json.JSONDecodeError: pass

    for part_id, query in TEXTBOOK_QUERIES.items():
        results_to_check = SOURCES_PER_LABEL
        try:
            print(f"\n--- Searching for textbooks with query: '{query}' ---")
            
            search_url = f"https://annas-archive.org/search?q={query.replace(' ', '+')}&content=book_nonfiction&ext=pdf&lang=en&sort=popular"
            
            response = requests.get(search_url, headers=REQUESTS_HEADERS, timeout=REQUESTS_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')


            result_containers = soup.find_all('div', class_=re.compile(r"h-\[110px\]"), limit=results_to_check * 4)
            
            if not result_containers:
                print(f"No results found for '{query}'.")
                continue
            
            download_count = 0
            for container in result_containers:
                if download_count >= results_to_check: break
                
            
                details_div = container.find('div', class_=re.compile(r"line-clamp-\[2\]"))
                title_tag = container.find('h3')
                author_tag = container.find('div', class_='italic')
                # publisher after h3 tag
                publisher_tag = title_tag.find_next_sibling('div') if title_tag else None
                link_tag = container.find('a', href=lambda href: href and href.startswith('/md5/'))

                # double check langage even though its already in our link up above
                if not details_div or 'English' not in details_div.text:
                    continue

                # Ensures all infof ound
                if not all([title_tag, author_tag, publisher_tag, link_tag]):
                    continue

                title = title_tag.text.strip()
                author = author_tag.text.strip()
                publisher = publisher_tag.text.strip().split(',')[0]
                md5_hash = link_tag['href'].split('/md5/')[1]

                if md5_hash in skipped_hashes: continue

                print(f"\n✅ Found Source: '{title}' by {author} (Publisher: {publisher})")
                
                if not is_source_reliable_llm(title, author, publisher):
                    print(f"-> LLM rejected source. Adding to skip list.")
                    skipped_hashes.add(md5_hash)
                    time.sleep(2)
                    continue
                
                print("-> Source passed validation. Getting download link.")
                book_page_url = f"https://annas-archive.org{link_tag['href']}"
                response = requests.get(book_page_url, headers=REQUESTS_HEADERS, timeout=REQUESTS_TIMEOUT)
                book_soup = BeautifulSoup(response.content, 'html.parser')
                
                download_link_tag = book_soup.find('a', string=re.compile(r"Slow Partner Server #1"))
                if not download_link_tag:
                    print(f"-> Could not find 'Slow Partner Server #1' link for '{title}'. Skipping.")
                    continue

                safe_title = re.sub(r'[^\w\s-]', '', title).strip()
                filename = f"{safe_title}.pdf"
                if os.path.exists(os.path.join(FILE_SOURCES_DIR, filename)): continue

                full_download_url = f"https://annas-archive.org{download_link_tag['href']}"
                final_path = download_file(full_download_url, FILE_SOURCES_DIR, filename)
                
                if final_path:
                    textbook_info = {'title': safe_title, 'author': author, 'size': os.path.getsize(final_path), 'path': book_page_url, 'part_id': part_id}
                    if add_textbook_to_db(textbook_info):
                        process_pdf_file(final_path, 'textbook')
                    download_count += 1
                time.sleep(5)
        except Exception as e:
            print(f"An error occurred while getting textbooks for query '{query}': {e}")
            
    with open(SKIPPED_SOURCES_JSON_PATH, 'w') as f:
        json.dump(list(skipped_hashes), f, indent=4)
    print(f"\nUpdated skip list with {len(skipped_hashes)} entries.")


def download_research_papers():
    """Finds and downloads academic research papers."""
    print("\n--- 📄 Searching for Research Papers ---")
    s2 = SemanticScholar()
    for label, query in LABELS_TO_SCRAPE.items():
        print(f"\n--- Searching for label '{label}' with query: '{query}' ---")
        try:
            results = s2.search_paper(query, limit=SOURCES_PER_LABEL * 2)
            download_count = 0
            for paper in results:
                if download_count >= SOURCES_PER_LABEL: break
                if not paper.isOpenAccess or not paper.openAccessPdf: continue

                safe_title = re.sub(r'[^\w\s-]', '', paper.title).strip()
                filename = f"{safe_title}.pdf"
                if os.path.exists(os.path.join(FILE_SOURCES_DIR, filename)) or os.path.exists(os.path.join(TEXT_FILES_DIR, f"{safe_title}.txt")): continue
                
                temp_path = download_file(paper.openAccessPdf['url'], FILE_SOURCES_DIR, f"temp_{filename}")
                if not temp_path: continue

                if has_images(temp_path):
                    final_path = os.path.join(FILE_SOURCES_DIR, filename)
                    os.rename(temp_path, final_path)
                    paper_info = {'title': safe_title, 'size': os.path.getsize(final_path), 'path': paper.url, 'part_id': label}
                    if add_paper_to_db(paper_info):
                        process_pdf_file(final_path, 'paper')
                else:
                    doc = fitz.open(temp_path)
                    full_text = "".join(page.get_text() for page in doc)
                    doc.close()
                    txt_path = os.path.join(TEXT_FILES_DIR, f"{safe_title}.txt")
                    with open(txt_path, 'w', encoding='utf-8') as f:
                        f.write(full_text)
                    os.remove(temp_path)
                    print(f"📄 Converted (no images): '{filename}' to text_files/")
                download_count += 1
                time.sleep(2)
        except Exception as e:
            print(f"An error occurred while searching for label '{label}': {e}")