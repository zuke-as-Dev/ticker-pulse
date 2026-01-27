from pathlib import Path
import yaml
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent.parent
WEIGHTS_FILE = BASE_DIR / "config" / "source_weights.yaml"

WEIGHT_MAP = {"high": 3, "medium": 2, "low": 1}

def load_source_weights():
    with open(WEIGHTS_FILE, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    domain_weights = {}
    for level, domains in raw.items():
        for d in domains:
            domain_weights[d] = WEIGHT_MAP[level]
    return domain_weights

SOURCE_WEIGHTS = load_source_weights()

def get_source_weight(url: str) -> int:
    domain = urlparse(url).netloc.replace("www.", "")
    return SOURCE_WEIGHTS.get(domain, 1)
