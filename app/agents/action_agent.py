import json

from app.tools.tool_router import select_tool, execute_tool


def get_previous_jobs(user_context):

    conversation = user_context.get(
        "conversation",
        []
    ) if user_context else []

    for message in reversed(conversation):

        if message.get("role") != "assistant":
            continue

        try:
            response = json.loads(
                message.get("content", "")
            )

            if response.get("agent") == "search_agent":
                return response.get("results", [])

        except (json.JSONDecodeError, TypeError):
            continue

    return []


def resolve_job(query: str, jobs):

    query_lower = query.lower()

    if not jobs:
        return None

    # "first job", "first one"
    if "first" in query_lower:
        return jobs[0]

    # "second job", "second one", "job 2"
    if (
        "second" in query_lower
        or "job 2" in query_lower
    ):
        if len(jobs) >= 2:
            return jobs[1]

    # "third job", "third one", "job 3"
    if (
        "third" in query_lower
        or "job 3" in query_lower
    ):
        if len(jobs) >= 3:
            return jobs[2]

    # "this job", "this one"
    if (
        "this job" in query_lower
        or "this one" in query_lower
    ):
        return jobs[0]

    return None


def handle_job_action(query: str, user_context=None):

    print("------ Job Action Agent -----")
    print("Action Query:", query)

    user = (
        user_context.get("user", {})
        if user_context
        else {}
    )

    user_id = user.get("user_id")

    # ---------------------------------------
    # Select action tool
    # ---------------------------------------

    tool_name = select_tool(
        "job_action",
        query
    )

    print(
        "Selected action tool:",
        tool_name
    )

    if tool_name is None:
        return {
            "error": "Could not determine job action"
        }

    # ---------------------------------------
    # Get saved jobs
    # ---------------------------------------

    if tool_name == "get_saved_jobs":

        result = execute_tool(
            tool_name,
            query,
            user_id=user_id
        )

        return {
            "intent": "job_action",
            "agent": "action_agent",
            "tool": tool_name,
            "results": result
        }

    # ---------------------------------------
    # Get previous search results
    # ---------------------------------------

    jobs = get_previous_jobs(
        user_context
    )

    print(
        "Previous search jobs:",
        len(jobs)
    )

    # ---------------------------------------
    # Resolve referenced job
    # ---------------------------------------

    job = resolve_job(
        query,
        jobs
    )

    if job is None:

        return {
            "intent": "job_action",
            "agent": "action_agent",
            "tool": tool_name,
            "error": (
                "Could not identify the job. "
                "Please specify the job number or title."
            )
        }

    print(
        "Resolved Job:",
        job.get("id"),
        job.get("title")
    )

    # ---------------------------------------
    # Execute action
    # ---------------------------------------

    result = execute_tool(
        tool_name,
        query,
        user_id=user_id,
        job=job
    )

    return {
        "intent": "job_action",
        "agent": "action_agent",
        "tool": tool_name,
        "job": job,
        "result": result
    }