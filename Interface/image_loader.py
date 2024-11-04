from tkinter import PhotoImage
from PIL import Image, ImageTk
import UI_Utils as utils
from tkinter import Label

images = {}
key_num = 0

# adds the image and returns the key that will be associated with it
def add_image(image_path: str):
    global images, key_num
    try:
        key_num += 1
        opened_image = Image.open(image_path)
        images.update({key_num: ImageTk.PhotoImage(opened_image)})
        return key_num
    except:
        utils.info_box("Issue opening image")

class ImageLabel:
    label: Label
    key: int

    def __init__(self, window, path: str, x=0, y=0):
        self.key = add_image(path)
        self.label = Label(window, image=images.get(self.key))
        self.label.place(x=x, y=y)

    def change_image(self, new_image_path, dimensions: tuple = (100, 100)):
        global images
        try:
            images[self.key] = ImageTk.PhotoImage(Image.open(new_image_path).resize(dimensions))
            self.label.config(image=images.get(self.key))
        except:
            utils.info_box("error opening image")



