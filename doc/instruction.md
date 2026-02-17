# Steps

1. <export_birds_data.py> --> Generate JSON data (including images) for birds found in Japan.
2. <CN_export_birds_data.py> --> Generate JSON data (excluding images) for birds found in China.
3. <merge_json.py> --> merge two JSONs.
4. <get_image_url.py> --> Get images url from wikimedia via API.
5. <refeed_image_url> --> Fetch the missing images.
