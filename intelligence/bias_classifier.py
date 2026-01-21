from intelligence.local_llm import run_llm


def classify_bias(article: dict) -> str:
    prompt = f"""
You are a trading analyst.
Respond in English only.

Based on the news below, classify the likely short-term market impact
on the related instrument as ONE of:

- Bullish
- Bearish
- Neutral
- Unclear

Then give ONE short reason.

Respond in this exact format:
Bias: <one word>
Reason: <one sentence>

TITLE:
{article['title']}

SUMMARY:
{article['summary']}
"""

    return run_llm(prompt)
