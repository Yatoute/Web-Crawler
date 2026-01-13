import json

from crawler import Crawler

crawler = Crawler(
    seed_urls=["https://web-scraping.dev/products"],
    sleep_seconds=1
    )

results = crawler.run()

with open("./outputs/products.json", "w") as f:
    json.dump(results, f)