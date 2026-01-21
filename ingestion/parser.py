def normalize_articles(raw_articles: list) -> list:
    normalized = []

    for article in raw_articles:
        normalized.append({
            "title": article["title"].strip(),
            "summary": article["summary"].strip(),
            "link": article["link"],
            "source": article["source"],
            "category": article["category"],
        })

    return normalized
