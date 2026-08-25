import faiss
import json
import numpy as np

from app.services.vector_service import INDEX_PATH, search_index

METADATA_PATH = "data/job_metadata.json"


# Load FAISS index
index = faiss.read_index(INDEX_PATH)

print("Vectors in index:", index.ntotal)
print("Vector dimension:", index.d)


# Load job metadata
with open(METADATA_PATH, "r") as f:
    job_metadata = json.load(f)

print("Metadata count:", len(job_metadata))


# Use vector #0 as test query
query_vector = index.reconstruct(0)

query_vector = np.array(
    [query_vector],
    dtype="float32"
)


# Search
distances, indices = search_index(
    index,
    query_vector,
    top_k=3
)

print("Distances:", distances)
print("Indices:", indices)


# Map vector IDs → jobs
for rank, vector_id in enumerate(indices[0]):
    job = job_metadata[vector_id]

    print(
        f"Rank {rank + 1}: "
        f"Vector ID={vector_id}, "
        f"Title={job['title']}, "
        f"Similarity={distances[0][rank]:.4f}"
    )