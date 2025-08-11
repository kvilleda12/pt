import time
from typing import List
import requests
from config import SERP_API_KEY, REQUEST_TIMEOUT, SEARCH_SLEEP
from logger import log

def search_serpapi(query: str, num: int) -> List[str]:
    if not SERP_API_KEY:
        log("[SEARCH] SERP_API_KEY missing")
        return []
    log(f"[SEARCH] Query: {query} (limit {num})")
    params = {"engine":"google","q":query,"num":min(num,10),"api_key":SERP_API_KEY}
    r = requests.get("https://serpapi.com/search.json", params=params, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    data = r.json()
    links = [it.get("link") for it in data.get("organic_results", []) if it.get("link")]
    log(f"[SEARCH] Got {len(links)} URLs")
    return links[:num]

def search_web(query: str, num: int) -> List[str]:
    urls = search_serpapi(query, num)
    time.sleep(SEARCH_SLEEP)
    return urls
