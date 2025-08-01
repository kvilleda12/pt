import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Database ---
DATABASE_URL = os.getenv("DATABASE_URL")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')) 

FILE_SOURCES_DIR = os.path.join(BASE_DIR, 'backend', 'file_sources')
TEXT_FILES_DIR = os.path.join(BASE_DIR, 'backend', 'text_files')
IMAGE_STORAGE_DIR = os.path.join(BASE_DIR, 'backend', 'image_storage')
PROCESSED_ARCHIVE_DIR = os.path.join(BASE_DIR, 'backend', 'processed_archive')
CAPTIONS_JSON_PATH = os.path.join(IMAGE_STORAGE_DIR, 'captions.json')
SKIPPED_SOURCES_JSON_PATH = os.path.join(BASE_DIR, 'backend', 'skipped_sources.json')

# queries for research paper
LABELS_TO_SCRAPE = {
    'n': 'neck pain physical therapy OR cervical spine rehabilitation exercises',
    'f': 'foot injury rehabilitation OR ankle biomechanics physical therapy',
    'h': 'headache physical therapy OR concussion rehabilitation',
    'a': 'arm injury physical therapy OR upper limb movement analysis',
    'l': 'leg injury rehabilitation OR lower limb biomechanics stretches',
    's': 'shoulder impingement physical therapy OR rotator cuff repair exercises',
    'c': 'chest wall pain physical therapy OR thoracic spine mobility',
    'b': 'low back pain rehabilitation OR spine stabilization exercises'
}

# Dqueries for looking for textbooks
TEXTBOOK_QUERIES = {
    'e': "physical therapy", # General query
}

SOURCES_PER_LABEL = 4

# network 
REQUESTS_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
REQUESTS_TIMEOUT = 60

# Create directories if they don't exist
os.makedirs(FILE_SOURCES_DIR, exist_ok=True)
os.makedirs(TEXT_FILES_DIR, exist_ok=True)
os.makedirs(IMAGE_STORAGE_DIR, exist_ok=True)
os.makedirs(PROCESSED_ARCHIVE_DIR, exist_ok=True)