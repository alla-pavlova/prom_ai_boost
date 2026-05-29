"""
Duplicate checker by SKU.
"""


def is_duplicate_sku(sku: str, processed_skus: set) -> bool:
    return bool(sku and sku in processed_skus)


def add_sku(sku: str, processed_skus: set) -> None:
    if sku:
        processed_skus.add(sku)