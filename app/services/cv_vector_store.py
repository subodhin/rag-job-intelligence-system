import os
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY or None,
)

COLLECTION_NAME = "cv_documents"


def store_cv_embeddings(cv_id, embedded_chunks):
    points = []

    for index, item in enumerate(embedded_chunks):
        document = item["document"]
        vector = item["vector"]

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "cv_id": cv_id,
                    "text": document.page_content,
                    "page": document.metadata.get("page"),
                    "chunk_index": index,
                },
            )
        )

    if points:
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
        )

    return len(points)


def ensure_cv_collection():
    collections = client.get_collections()

    exists = any(
        collection.name == COLLECTION_NAME
        for collection in collections.collections
    )

    if not exists:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=768,
                distance=Distance.COSINE,
            ),
        )


def search_cv(cv_id, query_vector, top_k=3):
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        query_filter={
            "must": [
                {
                    "key": "cv_id",
                    "match": {"value": cv_id},
                }
            ]
        },
    )

    return results.points
