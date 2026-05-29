from app.config import INPUT_FILE, OUTPUT_FILE
from app.excel_service import read_excel_file, save_excel_file
from app.generator import generate_product_content
from datetime import datetime

def main():
    print("Старт обработки файла...")

    df = read_excel_file(INPUT_FILE)

    if "name" not in df.columns:
        raise ValueError("В Excel нет обязательной колонки: name")

    description_ua = []
    description_ru = []
    html_description = []
    seo_tags = []
    statuses = []
    error_messages = []
    processed_skus = set()
    processed_at = []

    for index, row in df.iterrows():
        name = str(row.get("name", "")).strip()
        sku = str(row.get("sku", "")).strip()
        description = str(row.get("description", "")).strip()

        if not name:
            print(f"Строка {index + 2}: пропущена, нет названия")

            description_ua.append("")
            description_ru.append("")
            html_description.append("")
            seo_tags.append("")
            statuses.append("skipped")
            error_messages.append("No product name")
            processed_at.append("")
            continue

        if sku and sku in processed_skus:
            print(f"Строка {index + 2}: дубль по SKU {sku}")

            description_ua.append("")
            description_ru.append("")
            html_description.append("")
            seo_tags.append("")
            statuses.append("duplicate")
            error_messages.append(f"Duplicate SKU: {sku}")
            processed_at.append("")
            continue

        if sku:
            processed_skus.add(sku)

        print(f"Обработка: {name}")

        try:
            result = generate_product_content(
                name=name,
                sku=sku,
                description=description,
            )

            description_ua.append(result.get("description_ua", ""))
            description_ru.append(result.get("description_ru", ""))
            html_description.append(result.get("html_description", ""))
            seo_tags.append(result.get("seo_tags", ""))
            statuses.append(result.get("status", "processed"))
            error_messages.append("")
            processed_at.append(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

        except Exception as e:
            error_text = str(e)
            print(f"Ошибка в строке {index + 2}: {error_text}")

            description_ua.append("")
            description_ru.append("")
            html_description.append("")
            seo_tags.append("")
            statuses.append("error")
            error_messages.append(error_text)
            processed_at.append("")

    df["description_ua"] = description_ua
    df["description_ru"] = description_ru
    df["html_description"] = html_description
    df["seo_tags"] = seo_tags
    df["status"] = statuses
    df["error_message"] = error_messages
    df["processed_at"] = processed_at

    save_excel_file(df, OUTPUT_FILE)

    print(f"Готово. Файл сохранён: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()