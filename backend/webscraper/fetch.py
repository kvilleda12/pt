import time
from typing import Optional
import requests
import urllib.robotparser as urobot
from urllib.parse import urlparse
from config import USER_AGENT, REQUEST_TIMEOUT, RETRIES, BACKOFF
from logger import log

def robots_allowed(url: str, user_agent: str = USER_AGENT) -> bool:
    try:
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        rp = urobot.RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        allowed = rp.can_fetch(user_agent, url)
        log(f"[ROBOTS] {url} -> {'ALLOW' if allowed else 'DISALLOW'}")
        return allowed
    except Exception as e:
        log(f"[ROBOTS] {url} -> ALLOW (fallback: {e})")
        return True

def http_get(url: str) -> Optional[requests.Response]:
    for i in range(RETRIES + 1):
        try:
            log(f"[FETCH] GET {url} (attempt {i+1})")
            resp = requests.get(url, timeout=REQUEST_TIMEOUT, headers={"User-Agent": USER_AGENT})
            resp.raise_for_status()
            log(f"[FETCH] OK {url} ({len(resp.text)} bytes)")
            return resp
        except Exception as e:
            log(f"[FETCH] ERR {url}: {e}")
            if i < RETRIES:
                time.sleep(BACKOFF ** (i + 1))
    return None
