#!/usr/bin/python
from tkinter import *
from tkinter import messagebox
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


class Filehandling:
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


def start_measurement_app(properties):
    # updating poperties global json
    update_properties(properties)
    
    # make dir for measurement
    path, path_file = mkdir(properties)
    properties['path'] = path

    # saving properties for measurement
    save_properties_measurement(properties)

    # main measuring part
    read_data(properties, path_file, app=True)

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
    print(properties['sensors'])
    save_properties = properties
    del save_properties['lastdir']
    json_string = js.dumps(save_properties, indent=4, sort_keys=True)
    json_name = properties['path'] + '\\info.json'
    with open(json_name, 'w') as outfile:
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
        self.row_counter_measure = 0
        self.row_counter_test = 0
        self.row_distance = 50 

        self.goemetry = '{0}x{1}'.format(self.width_window, self.height_window)
        self.root = tk.Tk()
        self.root.geometry(self.goemetry)
        self.reload_properties()

        # create tabs
        self.tabControl = ttk.Notebook(self.root)
        self.tab_measure = ttk.Frame(self.tabControl)
        self.tab_test = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_measure, text ='measure')
        self.tabControl.add(self.tab_test, text ='test')
        self.tabControl.pack(expand = 1, fill ="both")

        # tab measure #######################################################################################
        # folde browser
        self.label_path_preview = tk.Label(self.tab_measure, text='path')
        self.label_path_preview.place(x=self.col_1, y=self.set_row('measure')) 
        
        self.button_folder_browser = Button(self.tab_measure, text="Browse", command=self.browse_button)
        self.button_folder_browser.place(x=self.col_1b, y=self.set_row('measure', next=False))
        
        self.label_path = tk.Label(self.tab_measure, textvariable=self.path, wraplengt=150)
        self.label_path.place(x=self.col_2, y=self.set_row('measure', next=False)) 
        
        
        # entrys
        self.label_heigth = tk.Label(self.tab_measure, text='height')
        self.label_heigth.place(x=self.col_1, y=self.set_row('measure', rows=2))
        self.entry_heigth = tk.Entry(self.tab_measure)
        self.entry_heigth.insert(0, self.height.get())
        self.entry_heigth.place(x=self.col_2, y=self.set_row('measure', next=False))

        self.label_number = tk.Label(self.tab_measure, text='number')
        self.label_number.place(x=self.col_1, y=self.set_row('measure'))
        self.entry_number = tk.Entry(self.tab_measure)
        self.entry_number.insert(0, self.number.get())
        self.entry_number.place(x=self.col_2, y=self.set_row('measure', next=False))
        
        self.label_droptime = tk.Label(self.tab_measure, text='droptime')
        self.label_droptime.place(x=self.col_1, y=self.set_row('measure'))
        self.entry_droptime = tk.Entry(self.tab_measure)
        self.entry_droptime.insert(0, self.droptime.get())
        self.entry_droptime.place(x=self.col_2, y=self.set_row('measure', next=False))
        
        self.label_duration = tk.Label(self.tab_measure, text='duration')
        self.label_duration.place(x=self.col_1, y=self.set_row('measure'))
        self.entry_duration = tk.Entry(self.tab_measure)
        self.entry_duration.insert(0, self.duration.get())
        self.entry_duration.place(x=self.col_2, y=self.set_row('measure', next=False))
        
        self.label_rate = tk.Label(self.tab_measure, text='rate')
        self.label_rate.place(x=self.col_1, y=self.set_row('measure'))
        self.entry_rate = tk.Entry(self.tab_measure)
        self.entry_rate.insert(0, self.rate.get())
        self.entry_rate.place(x=self.col_2, y=self.set_row('measure', next=False))

        self.label_info = tk.Label(self.tab_measure, text='info')
        self.label_info.place(x=self.col_1, y=self.set_row('measure'))
        self.entry_info = tk.Entry(self.tab_measure)
        self.entry_info.place(x=self.col_2, y=self.set_row('measure', next=False), height=100)

        # check button
        checkvar_spec = BooleanVar()
        self.check_spec = Checkbutton(self.tab_measure, text = "log spectrometer", variable = checkvar_spec, 
                 onvalue = True, offvalue = False)
        self.check_spec.place(x=self.col_1, y=self.set_row('measure', rows=2.5))


        # dropdowns
        self.label_sample = tk.Label(self.tab_measure, text='sample')
        self.label_sample.place(x=self.col_1, y=self.set_row('measure'))
        self.sample = tk.StringVar()
        self.sample.set(self.samplelist[0])
        self.dropdown_sample = tk.OptionMenu(self.tab_measure, self.sample, *self.samplelist)
        self.dropdown_sample.place(x=self.col_2, y=self.set_row('measure', next=False))
        

        # Buttons
        self.button_start = tk.Button(self.tab_measure,
                                text="start measurement",
                                command=self.start_measurement)
        self.button_start.place(x=self.center, y=self.set_row('measure'))

        # tab test #######################################################################################

        # Buttons
        self.button_start = tk.Button(self.tab_test,
                                text="start test",
                                command=self.start_test)
        self.button_start.place(x=self.col_1, y=self.set_row('test'))

        self.button_start = tk.Button(self.tab_test,
                                text="stop test",
                                command=self.stop_test)
        self.button_start.place(x=self.col_2, y=self.set_row('test'))
        
        
        
        # running main
        self.root.mainloop()


    #reading props and setting varaibles
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
        self.height = IntVar()
        self.height.set(self.properties['height'])
        self.info = StringVar()
        self.sensor_to_plot = StringVar()
        self.sensor_to_plot.set('Mikro')
        

    def update_entrys(self):
        self.entry_heigth.delete(0, 'end')
        self.entry_number.delete(0, 'end')
        self.entry_droptime.delete(0, 'end')
        self.entry_duration.delete(0, 'end')
        self.entry_rate.delete(0, 'end')
        self.entry_info.delete(0, 'end')
        self.entry_heigth.insert(0, self.height.get())
        self.entry_number.insert(0, self.number.get())
        self.entry_droptime.insert(0, self.droptime.get())
        self.entry_duration.insert(0, self.duration.get())
        self.entry_rate.insert(0, self.rate.get())
        

    def set_row(self, tab, next=True, rows=1):
        if next:
            if tab == 'measure':
                # print(rows, next, self.row_counter)
                self.row_counter_measure += self.row_distance*rows 
                this_row_counter = self.row_counter_measure
            elif tab == 'test':
                self.row_counter_measure += self.row_distance*rows
                this_row_counter = self.row_counter_test
        else:
            if tab == 'measure':
                this_row_counter = self.row_counter_measure
            elif tab == 'test':
                this_row_counter = self.row_counter_test
        return this_row_counter


    def create_properties(self):
        rate= self.check_if_int(self.entry_rate.get())
        duration = self.check_if_int(self.entry_duration.get())
        sensors =self.sensors
        path = self.path.get()
        droptime = self.check_if_int(self.entry_droptime.get())
        sample = self.sample.get()
        number = self.check_if_int(self.entry_number.get())
        height = self.check_if_int(self.entry_heigth.get())
        time_stamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        last_dir = path[path.rfind('\\')+1:]
        print('last dir prop: ',last_dir)
        info = self.entry_info.get()
        
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
                    "samples": self.samplelist
                    }
        for item in properties:
            if properties[item] == None:
                return
            else:
                # Filehandling.update_properties(properties)
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
            start_measurement_app(this_properties)
            self.reload_properties()
            self.update_entrys()
            
        
    def browse_button(self):
        filename = filedialog.askdirectory()
        print('selected:', filename)
        self.path.set(filename) 
        
    def start_test(self):
        App_Test(3, 1000, 100, self.sensors, self.sensor_to_plot)
        
        # self.state_test = True
        # print('starting test')
        # self.test = Test_read()
        # while self.state_test == True:
        #     print(self.test.read_test_data())
            

    
    def stop_test(self):
        pass
        # try:
        #     self.state_test = False
        #     self.test.stop_process()
        # except:
        #     print('start test first!')

if __name__ == '__main__':
    App()


