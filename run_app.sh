#!/bin/bash
export GEMINI_API_KEY=AIzaSyBNL0hcquH1XPQbw5bBbomC4lsdbc9CKrI
source gemini-env/bin/activate
echo "Starting MCQ Evaluator with Gemini 2.5 Flash..."
streamlit run app.py
