#!/usr/bin/env python3
import argparse
import json
import sys
import time
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).resolve().parent))

from pipeline import run_pipeline
from config import DEFAULT_CRITERIA, SEARCH_RESULTS_PER_LABEL
from logger import log
from storage import load_links

def parse_args(argv):
    ap = argparse.ArgumentParser(description="Enhanced PT web scraper: search -> fetch -> classify -> archive.")
    ap.add_argument("--labels", help="Comma-separated label codes (e.g., n,rs,lh). Default: all.")
    ap.add_argument("--results-per-label", type=int, default=SEARCH_RESULTS_PER_LABEL, help="Search results per query template.")
    ap.add_argument("--process-existing", action="store_true", help="Convert files already in processed/ to raw/ and archive.")
    ap.add_argument("--criteria", help="Path to JSON to override classification criteria.")
    ap.add_argument("--dry-run", action="store_true", help="Show what would be scraped without actually doing it.")
    ap.add_argument("--verbose", action="store_true", help="Enable verbose logging.")
    ap.add_argument("--max-duration", type=int, default=3600, help="Maximum runtime in seconds (default: 1 hour).")
    return ap.parse_args(argv)

def print_stats():
    """Print current statistics about scraped content."""
    links = load_links()
    total = len(links)
    viable = sum(1 for link in links if link.get("viable", False))
    classified = sum(1 for link in links if link.get("viable") is not None)
    
    print(f"\n📊 CURRENT STATISTICS:")
    print(f"   Total documents: {total}")
    print(f"   Classified: {classified}")
    print(f"   Viable content: {viable}")
    print(f"   Success rate: {(viable/classified*100):.1f}%" if classified > 0 else "   Success rate: N/A")
    
    # Count by labels
    label_counts = {}
    for link in links:
        if link.get("viable", False):
            for label in link.get("labels", []):
                label_counts[label] = label_counts.get(label, 0) + 1
    
    if label_counts:
        print(f"   Content by body part:")
        for label, count in sorted(label_counts.items()):
            print(f"     {label}: {count}")

def main(argv=None):
    start_time = time.time()
    args = parse_args(argv or sys.argv[1:])
    
    # Set verbose mode
    if args.verbose:
        import os
        os.environ["PT_VERBOSE"] = "1"
    
    print("🚀 PT Web Scraper Starting...")
    print(f"   Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Max duration: {args.max_duration}s")
    
    # Load criteria
    criteria = DEFAULT_CRITERIA
    if args.criteria:
        try:
            with open(args.criteria, "r", encoding="utf-8") as f:
                user_criteria = json.load(f)
            criteria = {**criteria, **user_criteria}
            log("[MAIN] Loaded custom criteria JSON")
        except Exception as e:
            log(f"[MAIN] Could not load criteria file: {e}")
    
    # Parse labels
    labels = None
    if args.labels:
        labels = [c.strip() for c in args.labels.split(",") if c.strip()]
        log(f"[MAIN] Using labels: {labels}")
    
    # Show current stats
    print_stats()
    
    if args.dry_run:
        print("\n🔍 DRY RUN MODE - No actual scraping will occur")
        print(f"   Would search for labels: {labels or 'all'}")
        print(f"   Results per label: {args.results_per_label}")
        return
    
    # Run the pipeline
    try:
        print(f"\n🔄 Starting scraping pipeline...")
        res = run_pipeline(
            labels=labels,
            results_per_label=args.results_per_label,
            process_existing=args.process_existing,
            criteria=criteria
        )
        
        # Print results
        elapsed = time.time() - start_time
        print(f"\n✅ SCRAPING COMPLETED in {elapsed:.1f}s")
        print(f"   New documents scraped: {len(res.scraped)}")
        print(f"   Files converted: {len(res.converted_from_processed)}")
        print(f"   Duplicates skipped: {res.skipped_duplicates}")
        
        # Show updated stats
        print_stats()
        
    except KeyboardInterrupt:
        print(f"\n⏹️  Scraping interrupted by user after {time.time() - start_time:.1f}s")
    except Exception as e:
        print(f"\n❌ Scraping failed: {e}")
        log(f"[MAIN] ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
