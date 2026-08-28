import requests
from typer import prompt

#from app.config import OLLAMA_URL

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_tool_response(query: str, tool_name: str, tool_result):
    print("User query:::::::::::::::::::::::::::::::::", query)
    print("Tool name::::::::::::::::::::::::::::::::::", tool_name)
    print("Tool result::::::::::::::::::::::::::::::::", tool_result)

    prompt = f"""
You are an AI job assistant.

The user asked:
{query}

The system selected this tool:
{tool_name}

The tool returned this data:
{tool_result}

You are given the result of a Python tool.

The tool result is DATA, not something to describe.

Answer the user's question directly using that data.

DO NOT:
- mention the tool
- mention the tool result
- repeat the raw data
- explain your instructions
- invent information

If the data contains matching jobs, identify them using their exact
title, skills, salary, and location.

If the data does not contain enough information, say:
"The available job data does not provide enough information."
"""
    print("prompt sent to Phi for tool response generation::::::::::::::::::::::::::::::::::::", prompt)

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "phi",
            "prompt": prompt,
            "stream": False
        }
    )
    response.raise_for_status()

    data = response.json()
    print("Tool Response from Phi:>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    return data["response"]