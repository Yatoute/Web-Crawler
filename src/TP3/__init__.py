import json

from search_engine import SearchEngine

engine = SearchEngine(
    ranking_weights = {
        "bm25_title": 2.0,
        "bm25_description": 1.0,
        "exact_match": 1.5,
        "reviews": 0.7,
        },
)
results =  engine.search("brand MagicSteps")
with open("./output/MagicSteps.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
    
results =  engine.search("box of chocolate candy")
with open("./output/chocolate_candy.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
    
results =  engine.search("Light-Up Sneakers made in america")
with open("./output/sneakers_usa.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)