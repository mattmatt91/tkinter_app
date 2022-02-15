#!/usr/bin/python
from tkinter import *
from tkinter import messagebox
import tkinter as tk
from time import sleep
from tkinter import filedialog
from os import listdir
from os.path import isfile, join
import json as js
from datetime import datetime

class Communication:
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
        self.width_window = 400
        self.height_window = 600
        self.col_1 = 0
        self.col_2 = self.width_window/2 
        self.col_1b = self.width_window/4 
        self.col_2b = (self.width_window/4)*3 
        self.center = self.width_window/3 
        self.row_counter = 0
        self.row_distance = 50  
        self.goemetry = '{0}x{1}'.format(self.width_window, self.height_window)
        print(self.goemetry)
        self.root = tk.Tk()
        self.root.geometry(self.goemetry)
        margin = 0.23

        #reading props and setting varaibles
        properties = Communication.read_json()
        self.sensors = properties['sensors']
        self.samplelist = [i for i in properties['samples']]
        self.folder_path = StringVar()
        self.folder_path.set(properties['path'])
        self.number = IntVar()
        self.height_window = IntVar()
        self.droptime = IntVar()
        self.duration = IntVar()
        self.path = StringVar()
        self.duration = IntVar()
        self.sensors = properties['sensors']
        

        # folde browser
        self.label_path_preview = tk.Label(self.root, text='path')
        self.label_path_preview.place(x=self.col_1, y=self.set_row()) 
        
        self.button_folder_browser = Button(text="Browse", command=self.browse_button)
        self.button_folder_browser.place(x=self.col_1b, y=self.set_row(next=False))
        
        self.label_path = tk.Label(self.root, textvariable=self.folder_path, wraplengt=150)
        self.label_path.place(x=self.col_2, y=self.set_row(next=False)) 
        
        



    
        # entrys
        self.label_heigth = tk.Label(self.root, text='height')
        self.label_heigth.place(x=self.col_1, y=self.set_row())
        self.entry_heigth = tk.Entry(self.root)
        self.entry_heigth.place(x=self.col_2, y=self.set_row(next=False))

        self.label_number = tk.Label(self.root, text='number')
        self.label_number.place(x=self.col_1, y=self.set_row())
        self.entry_number = tk.Entry(self.root)
        self.entry_number.place(x=self.col_2, y=self.set_row(next=False))
        
        self.label_droptime = tk.Label(self.root, text='droptime')
        self.label_droptime.place(x=self.col_1, y=self.set_row())
        self.entry_droptime = tk.Entry(self.root)
        self.entry_droptime.place(x=self.col_2, y=self.set_row(next=False))
        
        self.label_duration = tk.Label(self.root, text='duration')
        self.label_duration.place(x=self.col_1, y=self.set_row())
        self.entry_duration = tk.Entry(self.root)
        self.entry_duration.place(x=self.col_2, y=self.set_row(next=False))
        
        self.label_rate = tk.Label(self.root, text='rate')
        self.label_rate.place(x=self.col_1, y=self.set_row())
        self.entry_rate = tk.Entry(self.root)
        self.entry_rate.place(x=self.col_2, y=self.set_row(next=False))

        

        
        
        
        # check button
        checkvar_spec = BooleanVar()
        self.check_spec = Checkbutton(self.root, text = "log spectrometer", variable = checkvar_spec, 
                 onvalue = True, offvalue = False)
        self.check_spec.place(x=self.col_1, y=self.set_row())
        
        
        
        # dropdowns
        self.label_sample = tk.Label(self.root, text='sample')
        self.label_sample.place(x=self.col_1, y=self.set_row())
        self.sample = tk.StringVar()
        self.sample.set(self.samplelist[0])
        self.dropdown_sample = tk.OptionMenu(self.root, self.sample, *self.samplelist)
        # self.dropdown_sample.config()
        self.dropdown_sample.place(x=self.col_2, y=self.set_row(next=False))
        
        # Buttons
        self.button_start = tk.Button(self.root,
                                text="start measurement",
                                command=self.start_measurement)
        self.button_start.place(x=self.center, y=self.set_row())

        # running main
        self.root.mainloop()

        
    def set_row(self, next=True):
        if next:
            self.row_counter += self.row_distance 
        else:
            pass
        return self.row_counter
     
        
    def create_properties(self):
        rate= self.check_if_int(self.entry_rate.get())
        duration = self.check_if_int(self.entry_duration.get())
        sensors =self.sensors
        this_path = 'test'
        droptime = self.check_if_int(self.entry_droptime.get())
        sample = self.sample
        number = self.check_if_int(self.entry_number.get())
        height = self.check_if_int(self.entry_heigth.get())
        info = 'test info'
        time_stamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        
        properties = {
                    "rate": rate,
                    "duration": duration,
                    "sensors": sensors,
                    "path": this_path,
                    "droptime": droptime,
                    "sample": sample,
                    "height": height,
                    "sample_number": number,
                    "info": info,
                    "datetime": time_stamp
                    }
        for item in properties:
            if properties[item] == None:
                return
            
        print(properties)
        return properties

    def check_if_int(self,value):
        try:
            int_value = int(value)
            return int_value
        except Exception as e:
            messagebox.showinfo("dtype warning", "Warning: {0}".format(e))

    
    def start_measurement(self):
        this_properties = self.create_properties()
        if this_properties == None:
            return
        Communication.get_files(self.folder_path.get())
        
        
    def browse_button(self):
        filename = filedialog.askdirectory()
        self.folder_path.set(filename)      

app =App()


