import re

def escape_md(text: str) -> str:
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text)

def bias_emoji(bias: str) -> str:
    bias = bias.lower()

    if bias == "bullish":
        return "🟢📈"
    if bias == "bearish":
        return "🔴📉"
    if bias == "neutral":
        return "⚪️➖"

    return "🟡❓"

from alerts.formatter import escape_md

def format_alert(
    symbol: str,
    title: str,
    summary: str,
    bias: str,
    reason: str,
    source: str,
    link: str,
) -> str:
    summary_lines = [
        f"• {escape_md(line.strip('- ').strip())}"
        for line in summary.splitlines()
        if line.strip()
    ]

    summary_block = "\n".join(summary_lines)

    return (
        "📢 *Ticker Pulse Alert*\n\n"
        f"*Instrument:* {escape_md(symbol)}\n"
        f"*Source:* {escape_md(source)}\n\n"
        f"*Headline:*\n*{escape_md(title)}*\n\n"
        f"*Summary:*\n{summary_block}\n\n"
        f"*Bias:* {bias_emoji(bias)} {escape_md(bias)}\n"        
        f"*Reason:* {escape_md(reason)}\n\n"
        f"🔗 [Read more]({escape_md(link)})"
    )