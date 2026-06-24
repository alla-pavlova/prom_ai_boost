"""
Prompt builder.

Prepares compact product facts for OpenAI.
The full source_facts JSON is saved to Excel,
but only compact_facts are sent to the model to reduce token usage.
"""

import json

from app.facts_validator import validate_facts


def build_compact_facts(source_facts: str) -> tuple[str, list[str]]:
    try:
        facts_data = json.loads(source_facts)
    except json.JSONDecodeError:
        return source_facts, []

    model = facts_data.get("model", "")

    validated_facts = validate_facts(
        facts_data.get("extracted_facts", []),
        model=model,
    )

    compact_data = {
        "name": facts_data.get("name", ""),
        "sku": facts_data.get("sku", ""),
        "brand": facts_data.get("brand", ""),
        "model": facts_data.get("model", ""),
        "category": facts_data.get("category", ""),
        "characteristics": facts_data.get("characteristics", {}),
        "facts": validated_facts,
    }

    return json.dumps(
        compact_data,
        ensure_ascii=False,
        indent=2,
    ), validated_facts