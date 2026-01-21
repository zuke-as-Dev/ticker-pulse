from intelligence.local_llm import run_llm


def summarize_article(article: dict) -> str:
    summary_text = article["summary"] or "No summary provided."

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
{summary_text}
"""

    return run_llm(prompt)

