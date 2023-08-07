import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

def crawl_links(base_url, output_file):
    unique_links = set()
    for page_number in range(1, 21):
        url = f"{base_url}-p{page_number}"
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            for link in soup.find_all("a"):
                href = link.get("href")
                if href and href.startswith("https://vnexpress.net"):
                    unique_links.add(href)

    with open(output_file, 'a', encoding='utf-8') as f:
        for link in unique_links:
            f.write(json.dumps({"url": link}) + '\n')

if __name__ == "__main__":
    base_urls = [
        "https://vnexpress.net/thoi-su",
        "https://vnexpress.net/goc-nhin",
        "https://vnexpress.net/the-gioi",
        "https://vnexpress.net/kinh-doanh",
        "https://vnexpress.net/bat-dong-san",
        "https://vnexpress.net/khoa-hoc",
        "https://vnexpress.net/giai-tri",
        "https://vnexpress.net/the-thao",
        "https://vnexpress.net/phap-luat",
        "https://vnexpress.net/giao-duc",
        "https://vnexpress.net/suc-khoe",
        "https://vnexpress.net/doi-song",
        "https://vnexpress.net/du-lich",
        "https://vnexpress.net/so-hoa",
        "https://vnexpress.net/oto-xe-may",
        "https://vnexpress.net/y-kien",
        "https://vnexpress.net/tam-su",
        "https://vnexpress.net/thu-gian",
    ]

    output_file = "found_links_vnexpress.jsonl"
    for base_url in base_urls:
        crawl_links(base_url, output_file)
