"""
Facts extractor.

Extracts short product facts from search results.
"""


def extract_facts_from_search_results(search_results: list[dict]) -> list[dict]:
    facts = []

    for item in search_results:
        title = item.get("title", "").strip()
        snippet = item.get("snippet", "").strip()
        url = item.get("url", "").strip()
        source_score = item.get("source_score", 1)

        fact_text = snippet or title

        if fact_text:
            facts.append(
                {
                    "text": fact_text,
                    "url": url,
                    "source_score": source_score,
                }
            )

        if len(facts) >= 5:
            break

    return facts