import re
from resume_parser import extract_skills, preprocess_text


# ---------- Extract Years ----------
def extract_years(text):

    text = text.lower()
    patterns = [r'(\d+)\+?\s*years', r'(\d+)\+?\s*yrs']
    years = []

    for pattern in patterns:
        matches = re.findall(pattern, text)
        for m in matches:
            years.append(int(m))

    return max(years) if years else 0


# ---------- Skill Match ----------
def skill_match_score(resume_text, job_desc_text):

    resume_text = preprocess_text(resume_text)
    job_desc_text = preprocess_text(job_desc_text)

    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_desc_text))

    if not job_skills:
        return 0, [], []

    matched = resume_skills.intersection(job_skills)
    missing = job_skills - resume_skills

    score = (len(matched) / len(job_skills)) * 100

    return round(score, 2), list(matched), list(missing)


# ---------- Experience Match ----------
def experience_match_score(resume_text, job_desc_text):

    resume_years = extract_years(resume_text)
    jd_years = extract_years(job_desc_text)

    if jd_years == 0:
        return 100, resume_years, jd_years

    if resume_years >= jd_years:
        return 100, resume_years, jd_years

    score = (resume_years / jd_years) * 100
    return round(score, 2), resume_years, jd_years


# ---------- AI Explanation ----------
def generate_explanation(skill_score, exp_score, missing_skills, final_score):

    reasons = []
    justification = []

    if missing_skills:
        reasons.append(f"Missing required skills: {', '.join(missing_skills)}")

    if skill_score < 60:
        reasons.append("Low skill match")

    if exp_score < 60:
        reasons.append("Insufficient experience")

    if final_score >= 80:
        justification.append("Strong skill alignment")
        justification.append("Good experience match")
    elif final_score >= 60:
        justification.append("Moderate profile match")
    else:
        justification.append("Profile does not meet requirements")

    return reasons, justification


# ---------- Final ATS Score ----------
def compute_match_percentage(resume_text, job_desc_text):

    skill_score, matched, missing = skill_match_score(resume_text, job_desc_text)
    exp_score, resume_years, jd_years = experience_match_score(resume_text, job_desc_text)

    final_score = (skill_score * 0.7) + (exp_score * 0.3)

    rejection_reasons, hiring_justification = generate_explanation(
        skill_score, exp_score, missing, final_score
    )

    return {
        "final_score": round(final_score, 2),
        "skill_score": skill_score,
        "experience_score": exp_score,
        "matched_skills": matched,
        "missing_skills": missing,
        "resume_years": resume_years,
        "jd_years": jd_years,
        "rejection_reasons": rejection_reasons,
        "hiring_justification": hiring_justification
    }
