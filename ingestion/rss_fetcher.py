from pathlib import Path
import feedparser
import yaml
from urllib.parse import urlparse
import socket

# Set a global timeout for socket operations (e.g., RSS fetching)
socket.setdefaulttimeout(10)  # ⏱️ hard timeout for RSS fetch


# Debug: confirm module loaded
print("✅ rss_fetcher.py LOADED FROM:", __file__)


BASE_DIR = Path(__file__).resolve().parent.parent

LEGACY_FEEDS_FILE = BASE_DIR / "config" / "feeds.yaml"
RSS_DIR = BASE_DIR / "rss"


def load_legacy_feeds() -> dict:
    if not LEGACY_FEEDS_FILE.exists():
        return {}

    with open(LEGACY_FEEDS_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_rss_directory_feeds() -> dict:
    feeds = {}

    if not RSS_DIR.exists():
        return feeds

    for yml_file in RSS_DIR.glob("*.yml"):
        category = yml_file.stem

        with open(yml_file, "r", encoding="utf-8") as f:
            urls = yaml.safe_load(f) or []

        feeds[category] = []

        for url in urls:
            parsed = urlparse(url)
            feeds[category].append(
                {
                    "name": f"{category}:{parsed.netloc}",
                    "url": url,
                }
            )

    return feeds



def load_all_feeds() -> dict:
    feeds = {}

    legacy = load_legacy_feeds()
    rss_dir_feeds = load_rss_directory_feeds()

    # Merge legacy feeds first
    feeds.update(legacy)

    # Add / override with rss directory feeds
    for category, feed_list in rss_dir_feeds.items():
        feeds.setdefault(category, [])
        feeds[category].extend(feed_list)

    return feeds


def fetch_articles() -> list:

    feeds = load_all_feeds()
    articles = []
    feed_stats = {}
    
    for category, feed_list in feeds.items():
        for feed in feed_list:
            
            # Debug: log feed being processed
            print(f"[RSS FETCH] {feed['name']}")


            # Validation
            if not isinstance(feed["url"], str):
                raise TypeError(f"Feed URL is not a string: {feed['url']}")


            try:
                parsed = feedparser.parse(feed["url"])
            except Exception as e:
                 print(f"[RSS ERROR] {feed['name']} → {e}")
                 continue
            count = 0

            for entry in parsed.entries:
                articles.append({
                    "title": entry.get("title", "").strip(),
                    "summary": entry.get("summary", "").strip(),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "source": feed["name"],
                    "category": category,
                })
                count += 1

            feed_stats[feed["name"]] = count

    # 🔍 Per-feed logging
    for feed_name, count in feed_stats.items():
        print(f"[RSS] {feed_name} → {count} articles")

    # 🔍 Category summary
    category_totals = {}
    for article in articles:
        category_totals[article["category"]] = (
            category_totals.get(article["category"], 0) + 1
        )

    print("\n[RSS SUMMARY]")
    print(f"Total feeds checked : {len(feed_stats)}")
    print(f"Total articles fetched : {len(articles)}")

    for category, count in category_totals.items():
        print(f"{category} : {count}")

    print("-" * 40)

    return articles
