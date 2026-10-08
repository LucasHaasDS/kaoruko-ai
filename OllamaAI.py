import ollama
import threading
from AI_config import USER_NAME, SYSTEM_PROMPT
from memory import MemoryManager
from database import create_database, create_session, add_message, get_messages, get_latest_session, get_sessions

class KaorukoAI:
    def __init__(self):

        create_database()

        self.memory = MemoryManager()

        latest_session = get_latest_session()

        if latest_session is None:
            self.session_id = create_session("Kaoruko Development")
        else:
            self.session_id = latest_session[0]

        self.messages = [
            {
                "role": "system",
                "content": self.get_system_prompt()
            }
        ]

        saved_messages = get_messages(self.session_id)

        for role, content, timestamp in saved_messages:

            self.messages.append({
                "role": role,
                "content": content
            })

    def chat(self, message):
        try:
            self.messages.append({"role": "user", "content": message})
            add_message(
                self.session_id,
                "user",
                message
            )
            response = ollama.chat(model="llama3.2", messages= self.messages)
            reply = response["message"]["content"]
            self.messages.append({"role": "assistant", "content": reply})

            add_message(
                self.session_id,
                "assistant",
                reply
            )
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

    def new_session(self, title):

        self.session_id = create_session(title)
        self.messages = [
            {
                "role": "system",
                "content": self.get_system_prompt()
            }
        ]

    def get_system_prompt(self):

        return f"""
        {SYSTEM_PROMPT}

        What you know about the user:
        Name: {self.memory.data["user_name"]}
        Projects: {self.memory.data["projects"]}
        Remember these facts: {self.memory.data["remembered_facts"]}
        """
    
    def load_session(self, session_id):
        self.session_id = session_id
        self.messages = [
            {
                "role": "system", 
                "content": self.get_system_prompt()
            }
        ]

        saved_messages = get_messages(session_id)
        
        for role, content, timestamp in saved_messages:
            self.messages.append({
                "role": role,
                "content": content
            })
        
        return [
            (role, content)
            for role, content, timestamp in saved_messages
        ]

    def get_all_sessions(self):
        return get_sessions()
    
    def get_current_session_messages(self):

        saved_messages = get_messages(self.session_id)

        return [
            (role, content)
            for role, content, timestamp in saved_messages
        ]
