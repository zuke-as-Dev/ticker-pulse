from pathlib import Path
import feedparser
import yaml
from urllib.parse import urlparse
import socket

# ⏱️ Hard timeout for RSS fetch
socket.setdefaulttimeout(10)

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

    feeds.update(load_legacy_feeds())

    rss_dir_feeds = load_rss_directory_feeds()
    for category, feed_list in rss_dir_feeds.items():
        feeds.setdefault(category, [])
        feeds[category].extend(feed_list)

    return feeds


def fetch_articles(keyword_map: dict | None = None) -> list:
    """
    Fetch RSS articles and optionally pre-filter them
    using instrument keyword map.
    """

    feeds = load_all_feeds()
    articles = []
    feed_stats = {}

    for category, feed_list in feeds.items():
        for feed in feed_list:
            print(f"[RSS FETCH] {feed['name']}")

            if not isinstance(feed["url"], str):
                print(f"[RSS ERROR] Invalid URL type → {feed['url']}")
                continue

            try:
                parsed = feedparser.parse(feed["url"])
            except Exception as e:
                print(f"[RSS ERROR] {feed['name']} → {e}")
                continue

            count = 0

            for entry in parsed.entries:
                title = entry.get("title", "").strip()
                summary = entry.get("summary", "").strip()

                # 🔍 Keyword pre-filter
                if keyword_map:
                    text_blob = f"{title} {summary}".lower()
                    matched = False

                    for terms in keyword_map.values():
                        if any(term in text_blob for term in terms):
                            matched = True
                            break

                    if not matched:
                        continue

                articles.append({
                    "title": title,
                    "summary": summary,
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
