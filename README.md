# 👥 people.ai - AI Recruitment Platform

An intelligent recruitment system that uses AI to parse resumes, calculate fitment scores, and match candidates with job requirements.

## 🚀 Features

- **AI-Powered Resume Parsing** - Automatic extraction using Google Gemini API
- **Fitment Score Calculation** - ML-based scoring algorithm
- **Big Five Personality Assessment** - Personality trait analysis
- **Email Notifications** - Automated confirmation and score emails
- **Beautiful Dashboard** - Modern, animated UI with glassmorphism design
- **Real-time Processing** - Instant score calculation and feedback

## 📁 Project Structure

```
people_ai_recruitment/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (API keys)
│
└── utils/
    ├── __init__.py
    ├── resume_parser.py        # Gemini AI resume parsing
    ├── fitment_scorer.py       # Fitment score calculation
    └── email_sender.py         # Email notification system
```

## 🛠️ Installation

### Step 1: Clone/Create Project
```bash
mkdir people_ai_recruitment
cd people_ai_recruitment
mkdir utils
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Create a `.env` file:
```env
GEMINI_API_KEY=your_gemini_api_key_here
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

#### Getting Gemini API Key:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create new API key
3. Copy and paste into `.env`

#### Getting Gmail App Password:
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Security → 2-Step Verification (enable if not enabled)
3. App Passwords → Generate
4. Copy 16-character password into `.env`

### Step 4: Run Application
```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

## 📊 How It Works

### 1. Upload Resume
- Drag & drop or click to upload
- Supports PDF, DOCX, DOC, TXT formats
- Max file size: 10MB

### 2. AI Parsing
- Gemini AI extracts all relevant information
- Auto-fills form with parsed data
- User can review and edit

### 3. Fitment Score Calculation
The system calculates a fitment score (0-100) based on:

**Dataset Score (30% or 70% weight):**
- Experience & Longevity (60%)
- Professional Development (9%)
- Research & Publications (17%)
- Achievements & Recognition (14%)

**Big Five Personality Score (70% or 30% weight):**
- Openness to Experience
- Conscientiousness
- Extraversion
- Agreeableness
- Emotional Stability (reversed Neuroticism)

### 4. Category Classification
- **Experienced**: Longevity ≥5 years AND Experience ≥3 years
- **Inexperienced**: Longevity >1 year AND Experience >1 year
- **Fresher**: Others

### 5. Email Notifications
- **Confirmation Email**: Sent immediately with personality test link
- **Score Email**: Sent after personality test completion with detailed breakdown

## 🎨 Customization

### Change Color Scheme
Edit `app.py` CSS section:
```python
# Primary purple gradient
background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);

# Accent colors
#c084fc  # Light purple
#6d28d9  # Dark purple
```

### Modify Scoring Weights
Edit `utils/fitment_scorer.py`:
```python
scores['longevity'] = self.score_longevity(data['longevity_years']) * 0.30  # Change weight
```

### Update Parsing Prompt
Edit `utils/resume_parser.py` to change what fields are extracted.

## 🐛 Troubleshooting

### Error: "404 models/gemini-pro not found"
**Solution:** Update has been applied. Now using `gemini-1.5-flash` model.

### Error: "GEMINI_API_KEY not found"
**Solution:** Check `.env` file exists and contains valid API key.

### Email Not Sending
**Solutions:**
- Verify Gmail app password is correct
- Enable 2-Step Verification on Google account
- Check SMTP settings (port 587 for TLS)
- Try different email provider if Gmail blocks

### Resume Parsing Inaccurate
**Solutions:**
- Ensure resume has clear structure
- Try different file format (PDF usually best)
- Adjust Gemini prompt in `resume_parser.py`
- Check resume text extraction is working

### UI Not Loading Properly
**Solutions:**
- Clear browser cache (Ctrl+Shift+R)
- Check Streamlit version: `pip install --upgrade streamlit`
- Try different browser

## 📧 Contact & Support

For issues or questions:
1. Check the troubleshooting section above
2. Review error messages in terminal
3. Verify all dependencies installed correctly
4. Check `.env` configuration

## 🔐 Security Notes

- Never commit `.env` file to version control
- Keep API keys secure and rotate regularly
- Use app-specific passwords for email
- Consider rate limiting for production use

## 📝 Future Enhancements

- [ ] Real personality test integration
- [ ] Database storage for applications
- [ ] Admin dashboard for HR team
- [ ] Advanced analytics and reporting
- [ ] Resume comparison tool
- [ ] Bulk resume processing
- [ ] Integration with ATS systems
- [ ] Video interview scheduling

## 📄 License

This project is for educational and internal use.

---

**Version:** 1.0.0  
**Last Updated:** October 2025  
**Tech Stack:** Streamlit, Google Gemini AI, Python 3.8+