import uuid
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List
from config import PROCESSED_DIR, RAW_DIR, ARCHIVE_DIR
from html_utils import html_to_text
from storage import add_or_update_link, sha256_text
from logger import log

def save_html_and_convert(url: str, html: str) -> Tuple[str, Path, Path, str]:
    doc_id = str(uuid.uuid4())
    html_path = PROCESSED_DIR / f"{doc_id}.html"
    html_path.write_text(html, encoding="utf-8")
    log(f"[STORE] Saved HTML -> {html_path.name}")
    text = html_to_text(html)
    raw_path = RAW_DIR / f"{doc_id}.txt"
    raw_path.write_text(text, encoding="utf-8")
    log(f"[STORE] Saved RAW -> {raw_path.name}")
    entry: Dict[str, Any] = {
        "id": doc_id,
        "url": url,
        "raw_file": str(raw_path),
        "html_file": str(html_path),
        "viable": None,
        "confidence": None,
        "reason": None,
        "labels": [],
        "hash": sha256_text(text),
    }
    add_or_update_link(entry)
    return doc_id, html_path, raw_path, text

def archive_processed_file(html_path: Path) -> None:
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    dst = ARCHIVE_DIR / html_path.name
    if html_path.exists():
        shutil.move(str(html_path), str(dst))
        log(f"[ARCHIVE] Moved {html_path.name} -> processed/archive/")

def process_existing_files_in_processed() -> List[Path]:
    created = []
    for p in PROCESSED_DIR.iterdir():
        if not p.is_file() or p.suffix.lower() not in {".html",".htm",".txt"}:
            continue
        try:
            log(f"[PROC->RAW] Converting {p.name}")
            content = p.read_text(encoding="utf-8", errors="ignore")
            if p.suffix.lower() in {".html",".htm"}:
                text = html_to_text(content)
            else:
                import re
                lines = [re.sub(r"\s+", " ", ln).strip() for ln in content.splitlines()]
                lines = [ln for ln in lines if ln]
                text = "\n".join(lines)
            doc_id = str(uuid.uuid4())
            raw_path = RAW_DIR / f"{doc_id}.txt"
            raw_path.write_text(text, encoding="utf-8")
            add_or_update_link({
                "id": doc_id,
                "url": f"file://processed/{p.name}",
                "raw_file": str(raw_path),
                "html_file": str(p),
                "viable": None, "confidence": None, "reason": None,
                "labels": [],
                "hash": sha256_text(text),
            })
            archive_processed_file(p)
            created.append(raw_path)
        except Exception as e:
            log(f"[PROC->RAW] ERROR {p.name}: {e}")
    if not created:
        log("[PROC->RAW] No convertible files in processed/")
    return created
