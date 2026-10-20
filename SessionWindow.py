import tkinter as tk


class SessionWindow:

    def __init__(self, root, ai, on_select_session):

        self.root = root
        self.ai = ai
        self.on_select_session = on_select_session

        self.window = None

    def show(self):

        if self.window is not None:
            return

        self.window = tk.Toplevel(self.root)

        self.window.title("Conversations")
        self.window.geometry("300x400")

        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.close
        )

        new_conversation_button = tk.Button(
            self.window,
            text="+ New Conversation",
            command=self.create_new_conversation
        )
        new_conversation_button.pack(
            fill="x",
            padx=10,
            pady=10
        )

        sessions = self.ai.get_all_sessions()

        for session_id, title, created_at, last_active in sessions:

            button = tk.Button(
                self.window,
                text=title,
                command=lambda session_id=session_id:
                self.select_session(session_id)
            )

            button.pack(
                fill="x", 
                padx=10,
                pady=5
            )
    
    def select_session(self, session_id):

        self.on_select_session(session_id)
        self.close()

    def close(self):

        self.window.destroy()
        self.window = None

    def create_new_conversation(self):
        self.ai.new_session("New Conversation")
        self.on_select_session(self.ai.session_id)
        self.close()