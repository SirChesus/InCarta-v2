import tkinter
from tkinter import filedialog
from tkinter import PhotoImage
from tkinter import *
from os import path
from os import listdir
import UI_Utils as utils

folder_selected = "-1"
png_list = [""]
image_selected = -1

# allows the user to select a folder, does not return the path, instead changes folder_selected variable for the image cycler
def select_folder():
    global folder_selected
    folder_selected = filedialog.askdirectory()

# sets png_list with all the pngs in the selected folder
def get_images():
    # checking if a file path is selected in the first place
    if path.isdir(folder_selected):
        global image_selected, png_list

        # clearing the list beforehand to make sure no artifacts remain
        png_list.clear()

        # loops through all files and adds any pngs it finds
        for x in listdir(folder_selected):
            if x.lower().endswith('.png'):
                png_list.append(x)

        # start on first image
        image_selected = 0

    # if no folder selected ask the user if they wanted to select a folder, if yes repeat, if no stop
    else:
        message = f"ERROR: No Folder Selected, instead {folder_selected}. Do you want to select a folder again?"
        utils.ask_yes_no(message, lambda: (select_folder(), get_images()), lambda: utils.info_box("No Folder Was Selected"))

# checks if the image is png, if so return it
def get_selected_image_path():
    if 0 <= image_selected < len(png_list):
        if png_list[image_selected].endswith('.png'):
            return png_list[image_selected]
        else:
            utils.info_box(f"Error with image selection, file is not a png {png_list[image_selected]}")
    else:
        utils.info_box(f"Error with image selection, outside of range img sel:{image_selected}, len of images {png_list}")

# changes image_selected by forward or backward by one making sure that it is still a valid file, true means right, specify also how far you want to move it
def change_image_selected(direction=True, num_steps=1):
    global image_selected, png_list
    # checks if the direction is false, if so flip num steps
    if not direction:
        num_steps *= -1

    # check if within bounds
    if 0 <= image_selected + num_steps < len(png_list):
        image_selected += num_steps
    else:
        utils.info_box(f"image steps were out of boundaries, image_selects: {image_selected}, Direction: {direction}, numSteps: {num_steps}")

def start_image_cycler_scene(window : tkinter.Tk):
    window.