from app.ai.groq_intent_detector import detect_intent_groq


def detect_intent(user_query: str):

    # Handle greetings without calling the LLM
    greetings = ["hi", "hello", "hey", "heyy"]

    if user_query.lower().strip() in greetings:
        return {
            "intent": "greeting",
            "message": "Hi! Ask me about jobs, salaries, or market insights."
        }

    try:
        intent_data = detect_intent_groq(user_query)

        print("Parsed Intent Data:", intent_data)

        return intent_data

    except Exception as e:
        print("Intent detection failed:", str(e))

        return {
            "intent": "unknown"
        }