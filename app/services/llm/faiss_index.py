import os, shutil
from app.interfaces.llm.vector_store import VectorStore

FAISS_INDEX_PATH = "app/vector_store/index"

class FAISSVectorStore(VectorStore):
    def index_document(self, content: str, metadata: dict) -> None:
        # TODO: FAISS vektör ekleme işlemi
        pass

    def search_similar(self, query: str, top_k: int = 5) -> list[dict]:
        # TODO: FAISS benzerlik araması
        return []

    def reset_index(self) -> None:
        if os.path.exists(FAISS_INDEX_PATH):
            shutil.rmtree(FAISS_INDEX_PATH)
        os.makedirs(FAISS_INDEX_PATH, exist_ok=True)
