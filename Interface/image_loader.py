from tkinter import PhotoImage
from PIL import Image, ImageTk
import PIL
import UI_Utils as utils
from tkinter import Label
from tkinter.ttk import *
from tkinter import *
from Image_Cycler import ImageCycler
from os import path

images = []
key_num = -1


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
        if True:
            images.append(ImageTk.PhotoImage(PIL.Image.open(new_image_path).resize(dimensions)))
            self.key = len(images)-1
            print(images[self.key])
            print(f"new image path : {new_image_path}")
            print(images)
            #images[self.key] = ImageTk.PhotoImage(Image.open(new_image_path).resize(dimensions))
            self.label.config(image=images[self.key])
        #except:
            #utils.info_box("error opening image")


# creates an image, a label for it that has the name
class ImageObject:
    photo_image: PhotoImage
    full_path: str
    image_name: StringVar
    image_label: ImageLabel
    caption_label: Label

    # updates the name based on the path, takes in no parameters
    def update_image_name(self):
        if utils.check_valid_image_path(self.full_path):
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
    def change_image(self):
        self.image_label.change_image(self.full_path)

    # just for ease of use
    def update_with_path(self, input_path: str):
        if self.set_path(input_path):
            #os.getcwd()
            self.update_image_name()
            self.change_image()

    def update_with_cycler(self, cyc: ImageCycler):
        print(cyc.image_selected_idx)
        print(cyc.get_selected_image_path())
        self.update_with_path(cyc.get_selected_image_path())

    def __init__(self, full_path_to: str, x: int, y: int, window: Tk, width: int = 100, height: int = 100):
        # checks if path is valid, if so set the image and name
        if self.set_path(full_path_to):
            # creating the photo image
            self.photo_image = ImageTk.PhotoImage(PIL.Image.open(self.full_path).resize((width, height)))

            self.image_name = StringVar()
            # updating image from the path
            self.update_image_name()
            self.image_label = ImageLabel(window, full_path_to, x, y)
            self.caption_label = Label(window, textvariable=self.image_name, font=('Arial', 16))
            self.caption_label.place(x=x, y=y+125)



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



