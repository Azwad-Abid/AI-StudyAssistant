from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("Groq_API_Key")

# Initialize Groq client
client = Groq(api_key=api_key)

# System prompt
system_prompt = """
You are an AI Study Assistant.
Explain concepts clearly and simply.
Help students understand topics step by step.
"""

print("AI Study Assistant Started!")
print("Type 'quit' to stop.\n")

# Chat loop
messages = [
    {
        "role": "system",
        "content": system_prompt
    }
]

while True:

    user_input = input("You: ")

    if user_input.lower() == "quit":
        break

    # Add user message
    messages.append({
        "role": "user",
        "content": user_input
    })

    # API call
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    assistant_reply = response.choices[0].message.content

    # Print reply
    print("\nAssistant:", assistant_reply, "\n")

    # Save assistant reply
    messages.append({
        "role": "assistant",
        "content": assistant_reply
    })