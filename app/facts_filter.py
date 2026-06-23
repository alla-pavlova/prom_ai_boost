from urllib.parse import urlparse


TRUSTED_DOMAINS = [
    "lenovo.ua",
    "logitech.com",
    "rozetka.com.ua",
    "comfy.ua",
    "citrus.ua",
]

BAD_WORDS = [
    "olx",
    "youtube",
    "б/у",
    "бу",
    "грн",
    "купити",
    "купить",
]

def is_trusted_url(url: str) -> bool:
    domain = urlparse(url).netloc.lower()

    return any(
        trusted_domain in domain
        for trusted_domain in TRUSTED_DOMAINS
    )


def filter_search_results(results: list[dict]) -> list[dict]:
    filtered = []

    for item in results:
        url = item.get("url", "")
        snippet = item.get("snippet", "").lower()

        if not is_trusted_url(url):
            continue

        if any(word in snippet for word in BAD_WORDS):
            continue

        filtered.append(item)

    return filtered