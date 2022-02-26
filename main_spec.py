
import seabreeze.spectrometers as sb
from seabreeze.spectrometers import Spectrometer
import pandas as pd
from matplotlib import pyplot as plt
from time import time_ns
import plotly.graph_objects as go

def read_spectra():
    start_time = time_ns()
    print('starting measurement')
    def get_time():
        return (time_ns() - start_time)/100000000


    ammount_spectras = 100
    spec = Spectrometer.from_first_available()
    spec.integration_time_micros(20000)
    counts = []
    timestamps = []

    for i in range(ammount_spectras):
        counts.append(spec.intensities())
        timestamps.append(get_time())


    fig = go.Figure(data=[go.Surface(z=counts, y=timestamps, x=spec.wavelengths())])
    fig.update_layout(title='spectra', autosize=True,
                    width=800, height=800, scene = dict(
                        xaxis_title='wavelength [nm]',
                        yaxis_title='time [s]',
                        zaxis_title='counts'))
                
    fig.show()


if __name__ == '__main__':
    read_spectra()


