import json
import re
from intelligence.local_llm import run_llm


def _extract_json(text: str) -> dict | None:
    """
    Extract first JSON object found in text.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None

    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return None


def profile_instrument(ticker: str) -> dict:
    prompt = f"""
You are a financial market classifier.

Given the ticker: {ticker}

Return ONLY a JSON object with these fields:
- type: one of [stock, commodity, forex, crypto, index]
- name: human-readable name
- primary_terms: list of exact identifiers used in headlines
- secondary_terms: list of contextual drivers
- market: one of [india, global, forex, crypto]

IMPORTANT:
- Respond with JSON ONLY
- No explanation
- No markdown
"""

    # Try twice before failing
    for attempt in range(2):
        output = run_llm(prompt)

        profile = _extract_json(output)
        if profile:
            return profile

    raise ValueError(f"Failed to parse instrument profile for {ticker}")