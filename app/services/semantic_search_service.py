import json

import faiss
import numpy as np
import ollama

from app.services.vector_service import INDEX_PATH, search_index

# Qdrant
from app.services.qdrant_service import client, COLLECTION_NAME


METADATA_PATH = "data/job_metadata.json"


def semantic_search(query: str, top_k: int = 3):

    print(
        "Semantic Search Query:::::",
        query,
        "Top K:::::",
        top_k
    )

    # ==================================================
    # OLD FAISS IMPLEMENTATION
    # KEEP FOR COMPARISON
    # ==================================================

    # Load FAISS index
    # index = faiss.read_index(INDEX_PATH)

    # Load job metadata
    # with open(METADATA_PATH, "r") as f:
    #     job_metadata = json.load(f)

    # Convert query to embedding
    response = ollama.embed(
        model="nomic-embed-text",
        input=query
    )

    query_vector = np.array(
        [response["embeddings"][0]],
        dtype="float32"
    )

    # ==================================================
    # OLD FAISS NORMALIZATION
    # ==================================================

    # faiss.normalize_L2(query_vector)

    # ==================================================
    # OLD FAISS SEARCH
    # ==================================================

    # distances, indices = search_index(
    #     index,
    #     query_vector,
    #     top_k=top_k
    # )

    # ==================================================
    # OLD FAISS RESULT MAPPING
    # ==================================================

    # results = []

    # for rank, vector_id in enumerate(indices[0]):
    #     results.append({
    #         "job": job_metadata[vector_id],
    #         "similarity": float(distances[0][rank])
    #     })

    # return results


    # ==================================================
    # NEW QDRANT SEARCH
    # ==================================================

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector[0].tolist(),
        limit=top_k,
        with_payload=True
    )

    # ==================================================
    # FORMAT QDRANT RESULTS
    # ==================================================

    qdrant_results = []

    for point in results.points:

        qdrant_results.append({
            "job": point.payload,
            "similarity": float(point.score)
        })

    return qdrant_results