#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from pipeline import run_pipeline
from config import DEFAULT_CRITERIA
from logger import log

def parse_args(argv):
    ap = argparse.ArgumentParser(description="Autonomous PT web scraper: search -> fetch -> classify -> archive.")
    ap.add_argument("--labels", help="Comma-separated label codes (e.g., n,rs,lh). Default: all.")
    ap.add_argument("--results-per-label", type=int, default=None, help="Search results per query template.")
    ap.add_argument("--process-existing", action="store_true", help="Convert files already in processed/ to raw/ and archive.")
    ap.add_argument("--criteria", help="Path to JSON to override classification criteria.")
    return ap.parse_args(argv)

def main(argv=None):
    args = parse_args(argv or sys.argv[1:])
    criteria = DEFAULT_CRITERIA
    if args.criteria:
        try:
            with open(args.criteria, "r", encoding="utf-8") as f:
                user_criteria = json.load(f)
            criteria = {**criteria, **user_criteria}
            log("[MAIN] Loaded custom criteria JSON")
        except Exception as e:
            log(f"[MAIN] Could not load criteria file: {e}")
    labels = None
    if args.labels:
        labels = [c.strip() for c in args.labels.split(",") if c.strip()]
        log(f"[MAIN] Using labels: {labels}")
    res = run_pipeline(
        labels=labels,
        results_per_label=args.results_per_label or 8,
        process_existing=args.process_existing,
        criteria=criteria
    )
    print(f"Scraped: {len(res.scraped)} | Converted: {len(res.converted_from_processed)} | Skipped dups: {res.skipped_duplicates}")

if __name__ == "__main__":
    main()
