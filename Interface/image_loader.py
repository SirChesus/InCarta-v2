from tkinter import PhotoImage
from PIL import Image, ImageTk
import PIL
import UI_Utils as utils
from tkinter import Label
from tkinter.ttk import *
from tkinter import *
from Image_Cycler import ImageCycler
from os import path, getcwd


images = []
key_num = -1

placeholder_img = fr"{path.dirname(getcwd())}\place_holder.png"

class ImageLabel:
    label: Label
    key: int

    def __init__(self, window, path: str, x=0, y=0):
        print(path)
        self.key = add_image(path)
        self.label = Label(window, image=images[self.key])
        self.label.place(x=x, y=y)

    def change_image(self, new_image_path, dimensions: tuple[int, int] = (100, 100)):
        global images
        try:
            images.append(ImageTk.PhotoImage(PIL.Image.open(new_image_path).resize(dimensions)))
            self.key = len(images)-1
            #images[self.key] = ImageTk.PhotoImage(Image.open(new_image_path).resize(dimensions))
            self.label.config(image=images[self.key])
        except:
            utils.info_box("error opening image")


# creates an image, a label for it that has the name
class ImageObject:
    photo_image: PhotoImage
    full_path: str
    image_name: StringVar
    image_label: ImageLabel
    caption_label: Label

    # updates the name based on the path, takes in no parameters
    def update_image_name(self, size: [int, int] = (100, 100)):
        if utils.check_valid_image_path(self.full_path):
            global images

            # updating position if size change
            self.caption_label.place(y=int(self.image_label.label.place_info().get("y")) + size[1] + 20)

            # creating a temp array that has all parts of the path
            temp_path = path.split(self.full_path)
            self.image_name.set(temp_path[len(temp_path)-1])
            # cuts off names when they get too long
            if len(self.image_name.get()) > 30:
                self.image_name.set(self.image_name.get()[:30])
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
    def change_image(self, size: tuple[int, int] = (100, 100)):
        self.image_label.change_image(self.full_path, size)

    # just for ease of use
    def update_with_path(self, input_path: str, size: tuple[int, int] = (100, 100)):
        if self.set_path(input_path):
            #os.getcwd()
            self.update_image_name(size)
            self.change_image(size)

    def update_with_cycler(self, cyc: ImageCycler, size: tuple[int, int] = (100, 100)):
        print(cyc.image_selected_idx)
        print(cyc.get_selected_image_path())
        self.update_with_path(cyc.get_selected_image_path(), size)

    def __init__(self, full_path_to: str, x: int, y: int, window: Tk, width: int = 100, height: int = 100):
        # checks if path is valid, if so set the image and name
        if self.set_path(full_path_to):
            # creating the photo image
            self.photo_image = ImageTk.PhotoImage(PIL.Image.open(self.full_path).resize((width, height)))

            self.image_name = StringVar()
            # updating image from the path
            self.image_label = ImageLabel(window, full_path_to, x, y)
            self.caption_label = Label(window, textvariable=self.image_name, font=('Arial', 16))
            self.caption_label.place(x=x, y=y+125)
            self.update_image_name()


# adds the image and returns the key that will be associated with it
def add_image(image_path: str):
    global images, key_num
    try:
        key_num += 1
        opened_image = PIL.Image.open(image_path)
        images.append([ImageTk.PhotoImage(opened_image)])
        return key_num
    except:
        utils.info_box("Issue opening image")



