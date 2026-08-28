from app.tools.tool_registry import get_tool


tool = get_tool("semantic_job_search")

print("Tool:", tool)
print("Tool Name:", tool.__name__)