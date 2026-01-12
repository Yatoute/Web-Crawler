from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

def parse_html(html: str):
    soup = BeautifulSoup(html, "html.parser")

    # URL (best-effort) : canonical si présent
    canonical = soup.select_one('link[rel="canonical"]')
    url = canonical["href"].strip() if canonical and canonical.get("href") else None

    # Title
    title = soup.title.get_text(strip=True) if soup.title else ""

    # Description (meta)
    desc_tag = soup.select_one('meta[name="description"]')
    description = desc_tag.get("content", "").strip() if desc_tag else ""

    # Product features
    product_features = {}
    for row in soup.select("tr.feature"):
        label = row.select_one(".feature-label")
        value = row.select_one(".feature-value")
        if label and value:
            k = label.get_text(" ", strip=True)
            v = value.get_text(" ", strip=True)
            product_features[k] = v

    # Links 
    links = []
    base_for_join = url or ""  # si on a canonical, on peut joindre les liens relatifs
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href:
            continue
        links.append(urljoin(base_for_join, href) if base_for_join else href)

    # Product reviews : depuis le JSON caché id="reviews-data"
    product_reviews = []
    reviews_tag = soup.select_one("#reviews-data")
    if reviews_tag and reviews_tag.string:
        try:
            product_reviews = json.loads(reviews_tag.string)
        except json.JSONDecodeError:
            product_reviews = []

    return {
        "url": url,
        "title": title,
        "description": description,
        "product_features": product_features,
        "links": links,
        "product_reviews": product_reviews,
    }
