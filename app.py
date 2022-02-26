"""
This module is the main module of the package. It includes a GUI for
reading, data and monitoring channels

:copyright: (c) 2022 by Matthias Muhr, Hochschule-Bonn-Rhein-Sieg
:license: see LICENSE for more details.
"""

#!/usr/bin/python
from msilib.schema import Class
from tkinter import *
from tkinter import messagebox, font
import tkinter as tk
from tkinter import ttk
from time import sleep
from tkinter import filedialog
from os import listdir
from os.path import isfile, join, isdir
import json as js
from datetime import datetime
from readdata import read_data 
from pathlib import Path
import plot_live
from plot_live import App_Test
from sub_window_spec import App_Test_Spec
from PIL import ImageTk, Image 
import os
from measure_multi import start_measurement_multi


class Filehandling:
    """This is a class with functions for handling files.
    Args:
        properties (dictionary): properties is a dictionary with all parameters for evaluating the data
    """
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
    for item in "rate duration sensors path lastdir droptime samples number height integration_time_micros log_spec".split():
        update_json[item]= properties[item]

    json_string = js.dumps(update_json, indent=4, sort_keys=True)
    with open('properties.json', 'w') as outfile:
        outfile.write(json_string)


def mkdir(properties, folder=None):
    """
    This file creates a new directory for a new measurent.
    The name consists of the sample, the number and a time stamp.

    Args:
        properties (dictionary): dictionary with all parameters for the measurement
        folder (string): name for new folder

    Returns:
        path (string): path to measurement folder
        path_file (string): path to measurement file
    """
    name = properties['sample'] + '_' + str(properties['sample_number']) + '_' + str(properties['datetime'])
    if folder != None:
        path = join(properties['path'], folder, name)
    else:
        path = join(properties['path'], name)
    Path(path).mkdir(parents=True, exist_ok=True)
    path_file = join(path, name)
    path_file = path_file + '.txt'
    return path, path_file


def save_properties_measurement(properties):
    """
    This function saves the measurement specific properties in a file called
    **info.json** in the measurement folder.

    Args:
        properties (dictionary): dictionary with all parameters for the measurement
    """
    save_properties = properties
    del save_properties['lastdir']
    json_string = js.dumps(save_properties, indent=4, sort_keys=True)
    json_name = properties['path'] + '\\info.json'
    with open(json_name, 'w') as outfile:
        outfile.write(json_string)


