from intelligence.local_llm import run_llm


def summarize_article(article: dict) -> list[str]:
    summary_text = article.get("summary") or "No summary provided."

    prompt = f"""
You are a financial news summarizer.

STRICT RULES:
- Output ONLY plain text
- One sentence per line
- NO bullet symbols
- NO numbering
- NO markdown
- NO JSON
- NO headings

TASK:
Write 3–5 short factual sentences summarizing the article.

ARTICLE:
{summary_text}
"""

    raw = run_llm(prompt)

    # 🔥 NORMALIZATION LAYER (THIS IS WHAT WAS MISSING)
    lines = []
    for line in raw.splitlines():
        line = line.strip()

        # remove any accidental bullets / dashes
        line = line.lstrip("•-*–— ").strip()

        if line:
            lines.append(line)

    return lines
