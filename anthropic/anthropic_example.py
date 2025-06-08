#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv
from anthropic import Anthropic

# 1) Load API key
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    sys.exit("⚠️ Missing ANTHROPIC_API_KEY in .env")

# 2) Init client (Anthropic SDK v0.3.x+)
client = Anthropic(api_key=api_key)

# 3) Discover the first Haiku model
models = client.models.list().data
haiku_models = [m.id for m in models if "haiku" in m.id.lower()]
if not haiku_models:
    sys.exit("⚠️ No Haiku model found via Anthropic API.")
model_id = haiku_models[0]
print(f"🔎 Using model: {model_id}")

# 4) Simple completion (Messages API)
print("\n=== Simple Completion ===")
resp = client.messages.create(
    model=model_id,
    messages=[{"role": "user", "content": "Tell me a fun fact about space."}],
    max_tokens=80,
    temperature=0.7
)
# resp.content is a list of content blocks with .type and .text
simple_text = "".join(
    block.text for block in resp.content if block.type == "text"
)
print(simple_text)

# 5) Streaming response
print("\n=== Streaming Response ===")
with client.messages.stream(
    model=model_id,
    messages=[{"role": "user", "content": "Write a 4-line poem about code."}],
    max_tokens=60,
    temperature=0.5
) as stream:
    for text in stream.text_stream:  # incremental text chunks
        print(text, end="", flush=True)
    print()
