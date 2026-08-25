import json

import faiss
import numpy as np
import ollama

from app.services.vector_service import INDEX_PATH, search_index


METADATA_PATH = "data/job_metadata.json"


def semantic_search(query: str, top_k: int = 3):
    print("Semantic Search Query:::::", query, "Top K:::::", top_k, "INDEX_PATH:::::", INDEX_PATH, "METADATA_PATH:::::", METADATA_PATH)
    # Load FAISS index
    index = faiss.read_index(INDEX_PATH)

    # Load job metadata
    with open(METADATA_PATH, "r") as f:
        job_metadata = json.load(f)

    # Convert query to embedding
    response = ollama.embed(
        model="nomic-embed-text",
        input=query
    )

    query_vector = np.array(
        [response["embeddings"][0]],
        dtype="float32"
    )

    # Normalize for cosine similarity
    faiss.normalize_L2(query_vector)

    # Search vector index
    distances, indices = search_index(
        index,
        query_vector,
        top_k=top_k
    )

    # Map vector IDs → actual jobs
    results = []

    for rank, vector_id in enumerate(indices[0]):
        results.append({
            "job": job_metadata[vector_id],
            "similarity": float(distances[0][rank])
        })

    return results