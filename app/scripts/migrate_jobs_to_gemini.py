import json
import sys
from pathlib import Path

from dotenv import load_dotenv
from qdrant_client.models import PointStruct

# Project root: ai-job-assistant/
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Load configuration before importing the Qdrant client
load_dotenv(PROJECT_ROOT / ".env")

sys.path.insert(0, str(PROJECT_ROOT))

from app.services.embedding_service import create_embedding
from app.services.qdrant_service import client, COLLECTION_NAME

METADATA_PATH = PROJECT_ROOT / "data" / "job_metadata.json"


def create_job_text(job):
    skills = ", ".join(job.get("skills", []))
    return (
        f"Title: {job.get('title', '')}\n"
        f"Skills: {skills}\n"
        f"Salary: {job.get('salary', '')}\n"
        f"Location: {job.get('location', '')}"
    )


def main():
    with open(METADATA_PATH, "r", encoding="utf-8") as file:
        jobs = json.load(file)

    existing_points, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=100,
        with_payload=True,
        with_vectors=False,
    )

    existing_by_id = {int(point.id): point for point in existing_points}
    expected_ids = list(range(1, len(jobs) + 1))

    if sorted(existing_by_id) != expected_ids:
        raise RuntimeError(
            "Qdrant IDs do not match expected job IDs. Migration stopped."
        )

    points_to_update = []

    # Generate all embeddings before changing the database.
    for job_id, job in enumerate(jobs, start=1):
        print(f"Generating Gemini embedding for job {job_id}/{len(jobs)}...")

        embedding = create_embedding(
            create_job_text(job),
            task_type="RETRIEVAL_DOCUMENT",
        )

        existing_payload = existing_by_id[job_id].payload or {}

        points_to_update.append(
            PointStruct(
                id=job_id,
                vector=embedding,
                payload=existing_payload,
            )
        )

    if len(points_to_update) != len(jobs):
        raise RuntimeError("Embedding count mismatch. Migration stopped.")

    print("\nAll embeddings generated successfully.")
    print("Updating existing Qdrant records...")

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points_to_update,
        wait=True,
    )

    info = client.get_collection(COLLECTION_NAME)

    print("\nMigration completed.")
    print("Jobs migrated:", len(points_to_update))
    print("Qdrant record count:", info.points_count)
    print("Embedding dimensions: 768")


if __name__ == "__main__":
    main()