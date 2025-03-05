import streamlit as st
import os
from dotenv import load_dotenv
import streamlit.runtime.scriptrunner as scriptrunner
import contextlib

# Load environment variables
load_dotenv()

# Initialize Streamlit context
@contextlib.contextmanager
def safe_streamlit_context():
    try:
        scriptrunner.add_script_run_ctx()
        yield
    finally:
        scriptrunner.get_script_run_ctx().reset()

# Set page configuration MUST be the first Streamlit command
with safe_streamlit_context():
    st.set_page_config(
        page_title="AI Resume Platform",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/yourusername/your-repo',
            'Report a bug': "https://github.com/yourusername/your-repo/issues",
            'About': "# AI Resume Platform\nThis is a secure resume analysis and builder platform."
        }
    )

# Custom CSS for better UI
st.markdown("""
<style>
    /* Global theme colors */
    :root {
        --background-primary: #0e1117;
        --background-secondary: #1e2028;
        --background-tertiary: #262833;
        --accent-primary: #4c8bf7;
        --accent-secondary: #2e7bf6;
        --text-primary: #ffffff;
        --text-secondary: #e0e0e0;
        --text-muted: #a0a0a0;
        --border-color: rgba(255, 255, 255, 0.1);
        --success-color: #2a9d8f;
    }

    /* Override Streamlit's default theme */
    .stApp {
        background-color: var(--background-primary);
    }

    .main .block-container {
        background-color: var(--background-primary);
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: var(--background-secondary);
        border-right: 1px solid var(--border-color);
    }

    /* Chat messages styling */
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    .chat-message.user {
        background-color: var(--accent-primary);
        color: var(--text-primary);
        border-bottom-right-radius: 0;
    }
    .chat-message.bot {
        background-color: var(--background-tertiary);
        color: var(--text-primary);
        border-bottom-left-radius: 0;
        border: 1px solid var(--border-color);
    }
    .chat-message .message-content {
        margin-top: 0.5rem;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    /* Sidebar elements */
    .sidebar .element-container {
        background-color: var(--background-tertiary);
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border: 1px solid var(--border-color);
    }

    /* Buttons */
    .stButton button {
        width: 100%;
        border-radius: 0.5rem;
        padding: 0.75rem 1rem;
        font-weight: 600;
        background-color: var(--accent-primary);
        color: var(--text-primary);
        border: none;
        transition: all 0.2s ease;
    }
    .stButton button:hover {
        background-color: var(--accent-secondary);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    /* Input fields */
    .stTextInput input, .stTextArea textarea {
        border-radius: 0.5rem;
        border: 1px solid var(--border-color);
        background-color: var(--background-primary);
        color: var(--text-primary);
        padding: 0.75rem;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--accent-primary);
        box-shadow: 0 0 0 1px var(--accent-primary);
    }

    /* File uploader */
    .stFileUploader {
        background-color: var(--background-tertiary);
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 2px dashed var(--border-color);
    }
    
    .stFileUploader:hover {
        border-color: var(--accent-primary);
    }

    /* Messages */
    .success-message {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: var(--success-color);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
    }
    .info-message {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: var(--accent-primary);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
    }

    /* Section dividers */
    .section-divider {
        margin: 1.5rem 0;
        border-bottom: 1px solid var(--border-color);
    }

    /* Headers and text */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-weight: 600;
    }
    p, li, span {
        color: var(--text-secondary);
    }
    
    /* Spinner/Loading state */
    .stSpinner {
        color: var(--accent-primary) !important;
    }

    /* Tooltips */
    .stTooltip {
        background-color: var(--background-tertiary);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
    }

    /* Markdown text */
    .stMarkdown {
        color: var(--text-secondary);
    }

    /* Selectbox */
    .stSelectbox select {
        background-color: var(--background-tertiary);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
    }

    /* Progress bar */
    .stProgress > div > div {
        background-color: var(--accent-primary);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: var(--background-secondary);
    }
    .stTabs [data-baseweb="tab"] {
        color: var(--text-secondary);
    }
    .stTabs [aria-selected="true"] {
        color: var(--accent-primary);
    }

    /* ATS Score Card */
    .ats-score-card {
        background-color: var(--background-tertiary);
        padding: 2rem;
        border-radius: 1rem;
        border: 1px solid var(--border-color);
        margin-bottom: 2rem;
    }
    .score-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.5rem;
    }
    .score-circle {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        color: var(--text-primary);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .score-details {
        background-color: var(--background-secondary);
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
    .score-item {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        padding: 0.5rem;
        border-radius: 0.5rem;
        background-color: var(--background-primary);
    }
    .score-item-icon {
        margin-right: 1rem;
        font-size: 1.2rem;
    }
    .progress-bar-container {
        width: 100%;
        height: 8px;
        background-color: var(--background-primary);
        border-radius: 4px;
        margin-top: 1rem;
    }
    .progress-bar {
        height: 100%;
        border-radius: 4px;
        background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
        transition: width 0.5s ease;
    }
</style>
""", unsafe_allow_html=True)

