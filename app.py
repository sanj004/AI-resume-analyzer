import streamlit as st
import sys
import os

# This makes sure Python can find your src folder
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from parser import extract_text_from_pdf
from analyzer import analyze_resume, score_resume
from rewriter import rewrite_resume, save_resume

# ── Page config ──────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)

# ── Title ─────────────────────────────────────────────────
st.title("🤖 AI Resume Analyzer & Rewriter")
st.markdown("Upload your resume and paste a job description to get an AI-powered analysis and rewrite!")

# ── Two columns layout ────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Upload Your Resume")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

with col2:
    st.subheader("💼 Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=200,
        placeholder="We are looking for a Machine Learning Engineer with..."
    )

# ── Analyze button ────────────────────────────────────────
if st.button("🚀 Analyze & Rewrite Resume", type="primary"):

    # Check both inputs are provided
    if not uploaded_file:
        st.error("Please upload a resume PDF!")
    elif not job_description:
        st.error("Please paste a job description!")
    else:
        # Save uploaded PDF temporarily
        temp_path = "data/temp_resume.pdf"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("Analyzing your resume..."):

            # Step 1: Extract text
            resume_text = extract_text_from_pdf(temp_path)

            # Step 2: Score it
            score_result = score_resume(resume_text, job_description)

            # Step 3: AI Analysis
            ai_analysis = analyze_resume(resume_text, job_description)

            # Step 4: Rewrite
            rewritten = rewrite_resume(
                resume_text,
                job_description,
                score_result['missing_keywords']
            )

            # Step 5: Save rewritten resume
            save_resume(rewritten)

        # ── Results ───────────────────────────────────────
        st.success("Analysis Complete!")

        # Score
        st.subheader("📊 Match Score")
        score = score_result['score']
        st.metric("Keyword Match Score", f"{score}%")

        # Color based on score
        if score >= 70:
            st.success("Great match! 🎉")
        elif score >= 40:
            st.warning("Moderate match — rewrite will help! 💪")
        else:
            st.error("Low match — definitely use the rewritten version! 🔄")

        # Keywords
        col3, col4 = st.columns(2)
        with col3:
            st.subheader("✅ Matching Keywords")
            st.write(", ".join(score_result['matching_keywords']))

        with col4:
            st.subheader("❌ Missing Keywords")
            st.write(", ".join(score_result['missing_keywords']))

        # AI Analysis
        st.subheader("🤖 AI Analysis")
        st.markdown(ai_analysis)

        # Rewritten Resume
        st.subheader("✍️ Rewritten Resume")
        st.markdown(rewritten)

        # Download button
        st.download_button(
            label="⬇️ Download Rewritten Resume",
            data=rewritten,
            file_name="rewritten_resume.txt",
            mime="text/plain"
        )