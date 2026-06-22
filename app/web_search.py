"""
Web search module.

Currently supports:
- mock search
- cache-ready JSON source facts

Later:
- Serper API
- Tavily API
- Google Search API
"""

import json
from datetime import datetime

from app.config import USE_WEB_SEARCH, SEARCH_PROVIDER
from app.search_cache import load_from_cache, save_to_cache


def search_with_mock(name: str, sku: str = "", description: str = "") -> dict:
    return {
        "name": name,
        "sku": sku,
        "description": description,
        "source": "input_excel",
        "source_url": "",
        "facts_found": bool(name or sku or description),
        "provider": "mock",
        "searched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def find_product_facts(name: str, sku: str = "", description: str = "") -> str:
    cached_facts = load_from_cache(sku, name)

    if cached_facts:
        cached_facts["from_cache"] = True
        return json.dumps(cached_facts, ensure_ascii=False)

    if not USE_WEB_SEARCH or SEARCH_PROVIDER == "mock":
        facts = search_with_mock(name, sku, description)
    else:
        facts = search_with_mock(name, sku, description)

    facts["from_cache"] = False

    save_to_cache(sku, name, facts)

    return json.dumps(facts, ensure_ascii=False)