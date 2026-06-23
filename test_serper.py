from app.serper_client import search_google

results = search_google("Lenovo IdeaPad 3")

print(f"Найдено: {len(results)}")

for item in results[:3]:
    print("-" * 50)
    print(item["title"])
    print(item["url"])
    print(item["snippet"])