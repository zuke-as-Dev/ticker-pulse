def score_relevance(article: dict, instrument: dict) -> float:
    """
    Simple keyword-based relevance scoring.
    Returns score between 0 and 1.
    """
    text = f"{article['title']} {article['summary']}".lower()
    keywords = [k.lower() for k in instrument["keywords"]]

    matches = sum(1 for k in keywords if k in text)

    if not keywords:
        return 0.0

    return matches / len(keywords)


def filter_relevant_articles(articles: list, instruments: dict, threshold: float = 0.2):
    relevant = []

    for symbol, instrument in instruments.items():
        for article in articles:
            score = score_relevance(article, instrument)

            if score >= threshold:
                relevant.append({
                    "symbol": symbol,
                    "score": round(score, 2),
                    "article": article,
                })

    return relevant
