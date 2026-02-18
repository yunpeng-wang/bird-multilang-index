"""
add pinyin dict for zh_index
"""

from pypinyin import lazy_pinyin, Style
import json
from common import JSON_PATH

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

zh_index = data["zh_index"]
new_zh_index = {}

for key in list(zh_index.keys()):
    new_zh_index[key] = {}
    new_zh_index[key]["id"] = zh_index[key]

    #py_full = lazy_pinyin(key)
    py_initials = lazy_pinyin(key, style=Style.FIRST_LETTER)
    #new_zh_index[key]["pinyin"] = "".join(py_full)
    new_zh_index[key]["pinyin_initials"] = "".join(py_initials)

data["zh_index"] = new_zh_index

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("🟢Adding pinyin succeeded!")
