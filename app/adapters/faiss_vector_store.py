import faiss
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
import uuid

class FAISSVectorStore:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dimension = 384  # embedding boyutu bu model için
        self.index = faiss.IndexFlatL2(self.dimension)
        self.texts = []
        self.metadata = []

    def add_texts(self, texts: List[str], metadata: List[dict]):
        vectors = self.model.encode(texts)
        self.index.add(np.array(vectors).astype('float32'))
        self.texts.extend(texts)
        self.metadata.extend(metadata)

    def search(self, query: str, k: int = 5):
        query_vector = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_vector).astype('float32'), k)
        results = []
        for i in indices[0]:
            if i < len(self.texts):
                results.append({
                    "text": self.texts[i],
                    "metadata": self.metadata[i]
                })
        return results
