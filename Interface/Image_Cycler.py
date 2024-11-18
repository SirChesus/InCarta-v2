from tkinter import filedialog, PhotoImage
from tkinter import PhotoImage as photo
from tkinter import *
from tkinter.ttk import *
import tkinter.ttk as ttk
from os import path, listdir, getcwd
import UI_Utils as utils
from PIL import Image, ImageTk
import image_loader

# creates an image, a label for it that has the name
class ImageObject:
    photo_image: PhotoImage
    full_path: str
    image_name: StringVar
    image_label: image_loader.ImageLabel
    caption_label: Label

    # updates the name based on the path, takes in no parameters
    def update_image_name(self):
        if utils.check_valid_image_path(self.full_path):
            # creating a temp array that has all parts of the path
            temp_path = path.split(self.full_path)
            self.image_name.set(temp_path[len(temp_path)-1])
            # cuts off names when they get too long
            if len(self.image_name.get()) > 20:
                self.image_name.set(self.image_name.get()[:20])
        else:
            utils.info_box("cannot update name bc of improper path")

    # sets the path depending on the inputted full path
    def set_path(self, input_path):
        if utils.check_valid_image_path(input_path):
            self.full_path = input_path
            return True
        else:
            utils.info_box("cannot set path bc of improper input path")
            return False

    # changes the image based on the path
    def change_image(self):
        self.image_label.change_image(self.full_path)

    # just for ease of use
    def update_with_path(self, input_path: str):
        if self.set_path(input_path):
            self.update_image_name()
            self.change_image()

    def __init__(self, full_path_to: str, x: int, y: int, window: Tk, width: int = 100, height: int = 100):
        # checks if path is valid, if so set the image and name
        if self.set_path(full_path_to):
            # creating the photo image
            self.photo_image = ImageTk.PhotoImage(Image.open(full_path_to).resize((width, height)))
            self.full_path = full_path_to
            self.image_name = StringVar()
            # updating image from the path
            self.update_image_name()
            self.image_label = image_loader.ImageLabel(window, full_path_to, x, y)
            self.caption_label = Label(window, textvariable=self.image_name, font=('Arial', 16))
            self.caption_label.place(x=x, y=y+125)


class ImageCycler:
    folder_selected: str
    image_selected_idx: int
    path_list: [str]

    # selects a folder and if invalid gives user the chance to fix it
    def select_folder(self):
        self.folder_selected = filedialog.askdirectory()
        # error detection
        if not path.isdir(folder_selected):
            utils.ask_yes_no(f"selected folder is not a valid directory, do you want to open another?"
                             f" {self.folder_selected}", select_folder(), lambda: utils.info_box("No folder selected"))

    def get_images(self):
        if path.isdir(folder_selected):
            self.path_list.clear()
            # loops through all files and adds any pngs it finds
            for x in listdir(folder_selected):
                # hate this many nested if statements
                if x.lower().endswith('.png'):
                    png_list.append(x)

            # start on first image
            self.image_selected_idx = 0

        else:
            message = f"ERROR: No Folder Selected, instead {folder_selected}. Do you want to select a folder again?"
            utils.ask_yes_no(message, lambda: (select_folder(), get_images()), lambda: utils.info_box("No Folder Was Selected"))



folder_selected = "-1"
png_list = []
image_selected_idx = 0
path_of_image: StringVar
file_index_text: StringVar
image_label: image_loader.ImageLabel

# allows the user to select a folder, does not return the path, instead changes folder_selected variable for the image cycler
def select_folder():
    global folder_selected
    folder_selected = filedialog.askdirectory()


# sets png_list with all the pngs in the selected folder
def get_images():
    # checking if a file path is selected in the first place
    if path.isdir(folder_selected):
        global image_selected_idx, png_list, path_of_image

        # clearing the list beforehand to make sure no artifacts remain
        png_list.clear()

        # loops through all files and adds any pngs it finds
        for x in listdir(folder_selected):
            if x.lower().endswith('.png'):
                png_list.append(x)

        # start on first image
        image_selected_idx = 0

        path_of_image.set(f"image selected: {png_list[image_selected_idx]}")
        file_index_text.set(f"img number on {str(image_selected_idx)} out of {str(len(png_list) - 1)}")
        image_label.change_image(f"{folder_selected}/{png_list[image_selected_idx]}")

    # if no folder selected ask the user if they wanted to select a folder, if yes repeat, if no stop
    else:
        message = f"ERROR: No Folder Selected, instead {folder_selected}. Do you want to select a folder again?"
        utils.ask_yes_no(message, lambda: (select_folder(), get_images()), lambda: utils.info_box("No Folder Was Selected"))

