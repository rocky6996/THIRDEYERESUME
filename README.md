# AI Resume Analyzer & Builder

An AI-powered platform for resume analysis and building, featuring ATS compatibility scoring and career guidance.

## 🚀 Features

- **Resume Analysis with ATS Scoring** – Evaluate resumes for Applicant Tracking System (ATS) compatibility.
- **AI-powered Resume Builder** – Generate optimized resumes based on industry standards.
- **Career Guidance Chatbot** – Receive personalized career insights and advice.
- **Skills Match Analysis** – Compare resume skills with job descriptions for better alignment.
- **Course Recommendations** – Get AI-driven learning suggestions to enhance your skill set.

## 🛠️ Setup & Deployment

### 🔧 Local Development

1. **Clone the Repository**
   ```bash
   git clone <your-repo-url>
   cd ANALYZER
   ```
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set Up Environment Variables**
   Create a `.env` file and add the following configurations:
   ```ini
   GOOGLE_API_KEY=your_google_api_key
   STREAMLIT_SERVER_PORT=8501
   STREAMLIT_SERVER_ADDRESS=localhost
   STREAMLIT_SERVER_MAX_UPLOAD_SIZE=5
   STREAMLIT_SERVER_ENABLE_CORS=false
   STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true
   ```
4. **Run the Application**
   ```bash
   streamlit run main.py
   ```

### ☁️ Streamlit Cloud Deployment

1. Push your code to GitHub.
2. Visit [Streamlit Cloud](https://share.streamlit.io) and connect your repository.
3. Add the required environment variables in Streamlit Cloud settings.
4. Deploy and access your application online!

## 🔒 Security Considerations

- Always use **HTTPS** in production.
- Keep **API keys secure**.
- Enable **XSRF protection** for security.
- Limit **file upload sizes** to prevent abuse.
- Disable **CORS** unless necessary.

## 🎯 Usage Guide

1. **Upload Your Resume** (PDF format preferred).
2. **Enter the Job Description** to compare your resume against.
3. **Click "Analyze Resume"** to receive an ATS compatibility score.
4. **View Detailed Insights** on resume optimization.
5. **Use the AI Chatbot** for career recommendations and improvements.

## 📸 Screenshots

![Resume Analysis](https://github.com/rocky6996/THIRDEYERESUME/blob/0cd8bdab1dbac0f5edce5a926d1001f94f8be5d7/Screenshot%202025-03-06%20005611.png)

![Career Guidance](https://github.com/rocky6996/THIRDEYERESUME/blob/0cd8bdab1dbac0f5edce5a926d1001f94f8be5d7/Screenshot%202025-03-06%20005640.png)

## 🌐 Live Demo

🔗 [Try the AI Resume Analyzer](https://thirdeyeresume-9bkccgzmkv4nmmhfthwjfm.streamlit.app/)

## 🤝 Contributing

We welcome contributions from the community! To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes and push to your fork.
4. Submit a **Pull Request** with a detailed description of your changes.

📩 For any issues, feel free to open an issue on GitHub!

---

💡 **Empower your career with AI-driven resume insights!** 🚀

