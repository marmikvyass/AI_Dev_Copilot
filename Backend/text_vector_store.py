
from rag.vector_store import VectorStoreService


def main():
    vector_store = VectorStoreService()

    vector_store.add_chunks([
        {
            "id": "test-project-12-chunk-0",
            "embedding": [0.1, 0.2, 0.3],
            "content": "def add(a, b): return a + b",
            "project_id": 12,
            "file_path": "app.py",
            "chunk_index": 0,
        }
    ]
    )

    print("Chroma record count:", vector_store.count())


if __name__ == "__main__":
    main()
