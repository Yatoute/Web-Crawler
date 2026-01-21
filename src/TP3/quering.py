from typing import List, Dict, Any, Set, Optional
import json

from utils import tokenize_text

def load_index(index_path: str) -> Dict[str, Any]:
    """Load an index by given the index path file"""

    with open(index_path, "r", encoding="utf-8") as f:
        return json.load(f)

def resolve_origin_from_synonym(
    origin_synonym: str,
    origin_synonyms_index: Dict[str, Any]
) -> Optional[str]:
    """Resolve origin from synomym"""
    
    origin_synonym = origin_synonym.lower().strip()
    for origin_key in origin_synonyms_index.keys():
        if (origin_synonym==origin_key) or (origin_synonym in origin_synonyms_index[origin_key]):
            return origin_key
    return None

def prepare_query(
    query: str,
    origin_synonyms_index: Dict[str, Any]
) -> List[str]:
    """
    Tokenize + normalize the user query and apply simple synonym expansion
    for origin-related tokens.
    """
    tokens = tokenize_text(query, normalize=True)

    expanded = set(tokens)
    for t in tokens:
        canonical = resolve_origin_from_synonym(t, origin_synonyms_index)
        if canonical:
            expanded.add(canonical)
    return list(expanded)

def find_docs_with_any_token(
    tokens_request: List[str],
    indexes: Dict[str, Dict[str, Any]]
) -> Set[str]:
    """OR filtering: docs that match at least one token in any index."""
    docs_found = set()
    for token in set(tokens_request):
        for index_key in ["title", "description", "brand", "origin"]:
            index = indexes[index_key]
            if token in index:
                docs = index[token]
                if isinstance(docs, list):
                    docs_found.update(docs)
                elif isinstance(docs, dict):
                    docs_found.update(docs.keys())
    return docs_found


def find_docs_with_all_tokens(
    tokens_request: List[str],
    indexes: Dict[str, Dict[str, Any]]
) -> Set[str]:
    """AND filtering: docs that match all tokens (after stopword removal)."""
    docs_found = set()
    for token in set(tokens_request):
        token_docs = set()
        for index_key in ["title", "description", "brand", "origin"]:
            index = indexes[index_key]
            if token in index:
                docs = index[token]
                if isinstance(docs, dict):
                    token_docs.update(docs.keys())
                else:
                    token_docs.update(docs)
        docs_found = (docs_found & token_docs) if docs_found else token_docs
    return docs_found
