

import re
import os
import google.generativeai as genai
import json

with open("config.json") as f:
    config = json.load(f)
# --- Rule-Based Classifier ---
def classify_question_rule_based(question: str) -> str:
    question = question.lower().strip()
    
    # --- Math patterns ---
    math_patterns = [
        r'\d+\s*[\+\-\*\/\%]\s*\d+',   # Basic operations: 2+2, 5*3
        r'what\s+is\s+\d+.*\d+',       # "what is 5 + 3"
        r'calculate|compute|solve',    # Math keywords
        r'square\s+root|factorial|log|logarithm|area|mean|average|deviation'
    ]
    
    # --- Factual patterns ---
    factual_patterns = [
        r'^(what|when|where|who|how)\s+is',
        r'^(what|when|where|who|how)\s+(was|were)',
        r'capital\s+of|population\s+of',
        r'definition\s+of|meaning\s+of'
    ]
    
    # --- Opinion patterns ---
    opinion_patterns = [
        r'^(what.*think|opinion|believe)',
        r'(better|worse|best|worst)',
        r'^(should|would|could).*you',
        r'(prefer|recommend|suggest)'
    ]
    
    for pattern in math_patterns:
        if re.search(pattern, question):
            return "math"
    
    for pattern in factual_patterns:
        if re.search(pattern, question):
            return "factual"
            
    for pattern in opinion_patterns:
        if re.search(pattern, question):
            return "opinion"
    
    return "factual"  # Default fallback


# --- Gemini API Classifier  ---
def classify_question_gemini(question: str) -> str:
    """
    Uses Gemini API to classify question as factual, opinion, or math.
    API key is loaded from environment variable GEMINI_API_KEY.
    """
    api_key = config["GEMINI_API_KEY"]
    if not api_key:
        raise ValueError(" Please set your GEMINI_API_KEY environment variable first.")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    Classify the following question into exactly one category:
    'factual', 'opinion', or 'math'.
    
    Question: "{question}"

    Only return the category name.
    """

    response = model.generate_content(prompt)
    return response.text.strip().lower()


if __name__ == "__main__":
    print("\nChoose mode:\n1. Rule-Based (default)\n2. Gemini API (bonus)")
    mode = input("Enter 1 or 2: ").strip()

    while True:
        q = input("\nEnter your question (or 'exit' to quit): ")
        if q.lower() == "exit":
            break
        
        if mode == "2":
            print(f"Category: {classify_question_gemini(q)}")
        else:
            print(f"Category: {classify_question_rule_based(q)}")
