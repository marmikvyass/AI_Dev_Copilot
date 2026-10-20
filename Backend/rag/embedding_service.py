import cohere
from core.config import settings

class EmbeddingService:
    def __init__(self):
        if not settings.COHERE_API_KEY:
            raise ValueError("COHERE_API_KEY is missing from .env")
        self.client = cohere.ClientV2(
            api_key = settings.COHERE_API_KEY
        )

        self.model = "embed-v4.0"

    def embed_text(self, text:str)-> list[float]:
        if not text.strip():
            raise ValueError("Text cannot be empty")

        response = self.client.embed(
            model=self.model,
            texts=[text],
            input_type="search_document",
            embedding_types=["float"]
        )

        return response.embeddings.float_[0]

    def embed_texts(self, texts: list[str])-> list[list[float]]:
        if not texts:
            return []

        if any(not text.strip() for text in texts):
            raise ValueError("Text cannot be empty")

        response = self.client.embed(
            model=self.model,
            texts=texts,
            input_type="search_document",
            embedding_types=["float"]
        )

        return response.embeddings.float_

    def embed_query(self, query: str) -> list[float]:
        if not query.strip():
            raise ValueError("Query cannot be empty")

        response = self.client.embed(
            model = self.model,
            texts = [query],
            input_type='search_query',
            embedding_types=['float']
        )

        return response.embeddings.float_[0]

