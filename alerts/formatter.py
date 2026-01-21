def format_alert(symbol: str, title: str, summary: str, bias: str, source: str, link: str) -> str:
    return (
        f"📢 *Ticker Pulse Alert*\n\n"
        f"*Instrument:* {symbol}\n"
        f"*Source:* {source}\n\n"
        f"*Headline:*\n{title}\n\n"
        f"*Summary:*\n{summary}\n\n"
        f"*Bias:*\n{bias}\n\n"
        f"🔗 [Read more]({link})"
    )
