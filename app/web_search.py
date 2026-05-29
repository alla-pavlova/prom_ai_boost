"""
Mock web search module.

Later this file can be connected to Google Search API,
Serper API, Tavily API or real web scraping.
"""


def find_product_facts(name: str, sku: str = "", description: str = "") -> str:
    facts = []

    if name:
        facts.append(f"Product name: {name}")

    if sku:
        facts.append(f"SKU: {sku}")

    if description:
        facts.append(f"Original description: {description}")

    return " | ".join(facts)