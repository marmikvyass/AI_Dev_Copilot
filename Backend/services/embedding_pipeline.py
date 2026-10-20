from sqlalchemy.orm import Session
from rag.vector_store import VectorStoreService
from rag.embedding_service import EmbeddingService
from models.code_chunk import CodeChunk

class EmbeddingPipeline:
    def __init__(self, db: Session):
        self.db = db
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreService()

    def index_project(self, project_id: int, batch_size : int = 48) -> dict:
        chunks = (
            self.db.query(CodeChunk).filter(CodeChunk.project_id == project_id).order_by(CodeChunk.id).all()
        )

        if not chunks:
            return {
                'project_id' : project_id,
                'chunk_found' : 0,
                'chunk_index' : 0
            }

        indexed = 0

        for start in range(0, len(chunks), batch_size):
            batch = chunks[start:start + batch_size]

            texts = [chunk.content for chunk in batch]
            embeddings = self.embedding_service.embed_texts(texts)

            records = []

            for chunk, embedding in zip(batch, embeddings):
                records.append({
                    "id": chunk.id,
                    "project_id": chunk.project_id,
                    "file_path": chunk.file_path,
                    "chunk_index": chunk.chunk_index,
                    "content": chunk.content,
                    "embedding": embedding,
                })

            self.vector_store.add_chunks(records)
            indexed += len(records)

            # Verify records for this project in Chroma
        stored = self.vector_store.collection.get(
            where={"project_id": project_id},
            include=["metadatas"],
        )

        return {
            "project_id": project_id,
            "chunks_found": len(chunks),
            "chunks_indexed": indexed,
            "chunks_in_chroma": len(stored["ids"]),
        }