"""
Facts validator.

Filters unsafe, too generic or conflicting facts before they are sent to OpenAI.
Supports source_score from trusted source ranking.
"""

BAD_FACT_PATTERNS = [
    "купить",
    "купити",
    "цена",
    "ціна",
    "грн",
    "б/у",
    "бу",
    "olx",
    "youtube",
]

GENERIC_SERIES_PATTERNS = [
    "серия",
    "серія",
    "линейка",
    "лінійка",
    "каталоге серии",
    "каталозі серії",
    "несколько вариантов",
    "декілька варіантів",
    "широкого спектра",
]

CPU_PATTERNS = [
    "core i3",
    "core i5",
    "core i7",
    "ryzen 3",
    "ryzen 5",
    "ryzen 7",
    "ghz",
    "ггц",
    "частота",
    "frequency",
    "поток",
    "thread",
    "ядр",
]


def contains_any(text: str, patterns: list[str]) -> bool:
    return any(pattern in text for pattern in patterns)


def has_conflicting_cpu_variants(text: str) -> bool:
    cpu_markers = [
        "core i3",
        "core i5",
        "core i7",
        "ryzen 3",
        "ryzen 5",
        "ryzen 7",
    ]

    found = [
        marker for marker in cpu_markers
        if marker in text
    ]

    return len(found) > 1


def is_valid_fact_item(fact_item: dict, model: str = "") -> bool:
    text = fact_item.get("text", "").lower().strip()
    source_score = fact_item.get("source_score", 1)

    if not text:
        return False

    if contains_any(text, BAD_FACT_PATTERNS):
        return False

    if contains_any(text, GENERIC_SERIES_PATTERNS):
        return False

    if " или " in text or " або " in text:
        return False

    if has_conflicting_cpu_variants(text):
        return False

    if contains_any(text, CPU_PATTERNS):
        if source_score < 5:
            return False

        if not has_exact_model_match(text, model):
            return False

    return True

def validate_facts(facts: list, model: str = "") -> list[str]:
    validated = []

    for fact in facts:
        if isinstance(fact, str):
            fact_item = {
                "text": fact,
                "source_score": 1,
            }
        else:
            fact_item = fact

        if is_valid_fact_item(fact_item, model=model):
            validated.append(fact_item.get("text", ""))

    return validated

def has_exact_model_match(fact_text: str, model: str) -> bool:
    if not model:
        return False

    text = fact_text.lower()
    model_text = model.lower()

    return model_text in text