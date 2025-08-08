from bs4 import BeautifulSoup
import requests
import json

url = 'https://www.womansday.com/relationships/dating-marriage/a41055149/best-pickup-lines/'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

all_pickup_line_dicts_list = []
pickup_line_dict = {}

titles = soup.find_all('h2', attrs={'title': True})

pickup_line_groups = [ul for ul in soup.find_all('ul', class_='css-1wk73g0') if ul.find('li')]
pickup_line_group = []

for i in range(len(titles)):
    pickup_line_group = []
    for li in pickup_line_groups[i].find_all('li'):
        text_parts = []
        for part in li.contents:
            if part.get_text(strip=True).startswith("RELATED"):
                break
            text_parts.append(part.get_text(strip=True))

        if text_parts:
            pickup_line_group.append(" ".join(text_parts))

    all_pickup_line_dicts_list.append({titles[i].text: pickup_line_group})

with open('pickup_line.json', 'w', encoding='utf-8') as f:
    json.dump(all_pickup_line_dicts_list, f, ensure_ascii=False, indent=4)
