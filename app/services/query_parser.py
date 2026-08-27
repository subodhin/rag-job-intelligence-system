def parse_query(query: str):

    query = query.lower()

    filters = {
        "skill": None,
        "skills": [],
        "location": None,
        "salary": None
    }

    skills = [
        "python",
        "java",
        "react",
        "javascript",
        "sql",
        "fastapi",
        "llm",
        "ai/ml",
        "golang",
        "go",
        "c++",
        "c#",
        "ruby",
        "ruby/rails",
        "node.js",
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "gcp",
        "postgresql",
        "mysql",
        "nlp"
    ]

    for skill in skills:

        if skill in query:
            filters["skills"].append(skill)

    # Keep backward compatibility with existing code
    if filters["skills"]:
        filters["skill"] = filters["skills"][0]

    if "remote" in query:
        filters["location"] = "remote"

    if "high paying" in query or "highest paying" in query:
        filters["salary"] = "high"

    return filters