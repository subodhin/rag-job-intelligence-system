import ollama

from app.services.qdrant_service import search_jobs


QUERY = "Find jobs similar to AI engineer with Python"


# Create query embedding
response = ollama.embed(
    model="nomic-embed-text",
    input=QUERY
)

query_vector = response["embeddings"][0]

print("Query:", QUERY)
print("Embedding dimension:", len(query_vector))


# Search Qdrant
results = search_jobs(
    query_vector=query_vector,
    top_k=3
)


print("\nQdrant Results:")

for result in results:

    print("\nScore:", result.score)
    print("Job:", result.payload)