# checks if the image is png, if so return it
def get_selected_image_path():
    if 0 <= image_selected_idx < len(png_list):
        if png_list[image_selected_idx].endswith('.png'):
            return png_list[image_selected_idx]
        else:
            utils.info_box(f"Error with image selection, file is not a png {png_list[image_selected_idx]}")
    else:
        utils.info_box(f"Error with image selection, outside of range img sel:{image_selected_idx}, len of images {png_list}")

# changes image_selected by forward or backward by one making sure that it is still a valid file, true means right, specify also how far you want to move it
def change_image_selected(direction=True, num_steps=1):
    global image_selected_idx, png_list, path_of_image
    # checks if the direction is false, if so flip num steps
    if not direction:
        num_steps *= -1

    # check if within bounds
    if 0 <= image_selected_idx + num_steps < len(png_list):
        image_selected_idx += num_steps
        path_of_image.set(f"image selected: {png_list[image_selected_idx]}")
        file_index_text.set(f"img number on {str(image_selected_idx)} out of {str(len(png_list)-1)}")
        image_label.change_image(f"{folder_selected}/{png_list[image_selected_idx]}")

    else:
        utils.info_box(f"image steps were out of boundaries, image_selects: {image_selected_idx}, Direction: {direction}, numSteps: {num_steps}")

def start_image_cycler_scene(window: Tk):
    global path_of_image, file_index_text, image_label

    path_of_image = StringVar()
    file_index_text = StringVar()

    #creating these variables, numbers are kind of random, and the purpose is to have less total calculation
    dimensions = [int(window.winfo_screenwidth()/1.02), int(window.winfo_screenheight()/1.02)]
    button_space = int(dimensions[0]/20) + 20
    button_locations = [int(dimensions[0]/40), int(dimensions[1] - int(dimensions[1]/8))]

    window.configure(bg='gray')

    # Button creation
    move_right = Button(window, text="next", command=change_image_selected)
    move_right.place(x=button_locations[0], y=button_locations[1])

    move_left = Button(window, text="previous", command=lambda: change_image_selected(False))
    move_left.place(x=button_locations[0] + button_space, y=button_locations[1])

    choose_dir = Button(window, text="choose directory", command=lambda: (select_folder(), get_images()))
    choose_dir.place(x=button_locations[0] + button_space*2, y=button_locations[1])

    # putting labels w/ file name and what index
    file_path_label = Label(window, textvariable=path_of_image, font=('Arial', 16))
    file_path_label.place(x=button_locations[0], y=button_locations[1]-int(button_space/2))

    file_index_label = Label(window, textvariable=file_index_text, font=('Arial', 16))
    file_index_label.place(x=button_locations[0], y=button_locations[1]-button_space)

    # creating the image to be displayed
    image_label = image_loader.ImageLabel(
        window, f"{path.dirname(getcwd())}/place_holder.png",
        x=button_locations[0], y=button_locations[1]-int(button_space*2.5)
    )

    test_image = ImageObject(f"{path.dirname(getcwd())}/place_holder.png", 400, 50, window)
    b = Button(window, text="testing", command=lambda: test_image.update_with_path(r'C:\Users\Test0\PycharmProjects\InCartaUNet-v2\Unused_Training_Images\SegTrackv2\GroundTruth\bird_of_paradise\bird_of_paradise_00021.png'))
    b.place(x=500, y=500)


# purpose is to make it more compact, makes an image w/ the name underneath
def create_image_and_label(window, image_path, x, y):
    image = image_loader.ImageLabel(
        window, image_path, x, y
    )
    label = Label(text=image_path.split())





