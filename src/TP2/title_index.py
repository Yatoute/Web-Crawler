from typing import List, Dict, Any, Set

import re

def create_title_index(
    products:List[Dict[str, Any]],
    stop_words:Set[str]=None
    ):
    
    documents = products.copy()
    title_index = {}
    for doc in documents:
        
        title_doc = (doc.get("title") or "").lower()
        # on supprime la ponctuation
        title_doc  = re.sub(r"[^\w\s]", "", title_doc)
        # Tokenisation par espace
        tokens = title_doc.split()
        # On ignore les stops words
        if stop_words:
            tokens = [t for t in tokens if t not in stop_words]
        
        doc_url = doc.get("url") 
        for token in set(tokens):
            token_index = title_index.setdefault(token, {})
            token_index[doc_url] = [idx for idx, t in enumerate(tokens) if t == token]
    
    return title_index