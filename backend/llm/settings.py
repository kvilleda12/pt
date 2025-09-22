from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Support both spellings just in case:
EXERCISES_CANDIDATES = [ "pt_exercises.json"]
QUERIES_FILE = "pt_queries.json"

CHROMA_DIR = BASE_DIR / ".chroma_pt_exercises"


TOP_K_VECTOR = 12       # per variant per retriever
TOP_K_FINAL = 8         # final fused results used in the prompt
RRF_K = 60              # rank dampening for RRF
N_MULTI_QUERIES = 4     # how many LLM variants
USE_HYDE = True         # also generate a hypothetical answer as a query

# Generation knobs
MAX_TOKENS = 700
TEMPERATURE = 0.4

SAFETY_DISCLAIMER = (
    "These exercises are general educational guidance and are not medical advice. "
    "Stop if you feel sharp pain, dizziness, or numbness, and consult a licensed clinician."
)
