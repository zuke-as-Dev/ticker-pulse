from agent.tracker import track_instrument


def handle_message(text: str, send_message):
    text = text.strip()

    # -------------------------
    # /track COMMAND
    # -------------------------
    if text.startswith("/track"):
        parts = text.split(maxsplit=1)

        if len(parts) < 2:
            send_message("⚠️ Usage: /track <TICKER>")
            return

        ticker = parts[1].upper()

        try:
            profile = track_instrument(ticker)

        except Exception:
            # Mark ticker as pending confirmation
            from agent.tracker import load_pending, save_pending

            pending = load_pending()
            pending[ticker] = {"status": "awaiting_confirmation"}
            save_pending(pending)

            send_message(
                f"⚠️ I couldn’t confidently identify {ticker}.\n\n"
                "Please confirm instrument type by replying:\n"
                "confirm stock | confirm forex | confirm commodity | confirm crypto"
            )
            return

        message = (
            f"✅ Now tracking {ticker}\n\n"
            f"Type: {profile['type'].title()}\n"
            f"Name: {profile['name']}\n\n"
            f"Primary identifiers:\n"
            + "\n".join(f"• {t}" for t in profile["primary_terms"])
            + "\n\nContext drivers:\n"
            + "\n".join(f"• {t}" for t in profile["secondary_terms"])
            + "\n\nStatus: Active"
        )

        send_message(message)
        return

    # -------------------------
    # confirm <type> COMMAND
    # -------------------------
    if text.startswith("confirm"):
        parts = text.split(maxsplit=1)

        if len(parts) < 2:
            send_message("⚠️ Usage: confirm <stock|forex|commodity|crypto>")
            return

        confirmed_type = parts[1].lower()

        if confirmed_type not in {"stock", "forex", "commodity", "crypto"}:
            send_message("⚠️ Invalid type. Choose stock, forex, commodity, or crypto.")
            return

        from agent.tracker import (
            load_pending,
            save_pending,
            load_tracked,
            save_tracked,
        )

        pending = load_pending()

        if not pending:
            send_message("ℹ️ No instrument awaiting confirmation.")
            return

        # Single-user assumption: confirm the most recent pending ticker
        ticker = list(pending.keys())[-1]

        profile = {
            "type": confirmed_type,
            "name": ticker,
            "primary_terms": [ticker],
            "secondary_terms": [],
            "market": confirmed_type,
        }

        tracked = load_tracked()
        tracked[ticker] = profile
        save_tracked(tracked)

        pending.pop(ticker)
        save_pending(pending)

        send_message(
            f"✅ Now tracking {ticker}\n\n"
            f"Type: {confirmed_type.title()}\n"
            "Status: Active"
        )
        return