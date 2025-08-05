import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_captions(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You summarize physical therapy session notes."},
                {"role": "user", "content": text}
            ],
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error calling LLM: {e}"
