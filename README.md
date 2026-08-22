# 🔷 AI Career Intelligence Platform

> An AI-powered backend platform that simplifies job discovery using **Python, FastAPI, Local LLMs, and Retrieval-Augmented Generation (RAG) concepts**.

**Status:** 🚧 Active Development (Version 1)

---

# 📋 Overview

This project started as an AI-powered job search assistant to explore modern AI backend development using FastAPI and Local LLMs.

It is now evolving into a **Career Intelligence Platform** that aims to automate repetitive job search workflows including job discovery, resume analysis, intelligent job matching, career insights, and AI-powered recommendations.

The long-term goal is to build a production-style AI platform using modern AI engineering practices.

---

# 📦 Current Features (Implemented)

| Feature | Concepts Demonstrated |
|----------|-----------------------|
| Intelligent Job Search | Natural Language Query Processing |
| Market Insights | AI Workflow Design |
| Intent Detection | Local LLM Classification |
| Query Parsing | Pydantic Models |
| AI Routing | Modular AI Pipelines |
| FastAPI REST APIs | Backend Engineering |
| Async API Processing | Async Python |
| External Job API Integration | REST API Integration |
| Structured Request Validation | Pydantic |
| Response Sanitization | Production API Practices |
| Swagger / OpenAPI Documentation | API Development |

---

# 🏛️ Current Architecture

```text
                          User Query
                              │
                              ▼
                       FastAPI REST API
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
              Direct APIs          /ai-agent
                    │                   │
                    │                   ▼
                    │          Intent Detection
                    │               (Phi)
                    │                   │
                    │                   ▼
                    │          AI Workflow Router
                    │                   │
                    │          ┌────────┴────────┐
                    │          ▼                 ▼
                    │     Job Search       Market Insights
                    │       Workflow          Workflow
                    │          │                 │
                    │          ▼                 ▼
                    │   External Job API    AI Processing
                    │          │                 │
                    └──────────┴─────────────────┘
                              │
                              ▼
                        Final Response
```

---

# 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| Backend | Python, FastAPI |
| AI / LLM | Ollama, Phi |
| AI Concepts | Prompt Engineering, Intent Detection, RAG Concepts |
| API & Validation | Pydantic, Swagger / OpenAPI |
| Tools | Git, GitHub, Python Virtual Environment (venv) |

---

# 🧬 AI Engineering Skills Demonstrated

| Backend Engineering | AI Engineering | Software Engineering |
|---------------------|---------------|----------------------|
| Python | Local LLM Integration | REST API Design |
| FastAPI | Prompt Engineering | Async Programming |
| API Development | Intent Detection | Modular Architecture |
| API Integration | AI Routing Pipelines | Request Validation |
| JSON Processing | RAG Fundamentals | Response Sanitization |

---

# 🔮 Planned Features

| Feature | AI / Engineering Concepts |
|----------|---------------------------|
| Multi-source Job Aggregation | Data Ingestion Pipelines |
| Job Knowledge Base | PostgreSQL |
| Resume Parser | Information Extraction |
| Resume ↔ Job Matching | Explainable AI |
| Skill Gap Analysis | AI Recommendations |
| Personalized Job Ranking | Recommendation Systems |
| Semantic Search | Embeddings |
| Vector Database | Qdrant / pgvector |
| Hybrid Retrieval | Advanced RAG |
| Multi-Agent Workflows | Agentic AI |
| Career Analytics Dashboard | Data Analytics |
| Application Tracker | Workflow Automation |
| Excel / CSV Export | Data Engineering |
| Frontend Dashboard | React / Next.js |
| Docker Deployment | Containerization |

---

# 📍 Roadmap

| Version | Focus |
|----------|-------|
| ✅ Version 1 | Intelligent Job Search & Market Insights |
| 🚧 Version 2 | Multi-source Job Collection & PostgreSQL Integration |
| 🚧 Version 3 | Resume Analysis, Job Matching & Skill Gap Analysis |
| 🚧 Version 4 | Semantic Search, Embeddings & Vector Database |
| 🚧 Version 5 | AI Recommendation Engine & Multi-Agent Workflows |
| 🚧 Version 6 | Career Analytics Dashboard, Docker & Production Deployment |

---

# 🌐 Long-Term Vision

Build a production-ready **AI Career Intelligence Platform** that helps users:

- Discover jobs from multiple sources
- Build a personal job knowledge base
- Analyze resumes and job descriptions
- Match resumes with suitable opportunities
- Identify skill gaps
- Receive personalized AI-powered career recommendations
- Track job applications
- Generate career insights from job market data

using modern AI engineering concepts including:

- Large Language Models (LLMs)
- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Embeddings
- Vector Databases
- Agentic AI
- Recommendation Systems
- Explainable AI
- Workflow Automation

---

# ✍️ Author

**Subodhi Nanayakkara**

Software Engineer with 6+ years of experience, currently expanding into **AI Engineering** by building production-style AI applications focused on LLMs, Retrieval-Augmented Generation (RAG), intelligent backend systems, and AI workflow automation.
