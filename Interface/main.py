import tkinter as tk
# only works on windows, need to change compatibility
from ctypes import windll
import Image_Cycler

comp_dim = windll.user32.GetSystemMetrics

def change_size(event, window):
    return window.change_dimensions_float(1.2)

def start_window():
    root.configure(bg='gray')


if __name__ == "__main__":
    root = tk.Tk()
    # creating the geometry based on the dimensions of the persons computer
    #root.geometry(f"{int(comp_dim(0)/1.1)}x{int(comp_dim(1)/1.1)}")
    root.geometry(f"{int(comp_dim(0)/1.02)}x{int(comp_dim(1)/1.02)}")

    Image_Cycler.start_image_cycler_scene(root)
    root.mainloop()
