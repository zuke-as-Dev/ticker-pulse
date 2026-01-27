MARKET_FEEDS = {
    "crypto": ["crypto"],
    "forex": ["forex", "macro"],
    "commodity": ["commodities", "macro"],
    "stock": ["global_equities", "india_equities", "macro"]
}

def get_allowed_feed_categories(instruments: dict) -> set[str]:
    categories = set()
    for data in instruments.values():
        market = data.get("type") or data.get("market")
        categories.update(MARKET_FEEDS.get(market, []))
    return categories
