"""
Facts validator.

Filters unsafe, too generic or conflicting facts before they are sent to OpenAI.
This helps reduce hallucinations and prevents mixing characteristics
from different product modifications.
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
    "доступный в",
    "доступний у",
    "широкого спектра",
    "разных задач",
    "різних завдань",
    "различных задач",
    "різних задач",
    "різних завдань",
    "автоматическое увеличение",
    "автоматичне збільшення",
    "тактовой частоты",
    "тактової частоти",
    "потоков данных",
    "потоків даних",
    ]

CONFLICT_PATTERNS = [
    " или ",
    " або ",
    " / ",
    "core i3",
    "core i5",
    "core i7",
    "ryzen 3",
    "ryzen 5",
    "ryzen 7",
]
def contains_cpu_details(text: str) -> bool:
    cpu_patterns = [
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
        "core",
    ]

    return any(pattern in text for pattern in cpu_patterns)

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

def is_valid_fact(fact: str) -> bool:
    text = fact.lower().strip()

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

    # Блокируем CPU-детали из поисковой выдачи,
    # если они относятся к серии, а не к конкретной модели
    if contains_cpu_details(text):
        return False

    return True

def validate_facts(facts: list[str]) -> list[str]:
    return [
        fact for fact in facts
        if is_valid_fact(fact)
    ]