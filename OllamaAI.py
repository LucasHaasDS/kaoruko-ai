import ollama
import threading
from AI_config import USER_NAME, SYSTEM_PROMPT
from memory import MemoryManager

class KaorukoAI:
    def __init__(self,):
        
        #Memory
        self.memory = MemoryManager()
        memory_text = f"""
        {SYSTEM_PROMPT}

        What you know about the user:
        Name: {self.memory.data["user_name"]}
        Projects: {self.memory.data["projects"]}
        Remember these facts: {self.memory.data["remembered_facts"]}
        """

        self.messages = [
            {"role": "system", "content": memory_text}
        ]

    def chat(self, message):
        try:
            self.messages.append({"role": "user", "content": message})
            response = ollama.chat(model="llama3.2", messages= self.messages)
            reply = response["message"]["content"]
            self.messages.append({"role": "assistant", "content": reply})
            return reply
        except Exception as e:
            return f"[Error occurred: {e}]"

    def chat_async(self, message, callback):
        def run():
            try:
                response = self.chat(message)
                callback(response)
            except Exception as e:
                callback(f"[Thread Error Occured:] {repr(e)}")
        
        thread = threading.Thread(target=run)
        thread.daemon = True  
        thread.start()

if __name__ == "__main__":
    ai = KaorukoAI()
    while True:
        user_message = input("You: ")
        if user_message.lower() == "quit":
            print("See you later Lucas ❤️")
            break
        print("Kaoruko:", ai.chat(user_message))