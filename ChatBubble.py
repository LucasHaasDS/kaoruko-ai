import os
import tkinter as tk
import textwrap
from AI_config import USER_NAME, SYSTEM_PROMPT, BG_COLOR, USER_BUBBLE_COLOR, AI_BUBBLE_COLOR, BUBBLE_TEXT_COLOR, INPUT_COLOR
from PIL import Image, ImageTk, ImageDraw, ImageFont

class ChatBubble:
    def __init__(self, root):
        self.root = root
        self.font = ImageFont.truetype("arial.ttf", 16)
        self.create_bubble_window()
        
    def create_bubble_window(self):
        self.bubble_window = tk.Toplevel(self.root)
        self.bubble_window.overrideredirect(True)
        self.bubble_window.attributes("-topmost", True)
        self.bubble_window.attributes("-transparentcolor", "#010101")
        self.bubble_window.configure(bg="#010101")
        self.bubble_label = tk.Label(self.bubble_window, bg="#010101")
        self.bubble_label.pack()
        self.bubble_window.withdraw()

    def show_speech_bubble(self, text):
        line_height = 24
        font = ImageFont.truetype("arial.ttf", 16)
        lines = textwrap.wrap(text, width=40)
        temp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
        max_width = max(temp.textbbox((0, 0), line, font=font)[2] for line in lines)
        bubble_width = max_width + 40
        bubble_height = (len(lines) * line_height) + 30
        bubble_img = Image.new("RGBA", (bubble_width, bubble_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(bubble_img)
        draw.rounded_rectangle([0, 0, bubble_width, bubble_height], radius=15, fill="white")
        y_position = 15
        for line in lines:
            draw.text((20, y_position), line, fill=BUBBLE_TEXT_COLOR, font=font)
            y_position += line_height
        self.bubble_tk = ImageTk.PhotoImage(bubble_img)
        self.bubble_label.configure(image=self.bubble_tk)
        self.bubble_window.geometry(f"+{self.root.winfo_x()}+{self.root.winfo_y() - bubble_height}")
        self.bubble_window.deiconify()
        self.root.after(5000, self.hide_speech_bubble)

    def hide_speech_bubble(self):
        self.bubble_window.withdraw()