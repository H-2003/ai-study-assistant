from groq import Groq

client = Groq(api_key="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")

def generate_quiz(text):
    prompt = f"""You are a study assistant. Based on the following text, generate 5 multiple choice questions.

{text}

Format each question exactly like this:
Q1: Question here
A) Option 1
B) Option 2
C) Option 3
D) Option 4
Answer: A

Repeat for Q2, Q3, Q4, Q5.
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content