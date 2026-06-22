"""
Search cache module.

Stores product facts in local JSON files to avoid repeated web/API requests.
"""

import json
import os
from pathlib import Path

from app.config import CACHE_DIR


def _safe_filename(value: str) -> str:
    value = value.strip().replace("/", "_").replace("\\", "_")
    value = value.replace(" ", "_")
    return value or "unknown_product"


def get_cache_path(sku: str, name: str) -> Path:
    cache_key = sku if sku else name
    filename = f"{_safe_filename(cache_key)}.json"

    return Path(CACHE_DIR) / filename


def load_from_cache(sku: str, name: str) -> dict | None:
    cache_path = get_cache_path(sku, name)

    if not cache_path.exists():
        return None

    with open(cache_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_to_cache(sku: str, name: str, facts: dict) -> None:
    os.makedirs(CACHE_DIR, exist_ok=True)

    cache_path = get_cache_path(sku, name)

    with open(cache_path, "w", encoding="utf-8") as file:
        json.dump(facts, file, ensure_ascii=False, indent=2)