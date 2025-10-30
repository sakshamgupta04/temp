# 🚀 Complete Setup Guide - people.ai with Big5 Integration

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- Git
- VS Code or any code editor

## 🔧 Step-by-Step Setup

### Part 1: Python Backend Setup

#### 1. Install Python Dependencies

```bash
cd people_ai_recruitment
pip install -r requirements.txt
```

#### 2. Configure Environment Variables

Create `.env` file in project root:

```properties
GEMINI_API_KEY=your_gemini_api_key
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
PERSONALITY_TEST_URL=http://localhost:5173
API_PORT=5000
```

#### 3. Test Database Initialization

```bash
python -c "from utils.database_manager import DatabaseManager; db = DatabaseManager(); print('Database initialized!')"
```

You should see: `✅ Database initialized successfully`

### Part 2: Big5 React App Setup

#### 1. Navigate to Big5 Folder

```bash
cd Big5
```

#### 2. Install Node Dependencies

```bash
npm install
```

#### 3. Create Big5 .env File

Create `Big5/.env`:

```properties
VITE_API_URL=http://localhost:5000
```

#### 4. Add API Integration Files

**Create `Big5/src/api/submit.ts`** - Copy the code provided earlier

**Update `Big5/src/App.tsx`** - Add the integration code provided

### Part 3: Running the Complete System

You need to run **3 separate terminals**:

#### Terminal 1: Streamlit App (Main Application)

```bash
cd people_ai_recruitment
streamlit run app.py
```

Access at: `http://localhost:8501`

#### Terminal 2: Flask API Server (Receives Big5 Results)

```bash
cd people_ai_recruitment
python -m utils.big5_integration
```

Or create a simple runner `run_api.py`:

```python
from utils.big5_integration import app
import os

if __name__ == '__main__':
    port = int(os.getenv('API_PORT', 5000))
    print(f"🚀 API Server running on http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
```

Then run:
```bash
python run_api.py
```

Access at: `http://localhost:5000`

#### Terminal 3: Big5 React App

```bash
cd Big5
npm run dev
```

Access at: `http://localhost:5173`

## 📊 Complete Workflow

### 1. Candidate Uploads Resume
- Go to `http://localhost:8501`
- Upload resume (PDF/DOCX/TXT)
- AI parses resume automatically

### 2. Candidate Fills Form
- Review and edit parsed information
- Submit application

### 3. System Processes
- ✅ Saves candidate data to database
- ✅ Saves resume file to database
- ✅ Calculates initial fitment score
- ✅ Creates personality test token
- ✅ Sends email with test link

### 4. Candidate Takes Test
- Clicks link in email
- Redirected to `http://localhost:5173?token=xxx`
- Completes Big5 personality test
- Test results sent to API automatically

### 5. Final Processing
- ✅ API receives test results
- ✅ Saves personality scores to database
- ✅ Recalculates fitment score with real Big5 data
- ✅ Sends final fitment score email

## 🗄️ Database Structure

The system creates `database.db` with these tables:

- **candidates** - All candidate profile data
- **resumes** - Resume files and extracted text
- **fitment_scores** - Calculated fitment scores
- **personality_tests** - Big5 test results
- **email_logs** - Email sending history

## 🔍 Verify Everything Works

### Test 1: API Health Check

```bash
curl http://localhost:5000/health
```

Expected: `{"status":"healthy"}`

### Test 2: Token Verification

```bash
curl http://localhost:5000/api/test/verify/test_token_here
```

### Test 3: Database Check

```bash
python -c "from utils.database_manager import DatabaseManager; db = DatabaseManager(); print(db.get_all_candidates())"
```

## 📧 Email Configuration

### Gmail Setup

1. **Enable 2-Step Verification**
   - Go to Google Account → Security
   - Enable 2-Step Verification

2. **Generate App Password**
   - Google Account → Security → App Passwords
   - Select "Mail" and "Other"
   - Copy 16-character password
   - Use in `.env` as `EMAIL_PASSWORD`

## 🐛 Troubleshooting

### Issue: Database not found

**Solution:**
```bash
python -c "from utils.database_manager import DatabaseManager; DatabaseManager()"
```

### Issue: Flask port already