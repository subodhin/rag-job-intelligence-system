from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


# QDRANT_PATH = "data/qdrant"
# COLLECTION_NAME = "jobs"

# client = QdrantClient(
#     path=QDRANT_PATH
# )


QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "jobs"

client = QdrantClient(
    url=QDRANT_URL
)


def create_collection(vector_size: int = 768):

    collections = client.get_collections().collections

    existing_names = [
        collection.name
        for collection in collections
    ]

    if COLLECTION_NAME not in existing_names:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )

        print(
            f"Qdrant collection created: {COLLECTION_NAME}"
        )

    else:

        print(
            f"Qdrant collection already exists: {COLLECTION_NAME}"
        )


def get_collection_info():

    return client.get_collection(
        collection_name=COLLECTION_NAME
    )

def search_jobs(query_vector, top_k=3):

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True
    )

    return results.points