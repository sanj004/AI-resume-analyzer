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
        model="llama-3.3-70b-versatile",  # ← replace llama3-8b-8192 with this
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
def score_resume(resume_text, job_description):
    """
    Scores how well the resume matches the job description
    based on keyword overlap. Returns a score out of 100.
    """
    # Clean and split text into individual words
    def get_words(text):
        # Convert to lowercase and split by spaces/newlines
        words = text.lower().split()
        # Remove punctuation from each word
        cleaned = set()
        for word in words:
            word = word.strip(".,!?():;-/")
            if len(word) > 2:  # ignore tiny words like "a", "is", "to"
                cleaned.add(word)
        return cleaned

    resume_words = get_words(resume_text)
    job_words = get_words(job_description)

    # Find matching keywords
    matching_words = resume_words & job_words

    # Calculate score
    if len(job_words) == 0:
        return 0

    score = round((len(matching_words) / len(job_words)) * 100, 2)

    # Find missing keywords (in job but not in resume)
    missing_keywords = job_words - resume_words

    return {
        "score": score,
        "matching_keywords": list(matching_words),
        "missing_keywords": list(missing_keywords)[:10]  # top 10 missing
    }

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

    print("=== KEYWORD MATCH SCORE ===")
    result = score_resume(sample_resume, sample_job)
    print(f"Match Score: {result['score']}%")
    print(f"\nMatching Keywords: {result['matching_keywords']}")
    print(f"\nMissing Keywords: {result['missing_keywords']}")

    print("\n=== AI ANALYSIS ===")
    print("Sending to Groq AI...")
    analysis = analyze_resume(sample_resume, sample_job)
    print(analysis)

    