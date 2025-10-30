"""
Database Manager for storing candidate data, resumes, and personality test results
Uses SQLite for simplicity - can be upgraded to PostgreSQL/MySQL later
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
import hashlib

class DatabaseManager:
    def __init__(self, db_path: str = "database.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Create database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Candidates table - main profile data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending',
                
                -- Personal Info
                address TEXT,
                summary TEXT,
                
                -- Education
                ug_institute_name TEXT,
                ug_institute_code TEXT,
                pg_institute_name TEXT,
                pg_institute_code TEXT,
                phd_institute_name TEXT,
                phd_institute_code TEXT,
                ug_institute INTEGER DEFAULT 0,
                pg_institute INTEGER DEFAULT 0,
                phd_institute INTEGER DEFAULT 0,
                
                -- Experience
                longevity_years REAL DEFAULT 0,
                average_experience REAL DEFAULT 0,
                number_of_unique_designations INTEGER DEFAULT 0,
                
                -- Professional Development
                workshops INTEGER DEFAULT 0,
                trainings INTEGER DEFAULT 0,
                workshops_list TEXT,
                trainings_list TEXT,
                
                -- Research & Publications
                total_papers INTEGER DEFAULT 0,
                total_patents INTEGER DEFAULT 0,
                books INTEGER DEFAULT 0,
                achievements INTEGER DEFAULT 0,
                research_papers_list TEXT,
                patents_list TEXT,
                books_list TEXT,
                achievements_list TEXT,
                
                -- Additional
                state_jk INTEGER DEFAULT 0,
                skills TEXT,
                skills_count INTEGER DEFAULT 0,
                projects TEXT,
                projects_count INTEGER DEFAULT 0,
                best_fit_for TEXT
            )
        ''')
        
        # Resume files table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate_id TEXT NOT NULL,
                filename TEXT NOT NULL,
                file_content BLOB NOT NULL,
                file_type TEXT NOT NULL,
                extracted_text TEXT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id)
            )
        ''')
        
        # Fitment scores table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fitment_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate_id TEXT NOT NULL,
                category TEXT,
                raw_dataset_score REAL,
                fitment_score REAL,
                big5_score REAL,
                overall_fitment_score REAL,
                
                -- Big5 trait scores
                openness_score REAL,
                conscientiousness_score REAL,
                extraversion_score REAL,
                agreeableness_score REAL,
                neuroticism_score REAL,
                
                calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id)
            )
        ''')
        
        # Personality test results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personality_tests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate_id TEXT NOT NULL,
                test_token TEXT UNIQUE NOT NULL,
                test_status TEXT DEFAULT 'pending',
                
                -- Big5 Scores (raw from test)
                openness INTEGER,
                conscientiousness INTEGER,
                extraversion INTEGER,
                agreeableness INTEGER,
                neuroticism INTEGER,
                
                -- Test metadata
                test_started_at TIMESTAMP,
                test_completed_at TIMESTAMP,
                test_duration_seconds INTEGER,
                test_answers TEXT,
                
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id)
            )
        ''')
        
        # Email logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate_id TEXT NOT NULL,
                email_type TEXT NOT NULL,
                recipient_email TEXT NOT NULL,
                subject TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT,
                error_message TEXT,
                FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully")
    
    def generate_candidate_id(self, email: str) -> str:
        """Generate unique candidate ID from email"""
        hash_object = hashlib.md5(email.encode())
        return f"CAND_{hash_object.hexdigest()[:12].upper()}"
    
    def generate_test_token(self, candidate_id: str) -> str:
        """Generate unique token for personality test"""
        timestamp = datetime.now().isoformat()
        hash_input = f"{candidate_id}_{timestamp}"
        hash_object = hashlib.sha256(hash_input.encode())
        return hash_object.hexdigest()[:32]
    
    def save_candidate(self, candidate_data: Dict[str, Any]) -> str:
        """Save or update candidate information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        email = candidate_data['email']
        candidate_id = self.generate_candidate_id(email)
        
        # Convert lists to JSON strings
        workshops_list = json.dumps(candidate_data.get('workshops_list', []))
        trainings_list = json.dumps(candidate_data.get('trainings_list', []))
        papers_list = json.dumps(candidate_data.get('research_papers_list', []))
        patents_list = json.dumps(candidate_data.get('patents_list', []))
        books_list = json.dumps(candidate_data.get('books_list', []))
        achievements_list = json.dumps(candidate_data.get('achievements_list', []))
        skills = json.dumps(candidate_data.get('skills', []))
        projects = json.dumps(candidate_data.get('projects', []))
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO candidates (
                    candidate_id, name, email, phone, address, summary,
                    ug_institute_name, ug_institute_code, pg_institute_name, pg_institute_code,
                    phd_institute_name, phd_institute_code, ug_institute, pg_institute, phd_institute,
                    longevity_years, average_experience, number_of_unique_designations,
                    workshops, trainings, workshops_list, trainings_list,
                    total_papers, total_patents, books, achievements,
                    research_papers_list, patents_list, books_list, achievements_list,
                    state_jk, skills, skills_count, projects, projects_count, best_fit_for,
                    updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                candidate_id, candidate_data['name'], email, candidate_data.get('phone', ''),
                candidate_data.get('address', ''), candidate_data.get('summary', ''),
                candidate_data['ug_institute_name'], candidate_data.get('ug_institute_code', ''),
                candidate_data['pg_institute_name'], candidate_data.get('pg_institute_code', ''),
                candidate_data['phd_institute_name'], candidate_data.get('phd_institute_code', ''),
                candidate_data['ug_institute'], candidate_data['pg_institute'], candidate_data['phd_institute'],
                candidate_data['longevity_years'], candidate_data['average_experience'],
                candidate_data['number_of_unique_designations'],
                candidate_data['workshops'], candidate_data['trainings'],
                workshops_list, trainings_list,
                candidate_data['total_papers'], candidate_data['total_patents'],
                candidate_data['books'], candidate_data['achievements'],
                papers_list, patents_list, books_list, achievements_list,
                candidate_data['state_jk'], skills, candidate_data.get('skills_count', 0),
                projects, candidate_data.get('projects_count', 0), candidate_data.get('best_fit_for', ''),
                datetime.now()
            ))
            
            conn.commit()
            print(f"✅ Candidate {candidate_id} saved successfully")
            return candidate_id
            
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error saving candidate: {str(e)}")
        finally:
            conn.close()
    
    def save_resume(self, candidate_id: str, filename: str, file_content: bytes, 
                    file_type: str, extracted_text: str) -> int:
        """Save resume file"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO resumes (candidate_id, filename, file_content, file_type, extracted_text)
                VALUES (?, ?, ?, ?, ?)
            ''', (candidate_id, filename, file_content, file_type, extracted_text))
            
            resume_id = cursor.lastrowid
            conn.commit()
            print(f"✅ Resume saved for candidate {candidate_id}")
            return resume_id
            
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error saving resume: {str(e)}")
        finally:
            conn.close()
    
    def save_fitment_score(self, candidate_id: str, score_data: Dict[str, Any]) -> int:
        """Save fitment score calculation"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            traits = score_data.get('big5_trait_scores', {})
            
            cursor.execute('''
                INSERT INTO fitment_scores (
                    candidate_id, category, raw_dataset_score, fitment_score, big5_score,
                    overall_fitment_score, openness_score, conscientiousness_score,
                    extraversion_score, agreeableness_score, neuroticism_score
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                candidate_id, score_data['category'], score_data['raw_dataset_score'],
                score_data['fitment_score'], score_data['big5_score'],
                score_data['overall_fitment_score'],
                traits.get('O', 0), traits.get('C', 0), traits.get('E', 0),
                traits.get('A', 0), traits.get('N', 0)
            ))
            
            score_id = cursor.lastrowid
            conn.commit()
            print(f"✅ Fitment score saved for candidate {candidate_id}")
            return score_id
            
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error saving fitment score: {str(e)}")
        finally:
            conn.close()
    
    def create_personality_test(self, candidate_id: str) -> str:
        """Create personality test entry and return token"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            test_token = self.generate_test_token(candidate_id)
            
            cursor.execute('''
                INSERT INTO personality_tests (candidate_id, test_token, test_started_at)
                VALUES (?, ?, ?)
            ''', (candidate_id, test_token, datetime.now()))
            
            conn.commit()
            print(f"✅ Personality test created for candidate {candidate_id}")
            return test_token
            
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error creating personality test: {str(e)}")
        finally:
            conn.close()
    
    def save_personality_test_results(self, test_token: str, test_results: Dict[str, Any]) -> bool:
        """Save completed personality test results"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE personality_tests 
                SET test_status = 'completed',
                    openness = ?,
                    conscientiousness = ?,
                    extraversion = ?,
                    agreeableness = ?,
                    neuroticism = ?,
                    test_completed_at = ?,
                    test_duration_seconds = ?,
                    test_answers = ?
                WHERE test_token = ?
            ''', (
                test_results.get('openness', 0),
                test_results.get('conscientiousness', 0),
                test_results.get('extraversion', 0),
                test_results.get('agreeableness', 0),
                test_results.get('neuroticism', 0),
                datetime.now(),
                test_results.get('duration', 0),
                json.dumps(test_results.get('answers', [])),
                test_token
            ))
            
            conn.commit()
            print(f"✅ Personality test results saved for token {test_token}")
            return True
            
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error saving test results: {str(e)}")
        finally:
            conn.close()
    
    def get_candidate_by_token(self, test_token: str) -> Optional[Dict[str, Any]]:
        """Get candidate information by test token"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            print(f"🔍 Searching for token: {test_token}")
            # First, let's see what tokens we have
            cursor.execute('SELECT test_token FROM personality_tests LIMIT 5')
            existing_tokens = cursor.fetchall()
            print(f"📋 Existing tokens in DB: {existing_tokens}")
            
            cursor.execute('''
                SELECT c.* FROM candidates c
                JOIN personality_tests p ON c.candidate_id = p.candidate_id
                WHERE p.test_token = ?
            ''', (test_token,))
            
            row = cursor.fetchone()
            if row:
                columns = [desc[0] for desc in cursor.description]
                result = dict(zip(columns, row))
                print(f"✅ Found candidate: {result['name']}")
                return result
            else:
                print(f"❌ No candidate found for token: {test_token}")
                return None
            
        except Exception as e:
            print(f"❌ Error in get_candidate_by_token: {str(e)}")
            return None  
      
        finally:
            conn.close()
    
    def log_email(self, candidate_id: str, email_type: str, recipient: str, 
                   subject: str, status: str, error: str = None):
        """Log email sending activity"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO email_logs (candidate_id, email_type, recipient_email, subject, status, error_message)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (candidate_id, email_type, recipient, subject, status, error))
            
            conn.commit()
            
        except Exception as e:
            print(f"Error logging email: {str(e)}")
        finally:
            conn.close()
    
    def get_all_candidates(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all candidates"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT * FROM candidates 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
            
        finally:
            conn.close()