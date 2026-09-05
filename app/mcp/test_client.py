import asyncio
import os

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# Configure MCP server process 
server_params = StdioServerParameters(
    command="python",
    args=["-m", "app.mcp.server"],
    cwd=os.getcwd(),
)


async def main():

    # Connect to MCP server 
    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            # ---------------------------------------------------------
            # 1. Initialize MCP connection.
            # ---------------------------------------------------------

            await session.initialize()

            # ---------------------------------------------------------
            # 2. Discover available MCP tools
            # ---------------------------------------------------------

            tools = await session.list_tools()

            print("AVAILABLE TOOLS:")

            for tool in tools.tools:
                print("-", tool.name)

            # ---------------------------------------------------------
            # 3. Get saved jobs
            # ---------------------------------------------------------

            result = await session.call_tool(
                "get_saved_jobs_mcp",
                arguments={
                    "user_id": "user_002"
                }
            )

            print("\nGET SAVED JOBS RESULT:")
            print(result)

            # ---------------------------------------------------------
            # 4. Save a test job
            # ---------------------------------------------------------

            save_result = await session.call_tool(
                "save_job_mcp",
                arguments={
                    "user_id": "user_002",
                    "job": {
                        "id": "9999999",
                        "title": "MCP Test AI Engineer",
                        "job_url": "https://example.com/mcp-test-job"
                    }
                }
            )

            print("\nSAVE JOB RESULT:")
            print(save_result)

            # ---------------------------------------------------------
            # 5. Track the test job
            # ---------------------------------------------------------

            track_result = await session.call_tool(
                "track_job_mcp",
                arguments={
                    "user_id": "user_002",
                    "job_id": "9999999",
                    "status": "applied"
                }
            )

            print("\nTRACK JOB RESULT:")
            print(track_result)

            # ---------------------------------------------------------
            # 6. Structured job search
            # ---------------------------------------------------------

            search_result = await session.call_tool(
                "search_jobs_mcp",
                arguments={
                    "filters": {
                        "title": "AI Engineer"
                    }
                }
            )

            print("\nSTRUCTURED SEARCH RESULT:")
            print(search_result)

            # ---------------------------------------------------------
            # 7. Semantic job search
            # ---------------------------------------------------------

            semantic_result = await session.call_tool(
                "semantic_job_search_mcp",
                arguments={
                    "query": "AI engineer with Python and RAG experience",
                    "top_k": 3
                }
            )

            print("\nSEMANTIC SEARCH RESULT:")
            print(semantic_result)

            # ---------------------------------------------------------
            # 8. End-to-End MCP Workflow
            # ---------------------------------------------------------

            print("\nEND-TO-END MCP WORKFLOW:")

            # Step 1: Search for AI Engineer jobs
            workflow_search_result = await session.call_tool(
                "search_jobs_mcp",
                arguments={
                    "filters": {
                        "title": "AI Engineer"
                    }
                }
            )

            print("1. Job search completed")

            # Step 2: Select a job from the search results
            selected_job = {
                "id": "1919266",
                "title": "Senior Independent AI Engineer / Architect",
                "job_url": (
                    "https://remotive.com/remote-jobs/"
                    "software-development/"
                    "senior-independent-ai-engineer-architect-1919266"
                )
            }

            print(
                "2. Job selected:",
                selected_job["title"]
            )

            # Step 3: Save the selected job
            workflow_save_result = await session.call_tool(
                "save_job_mcp",
                arguments={
                    "user_id": "user_002",
                    "job": selected_job
                }
            )

            print("3. Job saved")

            # Step 4: Track the job as applied
            workflow_track_result = await session.call_tool(
                "track_job_mcp",
                arguments={
                    "user_id": "user_002",
                    "job_id": selected_job["id"],
                    "status": "applied"
                }
            )

            print("4. Job marked as applied")

            # Step 5: Retrieve saved jobs
            workflow_saved_result = await session.call_tool(
                "get_saved_jobs_mcp",
                arguments={
                    "user_id": "user_002"
                }
            )

            print("5. Saved jobs retrieved")

            # Step 6: Display final workflow result
            print("\nFINAL WORKFLOW RESULT:")
            print(workflow_saved_result)

            print("\nEND-TO-END MCP WORKFLOW COMPLETED")


if __name__ == "__main__":
    asyncio.run(main())