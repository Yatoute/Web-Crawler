from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

INPUT_DIR = BASE_DIR / "input"

INDEX_PATHS = {
    "title": INPUT_DIR / "title_index.json",
    "description": INPUT_DIR / "description_index.json",
    "brand": INPUT_DIR / "brand_index.json",
    "reviews": INPUT_DIR / "reviews_index.json",
    "origin": INPUT_DIR / "origin_index.json",
    "origin_synonyms": INPUT_DIR / "origin_synonyms.json"
}
