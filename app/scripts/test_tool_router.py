from app.tools.tool_router import (
    select_tool,
    execute_tool
)

from app.services.agent_response_service import (
    generate_tool_response
)


query = "Find jobs similar to AI engineer with Python"

intent = "job_search"

tool_name = select_tool(
    intent,
    query
)

print("Selected Tool:", tool_name)

tool_result = execute_tool(
    tool_name,
    query
)

print("Tool Result:")
print(tool_result)

ai_response = generate_tool_response(
    query,
    tool_name,
    tool_result
)

print("\nAI Response:")
print(ai_response)