from pathlib import Path
import os

# Try to load dotenv if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available, continue without it

BASE_DIR = Path(__file__).resolve().parents[1]

WS_DIR = BASE_DIR / "website_files"
RAW_DIR = WS_DIR / "raw"
PROCESSED_DIR = WS_DIR / "processed"
ARCHIVE_DIR = PROCESSED_DIR / "archive"
AUDITS_DIR = WS_DIR / "audits"
LINKS_FILE = WS_DIR / "links.json"
HASH_INDEX = WS_DIR / "hash_index.json"
DUPLICATES_LOG = WS_DIR / "duplicates.json"

for d in (WS_DIR, RAW_DIR, PROCESSED_DIR, ARCHIVE_DIR, AUDITS_DIR):
    d.mkdir(parents=True, exist_ok=True)
if not LINKS_FILE.exists():
    LINKS_FILE.write_text("[]", encoding="utf-8")
if not HASH_INDEX.exists():
    HASH_INDEX.write_text("[]", encoding="utf-8")
if not DUPLICATES_LOG.exists():
    DUPLICATES_LOG.write_text("[]", encoding="utf-8")

USER_AGENT = "pt-scraper/1.0"
REQUEST_TIMEOUT = 20
RETRIES = 2
BACKOFF = 1.7
SEARCH_RESULTS_PER_LABEL = int(os.getenv("PT_RESULTS_PER_LABEL", "8"))
SEARCH_SLEEP = float(os.getenv("PT_SEARCH_SLEEP", "1.0"))
FETCH_SLEEP = float(os.getenv("PT_FETCH_SLEEP", "0.5"))

SERP_API_KEY = os.getenv("SERP_API_KEY")

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0.1"))
OLLAMA_MAX_TOKENS = int(os.getenv("OLLAMA_MAX_TOKENS", "512"))

DEFAULT_CRITERIA = {
    "keywords_any": [
        "physical therapy", "rehabilitation", "stretch", "exercise",
        "range of motion", "mobility", "strengthening", "PT", "physiotherapy",
        "therapeutic", "manual therapy", "recovery", "injury", "pain relief",
        "muscle", "joint", "flexibility", "stability", "posture", "movement",
        "treatment", "therapy", "rehab", "conditioning", "restoration"
    ],
    "min_text_len": 300,
    "reject_phrases_any": [
        "casino", "coupon", "price list", "terms of service", "disclaimer only",
        "buy now", "click here", "advertisement", "sponsored", "affiliate",
        "medical advice", "consult your doctor", "emergency", "call 911"
    ],
    "require_precision": True,
    "body_parts": [
        "neck", "chest", "shoulder", "tricep", "bicep", "abdomen",
        "back", "hamstring", "quad", "calf", "ankle", "knee", "hip",
        "wrist", "elbow", "foot", "spine", "pelvis", "core"
    ],
    "quality_indicators": [
        "step by step", "instructions", "repetitions", "sets", "duration",
        "technique", "form", "safety", "contraindications", "progression"
    ]
}
