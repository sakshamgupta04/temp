import google.generativeai as genai
import json
import re
from typing import Dict, Any
import PyPDF2
import docx
import io

class ResumeParser:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        
        # Use the correct model name without 'models/' prefix
        # This is the standard model name that works with most API keys
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def extract_text_from_pdf(self, file_bytes: bytes) -> str:
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception(f"Error extracting PDF: {str(e)}")
    
    def extract_text_from_docx(self, file_bytes: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(io.BytesIO(file_bytes))
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            raise Exception(f"Error extracting DOCX: {str(e)}")
    
    def extract_text_from_txt(self, file_bytes: bytes) -> str:
        """Extract text from TXT file"""
        try:
            return file_bytes.decode('utf-8')
        except Exception as e:
            raise Exception(f"Error extracting TXT: {str(e)}")
    
    def parse_resume(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        """Main method to parse resume using Gemini API"""
        
        # Extract text based on file type
        file_extension = filename.lower().split('.')[-1]
        
        if file_extension == 'pdf':
            resume_text = self.extract_text_from_pdf(file_bytes)
        elif file_extension in ['docx', 'doc']:
            resume_text = self.extract_text_from_docx(file_bytes)
        elif file_extension == 'txt':
            resume_text = self.extract_text_from_txt(file_bytes)
        else:
            raise ValueError("Unsupported file format. Please upload PDF, DOCX, or TXT")
        
        # Enhanced Gemini parsing prompt based on your original
        prompt = f"""
        Extract structured information from the following resume and return it in JSON format.
        Use double quotes for all keys and string values.
        
        Extract ALL of the following fields (use 0 for missing numbers, empty string "" for missing text, empty array [] for missing lists):
        
        REQUIRED FIELDS:
        - name: string (full name)
        - email: string 
        - phone: string
        - address: string
        - summary: string (professional summary)
        
        EDUCATION:
        - ug_institute_name: string (undergraduate institution full name)
        - ug_institute_code: string (UG institution abbreviation/code if mentioned)
        - pg_institute_name: string (postgraduate institution, "None" if not applicable)
        - pg_institute_code: string (PG institution abbreviation/code, "None" if not applicable)
        - phd_institute_name: string (PhD institution, "None" if not applicable)
        - phd_institute_code: string (PhD institution abbreviation/code, "None" if not applicable)
        - ug_institute: number (1 if IIT/NIT/IIIT/Tier-1 institution, else 0)
        - pg_institute: number (1 if IIT/NIT/IIIT/Tier-1 institution, else 0)
        - phd_institute: number (1 if IIT/NIT/IIIT/Tier-1 institution, else 0)
        
        EXPERIENCE:
        - longevity_years: number (average tenure at each job in years - calculate by total years / number of jobs)
        - average_experience: number (total professional work experience in years)
        - number_of_unique_designations: number (count of unique job titles/positions held)
        
        PROFESSIONAL DEVELOPMENT:
        - workshops: number (count of workshops attended)
        - trainings: number (count of training programs completed)
        - workshops_list: array of strings (list workshop names)
        - trainings_list: array of strings (list training program names)
        
        RESEARCH & PUBLICATIONS:
        - total_papers: number (research papers published)
        - total_patents: number (patents filed/granted)
        - books: number (books authored/co-authored)
        - research_papers_list: array of strings (list paper titles)
        - patents_list: array of strings (list patent titles)
        - books_list: array of strings (list book titles)
        
        ACHIEVEMENTS:
        - achievements: number (count of awards/achievements)
        - achievements_list: array of strings (list achievement descriptions)
        
        LOCATION:
        - state_jk: number (1 if from Jammu & Kashmir or mentions J&K, else 0)
        
        SKILLS:
        - skills: array of strings (technical and soft skills)
        - skills_count: number (count of skills)
        
        PROJECTS:
        - projects: array of strings (project names/descriptions)
        - projects_count: number (count of projects)
        
        ADDITIONAL:
        - best_fit_for: string (suggest 1-2 suitable job roles based on profile)
        
        IMPORTANT NOTES:
        1. For locations, check if resume mentions Jammu, Kashmir, Srinagar, or J&K and set state_jk to 1
        2. For longevity_years: Calculate average time spent at each job (total experience / number of jobs)
        3. For premier institutes (IIT/NIT/IIIT/top universities): Set respective field to 1
        4. Count all workshops, trainings, papers, patents, books, achievements carefully
        5. If information is not available, use 0 for numbers, "" for strings, [] for arrays, "None" for optional education
        
        Resume Text:
        {resume_text}
        
        Return ONLY a valid JSON object. Do not include markdown formatting or code blocks.
        """
        
        try:
            # Generate content with explicit configuration
            generation_config = {
                'temperature': 0.2,
                'top_p': 0.8,
                'top_k': 40,
                'max_output_tokens': 4096,
            }
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            response_text = response.text.strip()
            
            # Clean up response - remove markdown code blocks if present
            response_text = re.sub(r'^```json\s*', '', response_text)
            response_text = re.sub(r'^```\s*', '', response_text)
            response_text = re.sub(r'\s*```$', '', response_text)
            response_text = response_text.strip()
            
            parsed_data = json.loads(response_text)
            
            # Ensure all required fields exist with default values
            default_values = {
                'name': '', 'email': '', 'phone': '', 'address': '', 'summary': '',
                'ug_institute_name': '', 'ug_institute_code': '',
                'pg_institute_name': 'None', 'pg_institute_code': 'None',
                'phd_institute_name': 'None', 'phd_institute_code': 'None',
                'longevity_years': 0.0, 'average_experience': 0.0,
                'workshops': 0, 'trainings': 0, 'total_papers': 0,
                'total_patents': 0, 'achievements': 0, 'books': 0,
                'state_jk': 0, 'number_of_unique_designations': 0,
                'ug_institute': 0, 'pg_institute': 0, 'phd_institute': 0,
                'workshops_list': [], 'trainings_list': [],
                'research_papers_list': [], 'patents_list': [], 'books_list': [],
                'achievements_list': [], 'skills': [], 'skills_count': 0,
                'projects': [], 'projects_count': 0, 'best_fit_for': ''
            }
            
            for key, default_val in default_values.items():
                if key not in parsed_data:
                    parsed_data[key] = default_val
            
            return parsed_data
            
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse Gemini response as JSON: {str(e)}\nResponse: {response_text}")
        except Exception as e:
            raise Exception(f"Error parsing resume: {str(e)}")