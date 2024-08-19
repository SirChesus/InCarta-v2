import tkinter as tk
import numpy as np
# only works on windows, need to change compatibility
from ctypes import windll


comp_dim = windll.user32.GetSystemMetrics
class Screen:
    def __init__(self, window, title, width=comp_dim(0)/1.2, height=comp_dim(1)/1.2, objects=np.array(object, dtype=object)):
        # setting the dimensions of the screen as a np array and creating list of objects on that screen **TODO** create event listener loop / class
        self.dimensions = np.array([width, height], dtype=np.int16)
        self.objects = objects

        # creating the window, setting dimensions, and giving it a title
        self.window = window
        self.window.title(title)
        self.window.geometry(f"{self.dimensions[0]}x{self.dimensions[1]}")

    def get_dimensions(self):
        return self.dimensions

    def change_dimensions_float(self, num):
        self.dimensions = np.divide(self.dimensions, num)
        self.dimensions = np.ndarray.astype(self.dimensions, dtype=np.int16)
        self.window.geometry(f"{self.dimensions[0]}x{self.dimensions[1]}")

    def change_dimensions_np_array(self, dimensions=np.array([0, 0], dtype=np.int16)):
        self.dimensions = dimensions
        self.window.geometry(f"{self.dimensions[0]}x{self.dimensions[1]}")

    def add_object(self):
        pass




"""
def create_widget(parent, widget_type, **options):
    return widget_type(parent, **options)


window = create_widget(None, tk.Tk)
window.title("GUI Example")


frame = create_widget(window, tk.Frame, bg='lightblue', bd=3, cursor='hand2', height=1000,
                      highlightcolor='red', highlightthickness=2, highlightbackground='black',
                      relief=tk.RAISED, width=)

frame.pack(padx=20, pady=20)

# Run the Tkinter event loop
window.mainloop()

"""