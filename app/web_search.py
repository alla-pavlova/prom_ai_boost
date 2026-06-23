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
import re

from app.config import USE_WEB_SEARCH, SEARCH_PROVIDER
from app.search_cache import load_from_cache, save_to_cache


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