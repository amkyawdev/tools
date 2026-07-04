import hashlib
import os
from typing import Optional

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)

from app.utils.logger import setup_logger

logger = setup_logger(__name__)

# We use a deterministic hash-based embedding so we don't need external
# embedding APIs. Swap this out for a real embedding service in production.
EMBEDDING_DIM = 1536


class QdrantService:
    """Async wrapper around a Qdrant vector database instance."""

    def __init__(self) -> None:
        self.url = os.getenv("QDRANT_URL", "http://localhost:6333")
        self.api_key = os.getenv("QDRANT_API_KEY", "")
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "amkyawdev-tools")

        self.client = AsyncQdrantClient(
            url=self.url,
            api_key=self.api_key,
        )

    # ------------------------------------------------------------------
    # Collection management
    # ------------------------------------------------------------------

    async def ensure_collection(self) -> None:
        """Create the collection if it does not already exist."""
        collections = await self.client.get_collections()
        collection_names = [c.name for c in collections.collections]

        if self.collection_name not in collection_names:
            await self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=EMBEDDING_DIM, distance=Distance.COSINE
                ),
            )
            logger.info(f"Created collection: {self.collection_name}")

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    async def search(
        self,
        query: str,
        skill_filter: Optional[str] = None,
        limit: int = 10,
    ) -> list[dict]:
        """Semantic search over the knowledge base."""
        await self.ensure_collection()

        query_vector = await self._embed(query)

        query_filter: Optional[Filter] = None
        if skill_filter:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="skill", match=MatchValue(value=skill_filter)
                    )
                ]
            )

        results = await self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            query_filter=query_filter,
        )

        return [
            {
                "id": hit.id,
                "score": hit.score,
                "content": hit.payload.get("content", ""),
                "metadata": hit.payload.get("metadata", {}),
                "skill": hit.payload.get("skill", ""),
            }
            for hit in results
        ]

    # ------------------------------------------------------------------
    # Upsert / Delete
    # ------------------------------------------------------------------

    async def upsert(
        self,
        entry_id: str,
        content: str,
        metadata: Optional[dict] = None,
        skill: Optional[str] = None,
    ) -> None:
        """Insert or update a single knowledge entry."""
        await self.ensure_collection()

        vector = await self._embed(content)

        point = PointStruct(
            id=entry_id,
            vector=vector,
            payload={
                "content": content,
                "metadata": metadata or {},
                "skill": skill or "",
            },
        )

        await self.client.upsert(
            collection_name=self.collection_name, points=[point]
        )
        logger.info(f"Upserted knowledge entry: {entry_id}")

    async def delete(self, entry_id: str) -> None:
        """Delete a knowledge entry by id."""
        await self.client.delete(
            collection_name=self.collection_name, points_selector=[entry_id]
        )
        logger.info(f"Deleted knowledge entry: {entry_id}")

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    @staticmethod
    async def _embed(text: str) -> list[float]:
        """Deterministic embedding via SHA-256 (replace for production)."""
        hash_bytes = hashlib.sha256(text.encode()).digest()
        vector: list[float] = []
        for i in range(EMBEDDING_DIM):
            byte_val = hash_bytes[i % len(hash_bytes)]
            vector.append((byte_val / 255.0) * 2 - 1)
        return vector
