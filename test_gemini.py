from dotenv import load_dotenv
from google import genai
import os
from AI_config import USER_NAME, SYSTEM_PROMPT

load_dotenv()

client = genai.Client(api_key=os.getenv("API_KEY"))

chat_session = client.chats.create(
    model="models/gemini-2.5-flash",
    config={"system_instruction": SYSTEM_PROMPT}
)
while True:
        user_message = input("You: ")
        if user_message.lower() == "quit":
            break
        try:
            response = chat_session.send_message(user_message)
            print("Kaoruko:", response.text)
        except Exception as e:
            print("Sorry Lucas, something went wrong:", e)