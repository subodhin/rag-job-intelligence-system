import sys

from app.services.embedding_service import create_embedding
from app.services.qdrant_service import client, COLLECTION_NAME


def semantic_search(query: str, top_k: int = 3):
    print(
        "Semantic Search Query:",
        query,
        "Top K:",
        top_k,
        file=sys.stderr,
    )

    # Generate query embedding using Gemini
    query_vector = create_embedding(
        query,
        task_type="RETRIEVAL_QUERY",
    )

    # Search Qdrant Cloud
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True,
    )

    # Format results
    qdrant_results = []

    for point in results.points:
        qdrant_results.append({
            "job": point.payload,
            "similarity": float(point.score),
        })

    return qdrant_results