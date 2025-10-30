"""
Big Five Personality Test - Streamlit Application
Standalone test that candidates access via email link
Now includes Retention Risk Analysis
"""

import streamlit as st
import os
from dotenv import load_dotenv
from utils.database_manager import DatabaseManager
from utils.fitment_scorer import FitmentScorer
from utils.email_sender import EmailSender
from utils.retention_scorer import RetentionScorer
import time

load_dotenv()

# Page config
st.set_page_config(
    page_title="Big Five Personality Test | people.ai",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .test-header {
        text-align: center;
        color: white;
        padding: 2rem 0;
    }
    
    .test-header h1 {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .question-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        margin: 2rem auto;
        max-width: 800px;
    }
    
    .progress-bar-custom {
        height: 10px;
        background: #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        transition: width 0.3s ease;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    .stRadio > label {
        font-weight: 600;
        font-size: 1.1rem;
        color: #333;
    }
    
    .stRadio > div {
        margin-top: 1rem;
    }
    
    .result-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize database and services
db = DatabaseManager()
scorer = FitmentScorer()
retention_scorer = RetentionScorer()
mailer = EmailSender(
    os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    int(os.getenv('SMTP_PORT', 587)),
    os.getenv('EMAIL_ADDRESS'),
    os.getenv('EMAIL_PASSWORD')
)

# Big Five Questions (50 total - 10 per trait)
BIG5_QUESTIONS = [
    # Openness (10 questions)
    {"id": 1, "text": "I have a vivid imagination", "trait": "openness", "reverse": False},
    {"id": 2, "text": "I am interested in abstract ideas", "trait": "openness", "reverse": False},
    {"id": 3, "text": "I have difficulty understanding abstract ideas", "trait": "openness", "reverse": True},
    {"id": 4, "text": "I have a rich vocabulary", "trait": "openness", "reverse": False},
    {"id": 5, "text": "I enjoy thinking about complex topics", "trait": "openness", "reverse": False},
    {"id": 6, "text": "I am not interested in theoretical discussions", "trait": "openness", "reverse": True},
    {"id": 7, "text": "I enjoy hearing new ideas", "trait": "openness", "reverse": False},
    {"id": 8, "text": "I prefer routine to variety", "trait": "openness", "reverse": True},
    {"id": 9, "text": "I am curious about many different things", "trait": "openness", "reverse": False},
    {"id": 10, "text": "I avoid philosophical discussions", "trait": "openness", "reverse": True},
    
    # Conscientiousness (10 questions)
    {"id": 11, "text": "I am always prepared", "trait": "conscientiousness", "reverse": False},
    {"id": 12, "text": "I pay attention to details", "trait": "conscientiousness", "reverse": False},
    {"id": 13, "text": "I make a mess of things", "trait": "conscientiousness", "reverse": True},
    {"id": 14, "text": "I get chores done right away", "trait": "conscientiousness", "reverse": False},
    {"id": 15, "text": "I often forget to put things back", "trait": "conscientiousness", "reverse": True},
    {"id": 16, "text": "I like order", "trait": "conscientiousness", "reverse": False},
    {"id": 17, "text": "I shirk my duties", "trait": "conscientiousness", "reverse": True},
    {"id": 18, "text": "I follow a schedule", "trait": "conscientiousness", "reverse": False},
    {"id": 19, "text": "I am exacting in my work", "trait": "conscientiousness", "reverse": False},
    {"id": 20, "text": "I leave my belongings around", "trait": "conscientiousness", "reverse": True},
    
    # Extraversion (10 questions)
    {"id": 21, "text": "I am the life of the party", "trait": "extraversion", "reverse": False},
    {"id": 22, "text": "I don't talk a lot", "trait": "extraversion", "reverse": True},
    {"id": 23, "text": "I feel comfortable around people", "trait": "extraversion", "reverse": False},
    {"id": 24, "text": "I keep in the background", "trait": "extraversion", "reverse": True},
    {"id": 25, "text": "I start conversations", "trait": "extraversion", "reverse": False},
    {"id": 26, "text": "I have little to say", "trait": "extraversion", "reverse": True},
    {"id": 27, "text": "I talk to a lot of different people at parties", "trait": "extraversion", "reverse": False},
    {"id": 28, "text": "I don't like to draw attention to myself", "trait": "extraversion", "reverse": True},
    {"id": 29, "text": "I don't mind being the center of attention", "trait": "extraversion", "reverse": False},
    {"id": 30, "text": "I am quiet around strangers", "trait": "extraversion", "reverse": True},
    
    # Agreeableness (10 questions)
    {"id": 31, "text": "I feel others' emotions", "trait": "agreeableness", "reverse": False},
    {"id": 32, "text": "I am not really interested in others", "trait": "agreeableness", "reverse": True},
    {"id": 33, "text": "I make people feel at ease", "trait": "agreeableness", "reverse": False},
    {"id": 34, "text": "I insult people", "trait": "agreeableness", "reverse": True},
    {"id": 35, "text": "I sympathize with others' feelings", "trait": "agreeableness", "reverse": False},
    {"id": 36, "text": "I am not interested in other people's problems", "trait": "agreeableness", "reverse": True},
    {"id": 37, "text": "I have a soft heart", "trait": "agreeableness", "reverse": False},
    {"id": 38, "text": "I take time out for others", "trait": "agreeableness", "reverse": False},
    {"id": 39, "text": "I feel little concern for others", "trait": "agreeableness", "reverse": True},
    {"id": 40, "text": "I make people feel welcome", "trait": "agreeableness", "reverse": False},
    
    # Neuroticism (10 questions)
    {"id": 41, "text": "I get stressed out easily", "trait": "neuroticism", "reverse": False},
    {"id": 42, "text": "I am relaxed most of the time", "trait": "neuroticism", "reverse": True},
    {"id": 43, "text": "I worry about things", "trait": "neuroticism", "reverse": False},
    {"id": 44, "text": "I seldom feel blue", "trait": "neuroticism", "reverse": True},
    {"id": 45, "text": "I am easily disturbed", "trait": "neuroticism", "reverse": False},
    {"id": 46, "text": "I get upset easily", "trait": "neuroticism", "reverse": False},
    {"id": 47, "text": "I change my mood a lot", "trait": "neuroticism", "reverse": False},
    {"id": 48, "text": "I have frequent mood swings", "trait": "neuroticism", "reverse": False},
    {"id": 49, "text": "I get irritated easily", "trait": "neuroticism", "reverse": False},
    {"id": 50, "text": "I often feel blue", "trait": "neuroticism", "reverse": False},
]

# Initialize session state
if 'token' not in st.session_state:
    st.session_state.token = None
if 'candidate' not in st.session_state:
    st.session_state.candidate = None
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'test_start_time' not in st.session_state:
    st.session_state.test_start_time = time.time()
if 'verified' not in st.session_state:
    st.session_state.verified = False

# Get token from URL
def get_token_from_url():
    query_params = st.query_params
    return query_params.get('token', None)

# Verify token and load candidate
def verify_token(token):
    try:
        candidate = db.get_candidate_by_token(token)
        if candidate:
            st.session_state.candidate = candidate
            st.session_state.token = token
            st.session_state.verified = True
            return True
        return False
    except Exception as e:
        st.error(f"Error verifying token: {str(e)}")
        return False

# Calculate Big5 scores from answers
def calculate_big5_scores(answers):
    scores = {
        'openness': 0,
        'conscientiousness': 0,
        'extraversion': 0,
        'agreeableness': 0,
        'neuroticism': 0
    }
    
    for q_id, answer_value in answers.items():
        question = next((q for q in BIG5_QUESTIONS if q['id'] == q_id), None)
        if question:
            trait = question['trait']
            if question['reverse']:
                score = 6 - answer_value
            else:
                score = answer_value
            scores[trait] += score
    
    # Convert to 0-40 scale
    return {
        'openness': int((scores['openness'] - 10) * 40 / 40),
        'conscientiousness': int((scores['conscientiousness'] - 10) * 40 / 40),
        'extraversion': int((scores['extraversion'] - 10) * 40 / 40),
        'agreeableness': int((scores['agreeableness'] - 10) * 40 / 40),
        'neuroticism': int((scores['neuroticism'] - 10) * 40 / 40),
    }

# Main app logic
token = get_token_from_url()

if not token:
    st.markdown('<div class="test-header"><h1>🧠 Big Five Personality Test</h1></div>', unsafe_allow_html=True)
    st.error("❌ No test token found in URL. Please use the link from your email.")
    st.info("📧 Check your email for the personality test link.")
    st.stop()

# Verify token on first load
if not st.session_state.verified:
    with st.spinner("🔍 Verifying your test link..."):
        if not verify_token(token):
            st.error("❌ Invalid or expired test token. Please contact support.")
            st.stop()

candidate = st.session_state.candidate
current_q = st.session_state.current_question

# Header
st.markdown(f"""
<div class="test-header">
    <h1>🧠 Big Five Personality Test</h1>
    <p>Welcome, {candidate['name']}!</p>
</div>
""", unsafe_allow_html=True)

# Check if test is complete
if current_q >= len(BIG5_QUESTIONS):
    # Test completed
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.markdown("### 🎉 Test Complete! Calculating Your Profile...")
    
    with st.spinner("📊 Performing comprehensive analysis..."):
        # Calculate Big5 scores
        big5_scores = calculate_big5_scores(st.session_state.answers)
        
        # Save personality test results to database
        test_duration = int(time.time() - st.session_state.test_start_time)
        test_results = {
            **big5_scores,
            'duration': test_duration,
            'answers': list(st.session_state.answers.items())
        }
        
        db.save_personality_test_results(st.session_state.token, test_results)
        
        # Prepare candidate data
        candidate_data = {
            'longevity_years': candidate['longevity_years'],
            'average_experience': candidate['average_experience'],
            'workshops': candidate['workshops'],
            'trainings': candidate['trainings'],
            'total_papers': candidate['total_papers'],
            'total_patents': candidate['total_patents'],
            'achievements': candidate['achievements'],
            'books': candidate['books'],
            'state_jk': candidate['state_jk'],
            'number_of_unique_designations': candidate['number_of_unique_designations'],
            'ug_institute': candidate['ug_institute'],
            'pg_institute': candidate['pg_institute'],
            'phd_institute': candidate['phd_institute']
        }
        
        # Calculate FINAL fitment score with real Big5 data
        final_fitment = scorer.calculate_overall_fitment(candidate_data, big5_scores)
        
        # Add fitment score to candidate data for retention calculation
        candidate_data['fitment_score'] = final_fitment['overall_fitment_score']
        
        # Calculate RETENTION RISK
        retention_result = retention_scorer.calculate_retention_risk(
            candidate_data,
            final_fitment['overall_fitment_score'],
            big5_scores,
            final_fitment['category']
        )
        
        # Save final fitment score
        db.save_fitment_score(candidate['candidate_id'], final_fitment)
        
        # Send comprehensive final email with ALL results
        email_sent = mailer.send_comprehensive_results_email(
            candidate['email'],
            candidate['name'],
            final_fitment,
            big5_scores,
            retention_result
        )
        
        # Log email
        db.log_email(
            candidate['candidate_id'],
            'comprehensive_results',
            candidate['email'],
            f"Complete Assessment Results - Fitment: {final_fitment['overall_fitment_score']:.0f}/100",
            'sent' if email_sent else 'failed'
        )
    
    # Display comprehensive results
    st.success("✅ Complete assessment finished!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Fitment Score Card
    fitment_score = final_fitment['overall_fitment_score']
    fitment_emoji = "🏆" if fitment_score >= 80 else ("✨" if fitment_score >= 60 else "📈")
    
    st.markdown(f"""
    <div class="result-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-align: center;">
        <h2 style="margin: 0;">🎯 Your Final Fitment Score</h2>
        <h1 style="font-size: 4rem; margin: 1rem 0;">{fitment_emoji} {fitment_score:.0f}/100</h1>
        <h3 style="margin: 0;">Category: {final_fitment['category']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Big5 Personality Profile
    st.markdown("### 🧬 Your Personality Profile")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    traits_display = [
        (col1, "🎨 Openness", big5_scores['openness']),
        (col2, "📋 Conscient.", big5_scores['conscientiousness']),
        (col3, "🎤 Extravert.", big5_scores['extraversion']),
        (col4, "🤝 Agreeable.", big5_scores['agreeableness']),
        (col5, "😌 Stability", 40 - big5_scores['neuroticism'])
    ]
    
    for col, name, score in traits_display:
        with col:
            st.metric(name, f"{score}/40")
            st.progress(score / 40)
    
    # Retention Risk Analysis
    st.markdown("### 📊 Retention Risk Analysis")
    
    retention_score = retention_result['retention_score']
    retention_risk = retention_result['retention_risk']
    
    risk_colors = {'Low': '#10B981', 'Medium': '#F59E0B', 'High': '#EF4444'}
    risk_color = risk_colors[retention_risk]
    
    st.markdown(f"""
    <div class="result-card" style="border-left: 5px solid {risk_color};">
        <h3 style="color: {risk_color}; margin-top: 0;">Retention Score: {retention_score}/100</h3>
        <p style="font-size: 1.2rem; margin: 0.5rem 0;"><strong>Risk Level:</strong> <span style="color: {risk_color};">{retention_risk} Risk</span></p>
        <p style="margin: 0.5rem 0;"><strong>Risk Flags Identified:</strong> {retention_result['flag_count']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Component Scores
    with st.expander("📈 View Retention Component Scores"):
        comp = retention_result['component_scores']
        st.markdown(f"""
        - **Job Stability:** {comp['stability']}/100
        - **Personality Fit:** {comp['personality']}/100
        - **Professional Engagement:** {comp['engagement']}/100
        - **Fitment Factor:** {comp['fitment_factor']}/100
        """)
    
    # Risk Flags
    if retention_result['risk_flags']:
        with st.expander("⚠️ View Risk Flags"):
            for flag in retention_result['risk_flags']:
                st.warning(f"• {flag}")
    
    # Key Recommendations
    st.markdown("### 💡 Key Recommendations")
    for i, insight in enumerate(retention_result['insights'][:5], 1):
        st.info(f"{insight}")
    
    # Email Status
    if email_sent:
        st.success("📧 Complete results have been sent to your email!")
    else:
        st.error("⚠️ Email failed to send. Please contact support for your results.")
    
    st.balloons()
    st.stop()

# Display current question
question = BIG5_QUESTIONS[current_q]

st.markdown('<div class="question-card">', unsafe_allow_html=True)

# Progress bar
progress = (current_q / len(BIG5_QUESTIONS)) * 100
st.markdown(f"""
<div style="margin-bottom: 2rem;">
    <p style="color: #666; margin-bottom: 0.5rem;">Question {current_q + 1} of {len(BIG5_QUESTIONS)}</p>
    <div class="progress-bar-custom">
        <div class="progress-fill" style="width: {progress}%"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# Question
st.markdown(f"### {question['text']}")

# Answer options
answer = st.radio(
    "Select your response:",
    options=[1, 2, 3, 4, 5],
    format_func=lambda x: {
        1: "Strongly Disagree",
        2: "Disagree",
        3: "Neutral",
        4: "Agree",
        5: "Strongly Agree"
    }[x],
    key=f"q_{question['id']}",
    index=st.session_state.answers.get(question['id'], 3) - 1 if question['id'] in st.session_state.answers else 2
)

st.markdown('</div>', unsafe_allow_html=True)

# Navigation buttons
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if current_q > 0:
        if st.button("← Previous", use_container_width=True):
            st.session_state.current_question -= 1
            st.rerun()

with col3:
    if st.button("Next →" if current_q < len(BIG5_QUESTIONS) - 1 else "Finish", 
                 use_container_width=True, type="primary"):
        # Save answer
        st.session_state.answers[question['id']] = answer
        st.session_state.current_question += 1
        st.rerun()