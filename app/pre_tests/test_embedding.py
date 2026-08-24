import ollama

response = ollama.embed(
    model="nomic-embed-text",
    input="Python AI Engineer working with RAG and LLMs"
)

embedding = response["embeddings"][0]

print("Vector length:", len(embedding))
print("First 5 values:", embedding[:5])