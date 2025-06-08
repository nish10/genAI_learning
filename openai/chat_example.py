#!/usr/bin/env python3
import os
import sys
import json
from dotenv import load_dotenv
import openai

# 1) Load API key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    print("⚠️ Missing OPENAI_API_KEY in .env", file=sys.stderr)
    sys.exit(1)

# 2) List available models (first 5)
print("Models you can use:")
for m in openai.models.list().data[:5]:
    print("  -", m.id)
print()

# 3) Simple ChatCompletion
response = openai.chat.completions.create(
    model="gpt-3.5-turbo",    # unversioned alias always points to latest 3.5
    messages=[
        {"role": "system",  "content": "You are a helpful assistant."},
        {"role": "user",    "content": "Give me three bullet points on why AI is exciting."}
    ],
    temperature=0.7,
    max_tokens=100
)
print("Chat response:")
print(response.choices[0].message.content.strip())
print()

# 4) Streaming response example
print("Streaming response:")
stream = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system",  "content": "You are an assistant that streams your reply."},
        {"role": "user",    "content": "Stream me a haiku about coding."}
    ],
    temperature=0.5,
    stream=True
)
for chunk in stream:
    # delta.content holds the new text (or None)
    delta = chunk.choices[0].delta.content
    if delta:
        print(delta, end="", flush=True)
print("\n")

# 5) Function-calling stub
def get_current_weather(location: str) -> dict:
    # Dummy implementation — replace with real API calls if desired
    return {"location": location, "weather": "sunny", "temperature": "25°C"}

response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a weather bot."},
        {"role": "user",   "content": "What's the weather in Paris today?"}
    ],
    functions=[{
        "name": "get_current_weather",
        "description": "Get the current weather in a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"}
            },
            "required": ["location"]
        }
    }],
    function_call="auto",
    max_tokens=50
)

# Pydantic model: check `.function_call` attribute  
message = response.choices[0].message
if message.function_call:
    args = json.loads(message.function_call.arguments)
    result = get_current_weather(**args)
    print("Function call result:", result)
