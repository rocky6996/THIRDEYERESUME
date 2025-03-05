# AI Resume Analyzer & Builder

An AI-powered platform for resume analysis and building, featuring ATS compatibility scoring and career guidance.

## Features

- Resume Analysis with ATS Scoring
- AI-powered Resume Builder
- Career Guidance Chatbot
- Skills Match Analysis
- Course Recommendations

## Setup & Deployment

### Local Development

1. Clone the repository:
```bash
git clone <your-repo-url>
cd ANALYZER
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with:
```
GOOGLE_API_KEY=your_google_api_key
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
STREAMLIT_SERVER_MAX_UPLOAD_SIZE=5
STREAMLIT_SERVER_ENABLE_CORS=false
STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true
```

4. Run the application:
```bash
streamlit run main.py
```

### Streamlit Cloud Deployment

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add your environment variables in Streamlit Cloud settings
5. Deploy!

### Security Considerations

- Always use HTTPS in production
- Keep API keys secure
- Enable XSRF protection
- Limit file upload sizes
- Disable CORS unless necessary

## Usage

1. Upload your resume (PDF format)
2. Enter the job description
3. Click "Analyze Resume"
4. View ATS compatibility score and analysis
5. Use the AI chatbot for career guidance

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 