import json
from pathlib import Path
from intelligence.profiler import profile_instrument

STORE = Path("data/tracked_instruments.json")
PENDING = Path("data/pending_confirmations.json")


def load_pending():
    if not PENDING.exists():
        return {}

    try:
        content = PENDING.read_text().strip()
        if not content:
            return {}
        return json.loads(content)
    except Exception:
        # Auto-heal corrupted file
        return {}


def save_pending(data: dict):
    tmp = PENDING.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2))
    tmp.replace(PENDING)

def load_tracked():
    if not STORE.exists():
        return {}

    try:
        content = STORE.read_text().strip()
        if not content:
            return {}
        return json.loads(content)
    except Exception:
        return {}


def save_tracked(data: dict):
    tmp = STORE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2))
    tmp.replace(STORE)


def track_instrument(ticker: str) -> dict:
    data = load_tracked()

    if ticker in data:
        return data[ticker]

    profile = profile_instrument(ticker)
    data[ticker] = profile
    save_tracked(data)

    return profile