
import seabreeze.spectrometers as sb
from seabreeze.spectrometers import Spectrometer
import pandas as pd
from matplotlib import pyplot as plt
from time import time_ns
import plotly.graph_objects as go

def read_spectra(duration, integration_time, path, show_plot=False):   
    ammount_spectras = int(duration*(1/(integration_time/1000000)))
    print(f'ammaount spectra: {ammount_spectras}')
    print(f'duration: {duration}')
    print(f'integration time: {integration_time}\n')

    spec = Spectrometer.from_first_available()
    spec.integration_time_micros(integration_time)
    counts = []
    timestamps = []
    print('starting spectrometer')
    start_time = time_ns()
    for i in range(ammount_spectras):
        counts.append(spec.intensities())
        timestamps.append((time_ns() - start_time)/100000000)
    wavelength = spec.wavelengths()
    spec.close()

    end_time = time_ns()
    duration_measurement = (end_time - start_time)/1000000000
    print(f'duration spectra: {duration_measurement}')
    print(f'start spectrometer: {start_time} in ns')

    df = pd.DataFrame(counts).T
    df.columns = timestamps
    df['wavelength'] = wavelength
    df.set_index('wavelength', inplace=True)
    df.to_csv(path, sep='\t', decimal='.', index=True)

    if show_plot:
        fig = go.Figure(data=[go.Surface(z=counts, y=timestamps, x=wavelength)])
        fig.update_layout(title='spectra', autosize=True,
                        width=800, height=800, scene = dict(
                            xaxis_title='wavelength [nm]',
                            yaxis_title='time [s]',
                            zaxis_title='counts'))
                    
        fig.show()
    


if __name__ == '__main__':
    read_spectra(1, 20000, "C:\\Users\\Matthias\\Desktop\\Messaufbau\\dataaquisition\\data\\test_small\\Blank_25_26-02-2022_16-52-52\\Blank_25_26-02-2022_16-52-52_spectra.txt")


