from typing import List, Dict, Any, Set, Optional
import json

from config import INDEX_PATHS
from utils import tokenize_text

def load_index(index_path: str) -> Dict[str, Any]:
    """Load en index by given the index path file"""

    with open(index_path, "r", encoding="utf-8") as f:
        return json.load(f)

def resolve_origin_from_synonym(origin_synonym:str) -> Optional[str]:
    """Resolve origin from synomym"""
    
    origin_synonym = origin_synonym.lower().strip()
    origin_synonyms_index = load_index(INDEX_PATHS["origin_synonyms"])
    for origin_key in origin_synonyms_index.keys():
        if (origin_synonym==origin_key) or (origin_synonym in origin_synonyms_index[origin_key]):
            return origin_key
    return None

brand_index = load_index(index_path=INDEX_PATHS["brand"])

def find_docs_with_any_token(tokens_request:List[str]) -> Set[str]:
    """
    Return the set of document that contain at least one token
    from the given list across multiple indexes.
    """
    
    docs_found = set()
    for token in tokens_request:
        for index_key in ["title", "description", "brand", "origin"]:
            index = load_index(INDEX_PATHS[index_key])
            if token in index:
                docs = index[token]
                if isinstance(docs, list):
                    docs_found.update(docs)
                if isinstance(docs, dict):
                    docs_found.update(docs.keys())
             
    return docs_found

def find_docs_with_all_tokens(tokens_request:List[str]) -> Set[str]:
    """
    Return the set of documents that contain all tokens
    from the given list across multiple indexes.
    """
    
    docs_found = set()
    
    for index_key in ["title", "description", "brand", "origin"]:
        index = load_index(INDEX_PATHS[index_key])
        for token in tokens_request:
            if token in index:
                docs = index[token]
                if isinstance(docs, dict):
                    docs = docs.keys()
                docs = set(docs)
                docs_found = docs_found & docs if docs_found else docs
                
    return docs_found

        
          

            
