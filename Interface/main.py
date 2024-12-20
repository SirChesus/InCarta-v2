import tkinter as tk
from tkinter import Tk
from image_loader import ImageObject, ImageCycler
from os import path, getcwd, listdir, walk
from tkinter import filedialog
# only works on windows, need to change compatibility
from ctypes import windll

comp_dim = windll.user32.GetSystemMetrics

def change_size(event, window):
    return window.change_dimensions_float(1.2)

def start_window():
    root.configure(bg='gray')

def start_image_cycler_scene(window: Tk, main_directory=filedialog.askdirectory()):

    for x in listdir(main_directory):
        x = f"{main_directory}/{x}"
        if path.isdir(x):
           print(x)

    image_cycler = ImageCycler(main_directory)
    test_image = ImageObject(fr"{path.dirname(getcwd())}\place_holder.png", 100, 200, window)
    b = tk.Button(window, text="forward", command=lambda: image_cycler.change_image_selected_image_obj(test_image, size=(400, 400)))
    b.place(x=100, y=700)
    c = tk.Button(window, text="backward", command=lambda: image_cycler.change_image_selected_image_obj(test_image, size=(400, 400), direction=False))
    c.place(x=200, y=700)
    select_folder = tk.Button(window, text="selected_folder", command=lambda: (image_cycler.select_folder(), image_cycler.get_images()))
    select_folder.place(x=300, y=700)



if __name__ == "__main__":
    root = tk.Tk()
    root.geometry(f"{int(comp_dim(0)/1.02)}x{int(comp_dim(1)/1.02)}")
    start_image_cycler_scene(root)
    root.mainloop()
