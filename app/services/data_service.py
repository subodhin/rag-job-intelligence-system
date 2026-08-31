import json
from urllib import response

import faiss
from app.services.external_jobs import get_jobs
import ollama
from app.embedding_functions.create_job_embedding import embed_jobs
from app.services.vector_service import create_index, save_index
import os

def load_jobs():

    with open("app/data/jobs.json", "r") as file:

        jobs = json.load(file)

    return jobs

# def search_jobs(skill: str):
#     jobs = get_jobs()
#     print("embedding testing::::",jobs[0])
#     results = []

#     embedded_jobs = embed_jobs(jobs)

#     #index = create_index(embedded_jobs)

#     print("Number of vectors:", index.ntotal)
#     print("Vector dimension:", index.d)

#     os.makedirs("data", exist_ok=True)
#     index = create_index(embedded_jobs)



#     save_index(index)
#    # faiss.write_index(index, INDEX_PATH)
#    # print(f"Index saved to: {INDEX_PATH}")

#     print("Jobs:>>>>>", len(jobs))
#     print("Embedded:>>>>>", len(embedded_jobs))
#     print("Vector length:>>>>>>>>", len(embedded_jobs[0]["embedding"]))

#     query = skill.lower()

#     for job in jobs:
#         skills = [s.lower() for s in job["skills"]]

#         if any(s in query for s in skills):
#             results.append(job)

#     print("actaul result ::::::>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", results)

#     return results



def search_jobs(skill: str):
    jobs = get_jobs()
    results = []

    query = skill.lower()

    for job in jobs:
        skills = [s.lower() for s in job["skills"]]

        if any(s in query for s in skills):
            results.append(job)
    print("actaul result ::::::>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", results)

    return results

def format_jobs_context(jobs):

    if not jobs:
        return "No matching jobs found."

    context_lines = []

    for i, job in enumerate(jobs[:3], start=1):

        line = (
            f"JOB {i}\n"
            f"Title: {job['title']}\n"
            f"Skills: {', '.join(job['skills'])}\n"
            f"Salary: {job['salary']}\n"
            f"Location: {job['location']}\n"
        )

        context_lines.append(line)

        print(
            "Service - Formatted job context:\n",
            line
        )

    return "\n".join(context_lines)




# def format_jobs_context(jobs):

#     context = ""

#     for job in jobs:

#         context += f"""
#         Job Title: {job['title']}
#         Skills: {', '.join(job['skills'])}
#         Salary: {job['salary']}
#         Location: {job['location']}

#         """

#     return context


# def search_jobs_by_filters(filters):

# #local data set test!
#    # jobs = load_jobs()

#    #external API data set test!
#     jobs = get_jobs()

#     results = []

#     for job in jobs:

#         # Skill filtering
#         if filters["skill"]:

#             skills = [s.lower() for s in job["skills"]]

#             if filters["skill"] not in skills:
#                 continue

#         # Location filtering
#         if filters["location"]:

#             if filters["location"].lower() != job["location"].lower():
#                 continue

#         results.append(job)

#     return results

def search_jobs_by_filters(filters):

    jobs = get_jobs()
    scored_results = []

    title = filters.get("title")
    skills = filters.get("skills", [])
    location = filters.get("location")

    # Normalize filters
    title = title.lower().strip() if title else None

    skills = [
        skill.lower().strip()
        for skill in skills
        if skill
    ]

    location = location.lower().strip() if location else None

    for job in jobs:

        job_title = job.get("title", "").lower()

        job_skills = [
            skill.lower().strip()
            for skill in job.get("skills", [])
        ]

        job_location = job.get("location", "").lower()

        score = 0

        # --------------------------------
        # 1. TITLE MATCH — strongest
        # --------------------------------

        if title:

            title_words = title.split()

            matched_title_words = sum(
                word in job_title
                for word in title_words
            )

            score += matched_title_words * 50

        # --------------------------------
        # 2. SKILL MATCH
        # --------------------------------

        for skill in skills:

            if skill in job_skills:
                score += 10

        # --------------------------------
        # 3. LOCATION MATCH
        # --------------------------------

        if location:

            if location == "remote":

                remote_indicators = [
                    "remote",
                    "worldwide",
                    "europe",
                    "americas"
                ]

                if any(
                    indicator in job_location
                    for indicator in remote_indicators
                ):
                    score += 15

            elif location in job_location:

                score += 15

        # --------------------------------
        # Keep jobs with some relevance
        # --------------------------------

        if score > 0:

            scored_results.append(
                (score, job)
            )

    # --------------------------------
    # Highest score first
    # --------------------------------

    scored_results.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        job
        for score, job in scored_results[:10]
    ]

def generate_insights():

   # jobs = load_jobs()
    jobs = get_jobs()
    skill_counts = {}
    total_salary = 0
    #clean the logic - todo

    for job in jobs:
     salary = job.get("salary")
    if isinstance(salary, int):
        total_salary += salary
    for skill in job["skills"]:
        skill = skill.lower()
        if skill not in skill_counts:
            skill_counts[skill] = 0
        skill_counts[skill] += 1
    average_salary = total_salary / len(jobs)

# Sort skills by count-------
    top_skills = sorted(
        skill_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )

    print("Service - Average Salary:::::", average_salary)
    print("Service - Top Skills:::::", top_skills[:5])

    return {
        "average_salary": average_salary,
        "top_skills": top_skills[:5]
    } 