import json

from json_parser import parse_json
from index import (
    create_description_index, 
    create_title_index, 
    create_reviews_index,
    create_feature_index
)

products = parse_json("./input/products.jsonl")

# Title Index
title_index = create_title_index(products)
with open("./output/title_index.json", "w") as f:
    json.dump(title_index, f)
    
# Description Index
desc_index = create_description_index(products)
with open("./output/description_index.json", "w") as f:
    json.dump(desc_index, f)
    
# Reviews index
reviews_index = create_reviews_index(products)
with open("./output/reviews_index.json", "w") as f:
    json.dump(reviews_index, f)
    
# Origin index
origin_index = create_feature_index(products, "made in")
with open("./output/origin_index.json", "w") as f:
    json.dump(origin_index, f)
    
# Brand index
brand_index = create_feature_index(products, "brand")
with open("./output/brand_index.json", "w") as f:
    json.dump(brand_index, f)