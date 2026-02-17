"""
re-get image url from category page in case api doesn't work
"""
import json
import get_image_url
from common import JSON_PATH

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

keys = list(data["species"].keys())

counter = 0
for key in keys:
    single_dict = data["species"][key]
    if single_dict["img"] == "":
        counter += 1
        print(f"Processing {counter}-th data")
        aves = single_dict["aves"]
        single_dict["img"] = get_image_url.get_image_from_category(aves)

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)