from tkinter import *
import tkinter.filedialog
import tkinter.messagebox

Tk().withdraw()
name = tkinter.filedialog.askopenfilename()
print(name)
# tkinter.messagebox.showerror("message", "words")
