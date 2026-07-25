import time

class DragController:
    def __init__(self, root, on_context_menu, on_move):
        self.root = root
        self.on_context_menu = on_context_menu
        self.on_move = on_move
        self.offset_x = 0
        self.offset_y = 0
        self.dragging = False
        self.drag_start_time = time.time()

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
        self.on_move()

    def on_right_release(self, event):
        elapsed = time.time() - self.drag_start_time
        if not self.dragging and elapsed < 0.2:
            self.on_context_menu(event)