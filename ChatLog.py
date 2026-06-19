import os
import tkinter as tk
import textwrap
from AI_config import USER_NAME, SYSTEM_PROMPT, BG_COLOR, USER_BUBBLE_COLOR, AI_BUBBLE_COLOR, BUBBLE_TEXT_COLOR, INPUT_COLOR
from PIL import Image, ImageTk, ImageDraw, ImageFont

class ChatLog:
    def __init__(self, root, on_send):
        self.root = root
        self.on_send = on_send
        self.bubble_images = []
        self.chat_y_position = 10

        self.create_chat_log()

    def create_chat_log(self):
        self.log_window = tk.Toplevel(self.root)
        self.log_window.overrideredirect(True)
        self.log_window.attributes("-topmost", True)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        panel_width = 800
        panel_height = 600
        x = (screen_width // 2) - (panel_width // 2)
        y = (screen_height // 2) - (panel_height // 2)
        self.log_window.geometry(f"{panel_width}x{panel_height}+{x}+{y}")
        self.log_window.attributes("-alpha", 0.85)
        self.log_window.configure(bg=BG_COLOR)
        self.chat_canvas = tk.Canvas(
            self.log_window,
            bg=BG_COLOR,
            highlightthickness=0,
        )
        self.input_canvas = tk.Canvas(self.log_window,
            bg=BG_COLOR,
            highlightthickness=0, 
            height=45)
        self.chat_canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.input_canvas.pack(side="bottom", fill="x", padx=20, pady=15)
        self.input_canvas.create_rectangle(0, 0, 760, 45, fill=INPUT_COLOR, outline="", width=0)

        self.log_input_box = tk.Entry(self.input_canvas,  font=("Arial", 14), bg=INPUT_COLOR, fg=BUBBLE_TEXT_COLOR, insertbackground="white", relief="flat", bd=0)
        self.input_canvas.create_window(10, 8, anchor="nw", window=self.log_input_box, width=640, height=30)

        self.send_icon_img = Image.open("assets/icons/send.png")
        self.send_icon_img = self.send_icon_img.resize((32, 32))
        self.send_icon = ImageTk.PhotoImage(self.send_icon_img)
        
        self.send_btn = tk.Button(
            self.input_canvas,
            image=self.send_icon,
            command=self.send_message,
            bd=0,
            bg=INPUT_COLOR,
            activebackground=INPUT_COLOR,
            cursor="hand2"
        )
        self.input_canvas.create_window(720, 8, anchor="nw", window=self.send_btn, width=32, height=32)

        self.mic_icon_img = Image.open("assets/icons/microphone.png")
        self.mic_icon_img = self.mic_icon_img.resize((32, 32))
        self.mic_icon = ImageTk.PhotoImage(self.mic_icon_img)
        
        self.mic_btn = tk.Button(
            self.input_canvas,
            image=self.mic_icon,
            #command=
            bd=0,
            bg=INPUT_COLOR,
            activebackground=INPUT_COLOR,
            cursor="hand2"
        )
        self.input_canvas.create_window(680, 8, anchor="nw", window=self.mic_btn, width=32, height=32)

        self.chat_canvas.pack(fill="both", expand=True, padx=20, pady=15)
        self.log_input_box.bind("<Return>", self.send_message)
        self.log_window.withdraw()

    def add_message(self, sender, message):
        line_height = 20
        font = ImageFont.truetype("arial.ttf", 16)
        color = USER_BUBBLE_COLOR if sender == "Lucas" else AI_BUBBLE_COLOR
        lines = textwrap.wrap(message, width=67)
        temp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
        max_width = max(temp.textbbox((0, 0), line, font=font)[2] for line in lines)
        bubble_width = max_width + 40
        bubble_height = (len(lines) * line_height) + 30
        bubble_img = Image.new("RGBA", (bubble_width, bubble_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(bubble_img)
        draw.rounded_rectangle([0, 0, bubble_width, bubble_height], radius=15, fill=color)
        y_position = 15
        for line in lines:
            draw.text((20, y_position), line, fill="black", font=font)
            y_position += line_height
        self.bubble_tk = ImageTk.PhotoImage(bubble_img)
        self.bubble_images.append(self.bubble_tk)   
        canvas_width = self.chat_canvas.winfo_width()
        if sender == "Lucas":
            x = canvas_width - bubble_width - 20
        else:
            x = 20

        self.chat_canvas.create_image(x, self.chat_y_position, image=self.bubble_tk, anchor="nw")
        self.chat_y_position += bubble_height + 40
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        self.chat_canvas.yview_moveto(1.0)

    def toggle_chat_log(self):
        if self.log_window.state() == "withdrawn":
            self.log_window.deiconify()
            self.log_window.lift()
            self.log_window.focus_force()
        else:
            self.log_window.withdraw()
    
    def _on_mousewheel(self, event):
        self.chat_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def hide_chat_log(self):
        self.log_window.withdraw()

    def send_message(self, event=None):
        message = self.log_input_box.get()
        self.log_input_box.delete(0, tk.END)
        if not message.strip():
            return
        self.on_send(message)