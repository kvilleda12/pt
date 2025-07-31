import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Database ---
DATABASE_URL = os.getenv("DATABASE_URL")

# --- File Paths ---
# Use absolute paths to avoid issues when running scripts from different directories
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

FILE_SOURCES_DIR = os.path.join(BASE_DIR, 'backend', 'file_sources')
TEXT_FILES_DIR = os.path.join(BASE_DIR, 'backend', 'text_files')
IMAGE_STORAGE_DIR = os.path.join(BASE_DIR, 'backend', 'image_storage')
CAPTIONS_JSON_PATH = os.path.join(IMAGE_STORAGE_DIR, 'captions.json')
PROCESSED_ARCHIVE_DIR = os.path.join(BASE_DIR, 'backend', 'processed_archive')

# --- Scraping & Processing ---
LABELS_TO_SCRAPE = {
    'n': 'neck anatomy OR neck biomechanics',
    'f': 'foot anatomy OR feet biomechanics',
    'h': 'head and skull anatomy',
    'a': 'arm anatomy OR upper limb biomechanics',
    'l': 'leg anatomy OR lower limb biomechanics',
    's': 'shoulder anatomy OR shoulder girdle biomechanics',
    'c': 'chest anatomy OR thorax biomechanics',
    'b': 'back anatomy OR spine biomechanics'
}

# Number of sources to find for each label
SOURCES_PER_LABEL = 4

# Create directories if they don't exist
os.makedirs(FILE_SOURCES_DIR, exist_ok=True)
os.makedirs(TEXT_FILES_DIR, exist_ok=True)
os.makedirs(IMAGE_STORAGE_DIR, exist_ok=True)
os.makedirs(PROCESSED_ARCHIVE_DIR, exist_ok=True)