import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def rewrite_resume(resume_text, job_description, missing_keywords):
    """
    Takes the original resume, job description and missing keywords
    and rewrites the resume to better match the job.
    """
    prompt = f"""
    You are an expert resume writer.

    Here is the original resume:
    {resume_text}

    Here is the job description they are applying for:
    {job_description}

    These keywords are missing from the resume but are important for the job:
    {', '.join(missing_keywords)}

    Please rewrite the resume to:
    1. Naturally incorporate the missing keywords where relevant
    2. Strengthen the experience section to better match the job
    3. Keep all original information — do not make up fake experience
    4. Make it more professional and impactful
    5. Keep it concise and clean

    Return only the rewritten resume, nothing else.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def save_resume(rewritten_resume, output_path="outputs/rewritten_resume.txt"):
    """
    Saves the rewritten resume to a file.
    """
    with open(output_path, "w") as f:
        f.write(rewritten_resume)
    print(f"Rewritten resume saved to {output_path}")


if __name__ == "__main__":
    # Import our previous functions
    from analyzer import score_resume

    sample_resume = """
    John Doe
    Python Developer
    Skills: Python, Machine Learning, TensorFlow, SQL
    Experience: 2 years at ABC Corp building ML models
    Education: B.Tech Computer Science
    """

    sample_job = """
    We are looking for a Machine Learning Engineer with:
    - Strong Python skills
    - Experience with ML frameworks like TensorFlow or PyTorch
    - Knowledge of SQL and databases
    - Good communication skills
    """

    # Step 1: Score the resume first
    print("=== SCORING RESUME ===")
    score_result = score_resume(sample_resume, sample_job)
    print(f"Original Match Score: {score_result['score']}%")
    print(f"Missing Keywords: {score_result['missing_keywords']}")

    # Step 2: Rewrite the resume
    print("\n=== REWRITING RESUME ===")
    rewritten = rewrite_resume(
        sample_resume,
        sample_job,
        score_result['missing_keywords']
    )
    print(rewritten)

    # Step 3: Score the rewritten resume
    print("\n=== NEW SCORE AFTER REWRITE ===")
    new_score = score_resume(rewritten, sample_job)
    print(f"New Match Score: {new_score['score']}%")

    # Step 4: Save it
    save_resume(rewritten)