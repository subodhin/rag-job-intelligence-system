# AI Career Intelligence Platform

> A production-oriented AI backend for intelligent job discovery, semantic retrieval, market intelligence, and AI-powered career workflows.

**Status:** 🚧 Active Development

## Overview

The **AI Career Intelligence Platform** is an AI backend designed to reduce the manual effort involved in discovering, evaluating, and managing career opportunities.

The system combines **LLMs, agent routing, tool execution, RAG, embeddings, semantic search, and vector databases** to transform natural-language career queries into grounded, actionable responses.

The current implementation focuses on the core AI infrastructure required to evolve the system toward a larger career intelligence platform.

---

## Problem

Modern job searching is fragmented and highly manual.

Users often need to:

- Search across different job sources
- Repeat similar searches with different keywords
- Evaluate job relevance manually
- Compare skills and requirements
- Analyze salary and market information
- Determine which opportunities best match their goals
- Track and manage opportunities

Traditional keyword search also struggles when the user's wording differs from the terminology used in a job description.

### Approach

The platform introduces an AI-driven retrieval and workflow layer:

```text
Natural Language Query
        |
        v
    AI Agent
        |
        v
 Intent Detection
        |
        v
   Tool Routing
        |
        v
 Semantic Retrieval
        |
        v
    Embeddings
        |
        v
    Qdrant
        |
        v
 Relevant Job Data
        |
        v
    RAG Context
        |
        v
       LLM
        |
        v
 Grounded Response
```

The architecture is designed to progressively support personalization, career analysis, recommendations, and automated job workflows.

---

# Current Architecture

```text
                             User
                              |
                              v
                       FastAPI REST API
                              |
                              v
                        AI Agent Layer
                              |
                    +---------+---------+
                    |                   |
                    v                   v
              Intent Detection      Tool Router
                    |                   |
                    +---------+---------+
                              |
                              v
                        Job Search Tool
                              |
                              v
                       Semantic Search
                              |
                              v
                      nomic-embed-text
                              |
                              v
                    768-Dimensional Vector
                              |
                              v
                           Qdrant
                      Vector Database
                              |
                              v
                         Top-K Jobs
                              |
                              v
                         RAG Context
                              |
                              v
                            Phi
                              |
                              v
                       AI Response
```

---

# AI Agent Workflow

The system separates **reasoning, routing, retrieval, and generation** into independent components.

```text
User Query
    |
    v
Intent Detection
    |
    v
Tool Router
    |
    +----------------------+
    |                      |
    v                      v
Job Search            Market Insights
    |
    v
Semantic Retrieval
    |
    v
Qdrant
    |
    v
Retrieved Job Data
    |
    v
RAG Context
    |
    v
   Phi
    |
    v
Grounded Response
```

This modular structure allows additional tools and workflows to be introduced without tightly coupling them to the API layer.

---

# Semantic Retrieval

The platform uses **`nomic-embed-text`** to transform job descriptions and user queries into 768-dimensional vector representations.

```text
Job Description / User Query
            |
            v
     nomic-embed-text
            |
            v
   768-Dimensional Vector
            |
            v
          Qdrant
            |
            v
    Cosine Similarity
            |
            v
       Top-K Results
```

Example:

```text
Find jobs similar to AI engineer with Python
```

The query is embedded and compared against stored job embeddings to retrieve semantically relevant opportunities.

---

# Vector Database Migration

The project originally used **FAISS** as the vector retrieval layer.

The system has been migrated to **Qdrant**, while the FAISS implementation is retained as a retrieval baseline for validation.

### Previous

```text
nomic-embed-text
        |
        v
      FAISS
        |
        v
  Job Metadata
```

### Current

```text
nomic-embed-text
        |
        v
      Qdrant
        |
        +---- Vector
        |
        +---- Job Payload
```

### Current Configuration

```text
Collection:        jobs
Vector Dimension:  768
Distance:          COSINE
Stored Vectors:    19
```

The migration was validated by running identical queries through both FAISS and Qdrant.

Across the tested queries, both systems produced matching top-K rankings with near-identical similarity scores.

This provides a practical validation that the vector storage migration preserved retrieval behavior.

---

# RAG Pipeline

The retrieval layer is integrated with the local LLM to create a grounded response pipeline.

```text
User Query
    |
    v
Query Embedding
    |
    v
Qdrant Retrieval
    |
    v
Top-K Jobs
    |
    v
Context Construction
    |
    v
Phi
    |
    v
Grounded AI Response
```

The LLM receives retrieved job information as context and is instructed to base its response on the available data rather than inventing job details.

---

# Current Capabilities

### AI & LLM

- Local LLM inference with Ollama
- Phi integration
- Prompt engineering
- Structured LLM responses
- Intent detection
- AI agent routing
- Tool-based AI workflows
- RAG
- Context grounding

### Retrieval & Search

- Natural-language search
- Query parsing
- Text embeddings
- `nomic-embed-text`
- 768-dimensional vectors
- Semantic retrieval
- Cosine similarity
- FAISS vector search
- Qdrant vector database
- FAISS → Qdrant migration
- Retrieval validation

### Backend

- Python
- FastAPI
- REST APIs
- Async API processing
- Pydantic validation
- External API integration
- Modular service architecture
- Error handling
- Response sanitization
- Swagger / OpenAPI

### Infrastructure & Engineering

- Docker
- Local AI infrastructure
- Local vector database
- Git / GitHub
- Python virtual environments
- Component-level testing
- Retrieval comparison testing

---

# Technology Stack

