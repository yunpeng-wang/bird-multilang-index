# Steps

## 1. JP (Required)

1. <export_birds_data> --> Generate JSON data (including images) for birds found in Japan.
2. <refeed_image_url> --> Fetch the missing images.

## 2. CN (Optional)

1. <CN_export_birds_data> --> Generate JSON data (excluding images) for birds found in China.
2. <CN_add_data> --> Discard bird data shared between Japan and China and fetch images.
3. <refeed_image_url> --> Fetch the missing images (modify JSON path).

## 3. Post-process

1. merge two JSONs.
