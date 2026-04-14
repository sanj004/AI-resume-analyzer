import pdfplumber
import os

def extract_text_from_pdf(pdf_path):
    """
    Takes a path to a PDF file and returns all the text in it as a string.
    """
    # Check if the file actually exists
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"No file found at: {pdf_path}")
    
    # Check if it's actually a PDF
    if not pdf_path.endswith(".pdf"):
        raise ValueError("File must be a .pdf")

    extracted_text = ""

    # Open the PDF and read each page
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:  # some pages might be empty
                extracted_text += text + "\n"

    return extracted_text.strip()


def get_resume_sections(text):
    """
    Takes raw resume text and tries to identify key sections.
    """
    sections = {
        "education": "",
        "experience": "",
        "skills": "",
        "projects": ""
    }

    # Common section headers to look for
    keywords = {
        "education": ["education", "academic"],
        "experience": ["experience", "work history", "employment"],
        "skills": ["skills", "technical skills", "technologies"],
        "projects": ["projects", "personal projects"]
    }

    lines = text.lower().split("\n")
    current_section = None

    for line in lines:
        # Check if this line is a section header
        for section, triggers in keywords.items():
            if any(trigger in line for trigger in triggers):
                current_section = section
                break
        
        # Add line to current section
        if current_section:
            sections[current_section] += line + "\n"

    return sections


# This block runs only when you run this file directly
if __name__ == "__main__":
    # Test it with a sample resume
    test_path = "data/sample_resume.pdf"
    
    print("Extracting text from resume...")
    text = extract_text_from_pdf(test_path)
    
    print("\n--- RAW TEXT ---")
    print(text[:500])  # Print first 500 characters
    
    print("\n--- SECTIONS FOUND ---")
    sections = get_resume_sections(text)
    for section, content in sections.items():
        if content.strip():
            print(f"\n{section.upper()}:")
            print(content[:200])