import json
import hashlib
from typing import Any, Dict, List, Set
from pathlib import Path
from config import LINKS_FILE, HASH_INDEX, DUPLICATES_LOG
from logger import log

def _safe_load_json(path: Path, default):
    try:
        raw = path.read_text(encoding="utf-8")
        if not raw.strip():
            log(f"[STORAGE] Empty JSON at {path.name}; defaulting")
            return default
        return json.loads(raw)
    except Exception as e:
        log(f"[STORAGE] Corrupt JSON at {path.name}: {e}; defaulting")
        return default

def _atomic_write_json(path: Path, obj):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=4, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)

def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8", errors="ignore")).hexdigest()

def load_links() -> List[Dict[str, Any]]:
    return _safe_load_json(LINKS_FILE, [])

def save_links(data: List[Dict[str, Any]]) -> None:
    _atomic_write_json(LINKS_FILE, data)
    log(f"[STORAGE] Wrote links.json ({len(data)} entries)")

def add_or_update_link(entry: Dict[str, Any]) -> None:
    links = load_links()
    for i, it in enumerate(links):
        if it.get("id") == entry["id"]:
            links[i] = entry
            save_links(links)
            log(f"[STORAGE] Updated link id={entry['id']}")
            return
    links.append(entry)
    save_links(links)
    log(f"[STORAGE] Added link id={entry['id']}")

def update_link_fields(doc_id: str, **fields) -> None:
    links = load_links()
    for it in links:
        if it.get("id") == doc_id:
            it.update({k: v for k, v in fields.items() if v is not None})
            break
    save_links(links)
    log(f"[STORAGE] Updated fields for id={doc_id}: {list(fields.keys())}")

def load_hashes() -> Set[str]:
    arr = _safe_load_json(HASH_INDEX, [])
    return set(arr) if isinstance(arr, list) else set()

def save_hashes(hs: Set[str]) -> None:
    _atomic_write_json(HASH_INDEX, sorted(hs))
    log(f"[STORAGE] Wrote hash_index.json ({len(hs)} hashes)")

def log_duplicate(entry: Dict[str, Any]) -> None:
    data = _safe_load_json(DUPLICATES_LOG, [])
    data.append(entry)
    _atomic_write_json(DUPLICATES_LOG, data)
    log(f"[DUP] {entry.get('type')} {entry.get('url','')} ({entry.get('doc_id','')})")
