#!/usr/bin/python
from tkinter import *
from tkinter import messagebox
import tkinter as tk
from time import sleep
from tkinter import filedialog



class App():
    
    samplelist = [
        "TATP",
        "HMTD",
        "TNT",
        "Silverazide"
        ] 
    
    def __init__(self):
        # main window
        self.root = tk.Tk()
        self.root.geometry("300x200")
        
        # labels
        self.text = tk.StringVar()
        self.text.set("analyzing data")
        self.label = tk.Label(self.root, textvariable=self.text)
        self.label.pack()
        
        # Buttons
        self.button_start = tk.Button(self.root,
                                text="Click to change text below",
                                command=self.changeText)
        self.button_start.pack()
        self.button_start
        
        
        
        # check button
        checkvar_read = BooleanVar()
        self.check_read = Checkbutton(self.root, text = "read files", variable = checkvar_read, 
                 onvalue = True, offvalue = False, height=1, 
                 width = 20)
        self.check_read.pack()
        
        checkvar_statistics = BooleanVar()
        self.check_statistics = Checkbutton(self.root, text = "do statistics", variable = checkvar_statistics, 
                 onvalue = True, offvalue = False, height=1, 
                 width = 20)
        self.check_statistics.pack()
        
        checkvar_compare = BooleanVar()
        self.check_compare = Checkbutton(self.root, text = "do statistics", variable = checkvar_compare, 
                 onvalue = True, offvalue = False, height=1, 
                 width = 20)
        self.check_compare.pack()
        
        
        # dropdowns
        self.sample = tk.StringVar()
        self.sample.set(App.samplelist[0])
        self.dropdown_sample = tk.OptionMenu(self.root, self.sample, *App.samplelist)
        self.dropdown_sample.config(width=90)
        self.dropdown_sample.pack()
        
        # running main
        self.root.mainloop()

        
    def changeText(self):
        self.text.set("counting")
        
    def browseFiles(self):
        self.filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))
      
        label_file_explorer.configure(text="File Opened: "+filename)
        
               

app =App()

"""
window.geometry("500x500")
  
#Set window background color
window.config(background = "white")
  
# Create a File Explorer label
label_file_explorer = Label(window,
                            text = "File Explorer using Tkinter",
                            width = 100, height = 4,
                            fg = "blue")
  
      
button_explore = Button(window,
                        text = "Browse Files",
                        command = browseFiles)
  
button_exit = Button(window,
                     text = "Exit",
                     command = exit)
  
# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
label_file_explorer.grid(column = 1, row = 1)
  
button_explore.grid(column = 1, row = 2)
  
button_exit.grid(column = 1,row = 3)
  
# Let the window wait for any events
window.mainloop()
"""