import streamlit as st
import os
from dotenv import load_dotenv 
from utils.resume_parser import ResumeParser
from utils.fitment_scorer import FitmentScorer
from utils.email_sender import EmailSender
from utils.database_manager import DatabaseManager
import json

# Load environment variables
load_dotenv()

# Initialize database
db = DatabaseManager()

# Page configuration
st.set_page_config(
    page_title="people.ai - AI Recruitment",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background with animated gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom header with glow effect */
    .main-header {
        text-align: center;
        padding: 3rem 0 2rem 0;
        margin-bottom: 3rem;
        position: relative;
    }
    
    .main-header h1 {
        color: #c084fc;
        font-size: 5rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 0 40px rgba(192, 132, 252, 0.6),
                     0 0 80px rgba(192, 132, 252, 0.4);
        letter-spacing: -2px;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px rgba(192, 132, 252, 0.4), 0 0 40px rgba(192, 132, 252, 0.3); }
        to { text-shadow: 0 0 40px rgba(192, 132, 252, 0.8), 0 0 80px rgba(192, 132, 252, 0.6); }
    }
    
    .main-header p {
        color: #e0e7ff;
        font-size: 1.8rem;
        margin-top: 1rem;
        font-weight: 300;
        letter-spacing: 1px;
    }
    
    /* Upload section with glassmorphism */
    .upload-container {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(192, 132, 252, 0.3);
        border-radius: 30px;
        padding: 4rem;
        margin: 2rem auto;
        max-width: 900px;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3),
                    inset 0 0 60px rgba(192, 132, 252, 0.1);
        transition: all 0.3s ease;
    }
    
    .upload-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.4),
                    inset 0 0 80px rgba(192, 132, 252, 0.15);
    }
    
    /* File uploader styling */
    [data-testid="stFileUploader"] {
        background: rgba(139, 92, 246, 0.1);
        border: 3px dashed rgba(192, 132, 252, 0.5);
        border-radius: 20px;
        padding: 3rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #c084fc;
        background: rgba(139, 92, 246, 0.15);
        transform: scale(1.02);
    }
    
    [data-testid="stFileUploader"] label {
        color: #e0e7ff !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
    }
    
    /* Form styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        background-color: rgba(30, 41, 59, 0.8) !important;
        color: #e2e8f0 !important;
        border: 2px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 12px !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #c084fc !important;
        box-shadow: 0 0 20px rgba(192, 132, 252, 0.3) !important;
    }
    
    .stTextInput > label,
    .stNumberInput > label,
    .stSelectbox > label,
    .stTextArea > label {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Button styling with animation */
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 2.5rem;
        font-size: 1.2rem;
        font-weight: 700;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.6);
        background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Success/Error messages with better styling */
    .stSuccess {
        background: rgba(16, 185, 129, 0.15);
        border: 2px solid rgba(16, 185, 129, 0.5);
        border-radius: 15px;
        padding: 1.5rem;
        color: #6ee7b7;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.15);
        border: 2px solid rgba(239, 68, 68, 0.5);
        border-radius: 15px;
        padding: 1.5rem;
        color: #fca5a5;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.15);
        border: 2px solid rgba(245, 158, 11, 0.5);
        border-radius: 15px;
        padding: 1.5rem;
        color: #fcd34d;
    }
    
    .stInfo {
        background: rgba(59, 130, 246, 0.15);
        border: 2px solid rgba(59, 130, 246, 0.5);
        border-radius: 15px;
        padding: 1.5rem;
        color: #93c5fd;
    }
    
    /* Score card with premium design */
    .score-card {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.9) 0%, rgba(109, 40, 217, 0.9) 100%);
        border-radius: 30px;
        padding: 3rem;
        text-align: center;
        color: white;
        margin: 2rem 0;
        box-shadow: 0 20px 60px rgba(139, 92, 246, 0.5),
                    inset 0 0 100px rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .score-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transform: rotate(45deg);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .score-value {
        font-size: 5rem;
        font-weight: 900;
        margin: 1.5rem 0;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.5);
        position: relative;
        z-index: 1;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #c084fc !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #cbd5e1 !important;
        font-size: 1.1rem !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(139, 92, 246, 0.2) !important;
        color: #e2e8f0 !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        border: 2px solid rgba(192, 132, 252, 0.3) !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(139, 92, 246, 0.3) !important;
        border-color: #c084fc !important;
    }
    
    /* Section headers */
    h1, h2, h3 {
        color: #e0e7ff !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(192, 132, 252, 0.5), transparent);
        margin: 2rem 0;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #c084fc !important;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background-color: #8b5cf6 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'upload'
if 'parsed_data' not in st.session_state:
    st.session_state.parsed_data = None
if 'fitment_result' not in st.session_state:
    st.session_state.fitment_result = None
if 'resume_bytes' not in st.session_state:
    st.session_state.resume_bytes = None
if 'resume_filename' not in st.session_state:
    st.session_state.resume_filename = None

# Initialize API clients
@st.cache_resource
def init_clients():
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    email_address = os.getenv('EMAIL_ADDRESS')
    email_password = os.getenv('EMAIL_PASSWORD')
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    
    parser = ResumeParser(gemini_api_key)
    scorer = FitmentScorer()
    mailer = EmailSender(smtp_server, smtp_port, email_address, email_password)
    
    return parser, scorer, mailer

try:
    parser, scorer, mailer = init_clients()
except Exception as e:
    st.error(f"⚠️ Configuration Error: {str(e)}")
    st.info("Please check your .env file and ensure all API keys are configured correctly.")
    st.stop()

# Header
st.markdown("""
<div class="main-header">
    <h1>people.ai</h1>
    <p>AI that finds your perfect hire</p>
</div>
""", unsafe_allow_html=True)

# =========================
# PAGE 1: UPLOAD RESUME
# =========================
if st.session_state.page == 'upload':
    st.markdown('<div class="upload-container">', unsafe_allow_html=True)
    
    st.markdown("### 📄 Upload Your Resume")
    st.markdown("---")
    
    uploaded_file = st.file_uploader(
        "Drag & Drop Resume Here or Click to Upload",
        type=['pdf', 'docx', 'doc', 'txt'],
        help="Supported formats: PDF, DOCX, DOC, TXT (Max 10MB)",
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        st.success(f"✅ File uploaded successfully: **{uploaded_file.name}**")
        
        file_size = len(uploaded_file.getvalue()) / (1024 * 1024)  # Size in MB
        st.info(f"📊 File size: {file_size:.2f} MB")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 PARSE RESUME", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Read file bytes
                    status_text.text("📖 Reading file...")
                    progress_bar.progress(25)
                    file_bytes = uploaded_file.getvalue()
                    
                    # Store for later use
                    st.session_state.resume_bytes = file_bytes
                    st.session_state.resume_filename = uploaded_file.name
                    
                    # Parse resume
                    status_text.text("🤖 AI is analyzing your resume...")
                    progress_bar.progress(50)
                    parsed_data = parser.parse_resume(file_bytes, uploaded_file.name)
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Parsing complete!")
                    
                    st.session_state.parsed_data = parsed_data
                    st.session_state.page = 'form'
                    st.balloons()
                    st.rerun()
                    
                except Exception as e:
                    progress_bar.empty()
                    status_text.empty()
                    st.error(f"❌ Error parsing resume: {str(e)}")
                    st.info("💡 Try: 1) Check your Gemini API key 2) Ensure file is readable 3) Try a different file format")
    else:
        st.info("👆 Click above or drag & drop your resume to get started!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# PAGE 2: FORM VALIDATION
# =========================
elif st.session_state.page == 'form':
    st.markdown("### 📋 Verify & Complete Your Information")
    st.markdown("Please review and edit the extracted information if needed")
    st.markdown("---")
    
    data = st.session_state.parsed_data
    
    # Create form
    with st.form("candidate_form"):
        # Personal Information
        st.markdown("## 👤 Personal Information")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            name = st.text_input("Full Name *", value=data.get('name', ''))
        with col2:
            email = st.text_input("Email *", value=data.get('email', ''))
        with col3:
            phone = st.text_input("Phone Number *", value=data.get('phone', ''))
        
        st.markdown("---")
        
        # Educational Background
        st.markdown("## 🎓 Educational Background")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Undergraduate**")
            ug_institute_name = st.text_input("UG Institute Name", 
                                               value=data.get('ug_institute_name', ''),
                                               key='ug_name')
            ug_institute = st.selectbox("Premier Institute?", 
                                        options=[0, 1],
                                        index=data.get('ug_institute', 0),
                                        format_func=lambda x: "✅ Yes" if x == 1 else "❌ No",
                                        key='ug_premier')
        
        with col2:
            st.markdown("**Postgraduate**")
            pg_institute_name = st.text_input("PG Institute Name", 
                                               value=data.get('pg_institute_name', 'None'),
                                               key='pg_name')
            pg_institute = st.selectbox("Premier Institute?", 
                                        options=[0, 1],
                                        index=data.get('pg_institute', 0),
                                        format_func=lambda x: "✅ Yes" if x == 1 else "❌ No",
                                        key='pg_premier')
        
        with col3:
            st.markdown("**Doctorate (PhD)**")
            phd_institute_name = st.text_input("PhD Institute Name", 
                                                value=data.get('phd_institute_name', 'None'),
                                                key='phd_name')
            phd_institute = st.selectbox("Premier Institute?", 
                                         options=[0, 1],
                                         index=data.get('phd_institute', 0),
                                         format_func=lambda x: "✅ Yes" if x == 1 else "❌ No",
                                         key='phd_premier')
        
        st.markdown("---")
        
        # Professional Experience
        st.markdown("## 💼 Professional Experience")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            longevity_years = st.number_input("Average Tenure (Years)", 
                                              min_value=0.0, 
                                              value=float(data.get('longevity_years', 0)),
                                              step=0.1,
                                              help="Average time spent at each job")
        
        with col2:
            average_experience = st.number_input("Total Experience (Years)", 
                                                 min_value=0.0, 
                                                 value=float(data.get('average_experience', 0)),
                                                 step=0.1,
                                                 help="Total professional work experience")
        
        with col3:
            number_of_unique_designations = st.number_input("Unique Job Titles", 
                                                            min_value=0, 
                                                            value=int(data.get('number_of_unique_designations', 0)),
                                                            help="Number of different positions held")
        
        st.markdown("---")
        
        # Professional Development
        st.markdown("## 📚 Professional Development")
        
        col1, col2 = st.columns(2)
        
        with col1:
            workshops = st.number_input("Workshops Attended", 
                                       min_value=0, 
                                       value=int(data.get('workshops', 0)))
            trainings = st.number_input("Training Programs", 
                                       min_value=0, 
                                       value=int(data.get('trainings', 0)))
        
        with col2:
            with st.expander("📝 View Workshops List"):
                st.write(data.get('workshops_list', []))
            with st.expander("📝 View Trainings List"):
                st.write(data.get('trainings_list', []))
        
        st.markdown("---")
        
        # Research & Achievements
        st.markdown("## 🏆 Research & Achievements")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_papers = st.number_input("Research Papers", 
                                          min_value=0, 
                                          value=int(data.get('total_papers', 0)))
        
        with col2:
            total_patents = st.number_input("Patents", 
                                           min_value=0, 
                                           value=int(data.get('total_patents', 0)))
        
        with col3:
            achievements = st.number_input("Achievements/Awards", 
                                          min_value=0, 
                                          value=int(data.get('achievements', 0)))
        
        with col4:
            books = st.number_input("Books Authored", 
                                   min_value=0, 
                                   value=int(data.get('books', 0)))
        
        # Expandable sections for lists
        col1, col2 = st.columns(2)
        with col1:
            with st.expander("📄 View Research Papers"):
                papers_list = data.get('research_papers_list', [])
                if papers_list:
                    for i, paper in enumerate(papers_list, 1):
                        st.write(f"{i}. {paper}")
                else:
                    st.write("No papers listed")
            
            with st.expander("🏅 View Achievements"):
                achievements_list = data.get('achievements_list', [])
                if achievements_list:
                    for i, ach in enumerate(achievements_list, 1):
                        st.write(f"{i}. {ach}")
                else:
                    st.write("No achievements listed")
        
        with col2:
            with st.expander("⚖️ View Patents"):
                patents_list = data.get('patents_list', [])
                if patents_list:
                    for i, patent in enumerate(patents_list, 1):
                        st.write(f"{i}. {patent}")
                else:
                    st.write("No patents listed")
            
            with st.expander("📚 View Books"):
                books_list = data.get('books_list', [])
                if books_list:
                    for i, book in enumerate(books_list, 1):
                        st.write(f"{i}. {book}")
                else:
                    st.write("No books listed")
        
        st.markdown("---")
        
        # Additional Information
        st.markdown("## 🌍 Additional Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            state_jk = st.selectbox("From Jammu & Kashmir?", 
                                   options=[0, 1],
                                   index=data.get('state_jk', 0),
                                   format_func=lambda x: "✅ Yes" if x == 1 else "❌ No")
        
        with col2:
            best_fit = st.text_input("Best Fit For (Job Role)", 
                                    value=data.get('best_fit_for', ''),
                                    help="Suggested suitable role based on your profile")
        
        # Skills Section
        with st.expander("💻 View Skills"):
            skills_list = data.get('skills', [])
            if skills_list:
                st.write(", ".join(skills_list))
            else:
                st.write("No skills extracted")
        
        # Projects Section
        with st.expander("🚀 View Projects"):
            projects_list = data.get('projects', [])
            if projects_list:
                for i, project in enumerate(projects_list, 1):
                    st.write(f"{i}. {project}")
            else:
                st.write("No projects listed")
        
        st.markdown("---")
        
        # Form submission buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            back_button = st.form_submit_button("← Back", use_container_width=True)
        
        with col2:
            submit_button = st.form_submit_button("✅ SUBMIT APPLICATION", 
                                                  use_container_width=True,
                                                  type="primary")
        
        with col3:
            st.write("")  # Spacer
        
        if back_button:
            st.session_state.page = 'upload'
            st.session_state.parsed_data = None
            st.rerun()
        
        if submit_button:
            # Validation
            if not name or not email or not phone:
                st.error("❌ Please fill in all required fields (Name, Email, Phone)")
            elif '@' not in email:
                st.error("❌ Please enter a valid email address")
            else:
                # Prepare candidate data
                candidate_data = {
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'ug_institute_name': ug_institute_name,
                    'pg_institute_name': pg_institute_name,
                    'phd_institute_name': phd_institute_name,
                    'longevity_years': longevity_years,
                    'average_experience': average_experience,
                    'workshops': workshops,
                    'trainings': trainings,
                    'total_papers': total_papers,
                    'total_patents': total_patents,
                    'achievements': achievements,
                    'books': books,
                    'state_jk': state_jk,
                    'number_of_unique_designations': number_of_unique_designations,
                    'ug_institute': ug_institute,
                    'pg_institute': pg_institute,
                    'phd_institute': phd_institute,
                    'workshops_list': data.get('workshops_list', []),
                    'trainings_list': data.get('trainings_list', []),
                    'research_papers_list': data.get('research_papers_list', []),
                    'patents_list': data.get('patents_list', []),
                    'books_list': data.get('books_list', []),
                    'achievements_list': data.get('achievements_list', []),
                    'skills': data.get('skills', []),
                    'skills_count': data.get('skills_count', 0),
                    'projects': data.get('projects', []),
                    'projects_count': data.get('projects_count', 0),
                    'best_fit_for': best_fit,
                    'address': data.get('address', ''),
                    'summary': data.get('summary', ''),
                    'ug_institute_code': data.get('ug_institute_code', ''),
                    'pg_institute_code': data.get('pg_institute_code', ''),
                    'phd_institute_code': data.get('phd_institute_code', '')
                }
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Calculate INITIAL fitment score (without Big5)
                    status_text.text("🎯 Calculating initial score...")
                    progress_bar.progress(30)
                    
                    fitment_result = scorer.calculate_overall_fitment(candidate_data)
                    
                    # Save to database
                    status_text.text("💾 Saving to database...")
                    progress_bar.progress(50)
                    
                    # Save candidate
                    candidate_id = db.save_candidate(candidate_data)
                    
                    # Save resume if available
                    if st.session_state.resume_bytes:
                        db.save_resume(
                            candidate_id,
                            st.session_state.resume_filename,
                            st.session_state.resume_bytes,
                            st.session_state.resume_filename.split('.')[-1],
                            str(data)
                        )
                    
                    # Save initial fitment score
                    db.save_fitment_score(candidate_id, fitment_result)
                    
                    # Create personality test token
                    status_text.text("🧠 Creating personality test...")
                    progress_bar.progress(60)
                    test_token = db.create_personality_test(candidate_id)
                    
                    # Build test URL (Streamlit big5 test on port 8502)
                    test_url = f"http://localhost:8502?token={test_token}"
                    
                    # Send confirmation email with test link
                    status_text.text("📧 Sending confirmation email...")
                    progress_bar.progress(80)
                    
                    email_sent = mailer.send_confirmation_email(
                        email, 
                        name, 
                        test_token,
                        "http://localhost:8502"  # Big5 test URL
                    )
                    
                    # Log email
                    db.log_email(
                        candidate_id,
                        'confirmation',
                        email,
                        'Application Received - Next Steps',
                        'sent' if email_sent else 'failed',
                        None if email_sent else 'SMTP error'
                    )
                    
                    progress_bar.progress(100)
                    status_text.empty()
                    progress_bar.empty()
                    
                    # Store in session
                    st.session_state.fitment_result = fitment_result
                    st.session_state.candidate_data = candidate_data
                    st.session_state.candidate_id = candidate_id
                    st.session_state.test_token = test_token
                    st.session_state.test_url = test_url
                    
                    if email_sent:
                        st.success("✅ Application submitted successfully!")
                        st.info(f"📧 Check your email for the personality test link")
                    else:
                        st.warning(f"⚠️ Application submitted but email failed to send.")
                        st.info(f"🔗 Direct test link: {test_url}")
                    
                    st.session_state.page = 'results'
                    st.balloons()
                    st.rerun()
                    
                except Exception as e:
                    progress_bar.empty()
                    status_text.empty()
                    st.error(f"❌ Error processing application: {str(e)}")

# =========================
# PAGE 3: RESULTS
# =========================
elif st.session_state.page == 'results':
    result = st.session_state.fitment_result
    candidate_data = st.session_state.candidate_data
    test_url = st.session_state.get('test_url', 'http://localhost:8502')
    
    st.markdown("### 🎉 Application Submitted Successfully!")
    st.markdown("---")
    
    # Display PRELIMINARY fitment score
    score = result['overall_fitment_score']
    
    st.markdown(f"""
    <div class="score-card">
        <h2 style="margin: 0; font-size: 1.5rem; opacity: 0.9;">Preliminary Fitment Score</h2>
        <div class="score-value">📊 {score:.2f}/100</div>
        <h3 style="margin: 0; font-size: 1.5rem; font-weight: 600;">Category: {result['category']}</h3>
        <p style="margin-top: 1rem; opacity: 0.8; font-size: 0.95rem;">
            ⚠️ This is a preliminary score. Your final score will be calculated after completing the personality test.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Next steps with test link
    st.markdown("### 🧠 Next Step: Complete Personality Test")
    
    st.info(f"""
    **Important:** Your final fitment score will include your personality assessment results.
    
    📝 **Big Five Personality Test** (50 questions, ~10 minutes)
    
    ✅ Click the button below or use the link from your email
    """)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🧠 TAKE PERSONALITY TEST NOW", use_container_width=True, type="primary"):
            st.markdown(f'<meta http-equiv="refresh" content="0;url={test_url}">', unsafe_allow_html=True)
            st.info(f"🔗 If not redirected, click here: {test_url}")
    
    st.markdown("---")
    
    # Score breakdown (preliminary)
    st.markdown("### 📊 Preliminary Score Breakdown")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="📂 Dataset Score",
            value=f"{result['fitment_score']:.2f}",
            help=result['breakdown']['dataset_contribution']
        )
    
    with col2:
        st.metric(
            label="🧠 Personality Score", 
            value=f"{result['big5_score']:.2f}",
            help="Based on default values - will update after test"
        )
    
    with col3:
        st.metric(
            label="🎯 Preliminary Score",
            value=f"{result['overall_fitment_score']:.2f}",
            delta=f"{result['category']}"
        )
    
    st.markdown("---")
    
    # Timeline
    st.markdown("### 📬 What Happens Next")
    
    st.markdown("""
    1. ✅ **Complete the personality test** (link above or in email)
    2. 📊 **Your final fitment score** will be calculated automatically
    3. 📧 **Receive results via email** with detailed breakdown
    4. 🤝 **Our team reviews** your complete profile
    5. 📞 **We contact you** if your profile matches (5-7 business days)
    """)
    
    st.markdown("---")
    
    # Test link reminder
    with st.expander("🔗 View Test Link Again"):
        st.code(test_url, language="text")
        st.caption("Copy this link if you need to access the test later")
    
    # Detailed breakdown
    with st.expander("🔍 View Preliminary Breakdown (JSON)"):
        st.json(result)
    
    st.markdown("---")
    
    # Action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏠 START NEW APPLICATION", use_container_width=True):
            st.session_state.page = 'upload'
            st.session_state.parsed_data = None
            st.session_state.fitment_result = None
            st.session_state.candidate_data = None
            st.session_state.resume_bytes = None
            st.session_state.resume_filename = None
            st.rerun()
    
    with col2:
        if st.button("📥 DOWNLOAD PRELIMINARY RESULTS", use_container_width=True):
            import json
            result_json = json.dumps(result, indent=2)
            st.download_button(
                label="💾 Download JSON Report",
                data=result_json,
                file_name=f"preliminary_report_{candidate_data['name'].replace(' ', '_')}.json",
                mime="application/json",
                use_container_width=True
            )