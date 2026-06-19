import os
import time
import tkinter as tk
import textwrap
from AI_config import USER_NAME, SYSTEM_PROMPT, BG_COLOR, USER_BUBBLE_COLOR, AI_BUBBLE_COLOR, BUBBLE_TEXT_COLOR, INPUT_COLOR
from PIL import Image, ImageTk, ImageDraw, ImageFont

class ContextMenu:
    def __init__(self, root, on_quit):
        self.root = root
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Option 1", command=self.handle_click)
        self.context_menu.add_command(label="Option 2", command=self.handle_click)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Quit", command=on_quit)
        
    def on_right_click(self, event):
        self.drag_start_time = time.time()
        self.offset_x = event.x
        self.offset_y = event.y
        self.dragging = False

    def show_context_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)
    
    def handle_click(self):
        print("Hello")