import os
import time
import requests
from requests import Response

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(SCRIPT_DIR, "..")

DATABASE_DIR = os.path.join(ROOT_DIR, "avibase")

JSON_PATH = os.path.join(ROOT_DIR, "data", "birds-data.json")
JSON_JP_PATH = os.path.join(ROOT_DIR, "data", "birds-data-jp.json")
JSON_CN_PATH = os.path.join(ROOT_DIR, "data", "birds-data-cn.json")

AVIBASE_LINK = "https://avibase.bsc-eoc.org/"


def robo_requests(
    url: str,
    max_retries: int = 3,
    wait_time: int = 2,
    custom_headers: dict[str, str] | None = None,
    custom_params: dict[str, str] | None = None,
    time_out: int = 10,
) -> Response | None:
    default_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.3.1 Safari/605.1.15"
    }
    if custom_headers is None:
        custom_headers = default_headers

    ret = None
    for retry in range(max_retries):
        try:
            response = requests.get(
                url, params=custom_params, headers=custom_headers, timeout=time_out
            )
            if response.status_code == 200:
                ret = response
                break
            else:
                print(f"⚠️ Response error: {response.status_code}. Retry...")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Request exception: {e}. Retry...")

        if retry == max_retries - 1:
            print(f"🔴 All retry failed")
        else:
            time.sleep(wait_time)

    return ret
