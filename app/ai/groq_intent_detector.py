import os
import json
from dotenv import load_dotenv
import requests

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def detect_intent_groq(query: str):

    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not configured")

    prompt = f"""
You are an intent classifier for an AI job assistant.

Classify the user query into exactly ONE of these intents:

job_search
market_insights
job_action

Examples:

Find Python developer jobs
job_search

Find remote AI Engineer jobs
job_search

Find jobs similar to AI Engineer
job_search

What skills are most in demand?
market_insights

What are the salary trends?
market_insights

Save this job
job_action

Bookmark this job
job_action

Mark this job as applied
job_action

Show my saved jobs
job_action

User query:
{query}

Return ONLY valid JSON:

{{
    "intent": "job_search"
}}
"""

    response = requests.post(
        GROQ_URL,
        headers={
            "Authorization": "Bearer {}".format(GROQ_API_KEY),
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-oss-20b",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0,
            "response_format": {
                "type": "json_object"
            }
        },
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    raw_response = data["choices"][0]["message"]["content"]

    print("Groq RAW RESPONSE::::::::::::")
    print(raw_response)

    result = json.loads(raw_response)

    intent = result.get("intent", "unknown")

    if intent not in [
        "job_search",
        "market_insights",
        "job_action"
    ]:
        return {
            "intent": "unknown"
        }

    return {
        "intent": intent
    }