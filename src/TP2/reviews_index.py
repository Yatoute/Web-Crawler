from typing import List, Dict, Any
from datetime import datetime


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
        