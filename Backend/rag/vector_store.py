import chromadb
from pathlib import Path

from narwhals.selectors import matches


class VectorStoreService:
    def __init__(self):
        persist_dir = (Path(__file__).resolve().parent.parent / 'chroma_db')

        self.client = chromadb.PersistentClient(
            path=str(persist_dir)
        )

        self.collection = self.client.get_or_create_collection(
            name='code_chunks_v1',
            metadata={'hnsw:space': 'cosine'}
        )

    def add_chunks(self, chunks: list[dict]) -> None:
        if not chunks:
            return None

        self.collection.upsert(
            ids=[str(chunk['id']) for chunk in chunks],
            embeddings=[chunk['embedding'] for chunk in chunks],
            documents = [chunk['content'] for chunk in chunks],
            metadatas = [{
                'project_id' : int(chunk['project_id']),
                'file_path' : chunk['file_path'],
                'chunk_index' : int(chunk['chunk_index'])
            } for chunk in chunks ]
        )


    def count(self)-> int:
        return self.collection.count()

    def search(self, query_embedding: list[dict], project_id: int, n_result: int = 5) -> list[dict]:
        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results = n_result,
            where={'project_id' : project_id},
            include=['documents', 'metadatas', 'distances']
        )

        matches = []

        for i in range(len(result['ids'][0])):
            matches.append({
                'id': result['ids'][0][i],
                'content' : result['documents'][0][i],
                'metadata' : result['metadatas'][0][i],
                'distance' : result['distances'][0][i]
            })
        return matches