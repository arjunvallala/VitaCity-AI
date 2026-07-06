"""
VitaCity AI — RAG Engine
TF-IDF based Retrieval-Augmented Generation for the knowledge base.
No external vector DB required — runs fully in-memory.
"""

import logging
from typing import List, Dict, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from data.knowledge_base import get_all_chunks, DOMAIN_COLORS

logger = logging.getLogger(__name__)


class RAGEngine:
    """
    In-memory RAG engine using TF-IDF + cosine similarity.
    Indexes the VitaCity knowledge base and retrieves top-K relevant chunks
    to augment Gemini prompts.
    """

    def __init__(self, top_k: int = 5):
        self.top_k = top_k
        self._chunks: List[Dict] = []
        self._vectorizer: TfidfVectorizer = None
        self._tfidf_matrix = None
        self._texts: List[str] = []
        self._indexed = False
        self._build_index()

    def _build_index(self):
        """Build TF-IDF index over all knowledge chunks."""
        try:
            self._chunks = get_all_chunks()
            # Combine title, content, and tags for richer representation
            self._texts = [
                f"{c['title']} {c['content']} {' '.join(c.get('tags', []))}"
                for c in self._chunks
            ]
            self._vectorizer = TfidfVectorizer(
                ngram_range=(1, 2),
                min_df=1,
                max_df=0.95,
                stop_words="english",
                sublinear_tf=True,
            )
            self._tfidf_matrix = self._vectorizer.fit_transform(self._texts)
            self._indexed = True
            logger.info(f"RAG index built: {len(self._chunks)} chunks indexed.")
        except Exception as e:
            logger.error(f"RAG index build failed: {e}")
            self._indexed = False

    def retrieve(
        self,
        query: str,
        domain_filter: str = None,
        top_k: int = None,
    ) -> List[Dict]:
        """
        Retrieve top-K most relevant chunks for a query.

        Args:
            query: User's natural language question.
            domain_filter: Optional domain name to restrict results.
            top_k: Number of results to return (overrides instance default).

        Returns:
            List of chunk dicts with added 'similarity_score' key.
        """
        if not self._indexed or not query.strip():
            return []

        k = top_k or self.top_k

        try:
            query_vec = self._vectorizer.transform([query])
            scores = cosine_similarity(query_vec, self._tfidf_matrix)[0]

            # Apply domain filter if specified
            if domain_filter and domain_filter != "All Domains":
                filtered_scores = []
                for i, chunk in enumerate(self._chunks):
                    if domain_filter.lower() in chunk["domain"].lower():
                        filtered_scores.append((i, scores[i]))
                    else:
                        filtered_scores.append((i, 0.0))
                scored_indices = sorted(filtered_scores, key=lambda x: x[1], reverse=True)
            else:
                scored_indices = sorted(
                    enumerate(scores), key=lambda x: x[1], reverse=True
                )

            results = []
            for idx, score in scored_indices[:k]:
                if score > 0.01:  # Minimum relevance threshold
                    chunk = dict(self._chunks[idx])
                    chunk["similarity_score"] = float(score)
                    results.append(chunk)

            return results

        except Exception as e:
            logger.error(f"RAG retrieval error: {e}")
            return []

    def format_context(self, chunks: List[Dict]) -> str:
        """
        Format retrieved chunks into a context string for Gemini prompt.

        Args:
            chunks: List of retrieved chunk dicts.

        Returns:
            Formatted context string.
        """
        if not chunks:
            return ""

        lines = []
        for i, chunk in enumerate(chunks, 1):
            confidence_pct = int(chunk.get("similarity_score", 0) * 100)
            lines.append(
                f"### Source {i}: {chunk['title']}\n"
                f"**Domain:** {chunk['domain']} | **Relevance:** {confidence_pct}%\n\n"
                f"{chunk['content']}\n"
            )

        return "\n---\n".join(lines)

    def retrieve_and_format(
        self,
        query: str,
        domain_filter: str = None,
        top_k: int = None,
    ) -> Tuple[str, List[Dict]]:
        """
        Retrieve and format context in one step.

        Returns:
            Tuple of (formatted context string, list of chunk dicts)
        """
        chunks = self.retrieve(query, domain_filter=domain_filter, top_k=top_k)
        context = self.format_context(chunks)
        return context, chunks

    def get_domain_coverage(self, query: str) -> Dict[str, float]:
        """
        Calculate relevance scores per domain for a given query.
        Useful for showing which domains the question spans.
        """
        if not self._indexed:
            return {}

        try:
            query_vec = self._vectorizer.transform([query])
            scores = cosine_similarity(query_vec, self._tfidf_matrix)[0]

            domain_scores: Dict[str, List[float]] = {}
            for idx, chunk in enumerate(self._chunks):
                domain = chunk["domain"]
                if domain not in domain_scores:
                    domain_scores[domain] = []
                domain_scores[domain].append(float(scores[idx]))

            # Return max score per domain
            return {
                domain: round(max(score_list), 4)
                for domain, score_list in domain_scores.items()
            }
        except Exception as e:
            logger.error(f"Domain coverage error: {e}")
            return {}

    @property
    def chunk_count(self) -> int:
        return len(self._chunks)

    @property
    def is_ready(self) -> bool:
        return self._indexed


# Singleton
_engine: RAGEngine = None

def get_rag_engine() -> RAGEngine:
    """Get or create the RAG engine singleton."""
    global _engine
    if _engine is None:
        _engine = RAGEngine()
    return _engine
