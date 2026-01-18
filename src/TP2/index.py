from typing import List, Dict, Any
from datetime import datetime
from utils import tokenize_text


def create_description_index(
    products:List[Dict[str, Any]]
    ):
    
    documents = products.copy()
    description_index = {}
    for doc in documents:
        
        description_doc = doc.get("description") or ""
        
        # TOkenisation
        tokens = tokenize_text(description_doc)
        
        doc_url = doc.get("url") 
        for token in set(tokens):
            token_index = description_index.setdefault(token, {})
            token_index[doc_url] = [idx for idx, t in enumerate(tokens) if t == token]
    
    return description_index

def create_title_index(
    products:List[Dict[str, Any]]
    ):
    
    documents = products.copy()
    title_index = {}
    for doc in documents:
        
        title_doc = doc.get("title") or ""
        
        # TOkenisation
        tokens = tokenize_text(title_doc)
        
        doc_url = doc.get("url") 
        for token in set(tokens):
            token_index = title_index.setdefault(token, {})
            token_index[doc_url] = [idx for idx, t in enumerate(tokens) if t == token]
    
    return title_index

def create_reviews_index(
    products:List[Dict[str, Any]]
):
    """Create Reviews Index"""
    
    documents = products.copy()
    reviews_index = {}
    for doc in documents:
        doc_url = doc.get("url")
        reviews_index[doc_url] = {}
        
        doc_reviews = doc.get("product_reviews") or []
        total_reviews = len(doc_reviews)
        if total_reviews >0:
            reviews_index[doc_url]["total_reviews"] = total_reviews
            reviews_index[doc_url]["mean_mark"] = sum([review.get("rating") for review in doc_reviews])/len(doc_reviews)
            doc_reviews = sorted(
                doc_reviews,
                key=lambda r: datetime.strptime(r["date"], "%Y-%m-%d"),
                reverse=True
            )
            reviews_index[doc_url]["last_rating"] = doc_reviews[0].get("rating")
        else:
            reviews_index[doc_url] = {
                "total_reviews":0,
                "mean_mark":0,
                "last_rating":0
            }
            
    return reviews_index

def create_feature_index(
    products: List[Dict[str, Any]],
    feature: str
) -> Dict[str, Dict[str, List[int]]]:
    """
    Create a positional inverted index for a given product feature.
    """
    
    index: Dict[str, Dict[str, List[int]]] = {}

    for doc in products:
        doc_url = doc.get("url")
        if not doc_url:
            continue

        features = doc.get("product_features") or {}
        feature_text = features.get(feature) or ""

        tokens = tokenize_text(feature_text)

        for token in set(tokens):
            token_index = index.setdefault(token, [])
            token_index.append(doc_url)

    return index

