import os
import tkinter as tk
import time
import keyboard
from PIL import Image, ImageTk

from OllamaAI import KaorukoAI
from ChatBubble import ChatBubble
from ContextMenu import ContextMenu
from ChatLog import ChatLog


class KaorukoApp:
    def __init__(self, root):
        self.root = root

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = 300
        window_height = 300
        x = 0
        y = screen_height - window_height
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.ai = KaorukoAI()
        self.bubble = ChatBubble(root)

        self.chat_log = ChatLog(
            self.root,
            on_send=self.send_message
        )

        self.context_menu = ContextMenu(
            self.root,
            on_quit=self.root.destroy
        )

        self.create_chat_box()

        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "#010101")
        self.root.configure(bg="#010101")

        self.img = Image.open("assets/kaoruko.png")
        self.img = self.img.resize((300, 300))
        self.image = ImageTk.PhotoImage(self.img)

        self.canvas = tk.Canvas(self.root, bg="#010101", highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.image, anchor="nw")

        self.offset_x = 0
        self.offset_y = 0
        self.dragging = False
        self.drag_start_time = time.time()

        self.root.bind("<Button-3>", self.on_right_click)
        self.root.bind("<B3-Motion>", self.on_right_drag)
        self.root.bind("<ButtonRelease-3>", self.on_right_release)

        keyboard.add_hotkey("ctrl+space", self.toggle_window)
        keyboard.add_hotkey(
            "ctrl+shift+space",
            self.chat_log.toggle_chat_log
        )

    def send_message(self, message):
        self.chat_log.add_message("Lucas", message)

        self.ai.chat_async(
            message,
            self.on_response
        )

    def on_response(self, response):
        self.chat_log.add_message("Kaoruko", response)

    def create_chat_box(self):
        self.chat_window = tk.Toplevel(self.root)
        self.chat_window.geometry("500x150+500+300")

        self.input_box = tk.Entry(self.chat_window, font=("Arial", 14))
        self.input_box.pack(fill="x", padx=20, pady=20)

        self.input_box.bind("<Return>", lambda e: self.send_message(self.input_box.get()))

        self.chat_window.withdraw()

    def toggle_window(self):
        if self.chat_window.state() == "withdrawn":
            self.chat_window.deiconify()
            self.chat_window.lift()
            self.chat_window.focus_force()
            self.input_box.focus_set()
        else:
            self.chat_window.withdraw()

    def update_chat_box_position(self):
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        self.chat_window.geometry(f"+{root_x + 300}+{root_y}")

    def on_right_click(self, event):
        self.drag_start_time = time.time()
        self.offset_x = event.x
        self.offset_y = event.y
        self.dragging = False

    def on_right_drag(self, event):
        self.dragging = True
        x = event.x_root - self.offset_x
        y = event.y_root - self.offset_y
        self.root.geometry(f"+{x}+{y}")
        self.update_chat_box_position()

    def on_right_release(self, event):
        elapsed = time.time() - self.drag_start_time
        if not self.dragging and elapsed < 0.2:
            self.context_menu.show_context_menu(event)


root = tk.Tk()
app = KaorukoApp(root)
root.mainloop()