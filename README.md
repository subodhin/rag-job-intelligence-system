
# AI Career Intelligence Platform

> Production-oriented AI backend for intelligent job discovery using LLM agents, RAG, semantic retrieval, vector databases, and persistent user context.

**Status:** Active Development  
**Core Architecture:** Implemented

---

## Overview

An end-to-end AI backend that converts natural-language career queries into personalized, grounded job results.

The system combines **LLM orchestration, AI agents, tool execution, RAG, semantic retrieval, Qdrant, and persistent user context**.

---

## What I Built

| Engineering Area | Key Implementation |
|:---|:---|
| **AI Agents** | Intent detection · routing · tool execution · multi-step workflows |
| **LLM Orchestration** | Groq for intent/planning · Ollama/Phi for local generation |
| **Context & Memory** | Persistent profiles · preferences · conversation history |
| **Multi-Turn AI** | Context-aware follow-up query handling |
| **Query Planning** | Natural language → structured search filters |
| **RAG** | Job retrieval → context construction → grounded generation |
| **Semantic Retrieval** | `nomic-embed-text` · 768-D embeddings · cosine similarity |
| **Vector Database** | FAISS → Qdrant migration · retrieval validation |
| **Job Search** | Structured · natural-language · semantic retrieval |
| **Career Insights** | Skill and salary analysis |
| **Backend** | Python · FastAPI · Pydantic · modular services |
| **Data Integration** | External job APIs · normalized job data |

---

## Architecture

**Core architecture implemented**

```text
                         User Query
                              |
                              v
                         FastAPI API
                              |
                              v
                    Intent Detection
                         (Groq)
                              |
                              v
                        AI Agent
                              |
                 +------------+------------+
                 |            |            |
              Profile     Preferences  Conversation
                 +------------+------------+
                              |
                              v
                  Context-Aware Planner
                              |
                              v
                     Structured Filters
                              |
                    +---------+---------+
                    |                   |
                    v                   v
              Filter Search       Semantic Search
                                        |
                                        v
                                      Qdrant
                                        |
                                        v
                                    Top-K Jobs
                                        |
                                        v
                                       RAG
                                        |
                                        v
                                    Local LLM
                                        |
                                        v
                                  AI Response
````

---

## Context-Aware Search

The agent combines the current query with persistent user context:

```text
Current Query
     +
User Profile
     +
Preferences
     +
Conversation History
     |
     v
Context-Aware Planner
     |
     v
Structured Search Filters
```

Example:

```text
User: Find me remote AI Engineer jobs.

User: Show me some jobs.
```

The system can derive:

```json
{
  "title": "AI Engineer",
  "skills": ["Python", "RAG"],
  "location": "remote"
}
```

This allows follow-up queries to remain personalized without requiring the user to repeat previous requirements.

---

## Retrieval Pipeline

```text
Query
  |
Embedding
  |
Qdrant
  |
Top-K Jobs
  |
RAG Context
  |
LLM
  |
Grounded Response
```

| Component          | Configuration      |
| :----------------- | :----------------- |
| Embedding Model    | `nomic-embed-text` |
| Vector Dimension   | 768                |
| Similarity         | Cosine             |
| Vector Database    | Qdrant             |
| Previous Retrieval | FAISS              |

---

## Tech Stack

| Layer               | Technology                                |
| :------------------ | :---------------------------------------- |
| **Backend**         | Python · FastAPI · Uvicorn · Pydantic     |
| **LLMs**            | Groq · Ollama · Phi                       |
| **Agents**          | Intent Detection · Routing · Tool Calling |
| **RAG**             | Retrieval-Augmented Generation            |
| **Embeddings**      | `nomic-embed-text`                        |
| **Vector DB**       | Qdrant                                    |
| **Search**          | Structured · Semantic Search              |
| **Infrastructure**  | Docker                                    |
| **Version Control** | Git · GitHub                              |

---

## Current Capabilities

| Capability                        |  Status  |
| :-------------------------------- | :------: |
| FastAPI backend                   | Complete |
| Natural-language job search       | Complete |
| LLM intent detection              | Complete |
| AI agent routing                  | Complete |
| Tool execution                    | Complete |
| RAG pipeline                      | Complete |
| Semantic retrieval                | Complete |
| FAISS → Qdrant migration          | Complete |
| Persistent user context           | Complete |
| Context-aware query planning      | Complete |
| Profile & preference-aware search | Complete |
| Multi-turn interaction            | Complete |
| Job relevance ranking             | Complete |
| External job API integration      | Complete |

---

## Testing

```bash
# Start API
uvicorn app.main:app --reload

# Test Qdrant collection
python3 -m app.scripts.test_qdrant_collection

# Test semantic retrieval
python3 -m app.scripts.test_qdrant_semantic_search

# Compare FAISS and Qdrant
python3 -m app.scripts.compare_faiss_qdrant

# Test agent + tools
python3 -m app.scripts.test_tool_router

# Inspect persistent user context
python3 -c "from app.context.context_service import get_user_context, print_user_context; print_user_context(get_user_context('user_002'))"
```

### API

```text
POST /ai-agent
POST /ai-agent-context
POST /search
POST /search-ai
POST /insights
```

Swagger:

```text
http://localhost:8000/docs
```

---

## Project Structure

```text
ai-job-assistant/
├── app/
│   ├── ai/
│   ├── agents/
│   ├── context/
│   ├── embedding_functions/
│   ├── services/
│   ├── tools/
│   └── scripts/
├── data/
└── README.md
```

---

## What's Next

| Area                    | Planned Capability                                 |
| :---------------------- | :------------------------------------------------- |
| **Job Sources**         | Multiple job-board APIs                            |
| **Job Actions**         | Save · track · retrieve jobs                       |
| **Job Links**           | Direct job-post URLs                               |
| **Career Intelligence** | Resume matching · skill-gap analysis               |
| **Personalization**     | Advanced ranking · recommendations                 |
| **Dashboard**           | Applications · saved jobs · skill gaps · analytics |
| **Data Layer**          | PostgreSQL                                         |
| **AI Infrastructure**   | Hybrid retrieval · MCP                             |
| **Production**          | Deployment · monitoring · observability            |

---

## Engineering Focus

**LLM Orchestration · AI Agents · Tool Calling · RAG · Semantic Retrieval · Vector Databases · Persistent Context · FastAPI · AI Backend Architecture**

---

## Direction

```text
Job Discovery
      |
Intelligent Search
      |
Context-Aware AI
      |
Job Actions & Tracking
      |
Career Intelligence
```

> Building toward a personalized Career Intelligence Platform.

