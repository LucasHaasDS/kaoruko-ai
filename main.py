import os
import tkinter as tk
import time
from PIL import Image, ImageTk
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
        self.create_chat_panel()

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
        self.context_menu.add_command(label = "Option 1", command=self.handleClick)
        self.context_menu.add_command(label = "Option 2", command=self.handleClick)
        self.context_menu.add_separator()
        self.context_menu.add_command(label = "Quit", command=self.root.destroy)

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
        self.update_panel_position()

    def on_right_release(self, event):
        elapsed = time.time() - self.drag_start_time
        if not self.dragging and elapsed < 0.2:
            self.showContextMenu(event)

    def handleClick(self):
        print("Hello")

    def showContextMenu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)

    #Second Window
    def create_chat_panel(self):
        self.panel = tk.Toplevel(self.root)
        self.panel.overrideredirect(True)
        self.panel.configure(bg="#2b2b2b")
        self.panel.attributes("-topmost", True)
        self.panel.resizable(False, False)

        self.root.update_idletasks()
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()

        panel_width = 300
        panel_height = 300

        self.panel.geometry(
            f"{panel_width}x{panel_height}+{root_x +300}+{root_y}"
        )

        self.response_var = tk.StringVar()
        self.response_var.set("Hi Lucas! Type something...")
        self.response_label = tk.Label(
            self.panel, 
            textvariable=self.response_var,
            wraplength=280,
            justify="left",
            bg="#2b2b2b",
            fg="white"
        )
        self.response_label.pack(padx=10, pady=10)

        self.input_box = tk.Entry(
            self.panel,
            bg="#3c3c3c",
            fg="white",
            insertbackground="white"
        )
        self.input_box.pack(padx=10, pady=5)
        self.input_box.bind("<Return>", self.send_message)
        self.panel.bind("<Button-3>", self.showContextMenu)
        self.input_box.bind("<Button-3>", self.showContextMenu)
    
    def update_panel_position(self):
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()

        self.panel.geometry(
            f"+{root_x + 300}+{root_y}"
        )

    def send_message(self, event=None):
        message = self.input_box.get()
        if not message.strip():
            return
        self.input_box.delete(0, tk.END)
        self.response_var.set("Kaoruko is thinking...")
        self.ai.chat_async(message, self.on_response)

    def on_response(self, response):
        self.root.after(0, lambda: self.response_var.set(response))


root = tk.Tk()
app = KaorukoApp(root)
root.mainloop()