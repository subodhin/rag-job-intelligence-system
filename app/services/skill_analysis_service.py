def normalize_skills(skills):
    """Normalize skills into a unique, lowercase list."""

    if not skills:
        return []

    if isinstance(skills, str):
        skills = skills.split(",")

    return list(dict.fromkeys(
        skill.strip().lower()
        for skill in skills
        if isinstance(skill, str) and skill.strip()
    ))


# AI Engineer skill categories

HIGH_PRIORITY = {
    "python", "ai/ml", "artificial intelligence",
    "machine learning", "deep learning", "llm",
    "llms", "rag", "nlp", "generative ai",
    "data science", "data engineering"
}

MEDIUM_PRIORITY = {
    "fastapi", "docker", "kubernetes", "aws",
    "azure", "cloud", "postgresql", "mysql",
    "redis", "api", "rest", "distributed systems",
    "infrastructure", "gpu", "linux/unix"
}

LOW_PRIORITY = {
    "git", "github", "testing", "documentation",
    "typescript", "javascript", "react", "next.js",
    "solid", "security", "backend", "automation"
}


def classify_skill_priority(skill):

    if skill in HIGH_PRIORITY:
        return "high"

    if skill in MEDIUM_PRIORITY:
        return "medium"

    if skill in LOW_PRIORITY:
        return "low"

    return "other"


def analyse_skill_gaps(user_skills, jobs):

    user_skills = normalize_skills(user_skills)

    skill_counts = {}

    for job in jobs:

        job_skills = normalize_skills(job.get("skills", []))

        for skill in job_skills:
            skill_counts[skill] = (
                skill_counts.get(skill, 0) + 1
            )

    total_jobs = len(jobs)

    required_skills = sorted(
        skill_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )

    matched_skills = []
    missing_skills = []

    for skill, count in required_skills:

        frequency = (
            round((count / total_jobs) * 100, 2)
            if total_jobs else 0
        )

        skill_data = {
            "skill": skill,
            "job_count": count,
            "frequency_percentage": frequency,
            "priority": classify_skill_priority(skill)
        }

        if skill in user_skills:
            matched_skills.append(skill_data)
        else:
            missing_skills.append(skill_data)

    # Separate relevant and unrelated skills
    relevant_skills = [
        item for item in required_skills
        if classify_skill_priority(item[0]) != "other"
    ]

    relevant_matched = [
        item for item in matched_skills
        if item["priority"] != "other"
    ]

    # Overall coverage
    overall_coverage = (
        round(
            len(matched_skills) / len(required_skills) * 100, 2
        )
        if required_skills else 0
    )

    # Relevant skill coverage
    relevant_coverage = (
        round(
            len(relevant_matched) / len(relevant_skills) * 100, 2
        )
        if relevant_skills else 0
    )

    # Priority groups
    high_priority_gaps = [
        item for item in missing_skills
        if item["priority"] == "high"
    ]

    medium_priority_gaps = [
        item for item in missing_skills
        if item["priority"] == "medium"
    ]

    low_priority_gaps = [
        item for item in missing_skills
        if item["priority"] == "low"
    ]

    other_skills = [
        item for item in missing_skills
        if item["priority"] == "other"
    ]

    return {
        "total_jobs_analysed": total_jobs,
        "user_skills": user_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "high_priority_gaps": high_priority_gaps,
        "medium_priority_gaps": medium_priority_gaps,
        "low_priority_gaps": low_priority_gaps,
        "other_skills": other_skills,
        "overall_skill_coverage": overall_coverage,
        "relevant_skill_coverage": relevant_coverage,
        "total_required_skills": len(required_skills),
        "total_relevant_skills": len(relevant_skills)
    }