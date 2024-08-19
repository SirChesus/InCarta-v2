import Screen as s
import tkinter as tk

root = tk.Tk()

testing_window = s.Screen(root, "title")


def change_size(event):
    return testing_window.change_dimensions_float(1.2)


root.bind('<KeyPress>', change_size)

tk.mainloop()
