import tkinter as tk
import keyboard
from PIL import Image, ImageTk

from OllamaAI import KaorukoAI
from ChatBubble import ChatBubble
from ContextMenu import ContextMenu
from ChatLog import ChatLog
from ChatBox import ChatBox
from DragController import DragController


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
        
        self.chat_box = ChatBox(
            self.root,
            on_send=self.send_message
        )

        self.context_menu = ContextMenu(
            self.root,
            on_quit=self.root.destroy
        )

        self.drag_controller = DragController(
            self.root,
            on_context_menu=self.context_menu.show_context_menu,
            on_move=self.chat_box.update_position
        )

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

        self.root.bind("<Button-3>", self.drag_controller.on_right_click)
        self.root.bind("<B3-Motion>", self.drag_controller.on_right_drag)
        self.root.bind("<ButtonRelease-3>", self.drag_controller.on_right_release)

        keyboard.add_hotkey(
            "ctrl+space", 
            self.chat_box.toggle_window
        )
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

root = tk.Tk()
app = KaorukoApp(root)
root.mainloop()