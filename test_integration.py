"""
Test script to verify Big5 integration works
"""

from utils.database_manager import DatabaseManager
from utils.fitment_scorer import FitmentScorer
import json

db = DatabaseManager()
scorer = FitmentScorer()

# Test data
test_candidate = {
    'name': 'Test User',
    'email': 'test@example.com',
    'phone': '1234567890',
    'address': 'Test Address',
    'summary': 'Test Summary',
    'ug_institute_name': 'Test University',
    'ug_institute_code': 'TU',
    'pg_institute_name': 'None',
    'pg_institute_code': 'None',
    'phd_institute_name': 'None',
    'phd_institute_code': 'None',
    'longevity_years': 2.0,
    'average_experience': 3.0,
    'workshops': 5,
    'trainings': 3,
    'total_papers': 2,
    'total_patents': 0,
    'achievements': 3,
    'books': 0,
    'state_jk': 0,
    'number_of_unique_designations': 2,
    'ug_institute': 1,
    'pg_institute': 0,
    'phd_institute': 0,
    'workshops_list': [],
    'trainings_list': [],
    'research_papers_list': [],
    'patents_list': [],
    'books_list': [],
    'achievements_list': [],
    'skills': ['Python', 'JavaScript'],
    'skills_count': 2,
    'projects': ['Project 1'],
    'projects_count': 1,
    'best_fit_for': 'Software Developer'
}

print("1️⃣ Saving test candidate...")
candidate_id = db.save_candidate(test_candidate)
print(f"✅ Candidate saved with ID: {candidate_id}")

print("\n2️⃣ Calculating fitment score...")
fitment_result = scorer.calculate_overall_fitment(test_candidate)
print(f"✅ Fitment score: {fitment_result['overall_fitment_score']}/100")

print("\n3️⃣ Saving fitment score...")
db.save_fitment_score(candidate_id, fitment_result)
print("✅ Fitment score saved")

print("\n4️⃣ Creating personality test token...")
test_token = db.create_personality_test(candidate_id)
print(f"✅ Token created: {test_token}")

print("\n5️⃣ Testing token retrieval...")
candidate = db.get_candidate_by_token(test_token)
if candidate:
    print(f"✅ Token works! Found candidate: {candidate['name']}")
else:
    print("❌ Token not found!")

print("\n" + "="*60)
print(f"🔗 Test URL: http://localhost:5173?token={test_token}")
print(f"🧪 API Test: http://localhost:5000/api/test/verify/{test_token}")
print("="*60)