from PyPDF2 import PdfReader
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Groq Client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Extract PDF text
def extract_text(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text

# Analyze Resume
def analyze_resume(resume_text):

    prompt = f"""
    You are a professional ATS Resume Reviewer.

    Analyze this resume and provide:

    1. ATS Score out of 100
    2. Resume Summary
    3. Strengths
    4. Weaknesses
    5. Missing Skills
    6. Improvement Suggestions
    7. Recommended Job Roles

    Resume:
    {resume_text[:4000]}
    """

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.3
    )

    return response.choices[0].message.content

# Main
pdf_path = input("Enter Resume PDF Path: ")

resume_text = extract_text(pdf_path)

print("\nAnalyzing Resume...\n")

result = analyze_resume(resume_text)

print(result)