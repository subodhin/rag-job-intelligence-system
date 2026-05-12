from app.services.data_service import generate_insights

def handle_insight_search(query: str):
    print("------ insight Agent!-----")

    generated_insights = generate_insights()

    return {
        "intent": "market_insights",
        "agent": "insight_agent",
        "results": generated_insights
    }