from intelligence.local_llm import run_llm


def summarize_article(article: dict) -> str:
    prompt = f"""
You are a financial news analyst.

Summarize the following news into 3–5 concise bullet points.
Focus on facts and market impact. Avoid opinions.

TITLE:
{article['title']}

SUMMARY:
{article['summary']}
"""

    return run_llm(prompt)
