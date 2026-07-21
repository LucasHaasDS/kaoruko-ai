import tkinter as tk
class ChatBox:
    def __init__(self, root, on_send):
        self.root = root
        self.on_send = on_send
        self.create_chat_box()

    def create_chat_box(self):
        self.chat_window = tk.Toplevel(self.root)
        self.chat_window.geometry("500x150+500+300")

        self.input_box = tk.Entry(self.chat_window, font=("Arial", 14))
        self.input_box.pack(fill="x", padx=20, pady=20)

        self.input_box.bind("<Return>", lambda e: self.send_message(self.input_box.get()))

        self.chat_window.withdraw()