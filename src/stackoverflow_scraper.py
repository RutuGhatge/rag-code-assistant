import requests
import os
import json

def scrape_stackoverflow(query, max_results, save_dir):
    print(f"🔍 Scraping Stack Overflow for topic: '{query}'...")
    os.makedirs(save_dir, exist_ok=True)

    url = f"https://api.stackexchange.com/2.3/search/advanced"
    params = {
        "order": "desc",
        "sort": "relevance",
        "q": query,
        "site": "stackoverflow",
        "pagesize": max_results
    }

    response = requests.get(url, params=params)
    data = response.json().get("items", [])

    # Save cache
    file_path = os.path.join(save_dir, f"{query.replace(' ', '_')}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"✅ Fetched {len(data)} questions via API.")
    return [{"title": item["title"], "link": item["link"]} for item in data]
