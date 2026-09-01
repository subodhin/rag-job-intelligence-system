from fastapi import FastAPI, HTTPException
from opentelemetry import context
import requests
import time

# from app import rag_prompt
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

from app.services.semantic_search_service import semantic_search
from app.services.rag_service import check_required_skills
from app.tools.tool_router import select_tool, execute_tool

from app.context.router import router as context_router

from app.models.schemas import ContextAgentRequest
from app.models.schemas import AskRequest
from app.models.schemas import ContextAgentRequest
from app.context.context_service import get_user_context, print_user_context,save_message
from app.ai.groq_intent_detector import detect_intent_groq
from fastapi.responses import RedirectResponse
from app.tools.job_tools import record_job_event
from app.services.external_jobs import get_jobs as get_external_jobs
import json

app = FastAPI(
    swagger_ui_parameters={
        "syntaxHighlight.theme": "obsidian"
    }
)
app.include_router(context_router)

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

@app.get("/jobs/{job_id}/apply")
def apply_to_job(job_id: int, user_id: str):

    jobs = get_external_jobs()

    job = next(
        (job for job in jobs if job.get("id") == job_id),
        None
    )

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    record_job_event(
        user_id,
        job_id,
        "apply_clicked"
    )

    return RedirectResponse(
        url=job["job_url"]
    )


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
    print("filters:::::::::::::",filters)

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
    # response = route_request(
#     intent_result["intent"],
#     request.query,
#     user_context
# )

    

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


#
@app.post("/rag-v2")
def rag_v2(request: AskRequest):
    

    query = request.query

    # --------------------------------------------------
    # 1. Parse user query
    # --------------------------------------------------
    filters = parse_query(query)

    print("Parsed Filters:")
    print(filters)

    # --------------------------------------------------
    # 2. Semantic retrieval using FAISS
    # --------------------------------------------------
    retrieved_results = semantic_search_service.semantic_search(
        query=query,
        top_k=3
    )

    print("Retrieved Results:")
    print(retrieved_results)

    # --------------------------------------------------
    # 3. Extract jobs from FAISS results
    # --------------------------------------------------
    retrieved_jobs = [
        result["job"]
        for result in retrieved_results
    ]

    # --------------------------------------------------
    # 4. Get required skills dynamically
    # --------------------------------------------------
    required_skills = filters.get("skills") or []

    # Support your existing parser which currently
    # returns a single "skill" field
    if not required_skills and filters.get("skill"):
        required_skills = [filters["skill"]]

    print("Required Skills:")
    print(required_skills)

    # --------------------------------------------------
    # 5. Validate retrieved jobs using Python
    # --------------------------------------------------
    validated_jobs = check_required_skills(
        retrieved_jobs,
        required_skills
    )

    print("Validated Jobs:")
    print(validated_jobs)

    # --------------------------------------------------
    # 6. Add validation information to context
    # --------------------------------------------------
    context_jobs = []

    for item in validated_jobs:

        job = item["job"]

        context_jobs.append({
            **job,
            "matched_skills": item["matched_skills"],
            "missing_skills": item["missing_skills"]
        })

    # --------------------------------------------------
    # 7. Format context for Phi
    # --------------------------------------------------
    context = format_jobs_context(context_jobs)

    print("RAG Context:")
    print(context)

    # --------------------------------------------------
    # 8. Build grounded prompt
    # --------------------------------------------------
    rag_prompt = f"""
You are a job search assistant.

Use ONLY the information inside JOB DATA.

JOB DATA:
{context}

QUESTION:
{query}

Rules:
- Do not use outside knowledge.
- Do not invent information.
- Do not rename job titles.
- Do not change salary or location.
- Do not claim a skill unless it appears in JOB DATA.
- If a requested skill is missing, say that it is not specified.
- If no job clearly matches, say so.

Answer the question using only the JOB DATA.
"""

    print("Prompt Sent to Phi:")
    print(rag_prompt)
    # --------------------------------------------------
    # 9. Send prompt to Phi + measure LLM latency
    # --------------------------------------------------
    try:

        start_time = time.perf_counter()

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "phi",
                "prompt": rag_prompt,
                "stream": False
            }
        )

        llm_response_time = time.perf_counter() - start_time

        response.raise_for_status()

        data = response.json()

        ai_response = data["response"]

        print("Phi Response:")
        print(ai_response)

        print(
            f"Phi response time: "
            f"{llm_response_time:.2f} seconds"
        )

        # --------------------------------------------------
        # 10. Return final RAG response
        # --------------------------------------------------
        return {
            "query": query,
            "filters": filters,
            "retrieved_jobs": retrieved_results,
            "validated_jobs": validated_jobs,
            "ai_response": ai_response,
            "llm_response_time_seconds": round(
                llm_response_time, 2
            )
        }

    except requests.exceptions.RequestException as e:

        raise HTTPException(
            status_code=500,
            detail=f"LLM request failed: {str(e)}"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.post("/agent")
def agent(request: AskRequest):

    print("Agent Query:::::", request.query)

    query = request.query

    # 1. Detect intent
    intent = detect_intent(query)

    print("User Query:", query)
    print("Detected Intent::::::::::::::::::::::::::::::::::::::::::::::::::::", intent)

    # 2. Select tool
    tool_name = select_tool(
        intent,
        query
    )

    print("Selected Tool::::::::::::::::::::::::::::::::::::::::::", tool_name)

    # 3. Execute tool
    if tool_name:

        tool_result = execute_tool(
            tool_name,
            query
        )

    else:

        tool_result = {
            "message": "No suitable tool found."
        }

    print("Tool Result::::::::::::::::::::::::::::::::::::::::::::::::::::", tool_result)

    # 4. Return orchestration result
    return {
        "query": query,
        "intent": intent,
        "tool": tool_name,
        "tool_result": tool_result
    }


@app.post("/ai-agent-context")
async def ai_agent_context(request: ContextAgentRequest):

    print(":::::::::::::::::::/ai-agent-context:::::::::::::::::")
    print("User ID:", request.user_id)
    print("User Query:", request.query)

    # ---------------------------------------
    # Load existing persistent user context
    # ---------------------------------------

    user_context = get_user_context(request.user_id)

    if user_context is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    print("User Context:::::::::::::::::", user_context)

    # ---------------------------------------
    # Detect intent
    # ---------------------------------------

    intent_result = detect_intent_groq(request.query)

    print(
        "Detected Intent:::::::::::::::::",
        intent_result
    )

    # ---------------------------------------
    # Route request to agent
    # ---------------------------------------

    response = route_request(
        intent_result["intent"],
        request.query,
        user_context
    )

    # ---------------------------------------
    # Save current user message
    # ---------------------------------------

    save_message(
        user_id=request.user_id,
        role="user",
        content=request.query
    )

    # ---------------------------------------
    # Save assistant response
    # ---------------------------------------

    save_message(
        user_id=request.user_id,
        role="assistant",
        content=json.dumps(response)
    )

    # ---------------------------------------
    # Return response
    # ---------------------------------------

    print_user_context(
        get_user_context(request.user_id)
    )

    return {
        "user_id": request.user_id,
        "context": user_context,
        "intent": intent_result,
        "response": response
    }