def safe_text(value):
    if value is None:
        return ""
    return str(value).strip()


def normalize_articles(raw_articles: list) -> list:
    normalized = []

    for article in raw_articles:
        normalized.append({
            "title": safe_text(article.get("title")),
            "summary": safe_text(article.get("summary")),
            "link": article.get("link", ""),
            "source": article.get("source", ""),
            "category": article.get("category", ""),
        })

    return normalized
