import requests


def embed_documents(documents):
    embeddings = []

    for doc in documents:
        response = requests.post(
            "http://localhost:11434/api/embed",
            json={
                "model": "nomic-embed-text",
                "input": doc.page_content
            }
        )

        response.raise_for_status()

        vector = response.json()["embeddings"][0]
        print(f"Document embedded. Length of vector::::::::::::::: {len(vector)}")

        embeddings.append({
            "document": doc,
            "vector": vector
        })

    return embeddings

def embed_query(query: str):
    response = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "nomic-embed-text",
            "input": query
        }
    )

    response.raise_for_status()

    return response.json()["embeddings"][0]