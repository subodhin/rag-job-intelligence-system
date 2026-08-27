from app.services.rag_service import check_required_skills


jobs = [
    {
        "title": "Senior Data Engineer",
        "skills": ["Python", "SQL", "AWS"]
    },
    {
        "title": "AI Engineer",
        "skills": ["Python", "FastAPI", "AI/ML"]
    },
    {
        "title": "Frontend Developer",
        "skills": ["React", "JavaScript"]
    }
]

required_skills = ["Python", "LLM"]

results = check_required_skills(
    jobs,
    required_skills
)

for result in results:
    print("\nJob:", result["job"]["title"])
    print("Matched:", result["matched_skills"])
    print("Missing:", result["missing_skills"])