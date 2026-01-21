import json
from pathlib import Path
import hashlib

BASE_DIR = Path(__file__).resolve().parent.parent
MEMORY_FILE = BASE_DIR / "data" / "processed_articles.json"


def _load_memory() -> set:
    if not MEMORY_FILE.exists():
        return set()

    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return set(json.load(f))


def _save_memory(hashes: set):
    MEMORY_FILE.parent.mkdir(exist_ok=True)

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(list(hashes), f)


def article_hash(title: str, source: str) -> str:
    key = f"{title}:{source}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def is_new_article(title: str, source: str) -> bool:
    hashes = _load_memory()
    h = article_hash(title, source)

    if h in hashes:
        return False

    hashes.add(h)
    _save_memory(hashes)
    return True
def clear_memory():
    """
    Clears all processed article memory.
    Useful for testing.
    """
    if MEMORY_FILE.exists():
        MEMORY_FILE.unlink()
        print("[MEMORY] Cleared processed articles memory")
    else:
        print("[MEMORY] No memory file to clear")
