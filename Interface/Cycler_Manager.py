from image_loader import ImageObject, ImageCycler
#One object can have all the attached info so everything is more self-contained and can add to a dictionary more easily
class CyclerComponents:
    """Creates CyclerComponents class
    inputs are: ImageCycler, list of Image Object, Dictionary of functions with base system keys
    keywords: forward, backward, forward_group_one, backward_group_one"""
    def __init__(self, image_cycler:ImageCycler, images:[ImageObject], function_keywords:[], functions=None):
        if functions is None:
            functions = {}
        self.image_cycler = image_cycler
        self.images = images
        self.functions = functions

        if "forward" in function_keywords:


    def add_function(self, key, function):
        self.functions.update({key, function})

    def remove_function(self, key):
        self.functions.pop(key)

all_cyclers = {}
image_cycler_imgs = {

}
cycler_fxns_one = {

}

def create_cycler():
