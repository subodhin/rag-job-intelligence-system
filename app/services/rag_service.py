def check_required_skills(jobs, required_skills=None):

    if required_skills is None:
        required_skills = []

    validated_jobs = []

    for job in jobs:

        job_skills = {
            skill.lower().strip()
            for skill in job.get("skills", [])
        }

        matched_skills = [
            skill
            for skill in required_skills
            if skill.lower().strip() in job_skills
        ]

        missing_skills = [
            skill
            for skill in required_skills
            if skill.lower().strip() not in job_skills
        ]

        validated_jobs.append({
            "job": job,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        })

    return validated_jobs