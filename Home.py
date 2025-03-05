import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import pdfplumber
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import re

# Load environment variables
load_dotenv()

# Configure Google Gemini AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    st.error("API Key for Google Gemini AI is missing! Please check your .env file.")

# Add the show_career_resources function
def show_career_resources():
    st.title("📚 Career Resources")
    st.write("Explore various career development resources here.")

    st.subheader("Resume Writing Tips")
    st.write("1. Tailor your resume to each job application.")
    st.write("2. Use bullet points to highlight achievements.")
    st.write("3. Keep it concise and well-formatted.")

    st.subheader("Interview Preparation")
    st.write("1. Research the company and its culture.")
    st.write("2. Practice common interview questions.")
    st.write("3. Dress appropriately and be confident.")

    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.experimental_rerun()

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        # Try pdfplumber first
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        st.warning(f"Primary extraction failed, trying backup method...")
        try:
            # Fallback to PyPDF2
            with open(pdf_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            st.error(f"PDF text extraction failed. Please make sure the PDF is not encrypted or corrupted.")
            return ""
    
    return text.strip()

# Function to analyze resume with Gemini AI
def analyze_resume(resume_text, job_description=None):
    if not resume_text:
        return "Error: Resume text is required for analysis."
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        base_prompt = f"""
        You are an experienced HR professional. Analyze the following resume:
        - Evaluate the candidate's suitability for a technical role.
        - List strengths, weaknesses, and areas for improvement.
        - Provide resume enhancement suggestions.
        - Check for grammar and spelling mistakes.
        Resume: {resume_text}
        """
        if job_description:
            base_prompt += f"\n Compare with Job Description: {job_description}"
        response = model.generate_content(base_prompt)
        return response.text.strip()
    except Exception as e:
        return f"AI analysis failed: {e}"

# Function to calculate match score
def calculate_match_score(resume_text, job_description):
    if not job_description:
        return None
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
    match_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] * 100
    return round(match_score, 2)

