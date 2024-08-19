import tkinter as tk
from tkinter import ttk


# stealing form geeks for geeks to start
def create_widget(parent, widget_type, **options):
    return widget_type(parent, **options)


window = create_widget(None, tk.Tk)
window.title("GUI Example")

frame = create_widget(window, tk.Frame, bg='lightblue', bd=3, cursor='hand2', height=100,
                      highlightcolor='red', highlightthickness=2, highlightbackground='black',
                      relief=tk.RAISED, width=200)


frame.pack(padx=20, pady=20)

# Create Label widget with all options
label = create_widget(frame, tk.Label, text='GeeksForGeeks', font='50', bg='lightblue', bd=3, cursor='hand2',
                      highlightcolor='red', highlightthickness=2, highlightbackground='black',
                      relief=tk.RAISED)
label.pack()

# Create a frame for buttons
button_frame = create_widget(window, tk.Frame, bg='lightblue', bd=3, cursor='hand2', height=50,
                              highlightcolor='red', highlightthickness=2, highlightbackground='black',
                              relief=tk.RAISED, width=200)
button_frame.pack(pady=10)

class ColorButton:
    def __init__(self, backgorund_color = 'green', highlight_color = 'red' , highlight_thickness = '3', highlight_background = 'black'):
        self.background_color = backgorund_color
        self.highlight_color = highlight_color
        self.highlight_thickness = highlight_thickness
        self.highlight_background = highlight_background



# Function to create buttons with all options
def create_button(parent, text, fg, cb=ColorButton()):
    return create_widget(parent, tk.Button, text=text, fg=fg, bg=cb.background_color, bd=3,
                         highlightcolor=cb.highlight_color, highlightthickness=cb.highlight_thickness,
                         highlightbackground=cb.highlight_background,
                         relief=tk.RAISED)

# Create buttons
buttons_info = [("Geeks1", "red"), ("Geeks2", "brown"), ("Geeks3", "blue"),
                ("Geeks4", "white"), ("Geeks5", "yellow"), ("Geeks6", "orange")]

for text, fg in buttons_info:
    button = create_button(button_frame, text=text, fg=fg)
    button.pack(side=tk.LEFT)

# Run the Tkinter event loop
window.mainloop()