from rag.embedding_service import EmbeddingService
from rag.vector_store import VectorStoreService

class RetrievalService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreService()

    def retrieve_vector(self, ques: str, project_id: int, n_result : int = 5) -> list[dict]:
        if not ques.strip():
            raise ValueError('Question cannot be empty')

        query_embedding = self.embedding_service.embed_query(ques)

        matches = self.vector_store.search(
            query_embedding = query_embedding,
            project_id = project_id,
            n_result = n_result
        )
        return matches