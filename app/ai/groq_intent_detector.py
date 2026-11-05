import os
import json
import requests

from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

VALID_INTENTS = [
    "job_search",
    "market_insights",
    "skill_gap_analysis",
    "job_action"
]


def detect_intent_groq(query: str):

    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not configured")

    prompt = f"""
You are an intent classifier for an AI job assistant.

Classify the user query into exactly ONE of these intents:

1. job_search
   Find jobs, search for job opportunities, or filter jobs.

2. market_insights
   Analyse general job market trends, salary trends, and
   in-demand skills across the job market.

3. skill_gap_analysis
   Analyse the user's skills, identify missing skills,
   compare their profile against a target role, or
   recommend skills they should improve or learn.

4. job_action
   Save, bookmark, apply, or manage existing jobs.

EXAMPLES:

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

Which technologies are trending in the job market?
market_insights

Analyse my skill gaps
skill_gap_analysis

What skills am I missing for AI Engineer roles?
skill_gap_analysis

Compare my skills against AI Engineer requirements
skill_gap_analysis

What should I learn to become an AI Engineer?
skill_gap_analysis

How can I improve my profile for AI Engineer jobs?
skill_gap_analysis

Save this job
job_action

Bookmark this job
job_action

Mark this job as applied
job_action

Show my saved jobs
job_action

CLASSIFICATION RULES:

- Personal skill assessment belongs to skill_gap_analysis.
- General market trends belong to market_insights.
- Finding job opportunities belongs to job_search.
- Managing saved or applied jobs belongs to job_action.
- Return exactly one intent.
- Do not provide explanations.

USER QUERY:
{query}

Return ONLY valid JSON:

{{
    "intent": "job_search"
}}
"""

    response = requests.post(
        GROQ_URL,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
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

    if intent not in VALID_INTENTS:
        return {
            "intent": "unknown"
        }

    return {
        "intent": intent
    }