#!/usr/bin/python
from tkinter import *
from tkinter import messagebox
import tkinter as tk
from time import sleep

# Code to add widgets will go here...
"""top = Tk()
top.geometry("300x200")
def hello():
   messagebox.showinfo("Say Hello", "Hello World")

B1 = Button(top, text = "Say Hello", command = hello)
B1.place(x = 35,y = 50)

CheckVar1 = IntVar()
CheckVar2 = IntVar()
C1 = Checkbutton(top, text = "Music", variable = CheckVar1, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20)
C2 = Checkbutton(top, text = "Video", variable = CheckVar2, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20)
C1.pack()
C2.pack()

top.mainloop()"""

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
        
               

app =App()