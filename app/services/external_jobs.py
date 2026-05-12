import requests

REMOTIVE_URL = "https://remotive.com/api/remote-jobs"

def get_jobs():

    response = requests.get(REMOTIVE_URL)

    data = response.json()

    normalized_jobs = []

    for job in data["jobs"]:

        normalized_jobs.append({
            "title": job["title"],
            "skills": job["tags"],
            "salary": job.get("salary", "Not specified"),
            "location": job["candidate_required_location"]
        })

    return normalized_jobs