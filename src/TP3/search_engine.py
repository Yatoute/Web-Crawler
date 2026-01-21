# __init__.py
from typing import List, Dict, Any, Set, Optional, Tuple
import json

from config import INDEX_PATHS, PRODUCTS_PATH
from quering import (
    load_index,
    prepare_query,
    find_docs_with_any_token,
    find_docs_with_all_tokens,
)
from ranking import rank_documents


class SearchEngine:
    """
    search engine for products.
    """

    def __init__(
        self,
        indexes: Optional[Dict[str, Dict[str, Any]]] = None,
        products_path: str = PRODUCTS_PATH,
        index_paths: Dict[str, str] = INDEX_PATHS,
        use_and_filter: bool = False,
        ranking_weights: Optional[Dict[str, float]] = None,
        bm25_params: Optional[Dict[str, float]] = None,
    ):
        self.index_paths = index_paths
        self.products_path = products_path
        self.use_and_filter = use_and_filter

        # Ranking configuration
        self.ranking_weights = ranking_weights
        self.bm25_params = bm25_params

        self.indexes = indexes

    def _get_indexes(self) -> Dict[str, Dict[str, Any]]:
        """Get indexes, loading them if needed."""
        if self.indexes is None:
            self.indexes = {k: load_index(self.index_paths[k]) for k in self.index_paths.keys()}
        return self.indexes

    def _load_products_by_url(self, urls: Set[str]) -> Dict[str, Dict[str, Any]]:
        """
        Load products from the JSONL file, keeping only documents whose URL is in `urls`.
        Returns a dict: url -> product dict.
        """
        selected: Dict[str, Dict[str, Any]] = {}

        if not urls:
            return selected

        with open(self.products_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                u = obj.get("url")
                if u in urls:
                    selected[u] = obj

        return selected

    def search(self, query: str, top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Search products for a given query.
        
        Args:
            query: raw user query (string)
            top_k: optional maximum number of results returned (after ranking)

        Returns:
            List of product dicts, each enriched with a "_score" key.
        """
        indexes = self._get_indexes()

        # Query preparation (tokenize + normalize + synonym expansion)
        query_tokens = prepare_query(query, indexes["origin_synonyms"])

        # Candidate retrieval
        if self.use_and_filter:
            candidate_docs = find_docs_with_all_tokens(query_tokens, indexes)
        else:
            candidate_docs = find_docs_with_any_token(query_tokens, indexes)

        # Ranking
        ranked_docs = rank_documents(
            query_tokens=query_tokens,
            candidate_docs=candidate_docs,
            indexes=indexes,
            ranking_weights=self.ranking_weights,
            bm25_params=self.bm25_params,
            top_k=top_k,
        )

        # Load products for the ranked URLs only
        docs_urls = [url for url, _ in ranked_docs]
        products = self._load_products_by_url(set(docs_urls))

        # Return products ordered by ranking + attach score
        results: List[Dict[str, Any]] = []
        for url, score in ranked_docs:
            product = products.get(url)
            if not product:
                continue
            product = dict(product)
            product["_score"] = score
            results.append(product)

        return results

