from app.embedding_functions.create_job_embedding import embed_jobs
from app.services.external_jobs import get_jobs
from app.services.qdrant_service import (
    client,
    COLLECTION_NAME,
    create_collection
)
from qdrant_client.models import PointStruct


# 1. Get jobs
jobs = get_jobs()

print("Jobs:", len(jobs))


# 2. Generate embeddings
embedded_jobs = embed_jobs(jobs)

print("Embedded jobs:", len(embedded_jobs))


# 3. Make sure the collection exists
create_collection(768)


# 4. Create Qdrant points
points = []

for index, item in enumerate(embedded_jobs):

    job = item["job"]

    points.append(
        PointStruct(
            id=index,
            vector=item["embedding"],
            payload={
                "title": job["title"],
                "skills": job["skills"],
                "salary": job["salary"],
                "location": job["location"]
            }
        )
    )


# 5. Insert into Qdrant
client.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)


# 6. Verify
info = client.get_collection(
    collection_name=COLLECTION_NAME
)

print("Migrated points:", len(points))
print("Qdrant points:", info.points_count)