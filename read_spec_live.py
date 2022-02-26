

"""
This module reads data from the DAQ Hardware.
It is based on the mcculw libary.
"""



from time import sleep, time_ns, time
import seabreeze.spectrometers as sb
from seabreeze.spectrometers import Spectrometer

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class Test_read_spec:
    def __init__(self, rate, integration_time):
        self.integration_time = integration_time
        self.spec = Spectrometer.from_first_available()
        self.spec.integration_time_micros(self.integration_time)

    def read_test_data(self):
        counts = self.spec.intensities()
        return counts, self.spec.wavelengths()


    def stop_process(self):
        pass
        
        
if __name__ == '__main__':
    rate = 100
    test = Test_read_spec(rate)
    while True:
        print(test.read_test_data())
    # test.stop_process()