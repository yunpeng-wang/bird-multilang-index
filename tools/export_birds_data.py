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

bird_data_zh = parse_html(open(zh_html, "r", encoding="utf-8"), "zh")
bird_data_jp = parse_html(open(jp_html, "r", encoding="utf-8"), "jp")

good_for_concat = True
if len(bird_data_zh.aves) == len(bird_data_jp.aves):
    for i in range(len(bird_data_zh.aves)):
        if bird_data_zh.aves[i] != bird_data_jp.aves[i]:
            good_for_concat = False
            break

if good_for_concat:
    bird_data_zh.jp = bird_data_jp.jp
    print("🟢Two data merged!")
else:
    print("🔴Two data are not eligible to be concatenated!")

json_content = {}
json_content["species"] = {}
json_content_species_idx = 0
json_content["zh_index"] = {}
json_content_zh_idx = 0

for i in range(len(bird_data_zh.zh)):
    json_content["species"][bird_data_zh.avibaseid[i]] = {
        "aves": f"{bird_data_zh.aves[i]}",
        "en": f"{bird_data_zh.en[i]}",
        "zh": f"{bird_data_zh.zh[i]}",
        "jp": f"{bird_data_zh.jp[i]}",
        "link": f"{bird_data_zh.link[i]}",
        "rarity": f"{bird_data_zh.rarity[i]}",
    }
    zh_name = bird_data_zh.zh[i].split("/")
    for j in range(len(zh_name)):
        json_content["zh_index"][zh_name[j]] = bird_data_zh.avibaseid[i]

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(json_content, f, indent=2, ensure_ascii=False)