# Function to suggest courses based on missing skills
def suggest_courses(resume_text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    Based on the following resume, suggest a few relevant courses to improve missing skills:
    Resume: {resume_text}
    """
    response = model.generate_content(prompt)
    return response.text.strip()

# Function to calculate ATS score based on keywords
def calculate_ats_score(resume_text, job_description):
    if not job_description:
        return 0  # Return 0 if no job description is provided

    # Extract keywords from job description
    job_keywords = set(re.findall(r'\b\w+\b', job_description.lower()))  # Simple word extraction
    resume_words = set(re.findall(r'\b\w+\b', resume_text.lower()))  # Extract words from resume

    # Calculate the number of matching keywords
    matching_keywords = job_keywords.intersection(resume_words)
    ats_score = (len(matching_keywords) / len(job_keywords)) * 100 if job_keywords else 0  # Avoid division by zero

    return round(ats_score, 2)  # Return ATS score rounded to 2 decimal places

# Function to plot ATS score with improved visualization
def plot_ats_score(ats_score):
    # Create figure with dark theme
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 5), subplot_kw=dict(aspect="equal"))
    
    # Set background colors
    ax.set_facecolor('#1E1E1E')
    fig.patch.set_facecolor('#1E1E1E')
    
    # Calculate color based on score
    if ats_score >= 80:
        score_color = '#4CAF50'  # Green for high scores
    elif ats_score >= 60:
        score_color = '#FFA500'  # Orange for medium scores
    else:
        score_color = '#FF4444'  # Red for low scores
    
    # Create the gauge background (total range)
    ax.pie([100], 
           colors=['#333333'], 
           startangle=90, 
           counterclock=False,
           wedgeprops=dict(width=0.3, edgecolor='none'))

    # Create the actual score wedge
    wedges, _ = ax.pie([ats_score, 100 - ats_score], 
                       colors=[score_color, '#333333'], 
                       startangle=90, 
                       counterclock=False,
                       wedgeprops=dict(width=0.3, edgecolor='none'))

    # Add center circle for gauge effect
    centre_circle = plt.Circle((0, 0), 0.70, fc='#1E1E1E', ec='none')
    fig.gca().add_artist(centre_circle)

    # Add score text in center
    plt.text(0, 0.1, f"{int(ats_score)}", 
             horizontalalignment='center', 
             verticalalignment='center',
             color='white', 
             fontsize=30, 
             fontweight='bold')
    
    # Add percentage symbol
    plt.text(0, -0.1, "%", 
             horizontalalignment='center', 
             verticalalignment='center',
             color='white', 
             fontsize=20)

    # Add "ATS Score" text
    plt.text(0, -0.3, "ATS Parse Rate", 
             horizontalalignment='center', 
             color='#888888', 
             fontsize=12)

    # Set limits and remove axes
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.axis('off')

    # Add a subtle glow effect to the score wedge
    wedges[0].set_alpha(0.9)

    return fig

# Chatbot for real-time assistant
def get_ai_response(user_input):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"User: {user_input}\nAI:"
    response = model.generate_content(prompt)
    return response.text.strip()

# Streamlit UI setup
st.title("📄 AI Resume Analyzer")
st.write("Analyze your resume and match it with job descriptions using Google Gemini AI.")

# Sidebar: Upload Resume and Job Description
st.sidebar.header("Upload and Analyze")
uploaded_file = st.sidebar.file_uploader("📂 Upload your resume (PDF)", type=["pdf"])
job_description = st.sidebar.text_area("📝 Enter Job Description:", placeholder="Paste job description here...")

# Chatbot Section
st.sidebar.header("💬 Chatbot Assistant")
user_input = st.sidebar.text_input("Ask anything about resumes, jobs, or AI:")
if st.sidebar.button("Send"): 
    if user_input:
        ai_response = get_ai_response(user_input)
        st.sidebar.write(f"**AI:** {ai_response}")
    else:
        st.sidebar.warning("⚠️ Please enter a question.")

# Resume Analysis UI
def show_analysis(analysis_text, courses):
    st.markdown("---")  # Add a visual separator
    st.subheader("📊 Detailed Analysis")
    
    # Create tabs for different sections of analysis
    tab1, tab2 = st.tabs(["📌 Analysis Results", "🎓 Suggested Courses"])
    
    with tab1:
        # Format and display the analysis with better styling
        st.markdown(f"""
        <div style='background-color: #1E1E1E; padding: 20px; border-radius: 10px;'>
            {analysis_text}
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        # Format and display the course suggestions
        st.markdown(f"""
        <div style='background-color: #1E1E1E; padding: 20px; border-radius: 10px;'>
            {courses}
        </div>
        """, unsafe_allow_html=True)

if uploaded_file:
    st.success("✅ Resume uploaded successfully!")
    file_path = f"./{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    resume_text = extract_text_from_pdf(file_path)
    
    if st.sidebar.button("🚀 Analyze Resume"):
        with st.spinner("🔍 Analyzing resume..."):
            # Get all analysis results
            analysis = analyze_resume(resume_text, job_description)
            match_score = calculate_match_score(resume_text, job_description)
            course_suggestions = suggest_courses(resume_text)
            ats_score = calculate_ats_score(resume_text, job_description)
            
            # Create columns for scores
            col1, col2 = st.columns([1, 1])
            
            with col1:
                # Display ATS Score
                fig = plot_ats_score(ats_score)
                st.pyplot(fig)
                plt.close(fig)
            
            with col2:
                # Display Match Score
                st.write("### Match Score")
                st.write(f"🎯 **{match_score}%** match with job description")
            
            st.success("✅ Analysis complete!")
            
            # Display detailed analysis directly without a button
            show_analysis(analysis, course_suggestions)
            
            # Clean up the temporary file
            try:
                os.remove(file_path)
            except:
                pass
else:
    st.warning("⚠️ Please upload a resume in PDF format.")