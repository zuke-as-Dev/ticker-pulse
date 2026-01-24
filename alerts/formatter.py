def bias_emoji(bias: str) -> str:
    bias = bias.lower()

    if bias == "bullish":
        return "🟢📈 Bullish"
    if bias == "bearish":
        return "🔴📉 Bearish"
    if bias == "neutral":
        return "⚪️➖ Neutral"

    return "🟡❓ Unclear"


def format_alert(symbol, title, summary, bias, reason, source, link):
    summary_block = "\n".join(f"• {line}" for line in summary)

    return (
        "📢 <b>Ticker Pulse Alert</b>\n\n"
        f"<b>Instrument:</b> {symbol}\n"
        f"<b>Source:</b> {source}\n\n"
        "<b>Headline:</b>\n"
        f"<b>{title}</b>\n\n"
        "<b>Summary:</b>\n"
        f"{summary_block}\n\n"
        f"<b>Bias:</b> {bias_emoji(bias)}\n"
        f"<b>Reason:</b> {reason}\n\n"
        f"🔗 <a href=\"{link}\">Read more</a>"
    )
