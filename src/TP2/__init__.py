import json

from json_parser import parse_json
from utils import get_stop_words
from title_index import create_title_index
from description_index import create_description_index
from reviews_index import create_reviews_index

products = parse_json("./input/products.jsonl")

STOP_WORDS = get_stop_words()

# Title Index
title_index = create_title_index(products, STOP_WORDS)
with open("./output/title_index.json", "w") as f:
    json.dump(title_index, f)
    
# Description Index
desc_index = create_description_index(products, STOP_WORDS)
with open("./output/description_index.json", "w") as f:
    json.dump(desc_index, f)
    
# Reviews index
reviews_index = create_reviews_index(products)
with open("./output/reviews_index.json", "w") as f:
    json.dump(reviews_index, f)