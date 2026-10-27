import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-embedding-001"

GEMINI_EMBEDDING_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/"
    f"models/{GEMINI_MODEL}:embedContent"
)


def create_embedding(text: str, task_type: str = "RETRIEVAL_QUERY") -> list:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    response = requests.post(
        GEMINI_EMBEDDING_URL,
        headers={
            "x-goog-api-key": GEMINI_API_KEY,
            "Content-Type": "application/json",
        },
        json={
            "model": f"models/{GEMINI_MODEL}",
            "content": {"parts": [{"text": text}]},
            "taskType": task_type,
            "outputDimensionality": 768,
        },
        timeout=30,
    )

    response.raise_for_status()

    embedding = response.json()["embedding"]["values"]

    if len(embedding) != 768:
        raise ValueError(
            f"Expected 768 embedding dimensions, got {len(embedding)}."
        )

    return embedding