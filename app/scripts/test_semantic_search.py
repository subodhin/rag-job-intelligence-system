import faiss
import json
import numpy as np
import ollama

from app.services.vector_service import INDEX_PATH, search_index


METADATA_PATH = "data/job_metadata.json"

#QUERY = "AI engineer with Python and LLM experience"
#QUERY = "engineer with typescript knowledge"
#QUERY = "with experience in Java, React experince"
QUERY = "highest paying jobs for software engineers"




# Load FAISS index
index = faiss.read_index(INDEX_PATH)

print("Vectors in index:", index.ntotal)
print("Vector dimension:", index.d)


# Load metadata
with open(METADATA_PATH, "r") as f:
    job_metadata = json.load(f)

print("Metadata count:", len(job_metadata))


# Create embedding for user query
response = ollama.embed(
    model="nomic-embed-text",
    input=QUERY
)

query_vector = np.array(
    [response["embeddings"][0]],
    dtype="float32"
)

print("Query:", QUERY)
print("Query vector dimension:", query_vector.shape[1])


# Normalize query vector
faiss.normalize_L2(query_vector)


# Search FAISS
distances, indices = search_index(
    index,
    query_vector,
    top_k=3
)

print("Distances:", distances)
print("Indices:", indices)


# Map vector IDs → actual jobs
for rank, vector_id in enumerate(indices[0]):
    job = job_metadata[vector_id]

    print(
        f"Rank {rank + 1}: "
        f"Vector ID={vector_id}, "
        f"Title={job['title']}, "
        f"Similarity={distances[0][rank]:.4f}"
    )