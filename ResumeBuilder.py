import streamlit as st
import json
import os

def main():
    st.title("📄 Resume Builder")
    st.write("Create your professional resume with our easy-to-use builder")

    # Personal Information
    st.header("Personal Information")
    col1, col2 = st.columns(2)
    
    with col1:
        full_name = st.text_input("Full Name", key="rb_name")
        email = st.text_input("Email", key="rb_email")
        phone = st.text_input("Phone Number", key="rb_phone")
        
    with col2:
        location = st.text_input("Location", key="rb_location")
        linkedin = st.text_input("LinkedIn URL", key="rb_linkedin")
        portfolio = st.text_input("Portfolio URL", key="rb_portfolio")

    # Professional Summary
    st.header("Professional Summary")
    summary = st.text_area("Write a brief professional summary")

    # Work Experience
    st.header("Work Experience")
    num_experiences = st.number_input("Number of work experiences", min_value=0, max_value=10, value=1)
    
    experiences = []
    for i in range(num_experiences):
        st.subheader(f"Experience {i+1}")
        col1, col2 = st.columns(2)
        with col1:
            company = st.text_input(f"Company Name #{i+1}")
            position = st.text_input(f"Position #{i+1}")
        with col2:
            start_date = st.text_input(f"Start Date #{i+1}")
            end_date = st.text_input(f"End Date #{i+1}")
        responsibilities = st.text_area(f"Key Responsibilities #{i+1}")
        experiences.append({
            "company": company,
            "position": position,
            "start_date": start_date,
            "end_date": end_date,
            "responsibilities": responsibilities
        })

    # Education
    st.header("Education")
    num_education = st.number_input("Number of educational qualifications", min_value=0, max_value=5, value=1)
    
    education = []
    for i in range(num_education):
        st.subheader(f"Education {i+1}")
        col1, col2 = st.columns(2)
        with col1:
            institution = st.text_input(f"Institution #{i+1}")
            degree = st.text_input(f"Degree #{i+1}")
        with col2:
            grad_year = st.text_input(f"Graduation Year #{i+1}")
            gpa = st.text_input(f"GPA #{i+1}")
        education.append({
            "institution": institution,
            "degree": degree,
            "graduation_year": grad_year,
            "gpa": gpa
        })

    # Skills
    st.header("Skills")
    skills = st.text_area("Enter your skills (one per line)")

    # Generate Resume
    if st.button("Generate Resume"):
        resume_data = {
            "personal_info": {
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "location": location,
                "linkedin": linkedin,
                "portfolio": portfolio
            },
            "professional_summary": summary,
            "work_experience": experiences,
            "education": education,
            "skills": [skill.strip() for skill in skills.split("\n") if skill.strip()]
        }
        
        # Save resume data
        save_resume_data(resume_data)
        st.success("Resume generated successfully!")
        display_resume(resume_data)

def save_resume_data(data):
    """Save resume data to a JSON file"""
    os.makedirs("resumes", exist_ok=True)
    with open(f"resumes/{data['personal_info']['full_name']}_resume.json", "w") as f:
        json.dump(data, f, indent=4)

def display_resume(data):
    """Display the generated resume"""
    st.markdown("---")
    st.header("Generated Resume")
    
    # Personal Information
    st.subheader(data["personal_info"]["full_name"])
    st.write(f"📧 {data['personal_info']['email']} | 📱 {data['personal_info']['phone']}")
    st.write(f"📍 {data['personal_info']['location']}")
    if data["personal_info"]["linkedin"]:
        st.write(f"LinkedIn: {data['personal_info']['linkedin']}")
    if data["personal_info"]["portfolio"]:
        st.write(f"Portfolio: {data['personal_info']['portfolio']}")
    
    # Professional Summary
    st.markdown("### Professional Summary")
    st.write(data["professional_summary"])
    
    # Work Experience
    st.markdown("### Work Experience")
    for exp in data["work_experience"]:
        st.markdown(f"**{exp['position']} at {exp['company']}**")
        st.write(f"{exp['start_date']} - {exp['end_date']}")
        st.write(exp["responsibilities"])
    
    # Education
    st.markdown("### Education")
    for edu in data["education"]:
        st.markdown(f"**{edu['degree']} - {edu['institution']}**")
        st.write(f"Graduated: {edu['graduation_year']} | GPA: {edu['gpa']}")
    
    # Skills
    st.markdown("### Skills")
    st.write(" • ".join(data["skills"]))

if __name__ == "__main__":
    main()