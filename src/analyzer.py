import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_resume(resume_text, job_description):
    """
    Sends resume and job description to Groq AI and gets an analysis back.
    """
    prompt = f"""
    You are an expert resume reviewer.
    
    Here is a candidate's resume:
    {resume_text}
    
    Here is the job description they are applying for:
    {job_description}
    
    Please analyze:
    1. How well does the resume match the job description? Give a score out of 10.
    2. What are the top 3 strengths of this resume for this job?
    3. What are the top 3 weaknesses or missing skills?
    4. Overall recommendation.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # ← replace llama3-8b-8192 with this
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
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

    print("Sending resume to Groq AI for analysis...")
    result = analyze_resume(sample_resume, sample_job)
    print(result)