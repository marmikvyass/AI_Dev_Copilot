
from rag.embedding_service import EmbeddingService


def main():
    service = EmbeddingService()

    text = """
    def add(a, b):
        return a + b
    """

    embedding = service.embed_text(text)

    print("Embedding generated successfully")
    print("Vector dimensions:", len(embedding))
    print("First 5 values:", embedding)


if __name__ == "__main__":
    main()
