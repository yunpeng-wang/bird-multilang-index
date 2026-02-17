import json
import os
from common import JSON_PATH, JSON_CN_PATH

with open(JSON_PATH, "r", encoding="utf-8") as f:
    jp_data = json.load(f)

with open(JSON_CN_PATH, "r", encoding="utf-8") as f:
    cn_data = json.load(f)

jp_data["species"].update(cn_data["species"])
jp_data["zh_index"].update(cn_data["zh_index"])
jp_data["jp_index"].update(cn_data["jp_index"])

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(jp_data, f, indent=2, ensure_ascii=False)

print("🟢Json merged!")