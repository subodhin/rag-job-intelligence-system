from app.tools.tool_registry import get_tool


def select_tool(intent: str, query: str):
    print("Selecting tool for intent:::::::::::::::", intent, "and query:", query)

    if intent == "job_search":

        if any(
            word in query.lower()
            for word in ["semantic", "similar", "experience", "looking for"]
        ):
            return "semantic_job_search"

        return "search_jobs"

    if intent == "market_insights":
        return "job_insights"

    return None


def execute_tool(tool_name: str, query: str):

    tool = get_tool(tool_name)

    if tool is None:
        return {
            "error": f"Tool '{tool_name}' not found"
        }

    if tool_name == "semantic_job_search":
        return tool(query, top_k=3)

    if tool_name == "search_jobs":
        # We'll connect structured filters here
        # in the next step.
        return tool({})

    if tool_name == "job_insights":
        return tool()

    return {
        "error": f"Execution not implemented for '{tool_name}'"
    }