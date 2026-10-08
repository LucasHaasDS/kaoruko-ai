import tkinter as tk
from AI_config import USER_NAME, SYSTEM_PROMPT, BG_COLOR, USER_BUBBLE_COLOR, AI_BUBBLE_COLOR, BUBBLE_TEXT_COLOR, INPUT_COLOR
from PIL import Image, ImageTk
from MessageBubble import MessageBubble

class ChatLog:
    def __init__(self, root, on_send):
        self.root = root
        self.on_send = on_send
        self.bubble_images = []
        self.chat_y_position = 10
        self.pending_messages = None
        self.create_chat_log()

    def create_chat_log(self):
        self.create_window()
        self.create_chat_area()
        self.create_input_area()

    def create_window(self):
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

    def create_chat_area(self):
        self.chat_canvas = tk.Canvas(
                    self.log_window,
                    bg=BG_COLOR,
                    highlightthickness=0,
                )
        self.chat_canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.chat_canvas.pack(fill="both", expand=True, padx=20, pady=15)

    def create_input_area(self):
        self.input_canvas = tk.Canvas(self.log_window,
            bg=BG_COLOR,
            highlightthickness=0, 
            height=45)
        self.input_canvas.pack(side="bottom", fill="x", padx=20, pady=15)
        self.input_canvas.create_rectangle(0, 0, 760, 45, fill=INPUT_COLOR, outline="", width=0)

        self.log_input_box = tk.Entry(self.input_canvas,  font=("Arial", 14), bg=INPUT_COLOR, fg=BUBBLE_TEXT_COLOR, insertbackground="white", relief="flat", bd=0)
        self.input_canvas.create_window(10, 8, anchor="nw", window=self.log_input_box, width=640, height=30)

        self.log_input_box.bind("<Return>", self.send_message)
        self.create_send_button()
        self.log_window.withdraw()

    def create_send_button(self):
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


    def create_mic_button(self):    
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

    def add_message(self, sender, message, role=None):

        bubble = MessageBubble(sender, message)

        image, width, height = bubble.create_bubble()

        self.bubble_images.append(image)

        canvas_width = self.chat_canvas.winfo_width()

        if role == "user":
            x = canvas_width - width - 20
        else:
            x = 20

        self.chat_canvas.create_image(
            x,
            self.chat_y_position,
            image=image,
            anchor="nw"
        )

        self.chat_y_position += height + 40

        self.chat_canvas.configure(
            scrollregion=self.chat_canvas.bbox("all")
        )

        self.chat_canvas.yview_moveto(1.0)

    def toggle_chat_log(self):
        # keyboard hotkeys run off the Tk thread; schedule UI work on it
        self.root.after(0, self._toggle_chat_log_ui)

    def _toggle_chat_log_ui(self):

        if self.log_window.state() == "withdrawn":

            self.log_window.deiconify()
            self.log_window.lift()

            self.root.after_idle(
                self._load_pending_messages
            )

            self.log_input_box.focus_set()

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

    def clear_messages(self):

        self.chat_canvas.delete("all")
        self.bubble_images.clear()
        self.chat_y_position = 10

    def load_messages(self, messages):

        self.pending_messages = messages

        if self.log_window.state() == "withdrawn":
            return

        self._load_pending_messages()
        
    def _load_pending_messages(self):

        if self.pending_messages is None:
            return

        self.clear_messages()

        self.chat_canvas.update_idletasks()

        for role, content in self.pending_messages:

            if role == "user":
                sender = USER_NAME
            else:
                sender = "Kaoruko"

            self.add_message(sender, content, role)

        self.pending_messages = None