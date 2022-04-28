from tkinter import *

import tempfile
import os

from PIL import Image
from PIL import ImageGrab

from pytesseract import pytesseract
import clipboard


class Main:

    image_path = os.path.join(tempfile.gettempdir(), "img2txt.png")

    def __init__(self) -> None:

        self.root = Tk()
        self.root.overrideredirect(1)
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
        # Window always in the front
        self.root.attributes("-topmost", True)
        self.root.bind('<B1-Motion>', self.move_window)

        label = Label(self.root, text="img2txt")
        label.grid(row=0, column=0)

        exit_button = Button(self.root, text="X", command=exit)
        exit_button.grid(row=0, column=1)

        grab_button = Button(self.root, text="Grab", command=self.grab_button_clicked, height=3, width=15)
        grab_button.grid(row=1, column=0, columnspan=2)

        self.root.mainloop()

    def get_image_from_clipboard(self):
        """save image from clipboard"""
        try:
            img = ImageGrab.grabclipboard()
            img.save(self.image_path, 'PNG')
            return True
        except AttributeError:
            print("Error: No image found in the clip board")
            return False

    def get_text_from_image(self):
        """returns text from image"""
        img = Image.open(self.image_path)
        text = pytesseract.image_to_string(img)
        return text[:-1]

    def grab_button_clicked(self):
        """convert image to text"""
        print("="*40)

        if self.get_image_from_clipboard():
            text = self.get_text_from_image()
            clipboard.copy(text)
            print(text)
        
        print("="*40)
        print()

    def move_window(self, event):
        """move app window"""
        x, y = self.root.winfo_pointerxy()
        self.root.geometry(f"+{x}+{y}")


if __name__ == '__main__':
    Main()
