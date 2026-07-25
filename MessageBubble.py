import textwrap
from PIL import Image, ImageTk, ImageDraw, ImageFont

from AI_config import USER_NAME, SYSTEM_PROMPT, BG_COLOR, USER_BUBBLE_COLOR, AI_BUBBLE_COLOR, BUBBLE_TEXT_COLOR, INPUT_COLOR

class MessageBubble:
    def __init__(self, sender, message):
        self.sender = sender
        self.message = message

    def create_bubble(self):
        line_height = 20
        font = ImageFont.truetype("arial.ttf", 16)

        color = (
            USER_BUBBLE_COLOR 
            if self.sender == USER_NAME 
            else AI_BUBBLE_COLOR
        )
        lines = textwrap.wrap(self.message, width=67)
        temp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))

        max_width = max(
            temp.textbbox((0, 0), line, font=font)[2] 
            for line in lines
            )
        
        bubble_width = max_width + 40
        bubble_height = (len(lines) * line_height) + 30
        bubble_img = Image.new(
            "RGBA", 
            (bubble_width, bubble_height), 
            (0, 0, 0, 0)
        )

        draw = ImageDraw.Draw(bubble_img)
        draw.rounded_rectangle(
            [0, 0, bubble_width, bubble_height], 
            radius=15, fill=color
    )
        y_position = 15

        for line in lines:
            draw.text(
                (20, y_position),
                line,
                fill=BUBBLE_TEXT_COLOR,
                font=font
            )
            y_position += line_height

        bubble_tk = ImageTk.PhotoImage(bubble_img)
        
        return bubble_tk, bubble_width, bubble_height
        