class App(object):
    def __init__(self):
        # main window
        self.width_window = 600
        self.height_window = 850
        self.font_family = "Courier"
        self.font_size_label = 30
        self.font_size_text = 15
        self.font_string_text = f'{self.font_family} {self.font_size_text}'
        self.font_string_label = f'{self.font_family} {self.font_size_label}'
        self.col_1 = 0
        self.col_2 = self.width_window/2 
        self.col_1b = self.width_window/4 
        self.col_2b = (self.width_window/4)*3 
        self.center = self.width_window/3 
        self.row_counter_measure = 0
        self.row_counter_test = 0
        self.row_distance = 50 

        self.goemetry = '{0}x{1}'.format(self.width_window, self.height_window)
        self.root = tk.Tk()
        self.root.geometry(self.goemetry)
        
        # reloading properties for defualt entrys
        self.reload_properties()

        # setting font for text
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family=self.font_family,
                                   size=self.font_size_text,
                                   weight=font.BOLD)

        # create tabs
        self.tabControl = ttk.Notebook(self.root)
        self.tab_measure = ttk.Frame(self.tabControl)
        self.tab_test = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab_measure, text ='measure')
        self.tabControl.add(self.tab_test, text ='test')
        self.tabControl.pack(expand = 1, fill ="both")
        

        # tab measure ###########################################################################################
        # folde browser
        self.label_path_preview = tk.Label(self.tab_measure, text='path')
        self.label_path_preview.place(x=self.col_1, y=self.set_row('measure')) 
        
        self.button_folder_browser = Button(self.tab_measure, text="Browse", command=self.browse_button)
        self.button_folder_browser.place(x=self.col_1b, y=self.set_row('measure', next=False))
        
        self.label_path = tk.Label(self.tab_measure, textvariable=self.path, wraplengt=250)
        self.label_path.place(x=self.col_2, y=self.set_row('measure', next=False)) 

        self.button_folder_open = Button(self.tab_measure, text="open", command=self.open)
        self.button_folder_open.place(x=self.col_1b, y=self.set_row('measure'))

        
        # entrys
        self.label_heigth = tk.Label(self.tab_measure, text='height')
        self.label_heigth.place(x=self.col_1, y=self.set_row('measure', rows=2))
        self.entry_heigth = tk.Entry(self.tab_measure, font=self.font_string_text)
        self.entry_heigth.insert(0, self.height.get())
        self.entry_heigth.place(x=self.col_2, y=self.set_row('measure', next=False))

        self.label_number = tk.Label(self.tab_measure, text='number')
        self.label_number.place(x=self.col_1, y=self.set_row('measure'))
        self.entry_number = tk.Entry(self.tab_measure, font=self.font_string_text)
        self.entry_number.insert(0, self.number.get())
        self.entry_number.place(x=self.col_2, y=self.set_row('measure', next=False))
        
        self.label_droptime = tk.Label(self.tab_measure, text='droptime')
        self.label_droptime.place(x=self.col_1, y=self.set_row('measure'))
        self.entry_droptime = tk.Entry(self.tab_measure, font=self.font_string_text)
        self.entry_droptime.insert(0, self.droptime.get())
        self.entry_droptime.place(x=self.col_2, y=self.set_row('measure', next=False))
        
        self.label_duration = tk.Label(self.tab_measure, text='duration')
        self.label_duration.place(x=self.col_1, y=self.set_row('measure'))
        self.entry_duration = tk.Entry(self.tab_measure, font=self.font_string_text)
        self.entry_duration.insert(0, self.duration.get())
        self.entry_duration.place(x=self.col_2, y=self.set_row('measure', next=False))
        
        self.label_rate = tk.Label(self.tab_measure, text='rate')
        self.label_rate.place(x=self.col_1, y=self.set_row('measure'))
        self.entry_rate = tk.Entry(self.tab_measure, font=self.font_string_text)
        self.entry_rate.insert(0, self.rate.get())
        self.entry_rate.place(x=self.col_2, y=self.set_row('measure', next=False))

        self.label_info = tk.Label(self.tab_measure, text='info')
        self.label_info.place(x=self.col_1, y=self.set_row('measure'))
        self.entry_info = tk.Entry(self.tab_measure, font=self.font_string_text)
        self.entry_info.place(x=self.col_2, y=self.set_row('measure', next=False, rows=5), height=100)

        self.label_integration_time = tk.Label(self.tab_measure, text='integration time')
        self.label_integration_time.place(x=self.col_1, y=self.set_row('measure', rows=2.5))
        self.entry_integration_time = tk.Entry(self.tab_measure, font=self.font_string_text)
        self.entry_integration_time.insert(0, self.integration_time.get())
        self.entry_integration_time.place(x=self.col_2, y=self.set_row('measure', next=False))


        # check button
        self.check_spec = Checkbutton(self.tab_measure, text = "log spectrometer", variable = self.log_spec, 
                 onvalue = True, offvalue = False)
        self.check_spec.place(x=self.col_1, y=self.set_row('measure'))


        # dropdowns
        self.label_sample = tk.Label(self.tab_measure, text='sample')
        self.label_sample.place(x=self.col_1, y=self.set_row('measure'))
        self.sample = tk.StringVar()
        self.sample.set(self.samplelist[0])
        self.dropdown_sample = tk.OptionMenu(self.tab_measure, self.sample, *self.samplelist)
        self.dropdown_sample.place(x=self.col_2, y=self.set_row('measure', next=False))
        

        # Buttons
        self.img= (Image.open("ghs.png"))
        self.resized_image= self.img.resize((50,50), Image.ANTIALIAS)
        self.new_image= ImageTk.PhotoImage(self.resized_image)
        
        self.button_start = tk.Button(self.tab_measure,
                                image=self.new_image,
                                command=self.start_measurement,
                                height= 50, width=200,
                                padx=10, pady=10)
        self.button_start.place(x=self.col_1b, y=self.set_row('measure'))


        # tab test #######################################################################################
        #Label 
        self.label_test_sensors = tk.Label(self.tab_test, text='sensor')
        self.label_test_sensors.place(x=self.col_1, y=self.set_row('test'))
        self.label_test_sensors.config(font=self.font_string_label)


        # Buttons
        self.button_start = tk.Button(self.tab_test,
                                text="start test",
                                command=self.start_test)
        self.button_start.place(x=self.col_1b, y=self.set_row('test', rows=2))

        self.button_stop = tk.Button(self.tab_test,
                                text="stop test",
                                command=self.stop_test)
        self.button_stop.place(x=self.col_2, y=self.set_row('test', next=False, rows=2))
        
        # dropdown
        self.sensor_to_plot = tk.Label(self.tab_test, text='sensor')
        self.sensor_to_plot.place(x=self.col_1b, y=self.set_row('test'))
        self.sensor_to_plot = tk.StringVar()
        self.sensor_to_plot.set(self.sensors[0])
        self.dropdown_sensor_to_plot = tk.OptionMenu(self.tab_test, self.sensor_to_plot, *self.sensors)
        self.dropdown_sensor_to_plot.place(x=self.col_2, y=self.set_row('test', next=False, rows=2))
        
        # Enrtry
        self.label_width_test = tk.Label(self.tab_test, text='width test')
        self.label_width_test.place(x=self.col_1b, y=self.set_row('test'))
        self.entry_width_test = tk.Entry(self.tab_test, font=self.font_string_text)
        self.entry_width_test.insert(0, self.width_test.get())
        self.entry_width_test.place(x=self.col_2, y=self.set_row('test', next=False, rows=4))
        
        #### spectrometer ####
        # Label 
        self.label_test_sensors = tk.Label(self.tab_test, text='spectrometer')
        self.label_test_sensors.place(x=self.col_1, y=self.set_row('test', rows=3))
        self.label_test_sensors.config(font=self.font_string_label)

        # Buttons
        self.button_start_spec = tk.Button(self.tab_test,
                                text="start test",
                                command=self.start_test_spec)
        self.button_start_spec.place(x=self.col_1b, y=self.set_row('test', rows=2))

        self.button_stop_spec = tk.Button(self.tab_test,
                                text="stop test",
                                command=self.stop_test_spec)
        self.button_stop_spec.place(x=self.col_2, y=self.set_row('test', next=False, rows=2))


        # running main
        self.root.mainloop()


    #open file explorer
    def open(self):
            os.system('start ' + self.path.get())

    
    # updating entrys
    def update_entrys(self):
        self.entry_heigth.delete(0, 'end')
        self.entry_number.delete(0, 'end')
        self.entry_droptime.delete(0, 'end')
        self.entry_duration.delete(0, 'end')
        self.entry_rate.delete(0, 'end')
        self.entry_integration_time.delete(0, 'end')
        self.entry_info.delete(0, 'end')

        self.entry_heigth.insert(0, self.height.get())
        self.entry_number.insert(0, self.number.get())
        self.entry_droptime.insert(0, self.droptime.get())
        self.entry_duration.insert(0, self.duration.get())
        self.entry_rate.insert(0, self.rate.get())
        self.entry_integration_time.insert(0, self.integration_time.get())
         

    def set_row(self, tab, next=True, rows=1):
        if next:
            if tab == 'measure':
                self.row_counter_measure += self.row_distance*rows 
                this_row_counter = self.row_counter_measure
            elif tab == 'test':
                self.row_counter_test += self.row_distance*rows
                this_row_counter = self.row_counter_test
        else:
            if tab == 'measure':
                this_row_counter = self.row_counter_measure
            elif tab == 'test':
                this_row_counter = self.row_counter_test
        return this_row_counter


    def check_if_int(self,value):
        try:
            int_value = int(value)
            return int_value
        except Exception as e:
            messagebox.showinfo("dtype warning", "Warning: {0}".format(e))

        
    # functions for measurement
    # reloads the properties.json file
    def reload_properties(self):
        self.properties = Filehandling.read_json()
        self.sensors = self.properties['sensors']
        self.samplelist = [i for i in self.properties['samples']]
        self.folder_path = StringVar()
        self.folder_path.set(self.properties['path'])
        self.last_dir =StringVar()
        self.last_dir.set(self.properties['lastdir'])
        self.path = StringVar()
        self.path.set(join(self.folder_path.get(), self.last_dir.get()))
        self.number = IntVar()
        new_number = self.properties['number'] + 1
        self.number.set(new_number)
        self.droptime = IntVar()
        self.droptime.set(self.properties['droptime'])
        self.duration = IntVar()
        self.duration.set(self.properties['duration']) 
        self.rate = StringVar()
        self.rate.set(self.properties['rate'])
        self.integration_time = StringVar()
        self.integration_time.set(self.properties['integration_time_micros'])
        self.log_spec = BooleanVar()
        this_log_spec = self.properties['log_spec']
        self.log_spec.set(this_log_spec)
        self.height = IntVar()
        self.height.set(self.properties['height'])
        self.info = StringVar()
        self.width_test = IntVar()
        self.width_test.set(3)
        

    def create_properties(self):
        # creates properties json forn TK variables
        rate= self.check_if_int(self.entry_rate.get())
        integraion_time = self.check_if_int(self.entry_integration_time.get())
        duration = self.check_if_int(self.entry_duration.get())
        sensors =self.sensors
        path = self.path.get()
        droptime = self.check_if_int(self.entry_droptime.get())
        sample = self.sample.get()
        number = self.check_if_int(self.entry_number.get())
        height = self.check_if_int(self.entry_heigth.get())
        time_stamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        last_dir = path[path.rfind('\\')+1:]
        info = self.entry_info.get()
        log_spec = self.log_spec.get()
        
        properties = {
                    "rate": rate,
                    "duration": duration,
                    "sensors": sensors,
                    "path": path,
                    "droptime": droptime,
                    "sample": sample,
                    "height": height,
                    "sample_number": number,
                    "info": info,
                    "datetime": time_stamp,
                    "number": number,
                    "lastdir": last_dir,
                    "samples": self.samplelist,
                    "integration_time_micros": integraion_time,
                    "log_spec": log_spec
                    }
        for item in properties:
            if properties[item] == None:
                return
            else:
                return properties


    def start_measurement(self):
        this_properties = self.create_properties()
        if this_properties == None:
            return

        # updating poperties global json
        update_properties(this_properties)
        
        # make dir for measurement
        path, path_file = mkdir(this_properties)
        this_properties['path'] = path

        # saving properties for measurement
        save_properties_measurement(this_properties)

        # main measuring part
        start_measurement_multi(this_properties, path_file)

        # relaoding json 
        self.reload_properties()

        # updating default entrys
        self.update_entrys()
            
        
    def browse_button(self):
        filename = filedialog.askdirectory()
        print('selected:', filename)
        self.path.set(filename) 

    
    # functions for test sensors
    def start_test(self):
        self.width_test.set(self.entry_width_test.get())
        width = self.width_test.get()
        self.app_test = App_Test(width, 100, 10, self.sensors, self.sensor_to_plot.get())
        self.app_test.start()
        self.state_test = True
    

    def stop_test(self):
            try:
                self.app_test.stop()
                self.state_test = False
            except:
                    messagebox.showinfo("warning", "test panel is not running")
                    print('start test first!')


    # functions for test spectrometer
    def start_test_spec(self):
        self.app_test_spec = App_Test_Spec(100)
        self.app_test_spec.start()
        self.state_test_spec = True


    def stop_test_spec(self):
        self.app_test_spec.stop()
        self.state_test_spec = False

    

if __name__ == '__main__':
    App()