# Security headers
st.markdown("""
    <meta http-equiv="Content-Security-Policy" 
        content="default-src 'self' 'unsafe-inline' 'unsafe-eval' data: gap: https:; 
        style-src 'self' 'unsafe-inline'; 
        media-src *; 
        script-src 'self' 'unsafe-inline' 'unsafe-eval';">
""", unsafe_allow_html=True)

# Now we can safely import other modules
from Home import extract_text_from_pdf, analyze_resume, calculate_match_score, suggest_courses, calculate_ats_score, show_analysis
from ResumeBuilder import main as resume_builder_main

# Wrap the main app logic in the context manager
with safe_streamlit_context():
    # Initialize session state with context
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Chatbot helper function
    def get_chatbot_response(user_input):
        import google.generativeai as genai
        
        try:
            # Configure the model
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            model = genai.GenerativeModel("gemini-1.5-pro")
            
            # Create a context-aware prompt
            context = """You are a helpful career and resume assistant. You can:
            1. Provide resume writing tips
            2. Give career advice
            3. Suggest job search strategies
            4. Help with interview preparation
            5. Explain industry trends
            Please provide concise, practical advice."""
            
            prompt = f"{context}\n\nUser: {user_input}\nAssistant:"
            
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return "I apologize, but I'm having trouble connecting to the AI service. Please try again in a moment."

    # Sidebar Navigation
    st.sidebar.title("🚀 Navigation")

    # Simple navigation buttons with improved styling
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🏠 Resume Analyzer", use_container_width=True, key="nav_analyzer", help="Switch to Resume Analyzer"):
            st.session_state.page = "home"
            st.rerun()
    with col2:
        if st.button("📄 Resume Builder", use_container_width=True, key="nav_builder", help="Switch to Resume Builder"):
            st.session_state.page = "resume_builder"
            st.rerun()

    # Visual indicator of current page
    st.sidebar.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.sidebar.markdown(f"""
        <div style='text-align: center; padding: 0.5rem; background-color: #2e7bf6; border-radius: 0.5rem;'>
            <h3 style='margin: 0; color: white;'>
                {'📊 Resume Analyzer' if st.session_state.page == 'home' else '📝 Resume Builder'}
            </h3>
        </div>
    """, unsafe_allow_html=True)

    # Chatbot Section in Sidebar
    st.sidebar.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.sidebar.markdown("""
        <div style='background-color: #1a1c24; padding: 1rem; border-radius: 0.5rem;'>
            <h3 style='color: white; margin-bottom: 1rem;'>💬 AI Career Assistant</h3>
        </div>
    """, unsafe_allow_html=True)

    # Chat input with improved styling
    user_input = st.sidebar.text_input(
        "Ask anything about careers & resumes:",
        key="chat_input",
        help="Type your question here and press Enter or click Send"
    )

    # Send button with icon
    if st.sidebar.button("📤 Send", key="send_button"):
        if user_input:
            st.session_state.chat_history.append(("user", user_input))
            bot_response = get_chatbot_response(user_input)
            st.session_state.chat_history.append(("bot", bot_response))

    # Display chat history with improved styling
    chat_container = st.sidebar.container()
    with chat_container:
        for role, message in st.session_state.chat_history:
            if role == "user":
                st.markdown(f"""
                    <div class="chat-message user">
                        <div><strong>You</strong></div>
                        <div class="message-content">{message}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="chat-message bot">
                        <div><strong>AI Assistant</strong></div>
                        <div class="message-content">{message}</div>
                    </div>
                """, unsafe_allow_html=True)
        
        # Clear chat button with improved styling
        if st.session_state.chat_history:
            st.markdown('<div style="margin-top: 1rem;">', unsafe_allow_html=True)
            if st.button("🗑️ Clear Chat", key="clear_chat"):
                st.session_state.chat_history = []
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # Load the selected page
    if st.session_state.page == "home":
        # Display the Resume Analyzer content
        st.markdown("""
            <div style='background-color: var(--background-secondary); padding: 2rem; border-radius: 0.5rem; margin-bottom: 2rem; border: 1px solid var(--border-color);'>
                <h1 style='color: var(--text-primary); margin-bottom: 1rem;'>📊 AI Resume Analyzer</h1>
                <p style='font-size: 1.2rem; color: var(--text-secondary);'>
                    Analyze your resume and match it with job descriptions using Google Gemini AI.
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Sidebar: Upload Resume and Job Description
        st.sidebar.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.sidebar.markdown("""
            <div style='background-color: #1a1c24; padding: 1rem; border-radius: 0.5rem;'>
                <h3 style='color: white; margin-bottom: 1rem;'>📤 Upload and Analyze</h3>
            </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.sidebar.file_uploader(
            "📂 Upload your resume (PDF)", 
            type=["pdf"],
            key="resume_uploader"
        )
        
        job_description = st.sidebar.text_area(
            "📝 Enter Job Description:", 
            placeholder="Paste job description here...",
            key="job_description",
            height=150
        )

        # Rest of the Resume Analyzer logic with improved styling
        if uploaded_file:
            st.markdown("""
                <div class='success-message'>
                    ✅ Resume uploaded successfully!
                </div>
            """, unsafe_allow_html=True)
            
            file_path = f"./{uploaded_file.name}"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            resume_text = extract_text_from_pdf(file_path)
            
            if st.sidebar.button("🚀 Analyze Resume", key="analyze_button"):
                with st.spinner("🔍 Analyzing your resume..."):
                    analysis = analyze_resume(resume_text, job_description)
                    match_score = calculate_match_score(resume_text, job_description)
                    course_suggestions = suggest_courses(resume_text)
                    ats_score = calculate_ats_score(resume_text, job_description)
                    
                    # Display ATS Score
                    st.markdown(f"""
                        <div class="ats-score-card">
                            <div class="score-header">
                                <div>
                                    <h2>ATS Compatibility Score</h2>
                                    <p>How well your resume matches ATS requirements</p>
                                </div>
                                <div class="score-circle">
                                    {ats_score}%
                                </div>
                            </div>
                            <div class="score-details">
                                <div class="score-item">
                                    <span class="score-item-icon">📊</span>
                                    <div style="flex-grow: 1;">
                                        <strong>Overall Match</strong>
                                        <div class="progress-bar-container">
                                            <div class="progress-bar" style="width: {match_score}%;"></div>
                                        </div>
                                    </div>
                                    <span>{match_score}%</span>
                                </div>
                                <div class="score-item">
                                    <span class="score-item-icon">🎯</span>
                                    <div style="flex-grow: 1;">
                                        <strong>Keyword Match</strong>
                                        <div class="progress-bar-container">
                                            <div class="progress-bar" style="width: {ats_score}%;"></div>
                                        </div>
                                    </div>
                                    <span>{ats_score}%</span>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    # Display detailed analysis in tabs
                    tab1, tab2, tab3 = st.tabs(["📝 Resume Analysis", "🎯 Skill Match", "📚 Course Suggestions"])
                    
                    with tab1:
                        st.markdown("""
                            <div style='background-color: var(--background-tertiary); padding: 1.5rem; border-radius: 0.5rem; border: 1px solid var(--border-color);'>
                                <h3>Detailed Resume Analysis</h3>
                        """, unsafe_allow_html=True)
                        if isinstance(analysis, str):
                            st.markdown(f"<p>{analysis}</p>", unsafe_allow_html=True)
                        else:
                            show_analysis(analysis, None)
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    with tab2:
                        st.markdown("""
                            <div style='background-color: var(--background-tertiary); padding: 1.5rem; border-radius: 0.5rem; border: 1px solid var(--border-color);'>
                                <h3>Skills and Keywords Analysis</h3>
                        """, unsafe_allow_html=True)
                        
                        # Handle skills analysis based on data type
                        if isinstance(analysis, dict) and 'skills_match' in analysis:
                            for skill, match in analysis['skills_match'].items():
                                st.markdown(f"""
                                    <div class="score-item">
                                        <span class="score-item-icon">💡</span>
                                        <div style="flex-grow: 1;">
                                            <strong>{skill}</strong>
                                            <div class="progress-bar-container">
                                                <div class="progress-bar" style="width: {match * 100}%;"></div>
                                            </div>
                                        </div>
                                        <span>{int(match * 100)}%</span>
                                    </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("Skills analysis not available for this resume.")
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    with tab3:
                        st.markdown("""
                            <div style='background-color: var(--background-tertiary); padding: 1.5rem; border-radius: 0.5rem; border: 1px solid var(--border-color);'>
                                <h3>Recommended Courses</h3>
                        """, unsafe_allow_html=True)
                        if isinstance(course_suggestions, (list, tuple)) and course_suggestions:
                            for course in course_suggestions:
                                st.markdown(f"""
                                    <div class="score-item">
                                        <span class="score-item-icon">📚</span>
                                        <strong>{course}</strong>
                                    </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("No course suggestions available at this time.")
                        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.page == "resume_builder":
        resume_builder_main()

# Error handling for script context
def handle_script_context_error(func):
    def wrapper(*args, **kwargs):
        with safe_streamlit_context():
            return func(*args, **kwargs)
    return wrapper

# Wrap the chatbot function with error handling
@handle_script_context_error
def get_chatbot_response(user_input):
    import google.generativeai as genai
    
    try:
        # Configure the model
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel("gemini-1.5-pro")
        
        # Create a context-aware prompt
        context = """You are a helpful career and resume assistant. You can:
        1. Provide resume writing tips
        2. Give career advice
        3. Suggest job search strategies
        4. Help with interview preparation
        5. Explain industry trends
        Please provide concise, practical advice."""
        
        prompt = f"{context}\n\nUser: {user_input}\nAssistant:"
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return "I apologize, but I'm having trouble connecting to the AI service. Please try again in a moment."
