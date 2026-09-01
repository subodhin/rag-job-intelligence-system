from app.tools.tool_registry import get_tool


def select_tool(intent: str, query: str):

    print(
        "Selecting tool for intent:::::::::::::::",
        intent,
        "and query:",
        query
    )

    query_lower = query.lower()

    if intent == "job_search":

        if any(
            word in query_lower
            for word in ["semantic", "similar", "experience", "looking for"]
        ):
            return "semantic_job_search"

        return "search_jobs"

    if intent == "market_insights":
        return "job_insights"

    if intent == "job_action":

        if any(
            phrase in query_lower
            for phrase in ["saved jobs", "my jobs", "tracked jobs"]
        ):
            return "get_saved_jobs"

        if any(
            word in query_lower
            for word in ["applied", "interview", "rejected", "offer"]
        ):
            return "track_job"

        if any(
            word in query_lower
            for word in ["save", "bookmark"]
        ):
            return "save_job"

    return None


def execute_tool(tool_name: str, query: str, user_id=None, job=None):

    tool = get_tool(tool_name)

    if tool is None:
        return {
            "error": f"Tool '{tool_name}' not found"
        }

    if tool_name == "semantic_job_search":
        return tool(query, top_k=3)

    if tool_name == "search_jobs":
        return tool({})

    if tool_name == "job_insights":
        return tool()

    if tool_name == "save_job":

        if not user_id or not job:
            return {
                "error": "User ID and job are required"
            }

        return tool(
            user_id,
            job
        )

    if tool_name == "track_job":

        if not user_id or not job:
            return {
                "error": "User ID and job are required"
            }

        return tool(
            user_id,
            job["id"],
            "applied"
        )

    if tool_name == "get_saved_jobs":

        if not user_id:
            return {
                "error": "User ID is required"
            }

        return tool(user_id)

    return {
        "error": f"Execution not implemented for '{tool_name}'"
    }