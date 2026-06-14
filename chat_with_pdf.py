from groq import Groq

client = Groq(api_key="الكي_تبعك")

def chat_with_pdf(text, question):
    prompt = f"""You are a helpful study assistant. Answer the following question based ONLY on the provided text.
If the answer is not in the text, say "This information is not in the document."

Text:
{text}

Question: {question}

Answer:"""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
