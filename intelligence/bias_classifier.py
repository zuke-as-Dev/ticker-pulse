from intelligence.local_llm import run_llm


def classify_bias(title: str, summary_points: list[str]) -> tuple[str, str]:
    joined_summary = " ".join(summary_points)

    prompt = f"""
You are a trading analyst.

Determine the SHORT-TERM market bias for the instrument.

Respond in EXACTLY this format (no extra text):

Bias: <Bullish | Bearish | Neutral | Unclear>
Reason: <one concise sentence>

TITLE:
{title}

SUMMARY:
{joined_summary}
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
