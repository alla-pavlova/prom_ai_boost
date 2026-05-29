import json
from openai import OpenAI

from app.config import OPENAI_API_KEY, MODEL, USE_OPENAI
from app.prom_formatter import build_html_description


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
        }

    return {
        "description_ua": f"{name} — товар для щоденного використання. Дані взято з вхідного опису: {description}",
        "description_ru": f"{name} — товар для ежедневного использования. Данные взяты из исходного описания: {description}",
        "html_description": build_html_description(name, description, sku),
        "seo_tags": f"{name}, {sku}, купити, Prom.ua",
        "status": "mock_processed",
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

SOURCE_FACTS:
{source_facts}

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

        return result

    except Exception as e:
        return {
            "description_ua": "",
            "description_ru": "",
            "html_description": "",
            "seo_tags": "",
            "status": "error",
            "error_message": f"Invalid JSON response: {str(e)}",
        }