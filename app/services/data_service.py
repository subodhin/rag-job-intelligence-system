
import json
from app.services.external_jobs import get_jobs
import os


def load_jobs():

    with open("app/data/jobs.json", "r") as file:
        jobs = json.load(file)

    return jobs


def search_jobs(skill: str):

    jobs = get_jobs()
    results = []

    query = skill.lower()

    for job in jobs:

        skills = [
            skill.lower()
            for skill in job["skills"]
        ]

        if any(skill in query for skill in skills):
            results.append(job)

    print("Actual result:", results)

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

        print("Service - Formatted job context:\n", line)

    return "\n".join(context_lines)


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

        # 1. TITLE MATCH
        if title:

            title_words = title.split()

            matched_title_words = sum(
                word in job_title
                for word in title_words
            )

            score += matched_title_words * 50

        # 2. SKILL MATCH
        for skill in skills:

            if skill in job_skills:
                score += 10

        # 3. LOCATION MATCH
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

        # Keep relevant jobs
        if score > 0:
            scored_results.append((score, job))

    # Highest score first
    scored_results.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        job
        for score, job in scored_results[:10]
    ]
def get_jobs_for_skill_analysis(target_role: str):

    if not target_role:
        return []

    jobs = get_jobs()

    target = target_role.lower()

    # Direct AI engineering role keywords
    direct_keywords = [
        "ai engineer",
        "artificial intelligence engineer",
        "machine learning engineer",
        "ml engineer",
        "llm engineer",
        "generative ai engineer",
        "deep learning engineer",
        "nlp engineer"
    ]

    # Adjacent technical roles
    adjacent_keywords = [
        "software engineer",
        "backend developer",
        "back-end developer",
        "full-stack developer",
        "data engineer"
    ]

    ai_keywords = [
        "ai/ml",
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "llm",
        "rag",
        "nlp",
        "generative ai"
    ]

    direct_matches = []
    adjacent_matches = []

    for job in jobs:

        job_title = job.get("title", "").lower()

        job_tags = [
            tag.lower().strip()
            for tag in job.get("skills", [])
        ]

        has_ai_tag = any(
            keyword in tag
            for keyword in ai_keywords
            for tag in job_tags
        )

        # Direct role matching
        if any(keyword in job_title for keyword in direct_keywords):
            direct_matches.append(job)

        # Adjacent technical role with AI-related tags
        elif (
            any(keyword in job_title for keyword in adjacent_keywords)
            and has_ai_tag
        ):
            adjacent_matches.append(job)

    return direct_matches + adjacent_matches

def get_jobs_for_skill_analysis1(target_role: str):

    if not target_role:
        return []

    jobs = get_jobs()

    role_words = target_role.lower().split()

    # AI-related keywords
    ai_keywords = [
        "ai/ml",
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "llm",
        "llms",
        "rag",
        "nlp",
        "generative ai"
    ]

    relevant_jobs = []

    for job in jobs:

        job_title = job.get("title", "").lower()

        job_tags = [
            tag.lower().strip()
            for tag in job.get("skills", [])
        ]

        # 1. Title matching
        title_match = any(
            word in job_title
            for word in role_words
        )

        # 2. AI-related tag matching
        tag_match = any(
            keyword in tag
            for keyword in ai_keywords
            for tag in job_tags
        )

        if title_match or tag_match:
            relevant_jobs.append(job)

    return relevant_jobs


def generate_insights():

    jobs = get_jobs()

    skill_counts = {}
    total_salary = 0
    salary_count = 0

    for job in jobs:

        # Salary calculation
        salary = job.get("salary")

        if isinstance(salary, (int, float)):
            total_salary += salary
            salary_count += 1

        # Skill frequency calculation
        for skill in job.get("skills", []):

            skill = skill.lower().strip()

            skill_counts[skill] = (
                skill_counts.get(skill, 0) + 1
            )

    average_salary = (
        total_salary / salary_count
        if salary_count else 0
    )

    # Sort skills by frequency
    top_skills = sorted(
        skill_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )

    print("Service - Average Salary:", average_salary)
    print("Service - Top Skills:", top_skills[:5])

    return {
        "average_salary": average_salary,
        "top_skills": top_skills[:5]
    }
