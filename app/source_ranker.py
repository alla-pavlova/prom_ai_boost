from urllib.parse import urlparse


TRUSTED_SOURCE_SCORES = {
    "lenovo.ua": 5,
    "shop.lenovo.ua": 5,
    "logitech.com": 5,
    "rozetka.com.ua": 4,
    "hard.rozetka.com.ua": 4,
    "comfy.ua": 4,
    "citrus.ua": 4,
    "foxtrot.com.ua": 4,
    "moyo.ua": 3,
    "hotline.ua": 3,
}


BLOCKED_DOMAINS = [
    "olx.ua",
    "youtube.com",
    "youtu.be",
]


def get_domain(url: str) -> str:
    return urlparse(url).netloc.lower().replace("www.", "")


def get_source_score(url: str) -> int:
    domain = get_domain(url)

    for blocked_domain in BLOCKED_DOMAINS:
        if blocked_domain in domain:
            return 0

    for trusted_domain, score in TRUSTED_SOURCE_SCORES.items():
        if trusted_domain in domain:
            return score

    return 1


def rank_search_results(results: list[dict]) -> list[dict]:
    ranked = []

    for item in results:
        score = get_source_score(item.get("url", ""))
        if score <= 0:
            continue

        item["source_score"] = score
        ranked.append(item)

    return sorted(
        ranked,
        key=lambda item: item.get("source_score", 0),
        reverse=True,
    )