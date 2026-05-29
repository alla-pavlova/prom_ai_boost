"""
Prom AI Boost — CLI entry point.

This file:
- reads products from Excel
- generates product content
- checks duplicate SKU
- writes processing status
- saves versioned output file
- prints processing statistics
- writes logs to logs/app.log
"""

import logging
from datetime import datetime

from app.config import INPUT_FILE, OUTPUT_FILE
from app.excel_service import read_excel_file, save_excel_file
from app.generator import generate_product_content


logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)


def main():
    print("Старт обработки файла...")
    logging.info("Старт обработки файла")

    df = read_excel_file(INPUT_FILE)

    if "name" not in df.columns:
        raise ValueError("В Excel нет обязательной колонки: name")

    description_ua = []
    description_ru = []
    html_description = []
    seo_tags = []
    statuses = []
    error_messages = []
    processed_at = []

    processed_skus = set()

    for index, row in df.iterrows():
        name = str(row.get("name", "")).strip()
        sku = str(row.get("sku", "")).strip()
        description = str(row.get("description", "")).strip()

        if not name:
            print(f"Строка {index + 2}: пропущена, нет названия")
            logging.warning(f"Row {index + 2}: no product name")

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
            logging.warning(f"Duplicate SKU: {sku}")

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
            processed_at.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            logging.info(f"Processed product: {name}, SKU: {sku}")

        except Exception as e:
            error_text = str(e)
            print(f"Ошибка в строке {index + 2}: {error_text}")
            logging.error(f"Error in row {index + 2}: {error_text}")

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

    total_count = len(df)
    processed_count = statuses.count("mock_processed") + statuses.count("processed")
    duplicate_count = statuses.count("duplicate")
    error_count = statuses.count("error")
    skipped_count = statuses.count("skipped")

    print("\n===== Статистика обработки =====")
    print(f"Всего строк: {total_count}")
    print(f"Обработано: {processed_count}")
    print(f"Дубликатов: {duplicate_count}")
    print(f"Ошибок: {error_count}")
    print(f"Пропущено: {skipped_count}")
    print("================================\n")

    logging.info(
        f"Statistics: total={total_count}, "
        f"processed={processed_count}, "
        f"duplicates={duplicate_count}, "
        f"errors={error_count}, "
        f"skipped={skipped_count}"
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    versioned_output_file = OUTPUT_FILE.replace(".xlsx", f"_{timestamp}.xlsx")

    save_excel_file(df, versioned_output_file)

    print(f"Готово. Файл сохранён: {versioned_output_file}")
    logging.info(f"Файл сохранён: {versioned_output_file}")


if __name__ == "__main__":
    main()