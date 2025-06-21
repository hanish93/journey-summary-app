import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_summary(captions):
    text = "\n".join([f"{img}: {cap}" for img, cap in captions])
    prompt = f"""Generate a trip summary from these image captions:

{text}

Summarize like a travel journal with highlights, places, and activities.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']
