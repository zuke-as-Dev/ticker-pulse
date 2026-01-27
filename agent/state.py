from pathlib import Path
import yaml


BASE_DIR = Path(__file__).resolve().parent.parent
INSTRUMENTS_FILE = BASE_DIR / "config" / "instruments.yaml"


def load_instruments() -> dict:
    if not INSTRUMENTS_FILE.exists():
        raise FileNotFoundError("instruments.yaml not found")

    with open(INSTRUMENTS_FILE, "r", encoding="utf-8") as f:
        instruments = yaml.safe_load(f)

    return instruments

def build_keyword_map(instruments: dict) -> dict:
    keyword_map = {}

    for symbol, meta in instruments.items():
        terms = set()

        terms.add(symbol.lower())
        terms.add(meta.get("name", "").lower())

        for t in meta.get("primary_terms", []):
            terms.add(t.lower())

        for t in meta.get("secondary_terms", []):
            terms.add(t.lower())

        keyword_map[symbol] = [t for t in terms if t]

    return keyword_map
