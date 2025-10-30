"""
Check what's in the database
"""
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

print("\n" + "="*60)
print("📊 DATABASE CONTENTS")
print("="*60)

# Check candidates
print("\n1️⃣ CANDIDATES:")
cursor.execute('SELECT candidate_id, name, email FROM candidates')
candidates = cursor.fetchall()
for c in candidates:
    print(f"   ID: {c[0]}, Name: {c[1]}, Email: {c[2]}")

# Check personality tests and tokens
print("\n2️⃣ PERSONALITY TEST TOKENS:")
cursor.execute('SELECT candidate_id, test_token, test_status FROM personality_tests')
tests = cursor.fetchall()
for t in tests:
    print(f"   Candidate: {t[0]}")
    print(f"   Token: {t[1]}")
    print(f"   Status: {t[2]}")
    print()

# Check fitment scores
print("\n3️⃣ FITMENT SCORES:")
cursor.execute('SELECT candidate_id, overall_fitment_score, category FROM fitment_scores')
scores = cursor.fetchall()
for s in scores:
    print(f"   Candidate: {s[0]}, Score: {s[1]}, Category: {s[2]}")

# Check email logs
print("\n4️⃣ EMAIL LOGS:")
cursor.execute('SELECT candidate_id, email_type, recipient_email, status FROM email_logs ORDER BY sent_at DESC LIMIT 5')
emails = cursor.fetchall()
for e in emails:
    print(f"   To: {e[2]}, Type: {e[1]}, Status: {e[3]}")

conn.close()

print("\n" + "="*60)    