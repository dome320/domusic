import json
import time
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from notebase import *

apiKey = "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"
model = "gpt-4-turbo"
max_tokens = 200
temperature = 0.7

client = OpenAI(api_key=apiKey)

def generate_response(question):
    system_message = "You are a helpful assistant who's main role is to provide the user with melodies and melodies only."
    user_message = f"Question: {question}"
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    return response.choices[0].message.content

question = "Please generate me a python list of midi number repersentations of notes (48 through 84) that sound like a children's song. No words, no explanation of the melody, simply a list and nothing more. Please make the melody around 100 notes long. "

answer = generate_response(question) + "]" 

print(f"Melody: {answer}")

melody = json.loads(answer.strip())

melody_to_name = [get_note_name(i) for i in melody]

print(melody_to_name)
play_tune(melody_to_name, 200) 







