import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(SCRIPT_DIR, "..")

DATABASE_DIR = os.path.join(ROOT_DIR, "avibase")

JSON_PATH = os.path.join(ROOT_DIR, "data", "birds-data.json")
JSON_CN_PATH = os.path.join(ROOT_DIR, "data", "birds-data-cn.json")

AVIBASE_LINK = "https://avibase.bsc-eoc.org/"
