import json
import re


def parse_json(jsonl_path:str):
    
    """Parse the products json"""
    
    products = []
    url_pattern = re.compile(
        r"/product/(?P<id>\d+)(?:\?variant=(?P<variant>[a-zA-Z0-9_-]+))?"
    )
    with open(jsonl_path, "r", encoding="utf-8") as f:
        i = 0
        for line in f:
            product = json.loads(line)
            product_url = product.get("url") or ""
            match = url_pattern.search(product_url)
            if match:
                product_id = match.groupdict().get("id")
                if product_id:
                    product["id"] = product_id
                product_variant = match.groupdict().get("variant")
                if product_variant:
                    product["variant"] = product_variant
                
            products.append(product)
    
    return products
            
products = parse_json("./input/products.jsonl")