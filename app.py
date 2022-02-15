#!/usr/bin/python
from tkinter import *
from tkinter import messagebox
import tkinter as tk
from time import sleep
from tkinter import filedialog
from os import listdir
from os.path import isfile, join
import json as js

def get_files(path):
    print('test')
    try:
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        print(onlyfiles)
    except Exception as e:
        print(e)


def read_json():
    with open('properties.json') as json_file:
        return js.load(json_file)


class App():
    
    def __init__(self):
        # main window
        self.root = tk.Tk()
        self.root.geometry("600x400")
        margin = 0.23

        #reading props
        properties = read_json()
        self.samplelist = [i for i in properties['samples']]
        self.folder_path = StringVar()
        self.folder_path.set(properties['path'])


        # folde browser  
        self.button_folder_browser = Button(text="Browse", command=self.browse_button)
        self.button_folder_browser.pack()

        # labels
        self.text = tk.StringVar()
        self.text.set("analyzing data")
        self.label = tk.Label(self.root, textvariable=self.text)
        self.label.pack()


        self.label_path = tk.Label(self.root, textvariable=self.folder_path)
        self.label_path.pack()
        

        # entrys
        entry_heigth = tk.Entry(self.root)
        entry_heigth.pack()

        # Buttons
        self.button_start = tk.Button(self.root,
                                text="start measurement",
                                command=self.start_measurement)
        self.button_start.pack()
        self.button_start
        
        
        
        # check button
        checkvar_spec = BooleanVar()
        self.check_spec = Checkbutton(self.root, text = "log spectrometer", variable = checkvar_spec, 
                 onvalue = True, offvalue = False, height=1, 
                 width = 20)
        self.check_spec.pack()
        
        
        
        # dropdowns
        self.sample = tk.StringVar()
        self.sample.set(self.samplelist[0])
        self.dropdown_sample = tk.OptionMenu(self.root, self.sample, *self.samplelist)
        self.dropdown_sample.config(width=90)
        self.dropdown_sample.pack()
        
        

        # running main
        self.root.mainloop()

        
    def create_properties():
        pass


    def start_measurement(self):
        print('test')
        get_files(self.folder_path.get())
        
        
    def browse_button(self):
        filename = filedialog.askdirectory()
        self.folder_path.set(filename)      

app =App()


