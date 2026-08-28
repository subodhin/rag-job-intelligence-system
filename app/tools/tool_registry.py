from app.tools.job_tools import (
    search_jobs_tool,
    semantic_job_search_tool
)

from app.tools.insight_tools import (
    job_insights_tool
)


TOOLS = {
    "search_jobs": search_jobs_tool,
    "semantic_job_search": semantic_job_search_tool,
    "job_insights": job_insights_tool
}


def get_tool(tool_name):

    return TOOLS.get(tool_name)