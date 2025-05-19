import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_moral_judgment(dilemma, framework):
    prompt = f"""
You are a moral philosopher responding to the following dilemma using {framework}:

Dilemma: {dilemma}

1. What is the ethically appropriate action?
2. Justify it according to the principles of {framework}.
Return your answer as:
- Judgment:
- Justification:
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500,
        )
        answer = response.choices[0].message.content
        if "Judgment:" in answer and "Justification:" in answer:
            parts = answer.split("Justification:")
            judgment = parts[0].replace("Judgment:", "").strip()
            justification = parts[1].strip()
            return judgment, justification
        else:
            return "Error parsing response.", "Response was:\n" + answer
    except Exception as e:
        return "Error calling the language model.", str(e)
