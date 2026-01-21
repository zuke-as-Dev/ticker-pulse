import os
from pathlib import Path
from dotenv import load_dotenv
from agent.state import load_instruments
from alerts.telegram_bot import send_message
from agent.scheduler import sleep_minutes
from ingestion.rss_fetcher import fetch_articles
from ingestion.parser import normalize_articles

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


    while True:
        try:
            # Debug: confirm tracked instruments
            print(f"Tracking {len(instruments)} instruments")

            # Heartbeat (proves the agent is alive)
            send_message("⏱️ Ticker Pulse heartbeat — agent running")

             # ---- News ingestion ----
            raw_articles = fetch_articles()
            articles = normalize_articles(raw_articles)

            print(f"Fetched {len(articles)} articles")
            # ---- Future logic plugs in here ----
            # fetch_news()
            # analyze_news()
            # send_alerts()
            # -----------------------------------

        except Exception as e:
            send_message(f"⚠️ Ticker Pulse error: {e}")

        sleep_minutes(CHECK_INTERVAL_MINUTES)


if __name__ == "__main__":
    run_agent()
