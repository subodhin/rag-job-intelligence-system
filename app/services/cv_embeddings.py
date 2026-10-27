
from app.services.embedding_service import create_embedding


def embed_documents(documents):
    embeddings = []

    for doc in documents:
        vector = create_embedding(
            doc.page_content,
            task_type="RETRIEVAL_DOCUMENT"
        )

        print(
            f"Document embedded. "
            f"Vector dimensions: {len(vector)}"
        )

        embeddings.append({
            "document": doc,
            "vector": vector
        })

    return embeddings


def embed_query(query: str):
    return create_embedding(
        query,
        task_type="RETRIEVAL_QUERY"
    )