| Layer | Technology |
|---|---|
| Language | Python |
| API Framework | FastAPI |
| API Server | Uvicorn |
| LLM Runtime | Ollama |
| Local LLM | Phi |
| Embedding Model | `nomic-embed-text` |
| Vector Database | Qdrant |
| Vector Similarity | Cosine Similarity |
| Previous Vector Engine | FAISS |
| Data Validation | Pydantic |
| External Data | REST APIs |
| API Documentation | Swagger / OpenAPI |
| Infrastructure | Docker |
| Version Control | Git / GitHub |

---

# Engineering Focus

This project is intentionally built around **real AI system components rather than a single LLM API call**.

```text
                    AI Application
                         |
        +----------------+----------------+
        |                |                |
        v                v                v
      Agents          Retrieval          APIs
        |                |                |
        v                v                v
 Intent / Tools      Embeddings        FastAPI
 Routing             Vector DB         Pydantic
        |                |                |
        +----------------+----------------+
                         |
                         v
                         RAG
                         |
                         v
                        LLM
```

Key engineering areas demonstrated:

- LLM application architecture
- Retrieval-Augmented Generation
- Semantic retrieval
- Vector database integration
- Agent/tool architecture
- Backend API engineering
- Local AI infrastructure
- Retrieval evaluation
- Incremental system migration

---

# Validation & Testing

The project includes dedicated scripts for validating individual components and complete AI workflows.

### Qdrant Collection

```bash
python3 -m app.scripts.test_qdrant_collection
```

### Qdrant Semantic Search

```bash
python3 -m app.scripts.test_qdrant_semantic_search
```

### FAISS vs Qdrant

```bash
python3 -m app.scripts.compare_faiss_qdrant
```

### Agent + Tools + Phi

```bash
python3 -m app.scripts.test_tool_router
```

Validation currently covers:

- Qdrant connectivity
- Collection configuration
- Vector migration
- Semantic retrieval
- FAISS vs Qdrant consistency
- Tool routing
- Tool execution
- RAG retrieval
- LLM response generation

---

# Infrastructure

Qdrant currently runs locally using Docker.

```bash
docker run -d \
  --name qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  qdrant/qdrant
```

Qdrant Dashboard:

```text
http://localhost:6333/dashboard
```

The application communicates with the local Qdrant instance through its HTTP API.

---

# Project Structure

```text
ai-job-assistant/
|
+-- app/
|   |
|   +-- ai/
|   |   +-- intent_detecotor.py
|   |
|   +-- embedding_functions/
|   |   +-- create_job_embedding.py
|   |
|   +-- services/
|   |   +-- data_service.py
|   |   +-- external_jobs.py
|   |   +-- vector_service.py
|   |   +-- qdrant_service.py
|   |   +-- agent_response_service.py
|   |
|   +-- tools/
|   |   +-- tool_router.py
|   |   +-- ...
|   |
|   +-- scripts/
|       +-- build_job_index.py
|       +-- migrate_to_qdrant.py
|       +-- test_qdrant_collection.py
|       +-- test_qdrant_semantic_search.py
|       +-- compare_faiss_qdrant.py
|       +-- ...
|
+-- data/
|   +-- jobs.index
|   +-- job_metadata.json
|   +-- qdrant/
|
+-- venv/
|
+-- README.md
```

---

# Upcoming Work

The next stages focus on extending the retrieval system into a more complete career intelligence platform.

### Context & Personalization

- Persistent user profiles
- User preferences
- Conversation context
- Context-aware AI responses

### Career Intelligence

- Resume parsing
- Resume-to-job matching
- Skill-gap analysis
- Personalized job ranking
- Career recommendations

### AI Workflows

- Save jobs
- Track jobs
- Retrieve saved opportunities
- Multi-step AI workflows
- Automated job actions

### Retrieval & AI Infrastructure

- Hybrid retrieval
- Advanced RAG
- Retrieval evaluation
- Improved grounding
- Multi-agent workflows
- MCP integration

### Platform

- PostgreSQL integration
- Multi-source job aggregation
- Career analytics
- React / Next.js dashboard
- CSV / Excel export
- Production deployment
- Observability and monitoring

---

# Long-Term Vision

The goal is to evolve the system from an AI-powered job search assistant into a **Career Intelligence Platform**.

```text
                     Career Intelligence
                             |
          +------------------+------------------+
          |                  |                  |
          v                  v                  v
    Job Discovery      Career Analysis     Automation
          |                  |                  |
          v                  v                  v
   Semantic Search      Resume Analysis      Job Tracking
   Market Insights      Skill Analysis       AI Actions
   Recommendations      Job Matching          Workflows
          |                  |                  |
          +------------------+------------------+
                             |
                             v
                       AI Agent Layer
                             |
                             v
                        RAG + LLMs
```

The platform will progressively combine:

- Large Language Models
- Retrieval-Augmented Generation
- Semantic Search
- Embeddings
- Vector Databases
- AI Agents
- Recommendation Systems
- Career Analytics
- Workflow Automation

to reduce the manual effort involved in discovering, evaluating, and managing career opportunities.

---

# Development Philosophy

The project is developed incrementally, with each stage introducing a new system capability while preserving previous implementations for comparison and validation.

The objective is not simply to demonstrate that an LLM can generate text.

The objective is to build an **end-to-end AI system** with:

```text
Data
  |
Retrieval
  |
Reasoning
  |
Tools
  |
Context
  |
Generation
  |
Validation
```

while progressively moving toward a production-style architecture.

---

# Author

**Subodhi Nanayakkara**

Software Engineer with 6+ years of experience, currently specializing in the transition toward **AI Engineering** through hands-on development of production-oriented AI systems.

Focus areas:

- Large Language Models
- Retrieval-Augmented Generation
- Semantic Search
- Embeddings
- Vector Databases
- AI Agents
- Tool-based AI Workflows
- Intelligent Backend Systems
- AI Infrastructure
