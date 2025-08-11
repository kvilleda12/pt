import re
from bs4 import BeautifulSoup
from logger import log

def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script","style","noscript","header","footer","nav","img","svg","iframe","video","audio"]):
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]
    out = "\n".join(lines)
    log(f"[HTML] Extracted {len(out)} chars of text")
    return out