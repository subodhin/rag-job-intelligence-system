import json

def load_jobs():

    with open("app/data/jobs.json", "r") as file:

        jobs = json.load(file)

    return jobs

def search_jobs(skill: str):

    jobs = load_jobs()
    results = []
    print()

    # for job in jobs:
    #     skills = [s.lower() for s in job["skills"]]
    #     if skill.lower() in skills:

    #         results.append(job)

    #         print("Search_jobs::::::", results)

    # return results


    for job in jobs:

        skills = [s.lower() for s in job["skills"]]

    query = skill.lower()

    if any(s in query for s in skills):

        results.append(job)

        print("Search_jobs::::::", results)

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



def generate_insights():

    jobs = load_jobs()

    skill_counts = {}

    total_salary = 0

    for job in jobs:

        total_salary += job["salary"]

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