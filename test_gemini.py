from OllamaAI import KaorukoAI
from database import get_session_title, get_sessions

ai = KaorukoAI()

print("Current session ID:", ai.session_id)
print("All sessions:", get_sessions())
print("Current session title:", get_session_title(ai.session_id))