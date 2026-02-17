"""
Docstring for bird-multilang-index.tools.export_birds_data

Load raw html in database, parse birds data, and export to json.

avibase source link:
https://avibase.bsc-eoc.org/checklist.jsp?lang=ZH&region=jp&list=avibase&format=1
"""

from bs4 import BeautifulSoup as BS
from bs4 import Tag
import json
import os
import get_image_url

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(SCRIPT_DIR, "..")
avibase_link = "https://avibase.bsc-eoc.org/"
json_path = os.path.join(ROOT_DIR, "data", "birds-data.json")
databse_dir = os.path.join(ROOT_DIR, "avibase")


def parse_html(html, lang):
    soup = BS(html, "html.parser")
    bird_data = BirdData()

    # find tabel first
    table = soup.find("table", class_="table")
    if isinstance(table, Tag):
        # find all table content
        data_tr = table.find_all("tr", class_="highlight1")
        for i in range(len(data_tr)):
            data_tr_row = data_tr[i]
            if isinstance(data_tr_row, Tag):
                data_td = data_tr_row.find_all("td")
                if lang == "zh":
                    # skip if no zh name or invalid entry
                    if data_td[2].text != "" and data_td[2].text.find("未识别") == -1:
                        data_href = data_td[1].find("a").get("href")
                        bird_data.en.append(data_td[0].text)
                        bird_data.aves.append(data_td[1].text)
                        bird_data.link.append(avibase_link + data_href)
                        bird_data.avibaseid.append(data_href.split("=")[-1])
                        bird_data.zh.append(data_td[2].text)
                        bird_data.rarity.append(data_td[3].text)
                elif lang == "jp":
                    bird_data.aves.append(data_td[1].text)
                    bird_data.jp.append(data_td[2].text)
                    bird_data.rarity.append(data_td[3].text)

    if bird_data.aves == []:
        print(f"🔴 Failed in parsing {lang} html!")

    return bird_data


class BirdData:
    def __init__(self):
        self.avibaseid = []
        self.aves = []
        self.en = []
        self.zh = []
        self.jp = []
        self.link = []
        self.rarity = []


zh_html = os.path.join(databse_dir, "zh.html")
jp_html = os.path.join(databse_dir, "jp.html")

bird_data = parse_html(open(zh_html, "r", encoding="utf-8"), "zh")
bird_data_jp = parse_html(open(jp_html, "r", encoding="utf-8"), "jp")

# merge list
for i in range(len(bird_data.aves)):
    for j in range(len(bird_data_jp.aves)):
        if bird_data.aves[i] == bird_data_jp.aves[j]:
            bird_data.jp.append(bird_data_jp.jp[j])

print("🟢Bird data merged!")

json_content = {}
json_content["species"] = {}
json_content["zh_index"] = {}
json_content["jp_index"] = {}

for i in range(len(bird_data.zh)):
    print(f"Processing: {i}/{len(bird_data.zh)}")
    avibase_id = bird_data.avibaseid[i]

    json_content["species"][avibase_id] = {
        "aves": f"{bird_data.aves[i]}",
        "en": f"{bird_data.en[i]}",
        "zh": f"{bird_data.zh[i]}",
        "jp": f"{bird_data.jp[i]}",
        "link": f"{bird_data.link[i]}",
        "rarity": f"{bird_data.rarity[i]}",
        "img": f"{get_image_url.main_step(bird_data.aves[i])}",
    }

    zh_name = bird_data.zh[i].split("/")
    jp_name = bird_data.jp[i].split("/")
    for j in range(len(zh_name)):
        json_content["zh_index"][zh_name[j]] = avibase_id
    for n in range(len(jp_name)):
        json_content["jp_index"][jp_name[n]] = avibase_id

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(json_content, f, indent=2, ensure_ascii=False)

print("🟢Json Generated!")
