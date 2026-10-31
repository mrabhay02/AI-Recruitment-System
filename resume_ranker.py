
from backend.skill_extractor import extract_skills
from backend.similarity import calculate_similarity


def rank_resume(resume_text, job_description):
    resume_text = resume_text or ""
    job_description = job_description or ""

    similarity_score = calculate_similarity(
        resume_text,
        job_description
    )

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    matched_skills = sorted(
        set(resume_skills) & set(job_skills)
    )

    missing_skills = sorted(
        set(job_skills) - set(resume_skills)
    )

    if job_skills:
        skill_match_score = (
            len(matched_skills) / len(job_skills)
        ) * 100
    else:
        skill_match_score = 0.0

    return {
        "similarity_score": round(similarity_score, 2),
        "skill_match_score": round(skill_match_score, 2),
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    }
