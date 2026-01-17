
import os
import sys
from app import generate_questions

# Mock streamlit to avoid error when importing app.py (if it had top level streamlit calls that cause issues, but app.py is safe inside main and functions)
# However, app.py imports streamlit as st. If we run this script, it should be fine as long as streamlit is installed.

def test_generation():
    print("Testing MCQ Generation...")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("SKIPPING: GEMINI_API_KEY not found.")
        return

    questions = generate_questions("Python Basics", "Beginner")
    
    if not questions:
        print("FAILED: No questions returned.")
        sys.exit(1)
        
    print(f"SUCCESS: Generated {len(questions)} questions.")
    
    for i, q in enumerate(questions):
        print(f"Q{i+1}: {q.question_text}")
        print(f"Options: {q.options}")
        print(f"Answer Index: {q.correct_answer_index}")
        if len(q.options) != 4:
             print("FAILED: Question does not have 4 options.")
             sys.exit(1)
             
    print("ALL TESTS PASSED")

if __name__ == "__main__":
    test_generation()
