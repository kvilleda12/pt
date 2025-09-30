import re
from bs4 import BeautifulSoup
from logger import log

def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    
    # Remove unwanted elements
    for tag in soup(["script", "style", "noscript", "header", "footer", "nav", 
                    "img", "svg", "iframe", "video", "audio", "aside", "advertisement"]):
        tag.decompose()
    
    # Preserve structure for lists and numbered instructions
    for ul in soup.find_all(['ul', 'ol']):
        ul.name = 'div'
        ul['class'] = 'list-content'
    
    # Convert headings to preserve structure
    for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        heading.name = 'div'
        heading.string = f"\n{heading.get_text().strip()}\n"
    
    # Preserve paragraph breaks
    for p in soup.find_all('p'):
        p.string = f"{p.get_text().strip()}\n"
    
    # Get text with better formatting
    text = soup.get_text(separator="\n", strip=True)
    
    # Clean up whitespace while preserving structure
    lines = []
    for line in text.splitlines():
        # Clean excessive whitespace
        cleaned = re.sub(r'\s+', ' ', line.strip())
        if cleaned:
            lines.append(cleaned)
    
    # Join with single newlines
    out = '\n'.join(lines)
    
    # Remove excessive blank lines
    out = re.sub(r'\n{3,}', '\n\n', out)
    
    log(f"[HTML] Extracted {len(out)} chars of text")
    return out