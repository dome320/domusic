import json
import time  # Make sure time is imported
from openai import OpenAI  
from dotenv import load_dotenv, find_dotenv
from notebase import *

# Your API key
apiKey = "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"
model = "gpt-4-turbo"
max_tokens = 200  # Slightly increase to capture full response
temperature = 0.7

client = OpenAI(api_key=apiKey)

def generate_response(prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant whose main role is to provide the user with melodies and melodies only."},
        {"role": "user", "content": prompt}
    ]
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    return response.choices[0].message.content.strip()

# Request each voice separately
voice_1_prompt = """Please generate a python list of midi number representations of notes (48 through 84) that represents the first voice in a fugue. The list should be around 100 notes long.There should be no words simply a list and no other filler in your response so that it can be directly copied into a python statement and be used without any syntax error."""
voice_2_prompt = """Please generate a python list of midi number representations of notes (48 through 84) that represents the second voice in a fugue. The list should be around 100 notes long.There should be no words simply a list and no other filler in your response so that it can be directly copied into a python statement and be used without any syntax error."""
voice_3_prompt = """Please generate a python list of midi number representations of notes (48 through 84) that represents the third voice in a fugue. The list should be around 100 notes long.There should be no words simply a list and no other filler in your response so that it can be directly copied into a python statement and be used without any syntax error."""

voice_1 = generate_response(voice_1_prompt) + "]"
voice_2 = generate_response(voice_2_prompt) + "]"
voice_3 = generate_response(voice_3_prompt) + "]"

# Print the responses
print(voice_1)
print(voice_2)
print(voice_3)

melody1 = json.loads(voice_1.strip())
melody2 = json.loads(voice_2.strip())
melody3 = json.loads(voice_3.strip())

melody_1_notes = [get_note_name(i) for i in melody1]
melody_2_notes = [get_note_name(i) for i in melody2]
melody_3_notes = [get_note_name(i) for i in melody3]

# Play the melodies
play_tune([melody_1_notes, melody_2_notes, melody_3_notes], ms=200, play_individual=False)


