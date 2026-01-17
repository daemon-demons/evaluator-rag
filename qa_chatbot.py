import os
from google.genai import Client

# -------------------------------
# Get API key from environment
# -------------------------------
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("GOOGLE_API_KEY not found. Please set it in your environment.")

# -------------------------------
# Initialize Gemini client
# -------------------------------
client = Client(api_key=api_key)
model_name = "gemini-2.5-flash-lite"

# -------------------------------
# Function to generate MCQs
# -------------------------------
def generate_mcq(course_name, level):
    prompt = f"""
You are an instructor creating a BASIC assessment for students.

Course Name: {course_name}
Student Level: {level}

Purpose:
- Verify the student's understanding for course certification
- Questions should be beginner-friendly, not technical

Task:
- Generate 10 multiple-choice questions (MCQs)
- Each question must have 4 options (A, B, C, D)
- Only one correct answer per question
- Use simple language, avoid jargon
- No coding questions, only conceptual

Output Format:
Q1. Question
A) Option
B) Option
C) Option
D) Option
Correct Answer: A
"""

    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )
    return response.text

# -------------------------------
# Main Program
# -------------------------------
if __name__ == "__main__":
    print("=== Student Certification Assessment Generator ===\n")

    course_name = input("Enter course name: ")
    level = input("Enter student level: ")

    print("\nGenerating assessment...\n")
    assessment = generate_mcq(course_name, level)
    print(assessment)
