"""
Provide functions for requesting image url from Wikimedia Commons
"""

import requests
import time


def preprocess_name(name):
    # discard all content in () and [], and return string arrey, such as
    # Histrionicus histrionicus (pacificus) -> ["Histrionicus", "histrionicus"]
    # Anser [caerulescens x albifrons] -> ["Anser"]
    ret = name.split(" (")[0]
    ret = ret.split(" [")[0]
    ret = ret.split(" ")
    return ret


def get_image(scientific_name):
    HEADERS = {
        "User-Agent": "BirdNameIndexBot/1.0 (https://yunpeng-wang.github.io/bird-multilang-index/)"
    }
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "pageimages",
        "piprop": "original",
        "titles": scientific_name,
    }

    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=10)
        r.raise_for_status()
        data = r.json()

        pages = data["query"]["pages"]
        for page in pages.values():
            if "original" in page:
                return page["original"]["source"]

        return None

    except requests.exceptions.RequestException as e:
        print(f"Error for {scientific_name}: {e}")
        return None


def main_step(aves):
    name_arr = preprocess_name(aves)
    img_link = None

    while img_link is None and len(name_arr) > 0:
        concat_name = " ".join(name_arr)
        img_link = get_image(concat_name)
        name_arr.pop(-1)
        time.sleep(0.5)  # delay

    if img_link is None:
        print(f"💡Parsing image link done! Failed! Name={aves}")
        return ""
    else:
        print("💡Parsing image link done! Succeeded!")
        return img_link


if __name__ == "__main__":
    print(main_step("Cygnus columbianus"))
