import ollama

def create_job_text(job):
    return f"""
Title: {job['title']}
Skills: {', '.join(job['skills'])}
Location: {job['location']}
""".strip()


def embed_jobs(jobs):
    embedded_jobs = []

    for job in jobs:
        job_text = create_job_text(job)

        response = ollama.embed(
            model="nomic-embed-text",
            input=job_text
        )

        embedding = response["embeddings"][0]
        print(" ")
        print(
            "Embedding created for job:",
            job["title"],
            "Embedding :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::",
            embedding
        )


        embedded_jobs.append({
            "job": job,
            "text": job_text,
            "embedding": embedding
        })

    return embedded_jobs