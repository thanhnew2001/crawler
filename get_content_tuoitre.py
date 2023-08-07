import requests
import json
from bs4 import BeautifulSoup
import re

def crawl_and_extract(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            title_elem = soup.find(attrs={"data-role": "title"})
            title = title_elem.text.strip() if title_elem else ""

            sub_header_elem = soup.find(attrs={"data-role": "sapo"})
            sub_header = sub_header_elem.text.strip() if sub_header_elem else ""

            content_elem = soup.find(attrs={"data-role": "content"})
            content = content_elem.text.strip() if content_elem else ""

            tags_elem =  soup.find(attrs={"class": "detail-tab"})
            if tags_elem:
                tags = [tag.text.strip() for tag in tags_elem.find_all(class_="item")]
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
    pattern = r"https://tuoitre.vn/([^/\d]+)-\d+\.htm"
    if re.match(pattern, url):
        return True
    return False

def main():
    input_file = "links_tuoitre.jsonl"
    output_file = "output_tuoitre.jsonl"

    with open(input_file, 'r') as f_input, open(output_file, 'w', encoding='utf-8') as f_output:
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
