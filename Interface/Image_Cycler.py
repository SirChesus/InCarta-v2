import os.path
from tkinter import filedialog
from tkinter import *
from tkinter.ttk import *
from os import path, listdir, getcwd
import UI_Utils as utils

class ImageCycler:
    folder_selected: str
    image_selected_idx: int
    path_list = [""]

    # returns a path from the selected idx
    def get_selected_image_path(self):
        if 0 <= self.image_selected_idx < len(self.path_list):
            if self.path_list[self.image_selected_idx].endswith('.png'):
                return self.path_list[self.image_selected_idx]
            else:
                utils.info_box(f"Error with image selection, file is not a png {self.path_list[self.image_selected_idx]}")
        else:
            utils.info_box(
                f"Error with image selection, outside of range img sel:{self.image_selected_idx}, len of images {self.path_list}")

    # selects a folder and if invalid gives user the chance to fix it
    def select_folder(self):
        self.folder_selected = filedialog.askdirectory()
        print(self.folder_selected)
        # error detection
        if not path.isdir(self.folder_selected):
            utils.ask_yes_no(f"selected folder is not a valid directory, do you want to open another?"
                             f" {self.folder_selected}", self.select_folder, lambda: utils.info_box("No folder selected"))

    def get_images(self):
        if path.isdir(self.folder_selected):
            self.path_list.clear()
            # loops through all files and adds any pngs it finds
            for x in listdir(self.folder_selected):
                # hate this many nested if statements
                if x.lower().endswith('.png'):
                    self.path_list.append(f"{self.folder_selected}/{x}")

            # start on first image
            self.image_selected_idx = 0

        else:
            message = f"ERROR: No Folder Selected, instead {self.folder_selected}. Do you want to select a folder again?"
            utils.ask_yes_no(message, lambda: (self.select_folder(), self.get_images()), lambda: utils.info_box("No Folder Was Selected"))

    # changes the index
    def change_image_selected(self, direction=True, num_steps=1):
        # checks if the direction is false, if so flip num steps
        if not direction:
            num_steps *= -1

        # check if within bounds
        if 0 <= self.image_selected_idx + num_steps < len(self.path_list):
            self.image_selected_idx += num_steps

        else:
            utils.info_box(
                f"image steps were out of boundaries, image_selects: {self.image_selected_idx}, Direction: {direction}, numSteps: {num_steps}")

    def change_image_selected_image_obj(self, image_obj, direction=True, num_steps=1, size: tuple[int, int] = (100, 100)):
        # checks if the direction is false, if so flip num steps
        if not direction:
            num_steps *= -1

        # check if within bounds
        if 0 <= self.image_selected_idx + num_steps < len(self.path_list):
            self.image_selected_idx += num_steps
            # checks if it is a valid image Object, can't do it in parameters bc
            try:
                image_obj.update_with_cycler(self, size)
            except:
                utils.info_box("something went wrong with changing the image -2")


        else:
            utils.info_box(
                f"image steps were out of boundaries, image_selects: {self.image_selected_idx}, Direction: {direction}, numSteps: {num_steps}")

    def __init__(self, inputted_path='none'):
        # if more clarity is needed could make a seperate error statement for a non directory path
        if inputted_path == 'none' or not path.isdir(inputted_path):
            self.select_folder()
        # setting the selected folder to the inputed one if it is a real folder
        else:
            self.folder_selected = inputted_path

        if path.isdir(self.folder_selected):
            self.get_images()


