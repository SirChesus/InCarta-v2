# from ChatGPT as code is never going to be re-used, making some tweaks
import numpy as np
from PIL import Image
import os

def npy_to_png(npy_file, png_file, file_path, output_path, new_size=None):
    # Load the .npy file
    #print(f"{file_path}\\{npy_file}")
    array = np.load(f"{file_path}\\{npy_file}")

    #Normalize the array to the range [0, 255]
    #if np.issubdtype(array.dtype, np.floating):
        #array = np.uint8(255 * (array - np.min(array)) / (np.ptp(array)))
    #else:
        #array = np.uint8(array)

    # Handle different array dimensions
    if array.ndim == 2:
        # 2D array (grayscale image)
        image = Image.fromarray(array)
    elif array.ndim == 3:
        if array.shape[2] in [3, 4]:
            # 3D array with 3 channels (RGB) or 4 channels (RGBA)
            image = Image.fromarray(array)
        else:
            raise ValueError("Unsupported 3D array shape for image.")
    else:
        raise ValueError("Unsupported array dimensions.")

    if new_size:
        image = image.resize(new_size, Image.Resampling.LANCZOS)

    # Save the image
    image.save(f"{output_path}/{png_file}", format='PNG')


#npy_to_png('0001_NI000_slice000.npy', '0001_NI000_slice000.png', 'C:\\Users\\Test0\\PycharmProjects\\InCartaUNet-v2\\data2\\Image\\LIDC-IDRI-0001', 'C:\\Users\\Test0\\PycharmProjects\\InCartaUNet-v2\\data2\\PNG Image', (128,128))

'''
main_dir = 'C:\\Users\\Test0\\PycharmProjects\\InCartaUNet-v2\\Lung Images\\Original Data\\Mask'

current_file = ''
x = 0
# loop through folders in the main directory (all the folders in image in this case)
for folder_path in os.listdir(main_dir):
    path_without_image_name = f"{main_dir}\\{folder_path}\\"
    # loops through all the files within those folders, probably a more efficient way exists
    for file_name in os.listdir(path_without_image_name):
        output_path = 'C:\\Users\\Test0\\PycharmProjects\\InCartaUNet-v2\\Lung Images\\PNG Data\\PNG Masks'
        x += 1
        output_name = x.__str__() + '.png'
        try:
            npy_to_png(file_name, output_name, path_without_image_name, output_path, (512,512))

        except Exception as e:
            print(e)
            print(file_name, output_name, folder_path, output_path)

'''

shape_file = "/shape_images/test/Circle/Circle_0d9895c6-2a97-11ea-8123-8363a7ec19e6.png"

def is_touching(image_array, target_color, x, y):

    neighboring_pixels = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    height, width, _ = image_array.shape

    for nx, ny in neighboring_pixels:
        if 0 <= nx < width and 0 <= ny < height:  # Ensure neighbor is within bounds
            if np.array_equal(image_array[ny, nx], target_color):
                return True

    return False

# converts a shape into a mask and saves both the original image and mask to correct paths
def mask_converter(image_path, path_to_mask_output, path_to_image_output, name):
    image = Image.open(image_path)

    # gets the top left pixel which will always be the background
    background_color = image.getpixel((0,0))
    # creating a list of all the pixels in the image, using np arrays
    pixel_list = np.array(image)
    # creating a copy so that when we do comparisons previous changes have no affect
    border_mask = np.array(pixel_list)

    # Iterate through each pixel, feels like there should be much better way
    height, width,_ = pixel_list.shape
    for y in range(height):
        for x in range(width):
            if not is_touching(pixel_list, background_color, x, y) or np.array_equal(pixel_list[y, x], background_color):
                border_mask[y, x] = [0, 0, 0]
            else:
                border_mask[y, x] = [255, 255, 255]
    #
    new_image = Image.fromarray(border_mask)
    new_image = new_image.convert("L")
    new_image.save(f"{path_to_mask_output}/{name}.png", format="PNG")

    for y in range(height):
        for x in range(width):
            if np.array_equal(pixel_list[y, x], background_color):
                pixel_list[y, x] = [0, 0, 0]
            else:
                pixel_list[y, x] = [255,255,255]

    pixel_list = Image.fromarray(pixel_list).convert('L')
    pixel_list.save(f"{path_to_image_output}/{name}.png", "PNG")
    #new_image.show()


#mask_converter(shape_file,
#               'C:\\Users\\Test0\\PycharmProjects\\InCartaUNet-v2\\shape_images\\masks\\train',
#               'C:\\Users\\Test0\\PycharmProjects\\InCartaUNet-v2\\shape_images\\images\\train',
#               'Testing_Circle')


# converts a whole set of images and gives them names from 1-100
def convert_all(directory, path_to_mask_output, path_to_image_output):
    for folder_path in os.listdir(directory):
        # numbering for the naming
        x = 0
        for image_name in os.listdir(f"{directory}\\{folder_path}"):
            x += 1
            name = f"{folder_path} {x}" # folder path has the name of the shape
            image_path = f"{directory}\\{folder_path}\\{image_name}"
            # using a try statement since too lazy to fix the format in the actual folders
            try:
                mask_converter(image_path, path_to_mask_output, path_to_image_output, name)
            except:
                pass

# paths
directory = 'C:\\Users\\Test0\\PycharmProjects\\InCartaUNet-v2\\shape_images\\test'
path_to_mask = '/shape_images/masks/test'
path_to_image = '/shape_images/images/test'

convert_all(directory, path_to_mask, path_to_image)
