from typing import Protocol

class VectorStore(Protocol):
    def index_document(self, content: str, metadata: dict) -> None:
        ...

    def search_similar(self, query: str, top_k: int = 5) -> list[dict]:
        ...

    def reset_index(self) -> None:
        ...
