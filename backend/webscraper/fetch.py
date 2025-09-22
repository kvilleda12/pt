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
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    
    for i in range(RETRIES + 1):
        try:
            log(f"[FETCH] GET {url} (attempt {i+1})")
            resp = requests.get(
                url, 
                timeout=REQUEST_TIMEOUT, 
                headers=headers,
                allow_redirects=True,
                stream=False
            )
            resp.raise_for_status()
            
            # Check content type
            content_type = resp.headers.get('content-type', '').lower()
            if 'text/html' not in content_type and 'application/xhtml' not in content_type:
                log(f"[FETCH] SKIP {url} - not HTML content: {content_type}")
                return None
            
            # Check content length
            content_length = len(resp.text)
            if content_length < 100:
                log(f"[FETCH] SKIP {url} - content too short: {content_length} bytes")
                return None
                
            log(f"[FETCH] OK {url} ({content_length} bytes)")
            return resp
            
        except requests.exceptions.Timeout:
            log(f"[FETCH] TIMEOUT {url} (attempt {i+1})")
        except requests.exceptions.ConnectionError:
            log(f"[FETCH] CONNECTION ERROR {url} (attempt {i+1})")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code in [403, 404, 429]:
                log(f"[FETCH] HTTP ERROR {url}: {e.response.status_code}")
                return None  # Don't retry these errors
            log(f"[FETCH] HTTP ERROR {url}: {e}")
        except Exception as e:
            log(f"[FETCH] ERR {url}: {e}")
            
        if i < RETRIES:
            sleep_time = BACKOFF ** (i + 1)
            log(f"[FETCH] Retrying in {sleep_time}s...")
            time.sleep(sleep_time)
    
    log(f"[FETCH] FAILED {url} after {RETRIES + 1} attempts")
    return None
