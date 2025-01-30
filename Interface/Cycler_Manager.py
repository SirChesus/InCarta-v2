from image_loader import ImageObject, ImageCycler
#One object can have all the attached info so everything is more self-contained and can add to a dictionary more easily
class CyclerComponents:
    """Creates CyclerComponents class
    inputs are: ImageCycler, Attached Image, Dictionary of functions with base system keys
    keywords: forward, backward"""
    def __init__(self, image_cycler:ImageCycler, attached_image:ImageObject, function_keywords:[], functions=None, size:(int,int)=(100,100)):
        if functions is None:
            functions = {}

        self.image_cycler = image_cycler
        self.functions = functions
        self.attached_image = attached_image

        if "forward" in function_keywords:
            functions.update(
                {"forward": lambda: self.image_cycler.change_image_selected_image_obj(self.attached_image, size=size)})

        if "backward" in function_keywords:
            functions.update(
                {"backward": lambda: self.image_cycler.change_image_selected_image_obj(self.attached_image, False, size=size)})

    def add_function(self, key, function):
        self.functions.update({key, function})

    def remove_function(self, key):
        self.functions.pop(key)
