"""
Test OpenRouter Free Model
"""

import requests
import json

# Your API key
API_KEY = "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"

print("=" * 60)
print("Testing OpenRouter Free Model")
print("=" * 60)
print()

# Test 1: Simple question
print("Test 1: Simple question")
print("-" * 60)

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    data=json.dumps({
        "model": "openai/gpt-oss-20b:free",
        "messages": [
            {
                "role": "user",
                "content": "Say 'Hello! I am working!' in one sentence."
            }
        ]
    })
)

if response.status_code == 200:
    data = response.json()
    print("✅ Success!")
    print(f"Response: {data['choices'][0]['message']['content']}")
else:
    print(f"❌ Failed: {response.status_code}")
    print(f"Error: {response.text}")

print()

# Test 2: With reasoning
print("Test 2: With reasoning enabled")
print("-" * 60)

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    data=json.dumps({
        "model": "openai/gpt-oss-20b:free",
        "messages": [
            {
                "role": "user",
                "content": "What is 2+2? Think step by step."
            }
        ],
        "extra_body": {
            "reasoning": {"enabled": True}
        }
    })
)

if response.status_code == 200:
    data = response.json()
    print("✅ Success!")
    print(f"Response: {data['choices'][0]['message']['content']}")
else:
    print(f"❌ Failed: {response.status_code}")
    print(f"Error: {response.text}")

print()
print("=" * 60)
print("✅ OpenRouter Free Model is Working!")
print("=" * 60)
print()
print("Your LLM is ready to use in Phase 4!")
