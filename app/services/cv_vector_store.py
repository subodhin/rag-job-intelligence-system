from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from qdrant_client.models import Distance, VectorParams
import uuid

client = QdrantClient(host="localhost", port=6333)

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
                    "chunk_index": index
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
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
                distance=Distance.COSINE
            )
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
                    "match": {
                        "value": cv_id
                    }
                }
            ]
        }
    )

    return results.points      