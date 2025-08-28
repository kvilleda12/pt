import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional
from config import DEFAULT_CRITERIA, FETCH_SLEEP, SEARCH_RESULTS_PER_LABEL, SEARCH_SLEEP
from labels import LABEL_CODES, LABEL_MAP, SEARCH_QUERY_TEMPLATES
from storage import load_links, load_hashes, save_hashes, update_link_fields, sha256_text, log_duplicate
from search import search_web
from fetch import robots_allowed, http_get
from ingest import save_html_and_convert, archive_processed_file, process_existing_files_in_processed
from classify import classify_text
from logger import log

@dataclass
class RunResult:
    scraped: List[str]
    converted_from_processed: List[str]
    skipped_duplicates: int

def fetch_and_ingest(url: str, criteria: Dict, known_hashes: set) -> Optional[str]:
    log(f"[PIPE] Checking robots for: {url}")
    if not robots_allowed(url):
        log_duplicate({"type":"robots_disallow","url":url})
        log(f"[PIPE] SKIP robots: {url}")
        return None
    resp = http_get(url)
    if not resp:
        log_duplicate({"type":"fetch_error","url":url})
        log(f"[PIPE] SKIP fetch error: {url}")
        return None
    log(f"[PIPE] Converting HTML -> text for: {url}")
    doc_id, html_path, raw_path, text = save_html_and_convert(url, resp.text)
    h = sha256_text(text)
    if h in known_hashes:
        update_link_fields(doc_id, reason="duplicate_content_hash", viable=False, confidence=0.0)
        archive_processed_file(html_path)
        log_duplicate({"type":"content_hash","url":url,"doc_id":doc_id,"hash":h})
        log(f"[PIPE] DUP content hash -> skip: {url}")
        return None
    known_hashes.add(h)
    save_hashes(known_hashes)
    classify_text(doc_id, text, criteria)
    archive_processed_file(html_path)
    time.sleep(FETCH_SLEEP)
    return doc_id

def run_pipeline(
    labels: Optional[List[str]] = None,
    results_per_label: int = SEARCH_RESULTS_PER_LABEL,
    process_existing: bool = False,
    criteria: Optional[Dict] = None
) -> RunResult:
    criteria = criteria or DEFAULT_CRITERIA
    scraped_ids: List[str] = []
    converted_paths: List[str] = []
    skipped_dups = 0

    if process_existing:
        log("[PIPE] Processing existing files in processed/")
        converted = process_existing_files_in_processed()
        converted_paths = [str(p) for p in converted]
        for rp in converted:
            text = Path(rp).read_text(encoding="utf-8")
            for it in load_links():
                if it.get("raw_file") == str(rp):
                    classify_text(it["id"], text, criteria)
                    break

    label_codes = labels or list(LABEL_CODES)
    existing_urls = {it.get("url") for it in load_links() if it.get("url")}
    known_hashes = load_hashes()

    for code in label_codes:
        part = LABEL_MAP.get(code, code)
        for tmpl in SEARCH_QUERY_TEMPLATES:
            query = tmpl.format(part=part)
            urls = search_web(query, results_per_label)
            log(f"[PIPE] Query done: {query} -> {len(urls)} urls")
            time.sleep(SEARCH_SLEEP)
            for url in urls:
                if url in existing_urls:
                    skipped_dups += 1
                    log_duplicate({"type":"url_duplicate","url":url})
                    log(f"[PIPE] DUP url -> skip: {url}")
                    continue
                existing_urls.add(url)
                doc_id = fetch_and_ingest(url, criteria, known_hashes)
                if doc_id:
                    scraped_ids.append(doc_id)

    log(f"[PIPE] Done. New={len(scraped_ids)} Converted={len(converted_paths)} URL dups={skipped_dups}")
    return RunResult(scraped=scraped_ids, converted_from_processed=converted_paths, skipped_duplicates=skipped_dups)
