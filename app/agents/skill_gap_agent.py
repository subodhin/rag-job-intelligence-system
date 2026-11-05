from app.services.data_service import get_jobs_for_skill_analysis
from app.services.skill_analysis_service import analyse_skill_gaps
from app.services.skill_recommendation_service import generate_skill_recommendations


def handle_skill_gap_analysis(query: str, user_context=None):

    print("------ Skill Gap Agent ------")

    if not user_context:
        return {
            "intent": "skill_gap_analysis",
            "message": "User profile information is unavailable."
        }

    # 1. Get user profile
    profile = user_context.get("profile") or {}

    user_skills = profile.get("skills", [])
    target_role = profile.get("target_role")

    if not target_role:
        return {
            "intent": "skill_gap_analysis",
            "message": "Please set your target role in your profile."
        }

    # 2. Retrieve relevant jobs
    jobs = get_jobs_for_skill_analysis(target_role)

    if not jobs:
        return {
            "intent": "skill_gap_analysis",
            "message": f"No relevant jobs found for {target_role}."
        }

    # 3. Analyse skill gaps
    analysis = analyse_skill_gaps(user_skills, jobs)

    # 4. Generate AI recommendations
    recommendations = generate_skill_recommendations(
        target_role,
        analysis
    )

    # 5. Prepare UI-friendly skill groups
    skill_assessment = {
        "profile_skills": analysis["user_skills"],
        "matched_in_sample": analysis["matched_skills"],
        "high_priority_gaps": analysis["high_priority_gaps"],
        "medium_priority_gaps": analysis["medium_priority_gaps"],
        "low_priority_gaps": analysis["low_priority_gaps"]
    }

    # 6. Prepare overview metrics
    overview = {
        "jobs_analysed": analysis["total_jobs_analysed"],
        "profile_skill_count": len(analysis["user_skills"]),
        "profile_skills_found_in_sample": len(analysis["matched_skills"]),
        "high_priority_gaps": len(analysis["high_priority_gaps"]),
        "skill_coverage": analysis["relevant_skill_coverage"]
    }

    # 7. Final response
    return {
        "intent": "skill_gap_analysis",
        "agent": "skill_gap_agent",
        "target_role": target_role,

        "overview": overview,

        "skill_assessment": skill_assessment,

        "recommendations": recommendations,

        "data_quality": {
            "sample_size": len(jobs),
            "warning": (
                "This analysis is based on a limited sample of job postings. "
                "Results may not represent the entire job market."
            )
        }
    }