from intelligence.local_llm import run_llm


def classify_bias(article: dict) -> tuple[str, str]:
    summary_text = article.get("summary") or "No summary provided."

    prompt = f"""
You are a trading analyst.
Respond in English only.

Determine the SHORT-TERM market bias for the instrument.

Respond in EXACTLY this format (no extra text):

Bias: <Bullish | Bearish | Neutral | Unclear>
Reason: <one concise sentence>

TITLE:
{article.get('title', '')}

SUMMARY:
{summary_text}
"""

    output = run_llm(prompt)

    bias = "Unclear"
    reason = "No clear signal."

    for line in output.splitlines():
        if line.lower().startswith("bias:"):
            bias = line.split(":", 1)[1].strip()
        elif line.lower().startswith("reason:"):
            reason = line.split(":", 1)[1].strip()

    return bias, reason