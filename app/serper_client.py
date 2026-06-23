"""
Serper API client.

Used for real Google Search results.
"""

import requests

from app.config import SERPER_API_KEY


SERPER_SEARCH_URL = "https://google.serper.dev/search"


def search_google(query: str, num_results: int = 5) -> list[dict]:
    if not SERPER_API_KEY:
        raise ValueError("SERPER_API_KEY is missing")

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json",
    }

    payload = {
        "q": query,
        "num": num_results,
        "gl": "ua",
        "hl": "uk",
    }

    response = requests.post(
        SERPER_SEARCH_URL,
        headers=headers,
        json=payload,
        timeout=15,
    )

    response.raise_for_status()

    data = response.json()
    organic_results = data.get("organic", [])

    results = []

    for item in organic_results:
        results.append(
            {
                "title": item.get("title", ""),
                "url": item.get("link", ""),
                "snippet": item.get("snippet", ""),
            }
        )

    return results