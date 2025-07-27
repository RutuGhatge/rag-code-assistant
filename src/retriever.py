import requests

def scrape_stackoverflow(query, limit=10):
    url = f"https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q={query}&site=stackoverflow"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        questions = []
        for item in data.get("items", [])[:limit]:
            questions.append({
                "title": item["title"],
                "link": item["link"]
            })
        return questions
    return []
