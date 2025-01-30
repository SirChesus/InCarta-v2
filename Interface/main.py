import tkinter as tk
from tkinter import Tk
from image_loader import ImageObject, ImageCycler, placeholder_img
from os import path, getcwd, listdir, walk
from Cycler_Manager import CyclerComponents
from tkinter import filedialog
# only works on windows, need to change compatibility
from ctypes import windll

comp_dim = windll.user32.GetSystemMetrics

def change_size(event, window):
    return window.change_dimensions_float(1.2)


all_cyclers = []
image_cycler_imgs = []
all_buttons = []
cycler_fxns_one = []

def add_cycler_and_buttons(directory, window: Tk, image_x: int, image_y: int, image_dimension=100):
    global all_cyclers, all_buttons
    num_cyclers = len(all_cyclers)
    num_buttons = len(all_buttons)

    # creating local variable that will be appended later to have it not deleted after fxn ends
    local_cycler = ImageCycler(directory)
    all_cyclers.append(local_cycler)

    # attached_image
    attached_image = ImageObject(placeholder_img, image_x, image_y, window, width=image_dimension, height=image_dimension)
    image_cycler_imgs.append(attached_image)

    # creating functions to be used for buttons, adding them to the list
    def move_image_forward():
        local_cycler.change_image_selected_image_obj(attached_image, size=(image_dimension, image_dimension))
    cycler_fxns_one.append(move_image_forward)

    def move_image_backward():
        local_cycler.change_image_selected_image_obj(attached_image, False, size=(image_dimension, image_dimension))
    cycler_fxns_one.append(move_image_backward)

    forward = tk.Button(window, text="Forward", command=move_image_forward)
    backward = tk.Button(window, text="Backward", command=move_image_backward)
    all_buttons.append(forward)
    all_buttons.append(backward)
    forward.place(x=image_x, y=image_y+image_dimension+100)
    backward.place(x=image_x + 60, y=image_y+image_dimension+100)

def get_epoch_dirs(epoch: int = 1):
    parent_dir = fr"{path.dirname(getcwd())}\output_images\epoch_{epoch}"
    all_dirs = [parent_dir + r"\ground_truth", parent_dir + r"\original_images", parent_dir + r"\predictions"]
    return all_dirs


if __name__ == "__main__":
    root = tk.Tk()
    epoch_dirs = get_epoch_dirs()
    root.geometry(f"{int(comp_dim(0)/1.02)}x{int(comp_dim(1)/1.02)}")

    print(f"all dirs {epoch_dirs}")
    test_components = CyclerComponents(ImageCycler(epoch_dirs[1]), ImageObject(placeholder_img, 1000, 200, root), ["forward", "backward"], size=(400,400))
    second_components = CyclerComponents(ImageCycler(epoch_dirs[2]), ImageObject(placeholder_img, 200, 200, root), ["forward", "backward"], size=(400,400))
    test_components.image_cycler.get_images()
    print(f"components 1: {test_components.image_cycler.folder_selected} \ncomponents 2: {second_components.image_cycler.folder_selected}")
    print(f"1 {id(test_components.image_cycler.path_list)} \n2 {id(second_components.image_cycler.path_list)}")
    #test_components.functions["forward"]()

    root.mainloop()
