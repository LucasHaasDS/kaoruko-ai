import tkinter as tk
class ChatBox:
    def __init__(self, root, on_send):
        self.root = root
        self.on_send = on_send
        self.create_chat_box()
        
    def submit_message(self, event=None):
        message = self.input_box.get()
        self.input_box.delete(0, tk.END)
        if not message.strip():
            return
        self.on_send(message)

    def create_chat_box(self):
        self.chat_window = tk.Toplevel(self.root)
        self.chat_window.geometry("500x150+500+300")

        self.input_box = tk.Entry(self.chat_window, font=("Arial", 14))
        self.input_box.pack(fill="x", padx=20, pady=20)

        self.input_box.bind("<Return>", self.submit_message)

        self.chat_window.withdraw()

    def toggle_window(self):
        if self.chat_window.state() == "withdrawn":
            self.chat_window.deiconify()
            self.chat_window.lift()
            self.chat_window.focus_force()
            self.input_box.focus_set()
        else:
            self.chat_window.withdraw()
    
    def update_position(self):
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        self.chat_window.geometry(f"+{root_x + 300}+{root_y}")
