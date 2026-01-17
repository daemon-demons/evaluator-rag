from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.genai import Client
import os
from dotenv import load_dotenv
import json
import re

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY or GOOGLE_API_KEY is missing")

# Initialize Gemini client
client = Client(api_key=API_KEY)

# Initialize app
app = FastAPI()

# Add CORS middleware - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (no credentials needed)
    allow_credentials=False,  # No credentials needed for this API
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Model name - using gemini-2.5-flash (gemini-1.5-flash is deprecated)
model_name = "gemini-2.5-flash"


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Server is running"}


class QuestionRequest(BaseModel):
    level: str  # beginner | intermediate | expert
    course_name: str = "ERP"  # Course name/topic


@app.post("/generate-question")
def generate_question(req: QuestionRequest):
    level = req.level.lower()
    course_name = req.course_name.strip()

    if not course_name:
        raise HTTPException(status_code=400, detail="Course name is required")
    
    if level not in ["beginner", "intermediate", "expert"]:
        raise HTTPException(status_code=400, detail="Invalid level")

    # Define level-specific instructions
    level_instructions = {
        "beginner": """For BEGINNER level: Create a question that tests understanding of fundamental concepts, 
basic terminology, core principles, and practical applications. The question should require thinking and 
understanding, not just memorization. Make it challenging enough to differentiate between someone who 
understands the basics vs someone who doesn't. Cover important foundational topics, real-world scenarios, 
or basic problem-solving. Avoid trivial yes/no questions.""",
        "intermediate": """For INTERMEDIATE level: Create a question that tests deeper understanding, 
analysis of concepts, application of principles to scenarios, comparison of approaches, troubleshooting, 
and practical problem-solving. Should require knowledge beyond basics and ability to apply concepts.""",
        "expert": """For EXPERT level: Create a question that tests advanced knowledge, complex problem-solving, 
strategic thinking, optimization, integration of multiple concepts, best practices, and expert-level 
decision-making. Should require deep expertise and nuanced understanding."""
    }
    
    prompt = f"""
    You are an expert educator creating high-quality assessment questions. Generate ONE {level.upper()} level 
    multiple-choice question about {course_name}.
    
    {level_instructions.get(level, level_instructions["beginner"])}
    
    Requirements:
    - Question must be clear, specific, and professionally written
    - Question should be challenging and thought-provoking for the {level} level
    - Each of the 4 options should be plausible but only one correct
    - Options should be well-distributed in length (avoid obvious giveaway patterns)
    - Make the question test real understanding, not just recall
    - Use real-world scenarios or practical applications when relevant
    - Ensure the question is original and AI-generated (not generic templates)
    
    Respond ONLY in valid JSON format (no markdown, no code blocks, just pure JSON):

    {{
      "question": "string",
      "options": ["Option A text", "Option B text", "Option C text", "Option D text"],
      "answer": "exact option text (must match one of the options exactly)"
    }}
    """

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )

        if not response.text:
            raise ValueError("Empty Gemini response")

        # Extract JSON from response (remove markdown code blocks if present)
        text = response.text.strip()
        
        # Remove markdown code blocks if present
        if text.startswith("```json"):
            text = text[7:]  # Remove ```json
        elif text.startswith("```"):
            text = text[3:]   # Remove ```
        
        if text.endswith("```"):
            text = text[:-3]  # Remove closing ```
        
        text = text.strip()
        
        # Try to parse JSON
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            # If JSON parsing fails, try to extract JSON object from the text
            # Find the first { and last } to extract the JSON object
            start_idx = text.find('{')
            end_idx = text.rfind('}')
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                json_str = text[start_idx:end_idx + 1]
                try:
                    data = json.loads(json_str)
                except json.JSONDecodeError:
                    raise ValueError(f"Could not parse JSON from response: {text[:200]}")
            else:
                raise ValueError(f"Could not find JSON in response: {text[:200]}")

        return data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gemini generation failed: {str(e)}"
        )
