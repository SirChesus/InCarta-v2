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






def start_image_cycler_scene(window: Tk, main_directory=filedialog.askdirectory()):
    # creating lists for all the different cyclers
    all_cyclers = []
    image_objects = []

    for x in listdir(main_directory):
        x = f"{main_directory}/{x}"
        if path.isdir(x):
            all_cyclers.append(ImageCycler(x))
            image_objects.append(ImageObject(fr"{path.dirname(getcwd())}\place_holder.png", len(all_cyclers)*100, 200, window))

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
    #start_image_cycler_scene(root)
    add_cycler_and_buttons(root, 100, 200, 400)
    root.mainloop()
