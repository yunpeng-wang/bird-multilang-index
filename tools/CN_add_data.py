import json
import os
import get_image_url
from common import JSON_PATH, JSON_CN_PATH


with open(JSON_PATH, "r", encoding="utf-8") as f:
    jp_data = json.load(f)

with open(JSON_CN_PATH, "r", encoding="utf-8") as f:
    cn_data = json.load(f)

jp_keys = list(jp_data["species"].keys())
cn_keys = list(cn_data["species"].keys())

bird_id = []

for cn in cn_keys:
    found = True
    for jp in jp_keys:
        if cn == jp:
            found = False
            break
    if found:
        bird_id.append(cn)

json_content = {}
json_content["classification"] = cn_data["classification"]
json_content["species"] = {}
json_content["zh_index"] = {}
json_content["jp_index"] = {}

cn_species = cn_data["species"]
counter = 0
for id in bird_id:
    counter += 1
    print(f"Processing: {counter}/{len(bird_id)}")

    json_content["species"][id] = {
        "aves": f"{cn_species[id]["aves"]}",
        "en": f"{cn_species[id]["en"]}",
        "zh": f"{cn_species[id]["zh"]}",
        "jp": f"{cn_species[id]["jp"]}",
        "link": f"{cn_species[id]["link"]}",
        "rarity": f"{cn_species[id]["rarity"]}",
        "img": f"{get_image_url.main_step(cn_species[id]["aves"])}",
    }

    zh_name = cn_species[id]["zh"].split("/")
    jp_name = cn_species[id]["jp"].split("/")
    for i in range(len(zh_name)):
        json_content["zh_index"][zh_name[i]] = id
    for j in range(len(jp_name)):
        json_content["jp_index"][jp_name[j]] = id

with open(JSON_CN_PATH, "w", encoding="utf-8") as f:
    json.dump(json_content, f, indent=2, ensure_ascii=False)

print("🟢Json Generated!")