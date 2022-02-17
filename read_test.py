

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

class Test_read:
    def __init__(self):
        device_to_show = "USB-1808"
        self.board_num = 0
        rate = 1000
        points_per_channel = 100
        self.memory_handle = None
        ai_range = ULRange.BIP10VOLTS
        self.max_samples = rate*1
        sensors = ["Mikro", "Piezo", "VIS1", "IR1", "VIS2", "IR2"]



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
        
    def read_test(self):
            try:

                self.start_time = time_ns()
                sample_index = 0
                i = 0
                while self.status != Status.IDLE:
                    print(i)
                    i += 1
                    try:
                        # Get the status of the background operation
                        status, current_count, current_index = ul.get_status(
                            self.board_num, FunctionType.AIFUNCTION)
                            
                        # Display the data.
                        if current_index > self.buffer_mid_point:
                            print('lower')
                            # get the lower half.
                            if self.buff_check == 0:
                                self.buff_check = 1
                                loop_index = 0
                                while loop_index < self.buffer_mid_point:
                                    my_buffer = []
                                    sample_index += 1
                                    for data_index in range(loop_index,
                                                            (loop_index + self.num_channels)):
                                        eng_value = self.ctypes_array[data_index]
                                        my_buffer.append(eng_value)
                                    print(len(my_buffer), 1)
                                    loop_index += self.num_channels

                        elif current_index < self.buffer_mid_point:
                            print('upper')
                            # get the upper half.
                            if self.buff_check == 1:
                                self.buff_check = 0
                                loop_index = int(self.buffer_mid_point)
                                while loop_index < self.total_count:
                                    my_buffer = []
                                    sample_index += 1
                                    for data_index in range(loop_index,
                                                            (loop_index + self.num_channels)):
                                        eng_value = self.ctypes_array[data_index]
                                        my_buffer.append(eng_value)
                                    print(len(my_buffer), 2)
                                    loop_index += self.num_channels
                    except Exception as e:
                        print(e)

            except Exception as e:
                print('\n', e)

    def stop_process(self):
        try:
            ul.stop_background(self.board_num, FunctionType.AIFUNCTION)
            print('\nScan completed successfully')
            print('measurement time = ', '{:10d}'.format(time_ns()- self.start_time))

            if self.memory_handle:
                        # Free the buffer in a finally block to prevent a memory leak.
                        ul.win_buf_free(self.memory_handle)

        except Exception as e:
            print('error in finally: ',e)
        
        


if __name__ == '__main__':

    test = Test_read()
    test.read_test()
    test.stop_process()