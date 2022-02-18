

"""
This module reads data from the DAQ Hardware.
It is based on the mcculw libary.
"""

from __future__ import absolute_import, division, print_function
from builtins import *  # @UnusedWildImport

from time import sleep, time_ns, time
from ctypes import cast, POINTER, c_double

from mcculw import ul
from mcculw.enums import ULRange, AnalogInputMode, ScanOptions, \
    FunctionType, Status, DigitalPortType,  DigitalIODirection
from mcculw.device_info import DaqDeviceInfo

import pandas as pd
import matplotlib.pyplot as plt

import numpy as np

class Test_read:
    def __init__(self, sensors, rate, points_per_channel):
        device_to_show = "USB-1808"
        self.board_num = 0
        self.memory_handle = None
        ai_range = ULRange.BIP10VOLTS
        self.buff_check = 0  # 0 = lower_half, 1 = upper_half

        # Verify board is Board 0 in InstaCal.  If not, show message...
        print("Looking for Board 0 in InstaCal to be {0} series..."
            .format(device_to_show))

        try:
            # Get the devices name...
            board_name = ul.get_board_name(self.board_num)

        except Exception as e:
            if ul.ErrorCode(1):
                # No board at that number throws error
                print("\nNo board found at Board 0.")
                print(e)
                return

        else:
            if device_to_show in board_name:
                # Board 0 is the desired device...
                print("{0} found as Board number {1}.\n"
                    .format(board_name, self.board_num))
                ul.flash_led(self.board_num)

            else:
                # Board 0 is NOT desired device...
                print("\nNo {0} series found as Board 0. Please run InstaCal."
                    .format(device_to_show))
                return
        


        # select channels...
        low_channel = 0
        high_channel = len(sensors)-1
        self.num_channels = high_channel - low_channel + 1

        # Set channel(s) to single ended input mode...
        for channel in range(self.num_channels):
            ul.a_chan_input_mode(self.board_num, channel,
                                AnalogInputMode.SINGLE_ENDED)

        # Set up memory handle...
        self.total_count = points_per_channel * self.num_channels
        self.memory_handle = ul.scaled_win_buf_alloc(self.total_count)
        self.buffer_mid_point = self.total_count / 2

        # Convert the self.memory_handle to a ctypes array...
        self.ctypes_array = cast(self.memory_handle, POINTER(c_double))

        # Check if the buffer was successfully allocated...
        if not self.memory_handle:
            raise Exception('Error: Failed to allocate memory')

        scan_options = ScanOptions.BACKGROUND | ScanOptions.SCALEDATA
        scan_options |= ScanOptions.CONTINUOUS

        # Start the scan...
        ul.a_in_scan(
            self.board_num, low_channel, high_channel, self.total_count,
            rate, ai_range, self.memory_handle, scan_options)

        self.status, current_count, current_index = ul.get_status(
            self.board_num, FunctionType.AIFUNCTION)


    def read_test_data(self):

        try:
            while self.status != Status.IDLE:
                try:
                    # Get the status of the background operation
                    self.status, current_count, current_index = ul.get_status(
                        self.board_num, FunctionType.AIFUNCTION)
                    # print('status: {0} current count: {1} current index: {2} buffer mid point: {3}'
                    #            .format(self.status, current_count, current_index, self.buffer_mid_point))
                    # Display the data.
                    if current_index > self.buffer_mid_point:
                        # get the lower half.
                        if self.buff_check == 0:
                            self.buff_check = 1
                            loop_index = 0
                            my_buffer_outer =[]
                            while loop_index < self.buffer_mid_point:
                                my_buffer = []
                                for data_index in range(loop_index,
                                                        (loop_index + self.num_channels)):
                                    eng_value = self.ctypes_array[data_index]
                                    my_buffer.append(eng_value)
                                loop_index += self.num_channels
                                my_buffer_outer.append(my_buffer)
                            # print(np.array(my_buffer_outer).shape)
                            # print(np.array(my_buffer_outer))
                            # print()
                            
                            return np.array(my_buffer_outer)
                            
                    elif current_index < self.buffer_mid_point:

                        # get the upper half.
                        if self.buff_check == 1:
                            self.buff_check = 0
                            loop_index = int(self.buffer_mid_point)
                            my_buffer_outer =[]
                            while loop_index < self.total_count:
                                my_buffer = []
                                for data_index in range(loop_index,
                                                        (loop_index + self.num_channels)):
                                    eng_value = self.ctypes_array[data_index]
                                    my_buffer.append(eng_value)
                                loop_index += self.num_channels
                                my_buffer_outer.append(my_buffer)
                            # print(np.array(my_buffer_outer).shape)
                            # print(np.array(my_buffer_outer))
                            # print()
                            
                            return np.array(my_buffer_outer)
                except Exception as e:
                    print('error in measure loop')
                    print(e)

        except Exception as e:
            print('\n', e)
            ul.stop_background(self.board_num, FunctionType.AIFUNCTION)
            print('\nScan failed')

    def stop_process(self):
        try:
            ul.stop_background(self.board_num, FunctionType.AIFUNCTION)
            print('\nScan completed successfully')

            if self.memory_handle:
                        # Free the buffer in a finally block to prevent a memory leak.
                        ul.win_buf_free(self.memory_handle)

        except Exception as e:
            print('error in finally: ',e)
        
        


if __name__ == '__main__':
    sensor_to_plot = 'Mikro'
    width_to_show = 3
    rate = 100
    points_per_channel = 10
    sensors = ["Mikro", "Piezo", "VIS1", "IR1", "VIS2", "IR2"]
    test = Test_read(sensors, rate, points_per_channel)
    while True:
        print(test.read_test_data())
    # test.stop_process()