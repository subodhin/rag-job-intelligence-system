import os
import json
import requests

from dotenv import load_dotenv
from app.services.data_service import search_jobs_by_filters


load_dotenv()


GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def handle_job_search(query: str, user_context=None):

    print("------ Job Search Agent!-----")
    print("Agent Query:", query)
    print("Agent Context:", user_context)

    # ---------------------------------------
    # Extract persistent context
    # ---------------------------------------

    profile = user_context.get("profile", {}) if user_context else {}
    preferences = user_context.get("preferences", {}) if user_context else {}
    conversation = user_context.get("conversation", []) if user_context else []

    # Convert conversation into readable text
    conversation_text = "\n".join(
        f"{message.get('role', '').upper()}: {message.get('content', '')}"
        for message in conversation
    )

    # ---------------------------------------
    # Build context-aware planner prompt
    # ---------------------------------------

    prompt = f"""
You are a job-search query planner.

Your job is to convert the CURRENT USER QUERY into search filters.

You MUST use the user's profile, preferences, and previous
conversation when the current query is vague or is a follow-up.

USER PROFILE:
Target Role: {profile.get("target_role")}
Experience Level: {profile.get("experience_level")}
Skills: {profile.get("skills")}

USER PREFERENCES:
Remote Only: {preferences.get("remote_only")}
Preferred Locations: {preferences.get("preferred_locations")}
Preferred Skills: {preferences.get("preferred_skills")}

PREVIOUS CONVERSATION:
{conversation_text}

CURRENT USER QUERY:
{query}


IMPORTANT EXAMPLE:

Previous conversation:
USER: Find me remote AI Engineer jobs.

Current query:
Show me some jobs

The current query is a follow-up to the previous request.

Therefore the correct filters are:

{{
    "title": "AI Engineer",
    "skills": ["Python", "RAG"],
    "location": "remote"
}}


Now determine the filters for the ACTUAL current query.

Return ONLY a JSON OBJECT.

The JSON must have exactly these fields:

{{
    "title": null,
    "skills": [],
    "location": null
}}

Rules:

- If the current query is vague, use the previous conversation.
- Use the target role from the profile when appropriate.
- Use relevant preferred skills.
- If Remote Only is true, use "remote" as the location.
- A job role belongs in "title".
- Technical skills belong in "skills".
- Never return a JSON array.
- Never return [] as the entire response.
- Never return markdown.
- Never return an explanation.
"""

    # ---------------------------------------
    # Debug: show planner prompt
    # ---------------------------------------

    print("\n========== PLANNER PROMPT ==========")
    print(prompt)
    print("====================================\n")

    # ---------------------------------------
    # Call Groq
    # ---------------------------------------

    response = requests.post(
        GROQ_URL,
        headers={
            "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
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
            "temperature": 0
        },
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    # ---------------------------------------
    # Get raw Groq response
    # ---------------------------------------

    raw_response = data["choices"][0]["message"]["content"].strip()

    print("\nContext Query Planner RAW RESPONSE:>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(raw_response)

    # ---------------------------------------
    # Parse planner response
    # ---------------------------------------

    try:

        filters = json.loads(raw_response)

        # Planner must return a JSON object
        if not isinstance(filters, dict):

            print(
                "ERROR: Planner returned non-object JSON:",
                filters
            )

            filters = {
                "title": None,
                "skills": [],
                "location": None
            }

    except json.JSONDecodeError:

        print("ERROR: Could not parse planner response.")

        filters = {
            "title": None,
            "skills": [],
            "location": None
        }

    # ---------------------------------------
    # Debug derived filters
    # ---------------------------------------

    print("\nContext-derived filters:")
    print(filters)

    # ---------------------------------------
    # Search jobs
    # ---------------------------------------

    jobs = search_jobs_by_filters(filters)

    print(
        "\nContext-aware search results:",
        len(jobs)
    )

    # ---------------------------------------
    # Return agent response
    # ---------------------------------------

    return {
        "intent": "job_search",
        "agent": "search_agent",
        "filters": filters,
        "results": jobs
    }