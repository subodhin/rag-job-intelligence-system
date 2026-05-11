import json

def load_jobs():

    with open("app/data/jobs.json", "r") as file:

        jobs = json.load(file)

    return jobs

def search_jobs(skill: str):

    jobs = load_jobs()

    results = []

    for job in jobs:

        skills = [s.lower() for s in job["skills"]]
        if skill.lower() in skills:

            results.append(job)

    return results



def format_jobs_context(jobs):

    if not jobs:
        return "No matching jobs found."

    context_lines = []

    for job in jobs[:3]:

        line = (
            f"{job['title']} | "
            f"Skills: {', '.join(job['skills'])} | "
            f"Salary: {job['salary']}"
        )

        context_lines.append(line)
        print("Service - Formatted job context line:::::", line)

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


def search_jobs_by_filters(filters):

    jobs = load_jobs()

    results = []

    for job in jobs:

        # Skill filtering
        if filters["skill"]:

            skills = [s.lower() for s in job["skills"]]

            if filters["skill"] not in skills:
                continue

        # Location filtering
        if filters["location"]:

            if filters["location"].lower() != job["location"].lower():
                continue

        results.append(job)

    return results