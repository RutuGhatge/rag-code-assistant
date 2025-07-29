import requests
import os
from bs4 import BeautifulSoup

def get_short_content(post_body_div):
    if not post_body_div:
        return "Content not found."
    first_paragraph = post_body_div.find('p')
    summary = first_paragraph.get_text(strip=True) if first_paragraph else ""
    code_blocks = post_body_div.find_all('pre')
    code = "\n\n".join([block.get_text(strip=True) for block in code_blocks])
    if code:
        return f"{summary}\n\n--- Code Snippet(s) ---\n{code}"
    return summary

def scrape_stackoverflow(query, max_results, save_dir):
    print(f"🔍 Scraping Stack Overflow for topic: '{query}'...")
    os.makedirs(save_dir, exist_ok=True)
    api_url = "https://api.stackexchange.com/2.3/search/advanced"
    params = {
        "order": "desc",
        "sort": "relevance",
        "q": query,
        "site": "stackoverflow",
        "pagesize": max_results,
        "filter": "withbody"
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json().get("items", [])
        print(f"✅ Fetched {len(data)} questions via API.")
    except requests.exceptions.RequestException as e:
        print(f"  > API request failed: {e}")
        return []

    scraped_results = []
    for item in data:
        link, title = item.get("link"), item.get("title")
        print(f"  > Processing and summarizing: {title}")
        try:
            page_response = requests.get(link)
            page_response.raise_for_status()
            soup = BeautifulSoup(page_response.text, 'html.parser')

            question_html = item.get("body", "")
            question_post_div = BeautifulSoup(question_html, 'html.parser')
            question_summary = get_short_content(question_post_div)

            accepted_answer_div = soup.find('div', class_='accepted-answer')
            answer_summary = "No accepted answer found."
            if accepted_answer_div:
                answer_body_div = accepted_answer_div.find('div', class_='s-prose js-post-body')
                answer_summary = get_short_content(answer_body_div)

            scraped_results.append({
                "title": title,
                "content": f"Question Summary:\n{question_summary}\n\nAnswer Summary:\n{answer_summary}"
            })

        except requests.exceptions.RequestException as e:
            print(f"  > Could not fetch page {link}: {e}")
            continue

    return scraped_results
