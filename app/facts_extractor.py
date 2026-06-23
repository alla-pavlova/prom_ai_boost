"""
Facts extractor.

Extracts short product facts from search results.
"""


def extract_facts_from_search_results(search_results: list[dict]) -> list[str]:
    facts = []

    for item in search_results:
        title = item.get("title", "").strip()
        snippet = item.get("snippet", "").strip()
        url = item.get("url", "").strip()

        if snippet:
            facts.append(snippet)

        elif title:
            facts.append(title)

        if len(facts) >= 5:
            break

    return facts