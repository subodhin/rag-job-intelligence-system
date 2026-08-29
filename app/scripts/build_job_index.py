import os
import json

from app.embedding_functions.create_job_embedding import embed_jobs
#from app.main import get_jobs
from app.services.external_jobs import get_jobs

from app.services.vector_service import create_index, save_index


METADATA_PATH = "data/job_metadata.json"


# Create data directory
os.makedirs("data", exist_ok=True)


# Get jobs
jobs = get_jobs() 


# Generate embeddings
embedded_jobs = embed_jobs(jobs)

# Create metadata mapping
job_metadata = [
    item["job"]
    for item in embedded_jobs
]

# Create FAISS index
index = create_index(embedded_jobs)


# Debug information
print("Jobs:", len(jobs))
print("Embedded:", len(embedded_jobs))
print("Vectors:", index.ntotal)
print("Dimension:", index.d)
print("Metadata count:", len(job_metadata))


# Save FAISS index
save_index(index)


# Save job metadata
with open(METADATA_PATH, "w") as f:
    json.dump(job_metadata, f, indent=2)

print(f"Metadata saved to: {METADATA_PATH}")