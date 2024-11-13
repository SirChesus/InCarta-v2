from tkinter import messagebox
from os.path import exists
def ask_yes_no(message, yes_callback, no_callback, title="Yes/No"):
    response = messagebox.askyesno(title, message)
    if response:
        yes_callback()
    else:
        no_callback()

def info_box(message="nothing was inputted into the message box", title="Info"):
    messagebox.showinfo(title, message)

def check_valid_image_path(input_path: str):
    if exists(input_path):
        if input_path.endswith(".png"):
            return True
        else:
            info_box(f"image is not a png {input_path}")
            return False
    else:
        info_box(f"path doest not exist for creating image w/ path {input_path}")
        return False




