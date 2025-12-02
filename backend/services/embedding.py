"""Embedding service for generating text embeddings.

Uses OpenAI's text-embedding-3-small model by default.
"""

from openai import OpenAI

from core.config import get_settings


class EmbeddingError(Exception):
    """Error during embedding generation."""

    pass


class EmbeddingService:
    """Service for generating text embeddings using OpenAI.

    Uses text-embedding-3-small (1536 dimensions) by default.
    """

    def __init__(self) -> None:
        """Initialize embedding service with OpenAI client."""
        settings = get_settings()

        self.model = settings.openai_embedding_model
        self._client = OpenAI(api_key=settings.openai_api_key.get_secret_value())

    async def embed(self, text: str) -> list[float]:
        """Generate embedding vector for text.

        Args:
            text: Text to embed.

        Returns:
            List of floats representing the embedding vector.

        Raises:
            ValueError: If text is empty.
            EmbeddingError: If API call fails.
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        try:
            response = self._client.embeddings.create(
                model=self.model,
                input=text,
            )
            return response.data[0].embedding
        except Exception as e:
            raise EmbeddingError(f"Failed to generate embedding: {e}") from e

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed.

        Returns:
            List of embedding vectors.

        Raises:
            ValueError: If any text is empty.
            EmbeddingError: If API call fails.
        """
        if not texts:
            return []

        # Validate all texts
        for i, text in enumerate(texts):
            if not text or not text.strip():
                raise ValueError(f"Text at index {i} cannot be empty")

        try:
            response = self._client.embeddings.create(
                model=self.model,
                input=texts,
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            raise EmbeddingError(f"Failed to generate batch embeddings: {e}") from e
