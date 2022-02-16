#!/usr/bin/python
from tkinter import *
from tkinter import messagebox
import tkinter as tk
from time import sleep
from tkinter import filedialog
from os import listdir
from os.path import isfile, join, isdir
import json as js
from datetime import datetime

class Communication:
    def get_files(path):
        try:
            if isdir(path):
                onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
            else:
                print("path does not exist")
        except Exception as e:
            print(e)


    def read_json():
        with open('properties.json') as json_file:
            return js.load(json_file)


    def update_properties(properties):
        """
        This function updates the properties.jsoen file.

        Args:
            properties (dictionary): dictionary with all parameters for the measurement
        """
        update_json = {}
        for item in "rate duration sensors path lastdir droptime samples number height".split():
            update_json[item]= properties[item]

        json_string = js.dumps(update_json, indent=4, sort_keys=True)
        with open('properties.json', 'w') as outfile:
            outfile.write(json_string)


class App():
    
    def __init__(self):
        # main window
        self.width_window = 400
        self.height_window = 700
        self.col_1 = 0
        self.col_2 = self.width_window/2 
        self.col_1b = self.width_window/4 
        self.col_2b = (self.width_window/4)*3 
        self.center = self.width_window/3 
        self.row_counter = 0
        self.row_distance = 50 

        self.goemetry = '{0}x{1}'.format(self.width_window, self.height_window)
        self.root = tk.Tk()
        self.root.geometry(self.goemetry)
        self.reload_properties()


        # folde browser
        self.label_path_preview = tk.Label(self.root, text='path')
        self.label_path_preview.place(x=self.col_1, y=self.set_row()) 
        
        self.button_folder_browser = Button(text="Browse", command=self.browse_button)
        self.button_folder_browser.place(x=self.col_1b, y=self.set_row(next=False))
        
        self.label_path = tk.Label(self.root, textvariable=self.path, wraplengt=150)
        self.label_path.place(x=self.col_2, y=self.set_row(next=False)) 
        
        
        # entrys
        self.label_heigth = tk.Label(self.root, text='height')
        self.label_heigth.place(x=self.col_1, y=self.set_row())
        self.entry_heigth = tk.Entry(self.root)
        self.entry_heigth.insert(0, self.height.get())
        self.entry_heigth.place(x=self.col_2, y=self.set_row(next=False))

        self.label_number = tk.Label(self.root, text='number')
        self.label_number.place(x=self.col_1, y=self.set_row())
        self.entry_number = tk.Entry(self.root)
        self.entry_number.insert(0, self.number.get())
        self.entry_number.place(x=self.col_2, y=self.set_row(next=False))
        
        self.label_droptime = tk.Label(self.root, text='droptime')
        self.label_droptime.place(x=self.col_1, y=self.set_row())
        self.entry_droptime = tk.Entry(self.root)
        self.entry_droptime.insert(0, self.droptime.get())
        self.entry_droptime.place(x=self.col_2, y=self.set_row(next=False))
        
        self.label_duration = tk.Label(self.root, text='duration')
        self.label_duration.place(x=self.col_1, y=self.set_row())
        self.entry_duration = tk.Entry(self.root)
        self.entry_duration.insert(0, self.duration.get())
        self.entry_duration.place(x=self.col_2, y=self.set_row(next=False))
        
        self.label_rate = tk.Label(self.root, text='rate')
        self.label_rate.place(x=self.col_1, y=self.set_row())
        self.entry_rate = tk.Entry(self.root)
        self.entry_rate.insert(0, self.rate.get())
        self.entry_rate.place(x=self.col_2, y=self.set_row(next=False))

        self.label_info = tk.Label(self.root, text='info')
        self.label_info.place(x=self.col_1, y=self.set_row())
        self.entry_info = tk.Entry(self.root)
        self.entry_info.place(x=self.col_2, y=self.set_row(next=False), height=100)

        # check button
        checkvar_spec = BooleanVar()
        self.check_spec = Checkbutton(self.root, text = "log spectrometer", variable = checkvar_spec, 
                 onvalue = True, offvalue = False)
        self.check_spec.place(x=self.col_1, y=self.set_row(rows=2.5))


        # dropdowns
        self.label_sample = tk.Label(self.root, text='sample')
        self.label_sample.place(x=self.col_1, y=self.set_row())
        self.sample = tk.StringVar()
        self.sample.set(self.samplelist[0])
        self.dropdown_sample = tk.OptionMenu(self.root, self.sample, *self.samplelist)
        self.dropdown_sample.place(x=self.col_2, y=self.set_row(next=False))
        

        # Buttons
        self.button_start = tk.Button(self.root,
                                text="start measurement",
                                command=self.start_measurement)
        self.button_start.place(x=self.center, y=self.set_row())


        # running main
        self.root.mainloop()


    #reading props and setting varaibles
    def reload_properties(self):
        self.properties = Communication.read_json()
        self.sensors = self.properties['sensors']
        self.samplelist = [i for i in self.properties['samples']]
        self.folder_path = StringVar()
        self.folder_path.set(self.properties['path'])
        self.number = IntVar()
        new_number = self.properties['number'] + 1
        self.number.set(new_number)
        self.droptime = IntVar()
        self.droptime.set(self.properties['droptime'])
        self.duration = IntVar()
        self.duration.set(self.properties['duration'])
        self.last_dir =StringVar()
        self.last_dir.set(self.properties['lastdir'])
        self.path = StringVar()
        self.path.set(join(self.folder_path.get(), self.last_dir.get()))
        self.rate = StringVar()
        self.rate.set(self.properties['rate'])
        self.height = IntVar()
        self.height.set(self.properties['height'])
        self.info = StringVar()
        

    def update_entrys(self):
        self.entry_heigth.delete(0, 'end')
        self.entry_number.delete(0, 'end')
        self.entry_droptime.delete(0, 'end')
        self.entry_duration.delete(0, 'end')
        self.entry_rate.delete(0, 'end')
        self.entry_heigth.insert(0, self.height.get())
        self.entry_number.insert(0, self.number.get())
        self.entry_droptime.insert(0, self.droptime.get())
        self.entry_duration.insert(0, self.duration.get())
        self.entry_rate.insert(0, self.rate.get())
        

    def set_row(self, next=True, rows=1):
        if next:
            # print(rows, next, self.row_counter)
            self.row_counter += self.row_distance*rows 
        else:
            pass
        return self.row_counter


    def create_properties(self):
        rate= self.check_if_int(self.entry_rate.get())
        duration = self.check_if_int(self.entry_duration.get())
        sensors =self.sensors
        this_path = 'test'
        droptime = self.check_if_int(self.entry_droptime.get())
        sample = self.sample.get()
        number = self.check_if_int(self.entry_number.get())
        height = self.check_if_int(self.entry_heigth.get())
        time_stamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        last_dir = self.path.get()[self.path.get().rfind('\\')+1:]
        info = self.entry_info.get()
        
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
                    "datetime": time_stamp,
                    "number": number,
                    "lastdir": last_dir,
                    "samples": self.samplelist
                    }
        for item in properties:
            if properties[item] == None:
                return
            else:
                Communication.update_properties(properties)
                print(js.dumps(properties, indent=6, sort_keys=True))
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
        else:
            print('starting measurement\n')
            self.reload_properties()
            self.update_entrys()
        
    def browse_button(self):
        filename = filedialog.askdirectory()
        self.folder_path.set(filename)      

app =App()


