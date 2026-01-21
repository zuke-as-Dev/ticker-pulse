import os
from pathlib import Path
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


# Load .env explicitly from project root
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

CHECK_INTERVAL_MINUTES = float(os.getenv("CHECK_INTERVAL_MINUTES", 15))

def run_agent():
    instruments = load_instruments()
    instrument_list = ", ".join(instruments.keys())

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
            raw_articles = fetch_articles()
            articles = normalize_articles(raw_articles)
            raw_articles = fetch_articles()
            articles = normalize_articles(raw_articles)
            relevant = filter_relevant_articles(articles, instruments)

            new_relevant = []

            for item in relevant:
                article = item["article"]
                if is_new_article(article["title"], article["source"]):
                    new_relevant.append(item)
            print(f"Relevant new articles: {len(new_relevant)}")

            for item in new_relevant:
                article = item["article"]

                print("\n--- AI ANALYSIS ---")
                print(f"Instrument: {item['symbol']}")

                print("[AI] Generating summary...")
                summary = summarize_article(article)
                print(summary)

                print("[AI] Classifying bias...")
                bias = classify_bias(article)
                print(bias)


        except Exception as e:
            send_message(f"⚠️ Ticker Pulse error: {e}")

        sleep_minutes(CHECK_INTERVAL_MINUTES)


if __name__ == "__main__":
    run_agent()
