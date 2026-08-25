from fastapi import FastAPI, HTTPException
import requests

from app.prompts import SYSTEM_PROMPT
from app.models.schemas import AskRequest
from app.services import semantic_search_service
from app.services.data_service import (
    load_jobs,
    search_jobs,
    format_jobs_context,
    search_jobs_by_filters,
    generate_insights
)
from app.services.query_parser import parse_query
from app.models.schemas import AskRequest
from app.ai.intent_detecotor import detect_intent
from app.services.router_service import route_request

app = FastAPI(
    swagger_ui_parameters={
        "syntaxHighlight.theme": "obsidian"
    }
)
OLLAMA_URL = "http://localhost:11434/api/generate"


@app.get("/")
def home():
    return {
        "message": "AI Job Assistant Running!"
    }


@app.post("/ask")
def ask(request: AskRequest):

    query = request.query.lower()
    job_keywords = [
        "job",
        "salary",
        "skills",
        "developer",
        "python",
        "react",
        "backend",
        "frontend"
    ]

    if not any(word in query for word in job_keywords):

        raise HTTPException(
            status_code=400,
            detail="Only job-related queries are allowed."
        )

    full_prompt = f"""
    {SYSTEM_PROMPT}


    User Question:
    {request.query}
    """

    print("Your Query:::::", request.query)

    try:
      # print("Query sent:::::")
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "phi",
                "prompt": full_prompt,
                "stream": False
            }
            
        )
       

        data = response.json()
        print("Response received:::::", data["response"])

        return {
            "response": data["response"]
        }

    except Exception as e:
        print("Exception occurred:::::", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/jobs")
def get_jobs():
    #TEST API for raw data jobs  

    jobs = load_jobs()

    return jobs


#straight map form external API 
@app.get("/search")
def search(skill: str):

    results = search_jobs(skill)

    return {
        "results": results
    }

#external ai job listing based on that AI responses with resources used
@app.post("/search-ai")
def search_ai(request: AskRequest):

    query = request.query

    filters = parse_query(query)

    print("Parsed Filters:")
    print("filters:::::",filters)

    matched_jobs = search_jobs_by_filters(filters)

    context = format_jobs_context(matched_jobs)

    print("Formatted Context::::::")
    print(context)

    full_prompt = f"""
    {SYSTEM_PROMPT}

    Relevant Job Data:
    {context}

    User Question:
    {query}
    """
    print("Full Prompt Sent to AI::::::",full_prompt)
    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "phi",
                "prompt": full_prompt,
                "stream": False
            }
        )

        data = response.json()
        print("AI Response::::::::::::::", data["response"])
        return {
            "filters": filters,
            "matched_jobs": matched_jobs,
            "ai_response": data["response"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@app.get("/parse-query")
def parse(query: str):

    print("Parsing Query:::::", query)

    filters = parse_query(query)
    print  ("Parsed Filters:::::", filters)

    return filters
#current market(average salary insights)
@app.get("/insights")
def insights():

    data = generate_insights()

    return data


@app.post("/intent")
async def classify_intent(query: AskRequest):

    print("Classifying Intent for Query:::::", query.query)
    result = detect_intent(query.query)

    print("Detected Intent:::::", result)

    return result


# choose agent flows based on intent
@app.post("/ai-agent")
async def ai_agent(request: AskRequest):

    print(":::::::::::::::::::/ai-agent:::::::::::::::::")
    print("User input ::::", request)

    intent_result = detect_intent(request.query)

    print("::::::::::::::::::::::intent:::::::::::::::::::",intent_result)

    response = route_request(
        intent_result["intent"],
        request.query
    )

    

    return response

@app.post("/semantic-search")
def semantic_search(request: AskRequest):
    print("Semantic Search Query:::::", request.query)
    #results = semantic_search_service.semantic_search(query=request.query,top_k=request.top_k)
    results = semantic_search_service.semantic_search(
    query=request.query,
    top_k=3
)
    return {"results": results}

