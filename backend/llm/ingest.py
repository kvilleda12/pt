# pt/backend/llm/ingest.py
from typing import List, Dict
from pathlib import Path
from langchain_core.documents import Document

from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma

from .settings import CHROMA_DIR
from .utils import load_exercises_json

def _exercise_to_text(ex: Dict) -> str:
    steps = ex.get("steps", [])
    steps_text = "\n".join(f"- {s}" for s in steps)
    core = [
        f"Exercise: {ex.get('name','')}",
        f"Type: {ex.get('type','')}",
        f"Body Part: {ex.get('body_part','')}  (label: {ex.get('body_part_label','')})",
        f"Equipment: {ex.get('equipment','none')}",
        f"Description: {ex.get('description','')}",
        "Steps:",
        steps_text,
        f"Cues: {ex.get('cues','')}",
        f"Precautions: {ex.get('precautions','')}",
    ]
    return "\n".join(core)

def build_or_load_vectorstore(persist_dir: Path = CHROMA_DIR) -> Chroma:
    """
    Build Chroma index if not present; otherwise load it.
    """
    data = load_exercises_json()
    exercises = data.get("exercises", [])
    # Create documents
    docs: List[Document] = []
    for ex in exercises:
        text = _exercise_to_text(ex)
        meta = {
            "id": ex.get("id"),
            "name": ex.get("name"),
            "body_part_label": ex.get("body_part_label"),
            "body_part": ex.get("body_part"),
            "type": ex.get("type"),
            "equipment": ex.get("equipment"),
        }
        docs.append(Document(page_content=text, metadata=meta))

    embeddings = FastEmbedEmbeddings()  # local, no extra API key
    vs = Chroma(
        collection_name="pt_exercises",
        embedding_function=embeddings,
        persist_directory=str(persist_dir)
    )

    # If empty, add; if already populated, load-only
    if vs._collection.count() == 0:
        vs.add_documents(docs)
        vs.persist()
    return vs
