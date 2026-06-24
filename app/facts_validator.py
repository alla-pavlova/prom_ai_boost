"""
Facts validator.

Filters unsafe or too generic facts before they are sent to OpenAI.
This helps reduce hallucinations and prevents mixing characteristics
from different product modifications.
"""

BAD_FACT_PATTERNS = [
    "или",
    "або",
    "серия",
    "серія",
    "линейка",
    "лінійка",
    "купить",
    "купити",
    "цена",
    "ціна",
    "грн",
    "б/у",
    "бу",
]


def is_valid_fact(fact: str) -> bool:
    text = fact.lower()

    if not text.strip():
        return False

    for pattern in BAD_FACT_PATTERNS:
        if pattern in text:
            return False

    return True


def validate_facts(facts: list[str]) -> list[str]:
    return [
        fact for fact in facts
        if is_valid_fact(fact)
    ]