import json


def find_product_facts(name: str, sku: str = "", description: str = "") -> str:
    facts = {
        "name": name,
        "sku": sku,
        "description": description,
        "source": "input_excel",
    }

    return json.dumps(facts, ensure_ascii=False)