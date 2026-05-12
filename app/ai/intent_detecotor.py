import json
import requests

from app.prompts import INTENT_PROMPT

OLLAMA_URL = "http://localhost:11434/api/generate"


def detect_intent(user_query: str):



# Handle simple greeting queries without triggering expensive LLM workflows  
    greetings = ["hi", "hello", "hey", "heyy"]

    if user_query.lower().strip() in greetings:

        return {
            "intent": "greeting",
            "message": "Hi! Ask me about jobs, salaries, or market insights."
        }

    prompt = f"""
    {INTENT_PROMPT}

    User Query:
    {user_query}
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "phi",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    try:

        raw_response = data["response"]

        print("RAW RESPONSE::::")
        print(raw_response)

        cleaned_response = raw_response.replace("```json", "")
        cleaned_response = cleaned_response.replace("```", "")

        # Remove triple quotes
        cleaned_response = cleaned_response.replace('"""', '"')

        # Remove trailing commas
        cleaned_response = cleaned_response.replace(",}", "}")

        # Extract only JSON part
        json_end = cleaned_response.find("}") + 1
        cleaned_response = cleaned_response[:json_end]

        # Trim spaces
        cleaned_response = cleaned_response.strip()

        print("CLEANED RESPONSE::::")
        print(cleaned_response)

        intent_data = json.loads(cleaned_response)

        print("Parsed Intent Data::::", intent_data)

        return intent_data

    except Exception as e:

        print("JSON Decode Error::::", e)

        return {
            "intent": "unknown"
        }