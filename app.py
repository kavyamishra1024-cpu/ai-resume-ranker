import streamlit as st
import pdfplumber
import re

# -----------------------------------
# PAGE SETTINGS
# -----------------------------------
st.set_page_config(
    page_title="AI Resume Ranker",
    page_icon="🚀"
)

# -----------------------------------
# SAFE CSS
# -----------------------------------
st.markdown("""
<style>

.stApp {
    background-color: #0F172A;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

div.stButton > button {
    background-color: #00ADB5;
    color: white;
    border-radius: 10px;
    border: none;
}

[data-testid="stMetricValue"] {
    color: #00ADB5;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# SIDEBAR
# -----------------------------------
st.sidebar.title("🚀 AI Resume Ranker")

st.sidebar.write("""
### Features

✅ ATS Score  
✅ Skill Analysis  
✅ Missing Skills  
✅ Resume Suggestions  
✅ JD Match Score  
""")

st.sidebar.info("Made with Python + Streamlit")

# -----------------------------------
# CUSTOM TITLE
# -----------------------------------
st.markdown(
    """
    <h1 style='
    text-align:center;
    color:#00ADB5;
    font-size:42px;
    font-weight:bold;
    '>
    AI Resume Ranker
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style='
    text-align:center;
    color:#CBD5E1;
    font-size:18px;
    '>
    Upload your resume and get ATS analysis
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# -----------------------------------
# JOB ROLE
# -----------------------------------
job_role = st.selectbox(
    "Select Job Role",
    [
        "Software Developer",
        "Data Analyst",
        "Marketing",
        "HR",
        "Finance",
        "Teacher",
        "Process Engineer"
    ]
)

# -----------------------------------
# FILE UPLOAD
# -----------------------------------
uploaded_file = st.file_uploader(
    "Upload Your Resume",
    type=["pdf"]
)

# -----------------------------------
# SKILLS DATABASE
# -----------------------------------
role_skills = {

    "Software Developer": [
        "python",
        "java",
        "html",
        "css",
        "javascript",
        "sql",
        "react",
        "github",
        "project"
    ],

    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "power bi",
        "tableau",
        "statistics",
        "analysis"
    ],

    "Marketing": [
        "seo",
        "branding",
        "marketing",
        "sales",
        "communication",
        "social media"
    ],

    "HR": [
        "recruitment",
        "leadership",
        "management",
        "communication",
        "teamwork"
    ],

    "Finance": [
        "finance",
        "accounting",
        "excel",
        "tax",
        "budget",
        "analysis"
    ],

    "Teacher": [
        "teaching",
        "education",
        "presentation",
        "classroom",
        "training"
    ],

    "Process Engineer": [
        "chemical engineering",
        "process engineering",
        "manufacturing",
        "quality control",
        "process optimization",
        "plant operation",
        "production",
        "safety",
        "maintenance"
    ]
}

# -----------------------------------
# PROCESS RESUME
# -----------------------------------
if uploaded_file is not None:

    st.success("✅ Resume uploaded successfully!")

    text = ""

    try:

        with pdfplumber.open(uploaded_file) as pdf:

            for page in pdf.pages:

                extracted = page.extract_text()

                if extracted:
                    text += extracted

    except:
        st.error("❌ Error reading PDF")

    # -----------------------------------
    # IF TEXT EXISTS
    # -----------------------------------
    if text.strip() != "":

        # -----------------------------------
        # CONTACT INFO
        # -----------------------------------
        email = re.findall(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text
        )

        phone = re.findall(r"\d{10}", text)

        # -----------------------------------
        # SKILL ANALYSIS
        # -----------------------------------
        skills = role_skills[job_role]

        score = 0

        found_skills = []

        for skill in skills:

            if skill.lower() in text.lower():

                score += 10
                found_skills.append(skill)

        if score > 100:
            score = 100

        # -----------------------------------
        # TABS
        # -----------------------------------
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Resume Analysis",
            "🛠 Skills",
            "📄 ATS Report",
            "💼 JD Match"
        ])

        # -----------------------------------
        # TAB 1
        # -----------------------------------
        with tab1:

            st.subheader("Resume Score")

            st.progress(score)

            col1, col2 = st.columns(2)

            with col1:
                st.metric("ATS Score", f"{score}%")

            with col2:
                st.metric("Skills Found", len(found_skills))

            if score >= 80:
                st.success("🔥 Excellent Resume")
                st.balloons()

            elif score >= 50:
                st.warning("⚠ Average Resume")

            else:
                st.error("❌ Needs Improvement")

            # CONTACT INFO
            st.subheader("Contact Information")

            if email:
                st.write("📧 Email:", email[0])
            else:
                st.write("📧 Email not found")

            if phone:
                st.write("📱 Phone:", phone[0])
            else:
                st.write("📱 Phone not found")

            # RESUME TEXT
            with st.expander("📄 See Extracted Resume Text"):
                st.text(text[:2000])

        # -----------------------------------
        # TAB 2
        # -----------------------------------
        with tab2:

            st.subheader("✅ Skills Found")

            if found_skills:

                for skill in found_skills:
                    st.write(f"✔ {skill}")

            else:
                st.write("No matching skills found")

            st.subheader("❌ Missing Skills")

            missing_skills = []

            for skill in skills:

                if skill.lower() not in text.lower():

                    missing_skills.append(skill)

            if missing_skills:

                for skill in missing_skills:
                    st.write(f"❌ {skill}")

            else:
                st.write("No missing skills")

        # -----------------------------------
        # TAB 3
        # -----------------------------------
        with tab3:

            st.subheader("📄 ATS Resume Checker")

            if "project" not in text.lower():
                st.write("⚠ Add Projects Section")

            if "education" not in text.lower():
                st.write("⚠ Add Education Section")

            if len(text) < 1000:
                st.write("⚠ Resume content is too short")

            if len(text) > 4000:
                st.write("⚠ Resume is too lengthy")

            st.subheader("💡 Resume Suggestions")

            st.write("✔ Use action verbs like Developed, Built, Managed")
            st.write("✔ Add measurable achievements")
            st.write("✔ Keep resume ATS friendly")
            st.write("✔ Use clean formatting")
            st.write("✔ Add certifications and internships")

        # -----------------------------------
        # TAB 4
        # -----------------------------------
        with tab4:

            st.subheader("💼 Job Description Matching")

            job_description = st.text_area(
                "Paste Job Description"
            )

            if job_description:

                jd_score = 0

                jd_words = job_description.lower().split()

                for word in jd_words:

                    if word in text.lower():

                        jd_score += 1

                match_percent = min(jd_score, 100)

                st.progress(match_percent)

                st.write(f"🎯 JD Match Score: {match_percent}%")

    else:
        st.error("❌ Could not extract text from this PDF")