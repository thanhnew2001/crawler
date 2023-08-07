import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

def get_links_from_url(url):
    try:
        if "https" in url and "vnexpress.net" in url:
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful
            soup = BeautifulSoup(response.content, 'html.parser')
            links = []
            for link in soup.find_all('a', href=True):
                absolute_url = urljoin(url, link['href'])  # Convert relative URL to absolute URL
                links.append(absolute_url)
            return links
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return []

def follow_links(url, depth=1, visited_urls=set(), output_file=None):
    if depth <= 0 or url in visited_urls:
        return

    print("Visiting:", url)
    visited_urls.add(url)

    if output_file and "vnexpress.net" in url:  # Only write the link to the file if it contains "thanhnien.vn"
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"url": url}) + '\n')

    links = get_links_from_url(url)

    for link in links:
        if "https" in link and "vnexpress.net" in link:
            follow_links(link, depth - 1, visited_urls, output_file)

if __name__ == "__main__":
    starting_url = "https://vnexpress.net"
    max_depth = 5  # Increase the max_depth to 3
    output_file = "links_vnexpress2.jsonl"

    follow_links(starting_url, max_depth, output_file=output_file)
