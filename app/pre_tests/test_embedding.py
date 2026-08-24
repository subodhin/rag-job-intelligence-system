import ollama

job = {
    "title": "AI Engineer",
    "description": "Build LLM and RAG applications...",
    "skills": ["Python", "FastAPI", "RAG", "LLM"]
}

job_text = f"""
Title: {job['title']}
Description: {job['description']}
Skills: {', '.join(job['skills'])}
"""

response = ollama.embed(
    model="nomic-embed-text",
    input=job_text
)
embedding = response["embeddings"][0]

# embedding = response["embeddings"][0]

# print("Vector length:", len(embedding))
# print("First 5 values:", embedding[:5])


