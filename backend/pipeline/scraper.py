import os
import requests
import fitz  # PyMuPDF
import re
from semanticscholar import SemanticScholar
from .config import LABELS_TO_SCRAPE, SOURCES_PER_LABEL, FILE_SOURCES_DIR, TEXT_FILES_DIR
from .database_manager import add_paper_to_db

def has_images(pdf_path: str) -> bool:
    """Quickly checks if a PDF document contains any images."""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            if page.get_images():
                doc.close()
                return True
        doc.close()
        return False
    except Exception as e:
        print(f"Could not process {os.path.basename(pdf_path)} to check for images: {e}")
        return False

def download_and_process_source():
    """Finds and downloads academic PDFs for specified labels."""
    s2 = SemanticScholar()
    print("🚀 Starting academic source scraping...")

    for label, query in LABELS_TO_SCRAPE.items():
        print(f"\n--- Searching for label '{label}' with query: '{query}' ---")
        try:
            results = s2.search_paper(query, limit=SOURCES_PER_LABEL * 2)
            download_count = 0

            for paper in results:
                if download_count >= SOURCES_PER_LABEL:
                    break

                if not paper.isOpenAccess or not paper.openAccessPdf:
                    continue

                safe_title = re.sub(r'[^\w\s-]', '', paper.title).strip()
                filename = f"{safe_title}.pdf"
                pdf_path = os.path.join(FILE_SOURCES_DIR, filename)
                txt_path = os.path.join(TEXT_FILES_DIR, f"{safe_title}.txt")
                
                if os.path.exists(pdf_path) or os.path.exists(txt_path):
                    continue

                try:
                    pdf_url = paper.openAccessPdf['url']
                    response = requests.get(pdf_url, timeout=30, headers={'User-Agent': 'Mozilla/5.0'})
                    response.raise_for_status()

                    temp_pdf_path = os.path.join(FILE_SOURCES_DIR, f"temp_{filename}")
                    with open(temp_pdf_path, 'wb') as f:
                        f.write(response.content)

                    if has_images(temp_pdf_path):
                        os.rename(temp_pdf_path, pdf_path)
                        final_path = pdf_path
                        print(f"⬇️ Downloaded (with images): '{filename}'")
                    else:
                        doc = fitz.open(temp_pdf_path)
                        full_text = "".join(page.get_text() for page in doc)
                        doc.close()
                        with open(txt_path, 'w', encoding='utf-8') as f:
                            f.write(full_text)
                        os.remove(temp_pdf_path)
                        final_path = txt_path
                        print(f"📄 Converted (no images): '{filename}'")
                    
                    # *** This is the updated change ***
                    # 'path' here contains the URL and maps to the 'where' column in the db
                    paper_info = {
                        'title': safe_title,
                        'size': os.path.getsize(final_path),
                        'path': paper.url, 
                        'part_id': label,
                    }
                    add_paper_to_db(paper_info)
                    download_count += 1

                except requests.RequestException as e:
                    print(f"Failed to download {paper.title}. Reason: {e}")
                except Exception as e:
                    print(f"An error occurred while processing {paper.title}: {e}")
                    if 'temp_pdf_path' in locals() and os.path.exists(temp_pdf_path):
                        os.remove(temp_pdf_path)
        
        except Exception as api_error:
            print(f"Error calling Semantic Scholar API for label '{label}': {api_error}")

    print("\nScraping complete.")