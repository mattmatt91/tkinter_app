"""
This is the main mudule of the repository. It's main function starts a
measurement and guides the user through it. Set up path for saving data before start
"""

from datetime import datetime
import json as js
import os
from pathlib import Path

from readdata import read_data 

def get_immediate_subdirectories(a_dir):
    """
    This function creates a list with immediate subdirectories.

    Args:
        a_dir (string): path where subfolders are to be searched for

    Returns (list): list with pathes of subdiretories
    """
    print(a_dir)
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]  

def read_json(filename):
    """
    This function reads a json file and returns the content.
    The properties file with all parameters for the measurement
    is read here.

    Args:
        filename (stirng): name of the json file

    Returns:
        json_file (dictionary): dictionary with properties
    """
    with open(filename) as json_file:
        return js.load(json_file)
    
def get_path(properties):
    """
    This function guides the user into selecting the path to save the measurements.

    Args:
        properties (dictionary): dictionary with all parameters for the measurement

    Returns:
        folder (string): folder for saving measurements
        path (string): path for saving maeasurements
    """
    path = properties['path']
    last_dir = properties['lastdir']
    print('current directory: {0}'.format(path))
    print('select path')
    print('press:')
    folders = get_immediate_subdirectories(path)
    folders_dict = {1: last_dir}
    print('1 for last dir: ', last_dir)
    i = 2
    for folder in folders:
        folders_dict[i] = folder
        
        print(i, 'for ', folder)
        i += 1   
    print('press 0 for new folder') 
    folder = None
    while folder == None:
        user_input = input()
        try:
            folder = folders_dict[int(user_input)]
        except:
            try:
                if int(user_input) == 0:
                    user_input = input('set foldername: ')
                    directory = str(user_input)
                    this_path = os.path.join(path, directory)
                    Path(this_path).mkdir(parents=True, exist_ok=True)
                    print("Directory '%s' created" %directory)
                    folder = directory
            except:
                pass
                print('folder out of range')
    print(folder, ' selected')
    return folder, path

def select_sample(samples):
    """
    This function guides the user into selecting a sample for the measurement.

    Args:
        samples (list): list with all stored samples

    Returns:
        sample (string): sensor for measurement
    """
    print('select sample')
    print('press:')
    for sample, i in zip(samples, range(len(samples))):
        print(i, 'for', sample)
    sample = None
    while sample == None:
        user_input = int(input())
        try:
            sample = samples[user_input]
        except Exception as e:
            print('samlple out of range\n', e)
    print(sample, ' selected')
    return sample

def select_height():
    """
    This function guides the user into selecting height for measurements.

    Returns:
        height (int):height of the measurement
    """
    print('select height')
    print('enter int in cm:')
    height = None
    while height == None:
        user_input = input()
        try:
            height = int(user_input)
        except:
            pass
    print('height: ', height, 'cm')
    return height

def set_number():
    """
    This function guides the user into selecting a number for the measurement.

    Returns:
        sample_number (int): number for measurement
    """
    print('select number')
    print('enter int:')
    sample_number = None
    while sample_number == None:
        user_input = input()
        try:
            sample_number = int(user_input)
        except:
            print('not an integer')
    print('number: ', sample_number)
    return sample_number

def add_info():
    """
    This function guides the user into adding an info for the measurement.

    Returns:
        info (string): additional info for measurement
    """
    user_input = input('add info')
    return user_input

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
        path = os.path.join(properties['path'], folder, name)
    else:
        path = os.path.join(properties['path'], name)
    Path(path).mkdir(parents=True, exist_ok=True)
    path_file = os.path.join(path, name)
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

def start_measurement():
    """
    This is the main funciton of the module.
    It guides the user through the measurement via console.
    """

    # reading properties
    properties = read_json('properties.json')
    print(properties['samples'])
    samples = properties['samples']
    print(samples)
    # select path
    folder, path = get_path(properties)
    properties['lastdir'] = folder

    #select sample
    sample = select_sample(samples)
    properties["sample"]= sample

    #select height
    height = select_height()
    properties["height"]= height

    #select number of sample
    sample_number = set_number()
    properties['sample_number'] = sample_number

    #add info
    info = add_info()
    properties['info'] = info
    
    #setting timestamp
    properties["datetime"]= datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    # updating poperties global json
    update_properties(properties)
    
    # make dir for measurement
    path, path_file = mkdir(properties, folder)
    properties['path'] = path
    print(properties['sensors'])
    # saving properties for measurement
    save_properties_measurement(properties)
    # main measuring part
    print(properties['sensors'])
    read_data(properties, path_file)

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


if __name__ == '__main__':
    start_measurement()