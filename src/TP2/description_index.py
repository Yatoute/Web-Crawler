from typing import List, Dict, Any, Set

import re

def create_description_index(
    products:List[Dict[str, Any]],
    stop_words:Set[str]=None
    ):
    
    documents = products.copy()
    description_index = {}
    for doc in documents:
        
        description_doc = (doc.get("description") or "").lower()
        # on supprime la ponctuation
        description_doc  = re.sub(r"[^\w\s]", "", description_doc)
        # Tokenisation par espace
        tokens = description_doc.split()
        # On ignore les stops words
        if stop_words:
            tokens = [t for t in tokens if t not in stop_words]
        
        doc_url = doc.get("url") 
        for token in set(tokens):
            token_index = description_index.setdefault(token, {})
            token_index[doc_url] = [idx for idx, t in enumerate(tokens) if t == token]
    
    return description_index