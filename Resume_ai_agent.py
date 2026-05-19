import streamlit as st
from PyPDF2 import PdfReader
from openai import OpenAI
from dotenv import load_dotenv
import os
import re

# Load API key
load_dotenv()

# Groq Client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Page Config
st.set_page_config(
    page_title="AI Resume Reviewer",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

.stButton button {
    width: 100%;
    border-radius: 10px;
    height: 50px;
    font-size: 18px;
}

.score-box {
    padding: 20px;
    border-radius: 12px;
    background-color: #1E1E1E;
    text-align: center;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# Title
st.title("AI Resume Reviewer Agent")

st.write("Upload your resume and get AI-powered ATS analysis.")

# Upload PDF
uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

# Extract Text
def extract_text(pdf_file):

    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text

# AI Analysis
def analyze_resume(resume_text):

    # Limit large text
    resume_text = resume_text[:4000]

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
    {resume_text}
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

# Extract ATS Score
def extract_score(text):

    match = re.search(r'(\d+)\s*/\s*100', text)

    if match:
        return int(match.group(1))

    return 70

# Main App
if uploaded_file:

    st.success("Resume Uploaded Successfully")

    with st.spinner("Extracting Resume Text..."):

        resume_text = extract_text(uploaded_file)

    st.subheader("Resume Preview")

    st.text_area(
        "Extracted Text",
        resume_text[:3000],
        height=250
    )

    if st.button("Analyze Resume"):

        with st.spinner("AI is analyzing your resume..."):

            result = analyze_resume(resume_text)

            score = extract_score(result)

        # Score UI
        st.markdown(
            f"""
            <div class="score-box">
                <h1>ATS Score</h1>
                <h2>{score}/100</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(score)

        st.subheader("AI Analysis Report")

        st.write(result)