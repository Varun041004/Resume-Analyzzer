import streamlit as st
import pandas as pd
from resume_parser import extract_text, preprocess_text, extract_skills
from similarity import compute_match_percentage

st.set_page_config(page_title="ATS Resume Screener", layout="wide")

st.title("📄 Smart Resume Screening System (ATS)")
st.markdown("---")

job_desc = st.text_area("📌 Enter Job Description", height=150)

uploaded_files = st.file_uploader(
    "Upload Resumes",
    type=["pdf","docx","txt"],
    accept_multiple_files=True
)


# ---------- Helper: show numbered list ----------
def show_numbered(items):
    if not items:
        st.write("— None —")
    else:
        for i, item in enumerate(items, 1):
            st.write(f"{i}. {item}")


# ---------- PROCESS RESUMES ----------
if uploaded_files and job_desc:

    st.markdown("## 📊 ATS Screening Results")
    st.markdown("---")

    all_results = []

    for uploaded_file in uploaded_files:

        text = extract_text(uploaded_file)
        processed = preprocess_text(text)
        result = compute_match_percentage(processed, job_desc)

        all_results.append({
            "Candidate": uploaded_file.name,
            "Final Score": result["final_score"],
            "Skill Score": result["skill_score"],
            "Experience": result["resume_years"],
            "Matched Skills": ", ".join(result["matched_skills"]),
            "Missing Skills": ", ".join(result["missing_skills"])
        })

        # ---------- Candidate Report ----------
        with st.container():
            st.markdown(f"### 👤 {uploaded_file.name}")

            col1, col2, col3 = st.columns(3)

            col1.metric("Final Score", f"{result['final_score']}%")
            col2.metric("Skill Match", f"{result['skill_score']}%")
            col3.metric("Experience", f"{result['resume_years']} yrs")

            c1, c2 = st.columns(2)

            with c1:
                st.markdown("#### ✅ Matched Skills")
                show_numbered(result["matched_skills"])

                st.markdown("#### 💼 Hiring Justification")
                show_numbered(result["hiring_justification"])

            with c2:
                st.markdown("#### ❌ Missing Skills")
                show_numbered(result["missing_skills"])

                st.markdown("#### ⚠️ Rejection Reasons")
                show_numbered(result["rejection_reasons"])

            st.markdown("---")

    # ---------- Ranking Dashboard ----------
    df = pd.DataFrame(all_results).sort_values(by="Final Score", ascending=False)

    st.markdown("## 🏆 Candidate Ranking Dashboard")
    st.dataframe(df, use_container_width=True)

    # ---------- Recruiter Filters ----------
    st.markdown("## 🔎 Recruiter Filters")

    search_name = st.text_input("Search Candidate")
    min_exp = st.slider("Minimum Experience (Years)", 0, 20, 0)
    skill_filter = st.text_input("Filter by Skill")

    filtered_df = df.copy()

    if search_name:
        filtered_df = filtered_df[
            filtered_df["Candidate"].str.contains(search_name, case=False)
        ]

    if min_exp:
        filtered_df = filtered_df[filtered_df["Experience"] >= min_exp]

    if skill_filter:
        filtered_df = filtered_df[
            filtered_df["Matched Skills"].str.contains(skill_filter, case=False)
        ]

    st.write("### Filtered Results")
    st.dataframe(filtered_df, use_container_width=True)

    # ---------- Recommended Candidate ----------
    st.markdown("## ⭐ Recommended Hire")

    if not filtered_df.empty:
        top = filtered_df.iloc[0]
        st.success(f"Best Candidate: {top['Candidate']} (Score: {top['Final Score']}%)")
    else:
        st.warning("No candidate matches filters.")
