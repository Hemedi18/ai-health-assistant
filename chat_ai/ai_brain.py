from google import genai

import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Get API key from environment
API_KEY = os.getenv("GOOGLE_API_KEY")

try:

    client = genai.Client(api_key=API_KEY)


    # Use the specific preview ID which is active in Jan 2026

    MODEL_ID = "gemini-3-flash-preview"

    print(f"--- Starting AI Assistant ({MODEL_ID}) ---")

    chat = client.chats.create(model=MODEL_ID)

    while True:

        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:

            print("AI Assistant: Goodbye!")

            break

        response = chat.send_message(user_input)

        print(f"AI Assistant: {response.text}")

except Exception as e:

    print(f"\n[!] Error: {e}")

    print("\nTip: If you get a 404, try changing MODEL_ID to 'gemini-2.5-flash'")