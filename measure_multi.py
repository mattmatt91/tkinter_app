from readdata import read_data
from read_spec import read_spectra
import multiprocessing
import time


def start_measurement_multi(properties, path_file):
    duration = properties['duration']
    integration_time = properties['integration_time_micros']
    log_spec = properties['log_spec']  
    path_spectra = path_file[:path_file.rfind('.')] + '_spectra.txt'


    process_data = multiprocessing.Process(target=read_data, args=[properties, path_file])
    process_spectra = multiprocessing.Process(target=read_spectra, args=[duration, integration_time, path_spectra])

    process_data.start()
    process_spectra.start()

    print('starting measurent...')
    start_time = time.time_ns()

    process_data.join()
    process_spectra.join()

    end_time = time.time_ns()
    duration_multi_procces = (end_time - start_time)/1000000000
    print(f'duration: {duration_multi_procces}')