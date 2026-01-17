
import os
import streamlit as st
from google import genai
from google.genai import types
from pydantic import BaseModel

# Data Models
class Question(BaseModel):
    question_text: str
    options: list[str]
    correct_answer_index: int
    explanation: str

class Quiz(BaseModel):
    questions: list[Question]

class Recommendation(BaseModel):
    course_title: str
    reason: str

class Recommendations(BaseModel):
    recommendations: list[Recommendation]

def get_client():
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        st.error("GEMINI_API_KEY not found in environment variables. Please set it.")
        return None
    return genai.Client(api_key=api_key)

def generate_questions(course_name: str, level: str, count: int = 15) -> list[Question]:
    """Generates MCQs using Gemini API."""
    client = get_client()
    if not client:
        return []

    model_id = "gemini-2.5-flash" 

    difficulty_instruction = ""
    if level.lower() == "beginner":
        difficulty_instruction = "The questions should be for a beginner level, but please make them slightly challenging to truly test basic understanding. They should not be trivial."
    elif level.lower() == "intermediate":
        difficulty_instruction = "The questions should be intermediate level, covering core concepts and some edge cases."
    elif level.lower() == "expert":
        difficulty_instruction = "The questions should be expert level, focusing on deep conceptual understanding, performance, and best practices."

    prompt = f"""
    You are an expert exam setter for the course: {course_name}.
    Level: {level}.
    {difficulty_instruction}

    Generate {count} multiple-choice questions.
    For each question, provide:
    1. The question text.
    2. 4 options.
    3. The index of the correct option (0-3).
    4. A brief explanation of why the answer is correct.

    Respond with a JSON object that strictly follows this schema:
    {{
      "questions": [
        {{
          "question_text": "str",
          "options": ["str", "str", "str", "str"],
          "correct_answer_index": int,
          "explanation": "str"
        }}
      ]
    }}
    """
    
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=Quiz
            )
        )
        
        quiz_data = response.parsed
        return quiz_data.questions if quiz_data else []

    except Exception as e:
        print(f"Error generating questions: {e}")
        st.error(f"Error generating questions: {e}")
        return []

def get_recommendations(course_name: str, level: str, score: int, total: int) -> list[Recommendation]:
    """Generates course recommendations based on performance."""
    client = get_client()
    if not client:
        return []

    model_id = "gemini-2.5-flash"
    
    performance = "poor"
    if score / total > 0.8:
        performance = "excellent"
    elif score / total > 0.5:
        performance = "average"

    prompt = f"""
    A student just took a quiz on {course_name} (Level: {level}) and scored {score}/{total}.
    Their performance was {performance}.

    Suggest 3 specific courses or topics they should study next to improve or advance to the next level.
    For each suggestion, provide a title and a brief reason.

    Respond with a JSON object:
    {{
      "recommendations": [
        {{ "course_title": "str", "reason": "str" }}
      ]
    }}
    """
    
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=Recommendations
            )
        )
        return response.parsed.recommendations if response.parsed else []
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        st.error(f"Debug Error: {e}")
        return []

def main():
    st.set_page_config(page_title="MCQ Evaluator", page_icon="📝", layout="centered")
    st.title("🎓 Certification Knowledge Check")

    # Sidebar for Configuration
    with st.sidebar:
        st.header("Configuration")
        course_name = st.text_input("Course Name", value="Python Programming")
        level = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Expert"])
        
        # Reset Button logic
        if st.button("New Quiz", type="primary"):
             # Clear state to restart
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # Initialization
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    if "generated" not in st.session_state:
        st.session_state.generated = False

    # Start Screen
    if not st.session_state.generated:
        st.markdown(f"**Ready to test your {course_name} skills?**")
        st.info("Click 'Generate Quiz' to create a custom assessment.")
        if st.button("Generate Quiz"):
            with st.spinner("Generating 20 questions... This may take a moment."):
                questions = generate_questions(course_name, level, count=20)
                if questions:
                    st.session_state.questions = questions
                    st.session_state.generated = True
                    st.session_state.current_question = 0
                    st.rerun()
        return

    # Quiz Interface (Wizard Style)
    questions = st.session_state.questions
    total_q = len(questions)
    current_idx = st.session_state.current_question
    
    if not st.session_state.quiz_submitted:
        # Progress Bar
        progress = (current_idx + 1) / total_q
        st.progress(progress, text=f"Question {current_idx + 1} of {total_q}")
        
        q = questions[current_idx]
        
        st.subheader(f"Q{current_idx + 1}: {q.question_text}")
        
        # Display Options
        # We use a key based on the question index to persist selection across reruns
        selected_option = st.radio(
            "Choose your answer:", 
            q.options, 
            key=f"q_{current_idx}",
            index=None
        )
        
        # Navigation Buttons
        col1, col2, col3 = st.columns([1, 4, 1])
        
        with col1:
            if current_idx > 0:
                if st.button("⬅ Previous"):
                    st.session_state.current_question -= 1
                    st.rerun()
        
        with col3:
            if current_idx < total_q - 1:
                if st.button("Next ➡"):
                    st.session_state.current_question += 1
                    st.rerun()
            else:
                if st.button("Submit 🏁", type="primary"):
                    st.session_state.quiz_submitted = True
                    st.rerun()
    
    # Results Screen
    else:
        st.balloons()
        st.header("📊 Quiz Results")
        
        score = 0
        for i, q in enumerate(questions):
            user_selection = st.session_state.get(f"q_{i}")
            user_idx = -1
            if user_selection in q.options:
                user_idx = q.options.index(user_selection)
            
            if user_idx == q.correct_answer_index:
                score += 1

        percentage = (score / total_q) * 100
        st.metric("Final Score", f"{score}/{total_q}", f"{percentage:.1f}%")
        
        st.divider()
        
        # Recommendations
        st.subheader("💡 Recommended Next Steps")
        with st.spinner("Analyzing your performance..."):
            try:
                recommendations = get_recommendations(course_name, level, score, total_q)
                if recommendations:
                    cols = st.columns(3)
                    for idx, rec in enumerate(recommendations):
                        with cols[idx % 3]:
                            st.info(f"**{rec.course_title}**\n\n{rec.reason}")
                else:
                    st.warning("Could not generate recommendations. Keep practicing!")
            except Exception as e:
                st.error(f"An error occurred while generating recommendations: {e}")

        st.divider()
        with st.expander("View Detailed Answers"):
            for i, q in enumerate(questions):
                user_selection = st.session_state.get(f"q_{i}")
                user_idx = -1
                if user_selection in q.options:
                    user_idx = q.options.index(user_selection)
                
                is_correct = (user_idx == q.correct_answer_index)
                
                st.markdown(f"**Q{i+1}: {q.question_text}**")
                if is_correct:
                    st.success(f"✅ Correct! (Answer: {q.options[q.correct_answer_index]})")
                else:
                    st.error(f"❌ Incorrect. You chose: {user_selection}")
                    st.markdown(f"**Correct Answer:** {q.options[q.correct_answer_index]}")
                st.write(f"*Explanation: {q.explanation}*")
                st.divider()

if __name__ == "__main__":
    main()
