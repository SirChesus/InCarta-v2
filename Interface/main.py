import Screen as s
import tkinter as tk


def change_size(event, window):
    return window.change_dimensions_float(1.2)

def start_window():
    root = tk.Tk()

    testing_window = s.Screen(root, "title")



    root.bind('<KeyPress>', change_size)

    tk.mainloop()

if __name__ == "__main__":
    start_window()
