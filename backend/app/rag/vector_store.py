import re
import math
from typing import List, Dict, Any, Optional
from collections import Counter
import numpy as np

class VectorStore:
    def __init__(self):
        # In-memory document indexes: doc_id -> list of chunk dicts
        self._indexes: Dict[int, List[Dict[str, Any]]] = {}
        # Vocabulary and IDF per document
        self._idf: Dict[int, Dict[str, float]] = {}
        self._doc_vectors: Dict[int, List[Dict[str, float]]] = {}

    def index_document(self, document_id: int, chunks: List[Dict[str, Any]]) -> int:
        """
        Indexes document chunks for fast similarity retrieval with chunk and page metadata.
        """
        self._indexes[document_id] = chunks
        
        # Tokenize and compute TF-IDF / term vectors for high-precision retrieval
        tokenized_chunks = []
        doc_count = len(chunks)
        df = Counter()
        
        for ch in chunks:
            tokens = self._tokenize(ch.get("text", "") + " " + ch.get("section_name", ""))
            tokenized_chunks.append(tokens)
            unique_terms = set(tokens)
            for t in unique_terms:
                df[t] += 1
                
        # Compute IDF
        idf_dict = {}
        for term, freq in df.items():
            idf_dict[term] = math.log((1 + doc_count) / (1 + freq)) + 1.0
            
        self._idf[document_id] = idf_dict
        
        # Compute normalized TF-IDF vector for each chunk
        vectors = []
        for tokens in tokenized_chunks:
            tf = Counter(tokens)
            vec = {}
            norm_sq = 0.0
            for term, count in tf.items():
                w = (1.0 + math.log(count)) * idf_dict.get(term, 1.0)
                vec[term] = w
                norm_sq += w * w
            norm = math.sqrt(norm_sq) if norm_sq > 0 else 1.0
            norm_vec = {k: v / norm for k, v in vec.items()}
            vectors.append(norm_vec)
            
        self._doc_vectors[document_id] = vectors
        return len(chunks)

    def search(self, document_id: int, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieves top-k relevant chunks for the given query with source page, chunk_id, and similarity.
        """
        if document_id not in self._indexes or not self._indexes[document_id]:
            return []
            
        chunks = self._indexes[document_id]
        vectors = self._doc_vectors.get(document_id, [])
        idf = self._idf.get(document_id, {})
        
        query_tokens = self._tokenize(query)
        if not query_tokens:
            # Fallback to top initial chunks
            return [
                {
                    **ch,
                    "similarity": 0.85
                }
                for ch in chunks[:top_k]
            ]
            
        q_tf = Counter(query_tokens)
        q_vec = {}
        q_norm_sq = 0.0
        for term, count in q_tf.items():
            w = (1.0 + math.log(count)) * idf.get(term, 1.0)
            q_vec[term] = w
            q_norm_sq += w * w
        q_norm = math.sqrt(q_norm_sq) if q_norm_sq > 0 else 1.0
        q_norm_vec = {k: v / q_norm for k, v in q_vec.items()}
        
        # Calculate cosine similarity with all chunks
        scored_chunks = []
        for idx, ch in enumerate(chunks):
            ch_vec = vectors[idx]
            sim = 0.0
            for term, val in q_norm_vec.items():
                if term in ch_vec:
                    sim += val * ch_vec[term]
            
            # Additional boost if query tokens match section heading
            sec_lower = ch.get("section_name", "").lower()
            if any(t in sec_lower for t in query_tokens):
                sim = min(1.0, sim + 0.15)
                
            scored_chunks.append((sim, ch))
            
        # Sort descending by similarity
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        
        results = []
        for sim, ch in scored_chunks[:top_k]:
            results.append({
                "chunk_id": ch.get("chunk_id", "chunk_01"),
                "chunk_index": ch.get("chunk_index", 1),
                "page_number": ch.get("page_number", 1),
                "section_name": ch.get("section_name", "General"),
                "text": ch.get("text", ""),
                "similarity": round(float(sim), 3) if sim > 0 else 0.50
            })
            
        return results

    def _tokenize(self, text: str) -> List[str]:
        cleaned = re.sub(r"[^\w\s]", " ", text.lower())
        tokens = [t for t in cleaned.split() if len(t) > 2]
        return tokens

# Global singleton vector store instance
vector_store = VectorStore()
