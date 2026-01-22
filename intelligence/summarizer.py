from intelligence.local_llm import run_llm


def summarize_article(article: dict) -> str:
    summary_text = article.get("summary") or "No summary provided."

    prompt = f"""
You are a financial news analyst.
Respond in English only.

Summarize the news into 3–5 concise bullet points.
DO NOT include opinions, bias, or recommendations.
ONLY factual bullet points.

TITLE:
{article.get('title', '')}

SUMMARY:
{summary_text}
"""

    return run_llm(prompt)