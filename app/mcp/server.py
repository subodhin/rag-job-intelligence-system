import asyncio

from mcp.server.mcpserver import MCPServer
from app.tools.job_tools import (
    get_saved_jobs,
    save_job,
    track_job,
    search_jobs_tool,
    semantic_job_search_tool
)

# Create MCP server
server = MCPServer(name="AI Job Assistant")


# Expose get saved jobs through MCP
@server.tool()
async def get_saved_jobs_mcp(user_id: str) -> list:
    """Get all saved jobs for a user."""
    return get_saved_jobs(user_id)


# Expose save job through MCP
@server.tool()
async def save_job_mcp(user_id: str, job: dict) -> dict:
    """Save a job for a user."""
    return save_job(user_id, job)


# Expose track job through MCP
@server.tool()
async def track_job_mcp(
    user_id: str,
    job_id: str,
    status: str
) -> dict:
    """Update the tracking status of a job."""
    return track_job(user_id, job_id, status)

@server.tool()
async def search_jobs_mcp(filters: dict) -> list:
    """Search jobs using structured filters."""
    return search_jobs_tool(filters)


@server.tool()
async def semantic_job_search_mcp(
    query: str,
    top_k: int = 3
) -> list:
    """Search jobs using semantic similarity."""
    return semantic_job_search_tool(query, top_k)


# Start MCP server using stdio
async def main():
    await server.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())