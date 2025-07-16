import os, time, csv
from pathlib import Path
from googlesearch import search
from newspaper import Article
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import argparse
import itertools

# === Folder setup ===
ROOT = Path(__file__).resolve().parent.parent  # Root of the backend folder
TEXT_DIR = ROOT / "backend" / "text_files"  # Text-only articles
FILE_SOURCES_DIR = ROOT / "backend" / "file_sources"  # Articles with images
LOG_PATH = ROOT / "backend" / "database" / "web_sources.csv"

TEXT_DIR.mkdir(parents=True, exist_ok=True)
FILE_SOURCES_DIR.mkdir(parents=True, exist_ok=True)
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0"}

# === Utility ===
def get_domain(url: str) -> str:
    return urlparse(url).netloc.replace("www.", "")

# === Core scraping logic ===
def google_search(query: str, num_results=10):
    return list(search(query, num_results=num_results, lang="en"))

def extract_text(url: str):
    """Returns (text, has_images)"""
    try:
        article = Article(url)
        article.download()
        article.parse()
        has_images = bool(article.top_image or article.images)
        return article.text, has_images
    except:
        try:
            res = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(res.content, "html.parser")
            text = "\n".join(p.text for p in soup.find_all("p") if len(p.text.strip()) > 30)
            has_images = bool(soup.find_all("img"))
            return text, has_images
        except Exception as e:
            print(f"❌ Failed to extract {url}: {e}")
            return "", False

def save_text(text: str, url: str, has_images: bool) -> Path:
    name = url.split("//")[-1].split("/")[0].replace(".", "_")
    folder = FILE_SOURCES_DIR if has_images else TEXT_DIR
    filename = folder / f"{name}_{int(time.time())}.txt"
    filename.write_text(text, encoding="utf-8")
    return filename

def log_source(url: str, filepath: Path, has_images: bool):
    write_header = not LOG_PATH.exists()
    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["timestamp", "url", "domain", "file_path", "has_images"])
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), url, get_domain(url), str(filepath), has_images])

def scrape_sources(query: str, max_results=5):
    print(f"\n🔍 Scraping sources for: {query}")
    urls = google_search(query, num_results=max_results)
    for url in urls:
        text, has_images = extract_text(url)
        print(f"🔗 Source: {url} | Has images: {has_images}")
        if len(text) > 300:
            filepath = save_text(text, url, has_images)
            log_source(url, filepath, has_images)
            print(f"✅ Saved: {url} {'(with images)' if has_images else '(text only)'}")
        else:
            print(f"⚠️ Skipped (too short): {url}")

# === CLI entry point ===
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape web sources for PT topics.")
    parser.add_argument("--query", type=str, help="Search query to scrape")
    parser.add_argument("--topics-file", type=str, help="Text file with one query per line")
    parser.add_argument("--max", type=int, default=5, help="Max number of search results per query")
    parser.add_argument("--interval", type=int, default=6, help="Delay between topics in minutes")
    parser.add_argument("--limit", type=int, default=10, help="Number of topics to scrape per cycle")
    args = parser.parse_args()

    if args.query:
        scrape_sources(query=args.query, max_results=args.max)

    elif args.topics_file:
        topics_path = Path(args.topics_file)
        if not topics_path.exists():
            print(f"❌ File not found: {topics_path}")
            exit(1)

        with topics_path.open("r") as f:
            topics = [line.strip() for line in f if line.strip()]

        if not topics:
            print("⚠️ No topics found in file.")
            exit(1)

        delay = args.interval * 60  # convert to seconds
        max_per_cycle = args.limit

        print(f"\n🔁 Starting scraper loop (up to {max_per_cycle} topics per cycle, {args.interval} min interval)...")

        seen = set()
        for cycle_num in itertools.count(1):
            print(f"\n=== Cycle {cycle_num} ===")
            count = 0

            for topic in topics:
                if topic in seen:
                    continue

                print(f"\n⏳ [{count+1}/{max_per_cycle}] Scraping topic: {topic}")
                scrape_sources(query=topic, max_results=args.max)
                seen.add(topic)
                count += 1

                if count >= max_per_cycle:
                    print(f"\n✅ Reached limit of {max_per_cycle} topics for this cycle.")
                    break

                print(f"🕒 Waiting {args.interval} minutes before next topic...\n")
                time.sleep(delay)

            print(f"\n🔁 Sleeping for 60 seconds before next cycle...\n")
            time.sleep(60)  # cooldown before next cycle

    else:
        print("⚠️ Please provide either --query or --topics-file.")
        print("Example: python web_scraper.py --query 'ACL rehab'")
        print("         python web_scraper.py --topics-file topics.txt --interval 6 --limit 10")