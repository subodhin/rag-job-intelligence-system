from app.services.data_service import search_jobs

def handle_job_search(query: str):
    print("------ Job Search Agent!-----")


    jobs = search_jobs(query)

    return {
        "intent": "job_search",
        "agent": "search_agent",
        "results": jobs
    }