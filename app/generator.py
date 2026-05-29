import json
from openai import OpenAI

from app.config import OPENAI_API_KEY, MODEL, USE_OPENAI


def generate_mock_content(name: str, sku: str = "", description: str = "") -> dict:
    return {
        "description_ua": f"{name} — якісний товар для щоденного використання. {description}",
        "description_ru": f"{name} — качественный товар для ежедневного использования. {description}",
        "html_description": f"""
<h2>{name}</h2>
<p><strong>{description}</strong></p>
<ul>
  <li>Артикул: {sku}</li>
</ul>
""",
        "seo_tags": f"{name}, {sku}, купити, Prom.ua",
        "status": "mock_processed",
    }


def generate_product_content(name: str, sku: str = "", description: str = "") -> dict:
    if not USE_OPENAI:
        return generate_mock_content(name, sku, description)

    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt = f"""
Ты создаешь контент для карточки товара Prom.ua.

ВАЖНО:
- Не выдумывай технические характеристики.
- Используй только данные из названия, артикула и описания.
- Если данных мало, не добавляй конкретные характеристики.
- Верни только JSON без markdown.

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
        messages=[
            {"role": "system", "content": "Ты помощник для e-commerce и Prom.ua."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    content = response.choices[0].message.content
    return json.loads(content)