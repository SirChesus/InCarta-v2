from tkinter import filedialog
from os import path
import UI_Utils as utils

folder_selected = "-1"


def select_folder():
    global folder_selected
    folder_selected = filedialog.askdirectory()

def get_images():
    if path.isdir(folder_selected):
        pass
    # if no folder selected ask the user if they wanted to select a folder, if yes repeat, if no stop
    else:
        message = f"ERROR: No Folder Selected, instead {folder_selected}. Do you want to select a folder again?"
        utils.ask_yes_no(message, lambda: (select_folder(), get_images()), lambda: utils.info_box("No Folder Was Selected"))