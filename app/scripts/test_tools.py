from app.tools.job_tools import semantic_job_search_tool

result = semantic_job_search_tool(
    "AI engineer with Python",
    top_k=3
)

print(result)