from typing import TypedDict, List, Dict, Any

import requests

from langgraph.graph import StateGraph, START, END

from app.services.cv_embeddings import embed_query
from app.services.cv_vector_store import search_cv


class CVGraphState(TypedDict):
    cv_id: str
    query: str
    query_vector: List[float]
    results: List[Dict[str, Any]]
    answer: str


def embed_query_node(state: CVGraphState):

    print("\n========== LANGGRAPH: EMBED QUERY ==========")
    print("CV ID:", state["cv_id"])
    print("Query:", state["query"])

    vector = embed_query(state["query"])

    print("Vector generated")
    print("Vector length:", len(vector))

    return {
        "query_vector": vector
    }


def retrieve_cv_node(state: CVGraphState):

    print("\n========== LANGGRAPH: RETRIEVE CV ==========")
    print("CV ID:", state["cv_id"])
    print("Query vector length:", len(state["query_vector"]))

    results = search_cv(
        state["cv_id"],
        state["query_vector"],
        top_k=3
    )

    print("Results retrieved:", len(results))

    formatted_results = [
        {
            "text": result.payload["text"],
            "page": result.payload["page"],
            "chunk_index": result.payload["chunk_index"],
            "score": result.score
        }
        for result in results
    ]

    for result in formatted_results:
        print(
            "Chunk:",
            result["chunk_index"],
            "| Score:",
            result["score"]
        )

    return {
        "results": formatted_results
    }


def generate_answer_node(state: CVGraphState):

    print("\n========== LANGGRAPH: GENERATE ANSWER ==========")

    context = "\n\n".join(
        result["text"]
        for result in state["results"]
    )

    prompt = f"""
You are a CV assistant.

Answer the user's question using ONLY the CV context below.
If the CV does not contain enough information, say so.

CV CONTEXT:
{context}

QUESTION:
{state["query"]}

Give a concise, factual answer.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi",
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()

    answer = response.json()["response"]

    print("Answer generated")

    return {
        "answer": answer
    }


def build_cv_graph():

    print("\n========== BUILDING CV LANGGRAPH ==========")

    graph = StateGraph(CVGraphState)

    graph.add_node("embed_query", embed_query_node)
    graph.add_node("retrieve_cv", retrieve_cv_node)
    graph.add_node("generate_answer", generate_answer_node)

    graph.add_edge(START, "embed_query")
    graph.add_edge("embed_query", "retrieve_cv")
    graph.add_edge("retrieve_cv", "generate_answer")
    graph.add_edge("generate_answer", END)

    print(
        "Graph: START -> embed_query -> retrieve_cv -> generate_answer -> END"
    )

    return graph.compile()