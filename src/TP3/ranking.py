import math
from typing import Dict, List, Set, Any, Optional, Tuple


def exact_match_score(
    query_tokens: List[str],
    doc_url: str, 
    indexes: Dict[str, Dict[str, Any]]
    ) -> float:
    """
    Compute the proportion of query tokens that appear in the document,
    across all textual indexes (title, description, brand, origin).
    """
    if not query_tokens:
        return 0.0

    matched_tokens = set()

    for t in query_tokens:
        for index_key in ["title", "description", "brand", "origin"]:
            field_index = indexes[index_key]
            if t in field_index:
                docs = field_index[t]
                if isinstance(docs, dict) and doc_url in docs:
                    matched_tokens.add(t)
                elif isinstance(docs, list) and doc_url in docs:
                    matched_tokens.add(t)

    return len(matched_tokens) / len(query_tokens)

def term_frequency(
        token: str, 
        doc_url: str, 
        field_index: Dict[str, Dict[str, Any]]
    ) -> float:
    """
    TF per field, using only the index.
    """

    postings = field_index.get(token)
    if isinstance(postings, dict):
        tf = len(postings.get(doc_url, []))
    elif isinstance(postings, list):
        tf = 1 if doc_url in postings else 0
    else:
        tf = 0

    return tf


def bm25_score(
    query_tokens: List[str],
    doc_url: str,
    field_index: Dict[str, Dict[str, Any]],
    total_docs: Optional[int] = None,
    k1: float = 1.2,
    b: float = 0.75
) -> float:
    """
    Compute the BM25 score of a document for a given query on a single field.

    In this implementation, we follow the BM25 formulation presented in the course,
    using only the inverted index (no access to raw documents).
    """

    # --------------------------------------------------
    # Infer collection size N if not provided
    # --------------------------------------------------
    if total_docs is None:
        docs_union = set()
        for postings in field_index.values():
            if isinstance(postings, dict):
                docs_union.update(postings.keys())
            elif isinstance(postings, list):
                docs_union.update(postings)
        total_docs = len(docs_union)

    # --------------------------------------------------
    # Detect whether the index is positional
    # --------------------------------------------------
    positional = False
    for postings in field_index.values():
        positional = isinstance(postings, dict)
        break

    # --------------------------------------------------
    # Compute document lengths and average field length
    # --------------------------------------------------
    if positional:
        # Reconstruct document lengths from positions
        max_pos_by_doc: Dict[str, int] = {}
        for postings in field_index.values():
            if not isinstance(postings, dict):
                continue
            for url, positions in postings.items():
                if positions:
                    max_pos_by_doc[url] = max(
                        max_pos_by_doc.get(url, -1),
                        max(positions)
                    )

        doc_lens = {d: (m + 1) for d, m in max_pos_by_doc.items()}
        avg_len = (sum(doc_lens.values()) / len(doc_lens)) if doc_lens else 0.0

    else:
        # Non-positional index (brand/origin):
        # no notion of document length -> neutral normalization
        doc_lens = {}
        avg_len = 1.0

    # --------------------------------------------------
    # BM25 IDF function
    # --------------------------------------------------
    def idf(N: int, df: int) -> float:
        return math.log(1 + (N - df + 0.5) / (df + 0.5))

    # --------------------------------------------------
    # BM25 scoring
    # --------------------------------------------------
    score = 0.0

    for token in query_tokens:
        # Term frequency in the document
        tf = term_frequency(token, doc_url, field_index)
        if tf <= 0:
            continue

        postings = field_index.get(token)
        if not postings:
            continue

        # Document frequency
        df = len(postings)
        if df <= 0:
            continue

        # IDF component
        token_idf = idf(total_docs, df)

        # Length normalization
        if isinstance(postings, dict):
            doc_len = doc_lens.get(doc_url, 0)
        else:
            doc_len = 1

        if avg_len <= 0:
            continue

        # BM25 contribution
        score += token_idf * (
            (tf * (k1 + 1)) /
            (tf + k1 * (1 - b + b * (doc_len / avg_len)))
        )

    return score


def reviews_score(
    doc_url: str,
    reviews_index: Dict[str, Dict[str, Any]],
    default: float = 0.0,
) -> float:
    """
    Get the mean review mark for a given document.
    """
    r = reviews_index.get(doc_url)
    if not r:
        return default

    mean_mark = float(r.get("mean_mark", 0) or 0)
    return mean_mark

def linear_ranking_score(
    doc_url: str,
    query_tokens: List[str],
    indexes: Dict[str, Dict[str, Any]],
    ranking_weights: Optional[Dict[str, float]] = None,
    bm25_params: Optional[Dict[str, float]] = None,
) -> float:
    """
    Compute the final linear ranking score for one document, as a weighted sum
    of several base ranking signals (Linear Ranking model).

    Signals:
      - BM25(title)
      - BM25(description)
      - Exact match ratio
      - Reviews-based score
    """

    # Default weights
    if ranking_weights is None:
        ranking_weights = {
            "bm25_title": 2.0,
            "bm25_description": 1.0,
            "exact_match": 1.5,
            "reviews": 0.7,
        }

    # bm25_params
    bm25_params = bm25_params or {}
    bm25_allowed_parms = {"k1", "b", "total_docs"}
    bm25_params = {k: v for k, v in bm25_params.items() if k in bm25_allowed_parms}

    # Base ranking signals
    s_bm25_title = bm25_score(query_tokens, doc_url, indexes["title"], **bm25_params)
    s_bm25_desc = bm25_score(query_tokens, doc_url, indexes["description"], **bm25_params)
    s_exact = exact_match_score(query_tokens, doc_url, indexes)
    s_reviews = reviews_score(doc_url, indexes["reviews"])

    # Linear combination
    final_score = (
        ranking_weights.get("bm25_title", 0.0) * s_bm25_title
        + ranking_weights.get("bm25_description", 0.0) * s_bm25_desc
        + ranking_weights.get("exact_match", 0.0) * s_exact
        + ranking_weights.get("reviews", 0.0) * s_reviews
    )

    return final_score


def rank_documents(
    query_tokens: List[str],
    candidate_docs: Set[str],
    indexes: Dict[str, Dict[str, Any]],
    ranking_weights: Optional[Dict[str, float]] = None,
    bm25_params: Optional[Dict[str, float]] = None,
    top_k: Optional[int] = None,
) -> List[Tuple[str, float]]:
    """
    Rank a set of candidate documents for a query using the linear ranking model.
    """
    scored_docs = []
    
    for doc_url in candidate_docs:
        s = linear_ranking_score(
            doc_url=doc_url,
            query_tokens=query_tokens,
            indexes=indexes,
            ranking_weights=ranking_weights,
            bm25_params=bm25_params,
        )
        scored_docs.append((doc_url, s))

    scored_docs.sort(key=lambda x: x[1], reverse=True)
    
    if top_k:
        scored_docs = scored_docs[:top_k]
        
    return scored_docs

