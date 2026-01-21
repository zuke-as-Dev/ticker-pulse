import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Explicitly load .env from project root
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


def send_message(text: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise ValueError("Telegram credentials missing in .env file")

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }

    response = requests.post(TELEGRAM_API_URL, json=payload)

    if response.status_code != 200:
        raise RuntimeError(f"Telegram API error: {response.text}")

    return response.json()
