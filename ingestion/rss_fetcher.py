from pathlib import Path
import feedparser
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
FEEDS_FILE = BASE_DIR / "config" / "feeds.yaml"


def load_feeds() -> dict:
    if not FEEDS_FILE.exists():
        raise FileNotFoundError("feeds.yaml not found")

    with open(FEEDS_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def fetch_articles() -> list:
    feeds = load_feeds()
    articles = []

    for category, feed_list in feeds.items():
        for feed in feed_list:
            parsed = feedparser.parse(feed["url"])

            for entry in parsed.entries:
                articles.append({
                    "title": entry.get("title", ""),
                    "summary": entry.get("summary", ""),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "source": feed["name"],
                    "category": category,
                })
    print(f"[MAC RSS DEBUG] Total raw articles fetched: {len(articles)}")
    return articles
