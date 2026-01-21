import os
from pathlib import Path
from dotenv import load_dotenv

from alerts.telegram_bot import send_message
from agent.scheduler import sleep_minutes

# Load .env explicitly from project root
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

CHECK_INTERVAL_MINUTES = float(os.getenv("CHECK_INTERVAL_MINUTES", 15))

def run_agent():
    send_message("🟢 Ticker Pulse started — agent is online")

    while True:
        try:
            # Heartbeat (proves the agent is alive)
            send_message("⏱️ Ticker Pulse heartbeat — agent running")

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
