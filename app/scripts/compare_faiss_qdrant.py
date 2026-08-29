import json
import faiss
import numpy as np
import ollama

from app.services.vector_service import INDEX_PATH, search_index
from app.services.qdrant_service import client, COLLECTION_NAME


METADATA_PATH = "data/job_metadata.json"


QUERIES = [
    "Find jobs similar to AI engineer with Python",
    "highest paying jobs for software engineers",
    "Python developer jobs",
    "react developers with experience in TypeScript",
]


def search_faiss(query, top_k=3):

    # Load FAISS index
    index = faiss.read_index(INDEX_PATH)

    # Load metadata
    with open(METADATA_PATH, "r") as f:
        job_metadata = json.load(f)

    # Create query embedding
    response = ollama.embed(
        model="nomic-embed-text",
        input=query
    )

    query_vector = np.array(
        [response["embeddings"][0]],
        dtype="float32"
    )

    # FAISS cosine similarity
    faiss.normalize_L2(query_vector)

    distances, indices = search_index(
        index,
        query_vector,
        top_k=top_k
    )

    results = []

    for rank, vector_id in enumerate(indices[0]):

        results.append({
            "title": job_metadata[vector_id]["title"],
            "similarity": float(distances[0][rank])
        })

    return results


def search_qdrant(query, top_k=3):

    # Create query embedding
    response = ollama.embed(
        model="nomic-embed-text",
        input=query
    )

    query_vector = response["embeddings"][0]

    # Qdrant search
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True
    )

    qdrant_results = []

    for point in results.points:

        qdrant_results.append({
            "title": point.payload["title"],
            "similarity": float(point.score)
        })

    return qdrant_results


for query in QUERIES:

    print("\n" + "=" * 70)
    print("QUERY:", query)
    print("=" * 70)

    faiss_results = search_faiss(query)
    qdrant_results = search_qdrant(query)

    print("\nFAISS:")

    for rank, result in enumerate(faiss_results, start=1):

        print(
            f"{rank}. "
            f"{result['title']} "
            f"| score={result['similarity']:.6f}"
        )

    print("\nQDRANT:")

    for rank, result in enumerate(qdrant_results, start=1):

        print(
            f"{rank}. "
            f"{result['title']} "
            f"| score={result['similarity']:.6f}"
        )