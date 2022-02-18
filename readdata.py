
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


def read_data(properties, path, app=False):
    """
    This is the main function of the module.
    This function records data with the parameters stored in
    `properties.json <https://github.com/mattmatt91/Promotion_read/blob/17d5377d9a9d683c8a0f6951d904f73331a6ba1e/read_data/functions/properties.json>`_

    Args:
        properties (dictionary): dictionary with all parameters for the measurement
        path (string): path to the measurement file
    """
    print(properties)
    channel_num = 0
    device_to_show = "USB-1808"
    board_num = 0
    rate = properties['rate']
    points_per_channel = int(properties['rate']/10)
    memory_handle = None
    ai_range = ULRange.BIP10VOLTS
    max_samples = rate*properties['duration']
    droptime = properties['droptime']
    sensors = properties['sensors']



    buff_check = 0  # 0 = lower_half, 1 = upper_half

    # Verify board is Board 0 in InstaCal.  If not, show message...
    print("Looking for Board 0 in InstaCal to be {0} series..."
          .format(device_to_show))

    try:
        # Get the devices name...
        board_name = ul.get_board_name(board_num)

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
                  .format(board_name, board_num))
            ul.flash_led(board_num)

        else:
            # Board 0 is NOT desired device...
            print("\nNo {0} series found as Board 0. Please run InstaCal."
                  .format(device_to_show))
            return
    

    try:
        
        # select channels...
        low_channel = 0
        high_channel = len(sensors)-1
        num_channels = high_channel - low_channel + 1

        # Set channel(s) to single ended input mode...
        for channel in range(num_channels):
            ul.a_chan_input_mode(board_num, channel,
                                 AnalogInputMode.SINGLE_ENDED)
        
        # set up digital out
        port_value = 0xFF
        magnet = True
        daq_dev_info = DaqDeviceInfo(board_num)
        dio_info = daq_dev_info.get_dio_info()
        port = next((port for port in dio_info.port_info if port.supports_output),
                    None)
        if not port:
            raise Exception('Error: The DAQ device does not support '
                            'digital output')

        if port.is_port_configurable:
            ul.d_config_port(board_num, port.type, DigitalIODirection.OUT)
        print('Setting', port.type.name, 'to', port_value)
        ul.d_out(board_num, port.type, port_value)

        # Set up memory handle...
        total_count = points_per_channel * num_channels
        memory_handle = ul.scaled_win_buf_alloc(total_count)
        buffer_mid_point = total_count / 2

        # Convert the memory_handle to a ctypes array...
        ctypes_array = cast(memory_handle, POINTER(c_double))

        # Check if the buffer was successfully allocated...
        if not memory_handle:
            raise Exception('Error: Failed to allocate memory')

        scan_options = ScanOptions.BACKGROUND | ScanOptions.SCALEDATA
        scan_options |= ScanOptions.CONTINUOUS

        # Start the scan...
        ul.a_in_scan(
            board_num, low_channel, high_channel, total_count,
            rate, ai_range, memory_handle, scan_options)

        # print('actual scan rate = ', '{:.6f}'.format(rate), 'Hz\n')

        print('Please enter CTRL + C to terminate the process\n')

        status, current_count, current_index = ul.get_status(
            board_num, FunctionType.AIFUNCTION)
        if not app:
            start = False
            while start == False:
                user_input = input('press 1 to start')
                if int(user_input) == 1:
                    start = True
        print("starting...")

        try:
            data = []
            last_time = time()
            start_time = time_ns()
            sample_index = 0
            while status != Status.IDLE and sample_index <= max_samples:

                # controll the magnet
                ############################################
                if time() - last_time >= droptime and magnet:
                    magnet = False
                    ul.d_out(board_num, port.type, 0000)
                    print('magnet falling')
                ############################################
                try:
                    # Get the status of the background operation
                    status, current_count, current_index = ul.get_status(
                        board_num, FunctionType.AIFUNCTION)
                           
                    # Display the data.
                    if current_index > buffer_mid_point:
                        # get the lower half.
                        if buff_check == 0:
                            buff_check = 1
                            loop_index = 0
                            while loop_index < buffer_mid_point:
                                my_buffer = []
                                sample_index += 1
                                for data_index in range(loop_index,
                                                        (loop_index + num_channels)):
                                    eng_value = ctypes_array[data_index]
                                    my_buffer.append(eng_value)
                                data.append(my_buffer)
                                loop_index += num_channels

                    elif current_index < buffer_mid_point:
                        # get the upper half.
                        if buff_check == 1:
                            buff_check = 0
                            loop_index = int(buffer_mid_point)
                            while loop_index < total_count:
                                my_buffer = []
                                sample_index += 1
                                for data_index in range(loop_index,
                                                        (loop_index + num_channels)):
                                    eng_value = ctypes_array[data_index]
                                    my_buffer.append(eng_value)
                                data.append(my_buffer)
                                loop_index += num_channels
                except (ValueError, NameError, SyntaxError):
                    break

        except KeyboardInterrupt:
            pass

    except Exception as e:
        print('\n', e)

    finally:
        try:
            ul.stop_background(board_num, FunctionType.AIFUNCTION)
            print('\nScan completed successfully')
            print('measurement time = ', '{:10d}'.format(time_ns()- start_time))

            if memory_handle:
                        # Free the buffer in a finally block to prevent a memory leak.
                        ul.win_buf_free(memory_handle)

            df = pd.DataFrame(data, columns=properties['sensors'])
            df['time [s]'] = [i/rate for i in df.index]
            df.set_index('time [s]', inplace=True) 
            print(df.head())
            print(df.info())
            df.to_csv(path, sep='\t', decimal='.', index=True)
            df.plot()
            plt.show()
        except Exception as e:
            print('error in finally: ',e)
        
        



