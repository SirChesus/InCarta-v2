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
