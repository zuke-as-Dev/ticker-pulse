# ingestion/article_fetcher.py

import requests
from newspaper import Article
from readability import Document
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (TickerPulseBot/1.0)"
}

def fetch_full_article(url: str) -> str:
    # --- Method 1: newspaper3k ---
    try:
        article = Article(url)
        article.download()
        article.parse()
        if article.text and len(article.text) > 500:
            return article.text[:8000]
    except Exception:
        pass

    # --- Method 2: readability-lxml ---
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        doc = Document(resp.text)
        soup = BeautifulSoup(doc.summary(), "html.parser")
        text = soup.get_text(separator="\n")
        cleaned = _clean(text)
        if len(cleaned) > 500:
            return cleaned[:8000]
    except Exception:
        pass

    # --- Method 3: basic fallback ---
    try:
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        return _clean(soup.get_text(separator="\n"))[:4000]
    except Exception:
        return ""

def _clean(text: str) -> str:
    lines = [
        line.strip()
        for line in text.splitlines()
        if len(line.strip()) > 40
    ]
    return "\n".join(lines)
