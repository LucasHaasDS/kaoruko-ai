import os
import tkinter as tk
import time
import keyboard
import textwrap
from PIL import Image, ImageTk, ImageDraw
from gemini_client import KaorukoAI

class KaorukoApp:
    def __init__(self, root):
        #Window
        self.root = root
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = 300
        window_height = 300

        x = 0
        y = screen_height - window_height

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.ai = KaorukoAI()
        self.create_chat_box()

        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "#010101")
        self.root.configure(bg="#010101")

        #Image
        self.img = Image.open("kaoruko.png")
        self.img = self.img.resize((300, 300))
        self.image = ImageTk.PhotoImage(self.img)

        #Canvas
        self.canvas = tk.Canvas(
            self.root,
            bg="#010101",
            highlightthickness=0
        )
        self.canvas.pack()

        self.canvas.create_image(
            0,
            0,
            image=self.image,
            anchor="nw"
        )

        #Dragging
        self.offset_x = 0
        self.offset_y = 0

        self.root.bind("<Button-3>", self.on_right_click)
        self.root.bind("<B3-Motion>", self.on_right_drag)
        self.root.bind("<ButtonRelease-3>", self.on_right_release)
    
        #Right click menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label = "Option 1", command=self.handle_click)
        self.context_menu.add_command(label = "Option 2", command=self.handle_click)
        self.context_menu.add_separator()
        self.context_menu.add_command(label = "Quit", command=self.root.destroy)

        keyboard.add_hotkey("ctrl+space", self.toggle_window)
        keyboard.add_hotkey("ctrl+shift+space", self.toggle_chat_log)
        self.create_bubble_window()
        self.create_chat_log()

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
            self.show_context_menu(event)

    def handle_click(self):
        print("Hello")

    def show_context_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)

    #Second Window
    def create_chat_box(self):
        self.chat_window = tk.Toplevel(self.root)

        self.chat_window.geometry("500x150+500+300")

        self.input_box = tk.Entry(self.chat_window, font=("Arial", 14))
        self.input_box.pack(fill="x", padx=20, pady=20)
        self.input_box.bind("<Return>", self.send_message)

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

    def send_message(self, event=None, source=None):
        if source == "log":
            message = self.log_input_box.get()
            self.log_input_box.delete(0, tk.END)
        else:
            message = self.input_box.get()
            self.input_box.delete(0, tk.END)
        if not message.strip():
            return
        self.add_message_to_log("Lucas", message)
        self.ai.chat_async(message, self.on_response)

    def on_response(self, response):
        self.root.after(0, lambda: self.show_speech_bubble(response))
        self.root.after(0, lambda: self.add_message_to_log("Kaoruko", response))

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
        line_height = 20
        lines = textwrap.wrap(text, width=40)

        temp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
        max_width = max(temp.textbbox((0, 0), line)[2] for line in lines)

        bubble_width = max_width + 40
        bubble_height = (len(lines) * line_height) + 30
        bubble_x = self.root.winfo_x()
        bubble_y = self.root.winfo_y() - bubble_height

        bubble_img = Image.new("RGBA", (bubble_width, bubble_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(bubble_img)
        draw.rounded_rectangle([0, 0, bubble_width, bubble_height], radius=15, fill="white")

        y_position = 15
        for line in lines:
            draw.text((20, y_position), line, fill="black")
            y_position += line_height
        
        self.bubble_tk = ImageTk.PhotoImage(bubble_img) 
        self.bubble_label.configure(image=self.bubble_tk) 
        self.bubble_window.geometry(f"+{self.root.winfo_x()}+{self.root.winfo_y() - bubble_height}")  
        self.bubble_window.deiconify()
        self.root.after(5000, self.hide_speech_bubble)


    def hide_speech_bubble(self):
        self.bubble_window.withdraw()

    def create_chat_log(self):
        self.log_window = tk.Toplevel(self.root)
        self.log_window.overrideredirect(True)
        self.log_window.attributes("-topmost", True)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.log_window.geometry(f"{screen_width}x{screen_height}+0+0")
        self.log_window.attributes("-alpha", 0.85)
        self.log_window.configure(bg="#1a1a1a")
        self.chat_text = tk.Text(
        self.log_window,
        bg="#1a1a1a",
        fg="white",
        font=("Arial", 12),
        state="disabled",
        wrap="word"
    )
        self.log_input_box = tk.Entry(self.log_window, font=("Arial", 14))
        self.log_input_box.pack(side="bottom", fill="x", padx=20, pady=20)
        self.chat_text.pack(fill="both", expand=True, padx=20, pady=20)
        self.log_input_box.bind("<Return>", lambda e: self.send_message(e, source="log"))
        self.log_window.withdraw()
    def toggle_chat_log(self):
        if self.log_window.state() == "withdrawn":
            self.log_window.deiconify()
            self.log_window.lift()
            self.log_window.focus_force()
        else:
            self.log_window.withdraw()

    def hide_chat_log(self):
        self.log_window.withdraw()

    def add_message_to_log(self, sender, message):
        self.chat_text.configure(state="normal")
        self.chat_text.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_text.configure(state="disabled")
        self.chat_text.see(tk.END)

root = tk.Tk()
app = KaorukoApp(root)
root.mainloop()