from app.tools.insight_tools import (
    job_insights_tool
)

from app.tools.job_tools import (
    search_jobs_tool,
    semantic_job_search_tool,
    save_job,
    track_job,
    get_saved_jobs
)


# function to get the tool function by name!
TOOLS = {
    "search_jobs": search_jobs_tool,
    "semantic_job_search": semantic_job_search_tool,
    "job_insights": job_insights_tool,
    "save_job": save_job,
    "track_job": track_job,
    "get_saved_jobs": get_saved_jobs
}


def get_tool(tool_name):

    return TOOLS.get(tool_name)