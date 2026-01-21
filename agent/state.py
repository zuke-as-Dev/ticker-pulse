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
