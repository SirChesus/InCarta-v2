import tkinter as tk
from tkinter import Tk
from image_loader import ImageObject, ImageCycler, placeholder_img
from os import path, getcwd, listdir, walk
from tkinter import filedialog
# only works on windows, need to change compatibility
from ctypes import windll

comp_dim = windll.user32.GetSystemMetrics

def change_size(event, window):
    return window.change_dimensions_float(1.2)


all_cyclers = []
image_cycler_imgs = []
all_buttons = []

def add_cycler_and_buttons(window: Tk, image_x: int, image_y: int, image_dimension=100, directory=filedialog.askdirectory()):
    num_cyclers = len(all_cyclers)
    num_buttons = len(all_buttons)

    # creating local variable that will be appended later to have it not deleted after fxn ends
    local_cycler = ImageCycler(directory)
    all_cyclers.append(local_cycler)

    # attached_image
    attached_image = ImageObject(placeholder_img, image_x, image_y, window, width=image_dimension, height=image_dimension)
    image_cycler_imgs.append(attached_image)

    # defining local function to make things more clear, removed in memory afterward anyway
    def move_image_forward():
        local_cycler.change_image_selected_image_obj(attached_image, size=(image_dimension, image_dimension))

    def move_image_backward():
        local_cycler.change_image_selected_image_obj(attached_image, False, size=(image_dimension, image_dimension))

    forward = tk.Button(window, text="Forward", command=move_image_forward)
    backward = tk.Button(window, text="Backward", command=move_image_backward)
    all_buttons.append(forward)
    all_buttons.append(backward)
    forward.place(x=image_x, y=image_y+image_dimension+100)
    backward.place(x=image_x + 60, y=image_y+image_dimension+100)

def get_epoch_dirs(epoch: int = 1):
    parent_dir = f"{path.dirname(getcwd())}/output_images/epoch_{epoch}"
    all_dirs = [parent_dir + r"\\ground_truth", parent_dir + r"\\original_images", parent_dir + r"\\predictions"]
    return all_dirs


if __name__ == "__main__":
    root = tk.Tk()
    epoch_dirs = get_epoch_dirs()
    root.geometry(f"{int(comp_dim(0)/1.02)}x{int(comp_dim(1)/1.02)}")
    print(epoch_dirs)
    add_cycler_and_buttons(root, 100, 200, 400, directory=epoch_dirs[0])
    root.mainloop()
