from dotenv import load_dotenv
load_dotenv()
from intelligence.llm_config import LLM_MODEL, LLM_TEMPERATURE
import os
from pathlib import Path
import sys
from dotenv import load_dotenv
from agent.state import load_instruments
from alerts.telegram_bot import send_message
from agent.scheduler import sleep_minutes
from ingestion.rss_fetcher import fetch_articles
from ingestion.parser import normalize_articles
from intelligence.relevance import filter_relevant_articles
from agent.memory import is_new_article
from intelligence.summarizer import summarize_article
from intelligence.bias_classifier import classify_bias
from agent.memory import clear_memory
from alerts.formatter import format_alert
import threading
from alerts.telegram_bot import poll_messages
from ingestion.article_fetcher import fetch_full_article
from agent.state import build_keyword_map
from ingestion.source_ranker import get_source_weight
from ingestion.deduplicator import story_hash


# Debug: print LLM config on startup
print("🧠 LLM CONFIG")
print(f"Model       : {LLM_MODEL}")
print(f"Temperature : {LLM_TEMPERATURE}")
print("-" * 40)


# Load .env explicitly from project root
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

CHECK_INTERVAL_MINUTES = float(os.getenv("CHECK_INTERVAL_MINUTES", 15))

def run_agent():
    threading.Thread(target=poll_messages, daemon=True).start()
    instruments = load_instruments()
    instrument_list = ", ".join(instruments.keys())
    keyword_map = build_keyword_map(instruments)

    send_message(
    f"🟢 Ticker Pulse started\n"
    f"📡 Tracking instruments: {instrument_list}")

    #clear_memory()

    while True:
        try:
            # Debug: confirm tracked instruments
            print(f"Tracking {len(instruments)} instruments")

            # Heartbeat (proves the agent is alive)
            send_message("⏱️ Ticker Pulse heartbeat — agent running")

             # ---- News ingestion ----
            raw_articles = fetch_articles(keyword_map)
            print(f"Fetched {len(raw_articles)} articles")
            articles = normalize_articles(raw_articles)
            relevant = filter_relevant_articles(articles, instruments)

            # Debug: print relevant articles count
            # new_relevant = []

            # for item in relevant:
            #     article = item["article"]
            #     if is_new_article(article["title"], article["source"]):
            #         new_relevant.append(item)
            # print(f"Relevant new articles: {len(new_relevant)}")

            # Debug: print relevance breakdown
            per_symbol_count = {}
            for item in relevant:
                sym = item["symbol"]
                per_symbol_count[sym] = per_symbol_count.get(sym, 0) + 1

            print("\n[RELEVANCE BREAKDOWN]")
            for sym, count in per_symbol_count.items():
                print(f"{sym} : {count}")
            print("-" * 40)

            # ---- Deduplication based on source weight ----
            deduped = {}

            for item in relevant:
                article = item["article"]
                h = story_hash(article["title"])
                weight = get_source_weight(article["link"])

                if h not in deduped or weight > deduped[h]["weight"]:
                    deduped[h] = {
                        "item": item,
                        "weight": weight
                    }

            final_items = [v["item"] for v in deduped.values()]

            print(f"Deduplicated articles sent: {len(final_items)}")

            for item in final_items:
                article = item["article"]

                # Fetch full article text
                full_text = fetch_full_article(article["link"])
                article["content"] = full_text or article["summary"]
                # Debug: log enrichment
                print(f"[ENRICH] {item['symbol']} ← {len(article['content'])} chars")
                print("[DEBUG] Calling LLM...")

                summary = summarize_article(article)  # ← list[str]
                bias, reason = classify_bias(article["title"], summary)

                message = format_alert(
                    symbol=item["symbol"],
                    title=article["title"],
                    summary=summary,          # ← pass list, NOT string
                    bias=bias,
                    reason=reason,
                    source=article["source"],
                    link=article["link"],
                )

                send_message(message)

        except Exception as e:
            send_message(f"⚠️ Ticker Pulse error: {e}")

        sleep_minutes(CHECK_INTERVAL_MINUTES)


if __name__ == "__main__":
    if "--clear-memory" in sys.argv:
        clear_memory()
        sys.exit(0)
    run_agent()
