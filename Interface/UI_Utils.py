from tkinter import messagebox
def ask_yes_no(message, yes_callback, no_callback, title="Yes/No"):
    response = messagebox.askyesno(title, message)
    if response:
        yes_callback()
    else:
        no_callback()



def info_box(message = "nothing was inputted into the message box", title = "Info"):
    messagebox.showinfo(title, message)

