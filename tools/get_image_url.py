"""
Provide functions for requesting image url from Wikimedia Commons
"""

from bs4 import BeautifulSoup as BS
from bs4 import Tag
import requests
import time

HEADERS = {
    "User-Agent": "BirdNameIndexBot/1.0 (https://yunpeng-wang.github.io/bird-multilang-index/)"
}


def preprocess_name(name):
    ret = name.split(" ")
    return ret


def get_image_from_category(scientific_name):
    url = "https://commons.wikimedia.org/wiki/Category:"
    time.sleep(1.0)  # delay
    img_link = ""

    name_arr = preprocess_name(scientific_name)
    concat_name = "_".join(name_arr)
    response = requests.get(url + concat_name, headers=HEADERS)
    if response.status_code == 200:
        soup = BS(response.text, "html.parser")
        container = soup.find(id="wdinfobox")
        if isinstance(container, Tag):
            img = container.find("img", class_="mw-file-element")
            if isinstance(img, Tag):
                img_link = img.get("src")
    else:
        print(f"Failed! Code:{response.status_code}")

    if img_link == "":
        print(f"Error for {scientific_name}")

    return img_link


def get_image_from_api(scientific_name):
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
        img_link = get_image_from_api(concat_name)
        name_arr.pop(-1)
        time.sleep(0.5)  # delay

    if img_link is None:
        print(f"💡Parsing image link done! Failed! Name={aves}")
        return ""
    else:
        print("💡Parsing image link done! Succeeded!")
        return img_link


if __name__ == "__main__":
    print(main_step("Remiz consobrinus"))
