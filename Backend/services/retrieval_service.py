from typing import Any
from sqlalchemy.orm import Session

from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


from models.code_chunk import CodeChunk
from rag.embedding_service import EmbeddingService
from rag.vector_store import VectorStoreService


class RetrievalService(BaseRetriever):
    project_id: int
    n_result: int
    embedding_service: Any
    vector_store: Any


    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun)-> list[Document]:
        query_embedding = self.embedding_service.embed_query(query)

        matches = self.vector_store.search(
            query_embedding = query_embedding,
            project_id = self.project_id,
            n_result = self.n_result
        )

        return [
            Document(
                page_content=match["content"],
                metadata={
                    "project_id": int(match["metadata"]["project_id"]),
                    "file_path": match["metadata"]["file_path"],
                    "chunk_index": int(match["metadata"]["chunk_index"]),
                },
            )
            for match in matches
        ]
class HybridRetrievalService:
    def __init__(self, db: Session):
        self.db = db
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreService()

    def retrieve(
        self,
        query: str,
        project_id: int,
        n_result: int = 5,
    ) -> list[dict]:
        if not query.strip():
            raise ValueError("Question cannot be empty")

        # Load only this project's chunks for keyword retrieval.
        rows = (
            self.db.query(CodeChunk)
            .filter(CodeChunk.project_id == project_id)
            .order_by(CodeChunk.file_path, CodeChunk.chunk_index)
            .all()
        )

        if not rows:
            return []

        documents = [
            Document(
                page_content=row.content,
                metadata={
                    "project_id": int(row.project_id),
                    "file_path": row.file_path,
                    "chunk_index": int(row.chunk_index),
                },
            )
            for row in rows
        ]

        keyword_retriever = BM25Retriever.from_documents(
            documents,
            k=n_result,
        )

        semantic_retriever = RetrievalService(
            project_id=project_id,
            n_result=n_result,
            embedding_service=self.embedding_service,
            vector_store=self.vector_store,
        )

        ensemble = EnsembleRetriever(
            retrievers=[semantic_retriever, keyword_retriever],
            weights=[0.7, 0.3],
        )

        # RRF combines the rankings and deduplicates matching documents.
        merged = ensemble.invoke(query)

        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "distance": None,
            }
            for doc in merged[:n_result]
        ]