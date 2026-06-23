"""
Web search module.

Supports:
- mock search
- Serper API search
- cache-ready JSON source facts
"""

import json
import re
from datetime import datetime

from app.config import USE_WEB_SEARCH, SEARCH_PROVIDER
from app.search_cache import load_from_cache, save_to_cache
from app.serper_client import search_google
from app.facts_extractor import extract_facts_from_search_results
from app.facts_filter import filter_search_results

def clean_model(raw_model: str, brand: str) -> str:
    model = raw_model.strip()

    words_to_remove = [
        "Ноутбук",
        "ноутбук",
        "Мышка",
        "мышка",
        "Миша",
        "миша",
        "Lenovo",
        "lenovo",
        "Logitech",
        "logitech",
        brand,
    ]

    for word in words_to_remove:
        model = model.replace(word, "")

    return " ".join(model.split())


def detect_basic_metadata(name: str, description: str = "") -> dict:
    full_text = f"{name} {description}"

    brand = ""
    model = ""
    category = ""
    characteristics = {}

    if "lenovo" in full_text.lower():
        brand = "Lenovo"
        category = "Ноутбуки"

        match = re.search(r"lenovo\s+(.+)", full_text, re.IGNORECASE)
        if match:
            model = clean_model(match.group(1), brand)

        characteristics = {
            "brand": brand,
            "model": model,
            "category": category,
            "product_type": "Ноутбук",
        }

    elif "logitech" in full_text.lower():
        brand = "Logitech"
        category = "Компьютерные аксессуары"

        match = re.search(r"logitech\s+(.+)", full_text, re.IGNORECASE)
        if match:
            model = clean_model(match.group(1), brand)

        characteristics = {
            "brand": brand,
            "model": model,
            "category": category,
            "product_type": "Мышь",
            "connection_type": "Беспроводная",
        }

    return {
        "brand": brand,
        "model": model,
        "category": category,
        "characteristics": characteristics,
    }


def search_with_mock(name: str, sku: str = "", description: str = "") -> dict:
    metadata = detect_basic_metadata(name, description)

    return {
        "name": name,
        "sku": sku,
        "description": description,
        "brand": metadata["brand"],
        "model": metadata["model"],
        "category": metadata["category"],
        "characteristics": metadata["characteristics"],
        "source": "input_excel",
        "source_url": "",
        "search_results": [],
        "facts_found": bool(name or sku or description),
        "provider": "mock",
        "searched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def search_with_serper(name: str, sku: str = "", description: str = "") -> dict:
    metadata = detect_basic_metadata(name, description)

    query = f"{name} {sku} {description}".strip()
    results = search_google(query=query, num_results=5)

    results = filter_search_results(results)

    extracted_facts = extract_facts_from_search_results(results)

    source_url = results[0]["url"] if results else ""

    return {
        "name": name,
        "sku": sku,
        "description": description,
        "brand": metadata["brand"],
        "model": metadata["model"],
        "category": metadata["category"],
        "characteristics": metadata["characteristics"],
        "source": "serper_google_search",
        "source_url": source_url,
        "search_results": results,
        "extracted_facts": extracted_facts,
        "facts_found": bool(results),
        "provider": "serper",
        "searched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def find_product_facts(name: str, sku: str = "", description: str = "") -> str:
    cached_facts = load_from_cache(sku, name)

    if cached_facts:
        cached_facts["from_cache"] = True
        return json.dumps(cached_facts, ensure_ascii=False)

    if USE_WEB_SEARCH and SEARCH_PROVIDER == "serper":
        facts = search_with_serper(name, sku, description)
    else:
        facts = search_with_mock(name, sku, description)

    facts["from_cache"] = False

    save_to_cache(sku, name, facts)

    return json.dumps(facts, ensure_ascii=False)