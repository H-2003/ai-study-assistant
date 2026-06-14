from groq import Groq

client = Groq(api_key="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")

def generate_mind_map_data(text):
    prompt = f"""Based on the following text, create a mind map structure.
Return ONLY a JSON object like this exact format, nothing else:
{{
  "center": "Main Topic",
  "branches": [
    {{
      "title": "Branch 1",
      "children": ["point 1", "point 2", "point 3"]
    }},
    {{
      "title": "Branch 2", 
      "children": ["point 1", "point 2"]
    }},
    {{
      "title": "Branch 3",
      "children": ["point 1", "point 2", "point 3"]
    }},
    {{
      "title": "Branch 4",
      "children": ["point 1", "point 2"]
    }}
  ]
}}

Text:
{text}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    
    import json
    import re
    content = response.choices[0].message.content
    json_match = re.search(r'\{.*\}', content, re.DOTALL)
    if json_match:
        return json.loads(json_match.group())
    return None
