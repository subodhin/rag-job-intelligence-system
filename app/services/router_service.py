from app.agents.search_agent import handle_job_search
from app.agents.insights_agent import handle_insight_search


#AI orchestration engine
def route_request(intent: str, query: str):

    if intent == "job_search":

        return handle_job_search(query)
    
    if intent == "market_insights":

        return handle_insight_search(query)
    
    if intent == "unknown":

        return {
        "message": "Please ask a job-related question."
       }

    return {
        "error": "Unknown intent"
    }