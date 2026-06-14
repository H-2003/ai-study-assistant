from groq import Groq

client = Groq(api_key="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")

def generate_summary(text):
    prompt = f"""You are a study assistant. Summarize the following text in a clear and structured way:

{text}

Provide:
- Main topic
- Key points (bullet points)
- Conclusion
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content