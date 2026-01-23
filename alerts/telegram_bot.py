import os
import time
import requests
from alerts.telegram_commands import handle_message
from alerts.markdown import escape_md

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

API_URL = f"https://api.telegram.org/bot{TOKEN}"


def send_message(text: str):
    if not TOKEN or not CHAT_ID:
        raise ValueError("Telegram credentials missing in .env file")

    payload = {
        "chat_id": CHAT_ID,
        "text": escape_md(text),
        "parse_mode": "MarkdownV2",
        "disable_web_page_preview": True,
    }

    response = requests.post(f"{API_URL}/sendMessage", json=payload)

    # Prevent thread crash
    if not response.ok:
        print("[TELEGRAM ERROR]", response.text)


def poll_messages():
    """
    Long-poll Telegram for new messages and route commands.
    """
    offset = None

    while True:
        params = {"timeout": 30}
        if offset:
            params["offset"] = offset

        response = requests.get(f"{API_URL}/getUpdates", params=params)
        response.raise_for_status()

        data = response.json()

        for update in data.get("result", []):
            offset = update["update_id"] + 1

            message = update.get("message")
            if not message:
                continue

            text = message.get("text")
            if not text:
                continue

            # Route command text
            handle_message(text.strip(), send_message)

        time.sleep(1)