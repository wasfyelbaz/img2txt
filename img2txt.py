from tkinter import *

import tempfile
import os

from PIL import Image
from PIL import ImageGrab

from pytesseract import pytesseract
import clipboard
import pyperclip3 as pc

from sys import platform


class Main:

    image_path = os.path.join(tempfile.gettempdir(), "img2txt.png")

    def __init__(self) -> None:

        self.operating_system = self.detect_os()

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

    def detect_os(self):
        return platform

    def get_image_from_clipboard(self):
        """save image from clipboard"""
        try:
            if self.operating_system == "linux" or self.operating_system == "linux2":
                # linux
                os.system(f"xclip -selection clipboard -target image/png -out > {self.image_path}") # apt-get install xclip
            else:
                # windows / mac os x
                img = ImageGrab.grabclipboard()
                img.save(self.image_path, 'PNG')
            return True
        except NotImplementedError:
            print("Error: your system is not supported")
            exit()
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
