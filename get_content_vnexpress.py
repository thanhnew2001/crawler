import requests
import json
from bs4 import BeautifulSoup
import re

def crawl_and_extract(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            title_elem = soup.find(attrs={"class": "title-detail"})
            title = title_elem.text.strip() if title_elem else ""

            sub_header_elem = soup.find(attrs={"class": "description"})
            sub_header = sub_header_elem.text.strip() if sub_header_elem else ""

            # content_elem = soup.find(attrs={"class": "fck_detail "})
            # content = content_elem.text.strip() if content_elem else ""

            article_elem = soup.find("article", class_="fck_detail")
            if article_elem:
                paragraphs = article_elem.find_all("p", class_="Normal")
                content = " ".join([p.get_text(strip=True) for p in paragraphs])
            else:
                content = ""

            tags_elem = soup.find("p", class_="tags")
            if tags_elem:
                tags = [tag.a.get_text(strip=True) for tag in tags_elem.find_all(class_="item-tag")]
            else:
                a_tag = soup.find('a', class_='link-topic-detail')
                if a_tag:          
                    tags = [a_tag.get_text(strip=True)]
                else:
                    tags = []

            return {
                "title": title,
                "sub_header": sub_header,
                "content": content,
                "tags": tags
            }
        else:
            print(f"Failed to fetch {url}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")
        return None

def check_url_patterns(url):
    pattern = r"https://vnexpress.net/([^/\d]+)-\d+\.html"
    if re.match(pattern, url):
        return True
    return False

def main():
    input_file = "links_vnexpress_m.jsonl"
    output_file = "output_vnexpress_m.jsonl"

    with open(input_file, 'r') as f_input, open(output_file, 'a', encoding='utf-8') as f_output:
        for line in f_input:
            data = json.loads(line.strip())
            url = data.get("url")

            if url and check_url_patterns(url):
                print(url)
                result = crawl_and_extract(url)
                if result:
                    json.dump(result, f_output, ensure_ascii=False)
                    f_output.write("\n")

if __name__ == "__main__":
    main()
