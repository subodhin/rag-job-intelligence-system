
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def generate_skill_recommendations(target_role, analysis):

    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not configured")

    prompt = f"""
You are a senior AI engineering career coach.

Your task is to create a practical skill development plan
for someone targeting the following role.

TARGET ROLE:
{target_role}

USER'S EXISTING SKILLS:
{json.dumps(analysis.get("user_skills", []))}

HIGH PRIORITY SKILL GAPS:
{json.dumps(analysis.get("high_priority_gaps", []))}

MEDIUM PRIORITY SKILL GAPS:
{json.dumps(analysis.get("medium_priority_gaps", []))}

LOW PRIORITY SKILL GAPS:
{json.dumps(analysis.get("low_priority_gaps", []))}

JOB SAMPLE:
{analysis.get("total_jobs_analysed", 0)} jobs analysed.

IMPORTANT RULES:

1. Never recommend learning a skill the user already has.
2. Focus primarily on high-priority gaps.
3. Consider medium-priority gaps after addressing important foundations.
4. Do not overemphasize low-priority skills.
5. Recommend a maximum of 5 skills.
6. Keep the learning roadmap to a maximum of 6 steps.
7. Explain why each recommended skill matters in real AI engineering work.
8. Provide practical, achievable learning actions.
9. Build on the user's existing skills.
10. Suggest one project that combines existing skills with new skills.
11. Avoid unnecessary technologies and overly advanced tools.
12. Do not invent job market statistics.
13. Treat the job sample as limited evidence, not a complete representation
    of the job market.
14. If an observed gap is too broad (for example AI/ML), break it down
    into practical, specific learning topics.

RECOMMENDATION STYLE:

- Be specific.
- Be concise.
- Focus on production-level engineering skills.
- Prioritize skills that help the user build and deploy real AI applications.
- Do not generate generic advice.

Return ONLY valid JSON using this structure:

{{
    "summary": "Short personalized assessment",

    "top_recommendations": [
        {{
            "skill": "Docker",
            "priority": "medium",
            "reason": "Why this skill matters",
            "learning_action": "Specific practical action"
        }}
    ],

    "learning_roadmap": [
        {{
            "step": 1,
            "topic": "Topic",
            "goal": "Practical learning outcome"
        }}
    ],

    "project_idea": {{
        "title": "Project title",
        "description": "Project description",
        "technologies": ["Python", "FastAPI", "Docker"],
        "learning_outcomes": [
            "Learning outcome 1",
            "Learning outcome 2"
        ]
    }}
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
            "temperature": 0.2,
            "response_format": {
                "type": "json_object"
            }
        },
        timeout=30
    )

    response.raise_for_status()

    result = response.json()

    content = result["choices"][0]["message"]["content"]

    return json.loads(content)