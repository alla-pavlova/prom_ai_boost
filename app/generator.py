import json
from openai import OpenAI

from app.prom_formatter import build_html_description
from app.config import (
    OPENAI_API_KEY,
    MODEL,
    USE_OPENAI,
    OPENAI_INPUT_PRICE_PER_1M,
    OPENAI_OUTPUT_PRICE_PER_1M,
)
from app.prompt_builder import build_compact_facts

def generate_mock_content(
    name: str,
    sku: str = "",
    description: str = "",
    source_facts: str = "",
) -> dict:
    if not source_facts:
        return {
            "description_ua": "",
            "description_ru": "",
            "html_description": "",
            "seo_tags": "",
            "status": "no_data",
            "tokens_used": 0,
            "estimated_cost_usd": 0,
            "validated_facts": [],
        }

    return {
        "description_ua": f"{name} — товар для щоденного використання. Дані взято з вхідного опису: {description}",
        "description_ru": f"{name} — товар для ежедневного использования. Данные взяты из исходного описания: {description}",
        "html_description": build_html_description(name, description, sku),
        "seo_tags": f"{name}, {sku}, купити, Prom.ua",
        "status": "mock_processed",
        "tokens_used": 0,
        "estimated_cost_usd": 0,
    }


def generate_product_content(
    name: str,
    sku: str = "",
    description: str = "",
    source_facts: str = "",
) -> dict:
    if not USE_OPENAI:
        return generate_mock_content(name, sku, description, source_facts)

    client = OpenAI(api_key=OPENAI_API_KEY)

    compact_facts, validated_facts = build_compact_facts(source_facts)
    prompt = f"""
    
Ты создаешь контент для карточки товара Prom.ua.

ВАЖНО:
- Используй только факты из блока SOURCE_FACTS.
- Не выдумывай технические характеристики.
- Если фактов недостаточно, верни status = "no_data".
- Верни только JSON.
- Не используй markdown.
- Не используй ```json.
- Не добавляй пояснения.
- Не добавляй текст до JSON.
- Не добавляй текст после JSON.
- Не объединяй характеристики разных модификаций товара.
- Не указывай процессор, память, диагональ, разрешение или другие характеристики, если они не подтверждены однозначно.
- Если факт относится к серии товаров, а не к конкретной модели, не используй его как характеристику.

SOURCE_FACTS:
{compact_facts}

Товар:
Название: {name}
Артикул: {sku}
Описание: {description}

Формат ответа:
{{
  "description_ua": "...",
  "description_ru": "...",
  "html_description": "...",
  "seo_tags": "...",
  "status": "processed"
}}
"""

    response = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Ты помощник для e-commerce и Prom.ua."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content.strip()

    try:
        if content.startswith("```json"):
            content = content.replace("```json", "")
            content = content.replace("```", "")
            content = content.strip()

        result = json.loads(content)

        required_fields = [
            "description_ua",
            "description_ru",
            "html_description",
            "seo_tags",
            "status",
        ]

        for field in required_fields:
            if field not in result:
                raise ValueError(f"Missing field: {field}")

        usage = response.usage

        prompt_tokens = usage.prompt_tokens if usage else 0
        completion_tokens = usage.completion_tokens if usage else 0
        total_tokens = usage.total_tokens if usage else 0

        estimated_cost = (
                (prompt_tokens / 1_000_000) * OPENAI_INPUT_PRICE_PER_1M
                + (completion_tokens / 1_000_000) * OPENAI_OUTPUT_PRICE_PER_1M
        )

        result["tokens_used"] = total_tokens
        result["estimated_cost_usd"] = round(estimated_cost, 6)
        result["validated_facts"] = validated_facts

        return result

    except Exception as e:
        return {
            "description_ua": "",
            "description_ru": "",
            "html_description": "",
            "seo_tags": "",
            "status": "error",
            "error_message": f"Invalid JSON response: {str(e)}",
            "tokens_used": 0,
            "estimated_cost_usd": 0,
            "validated_facts": [],
        }
