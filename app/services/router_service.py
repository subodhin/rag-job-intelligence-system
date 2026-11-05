from app.agents.search_agent import handle_job_search
from app.agents.insights_agent import handle_insight_search
from app.agents.action_agent import handle_job_action
from app.agents.skill_gap_agent import handle_skill_gap_analysis


def route_request(intent: str, query: str, user_context=None):

    if intent == "job_search":
        return handle_job_search(query, user_context)

    if intent == "market_insights":
        return handle_insight_search(query)

    if intent == "job_action":
        return handle_job_action(query, user_context)

    if intent == "skill_gap_analysis":
        return handle_skill_gap_analysis(query, user_context)

    if intent == "unknown":
        return {
            "message": "Please ask a job-related question."
        }

    return {
        "error": "Unknown intent"
    }