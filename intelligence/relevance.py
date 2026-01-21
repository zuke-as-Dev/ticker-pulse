import re


def _contains_primary_keyword(title: str, primary_keywords: list) -> bool:
    title_lower = title.lower()

    for pk in primary_keywords:
        pk_lower = pk.lower()

        # match whole word / phrase using word boundaries
        pattern = r"\b" + re.escape(pk_lower) + r"\b"

        if re.search(pattern, title_lower):
            # Debug:print primary match
            # print(f"[PRIMARY MATCH] '{pk}' matched in title: {title}")
            return True

    return False


def score_relevance(article: dict, secondary_keywords: list) -> float:
    text = f"{article['title']} {article['summary']}".lower()
    matches = sum(1 for k in secondary_keywords if k.lower() in text)

    if not secondary_keywords:
        return 0.0

    return matches / len(secondary_keywords)


def filter_relevant_articles(articles: list, instruments: dict, threshold: float = 0.2):
    relevant = []

    for symbol, instrument in instruments.items():
        primary = instrument.get("primary_keywords")
        secondary = instrument.get("secondary_keywords", [])

        # 🚨 HARD ASSERT — THIS SHOULD NEVER BE NONE
        if not primary:
            raise RuntimeError(
                f"[CONFIG ERROR] Instrument {symbol} has no primary_keywords"
            )

        for article in articles:
            title = article["title"]

            # 🚫 HARD GATE
            if not _contains_primary_keyword(title, primary):
                continue

            score = score_relevance(article, secondary)

            if score >= threshold:
                relevant.append({
                    "symbol": symbol,
                    "score": round(score, 2),
                    "article": article,
                })

    return relevant
