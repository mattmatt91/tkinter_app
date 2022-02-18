#import serial
from re import T
from tkinter import *
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from read_test import Test_read
import numpy as np

class App_Test():
    def __init__(self):
        # setting params
        self.rate = 100
        self.points_per_channel = 10
        self.sensors = ["Mikro", "Piezo", "VIS1", "IR1", "VIS2", "IR2"]
        self.dict_sensors = {}
        for sensor, i in zip(self.sensors, range(len(self.sensors))):
            self.dict_sensors[sensor] = i
        self.num_channels = len(self.sensors)

        # creating window
        self.root = Tk()
        self.root.geometry('1300x450')
        self.root.title('This is my root window')

        # init read data
        self.test_data_reader = Test_read(self.sensors,
                self.rate, self.points_per_channel)

        self.xar1 = []
        self.yar1 = []
        self.flag = True
        style.use('ggplot')
        self.fig = plt.figure(figsize=(14, 4.5), dpi=100)
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        self.line1, = self.ax1.plot(self.xar1, self.yar1)
        


    def animate(self,i):
        self.new_data = np.array(self.test_data_reader.read_test_data())  
        self.new_data = np.reshape(self.new_data,(int(self.points_per_channel/2),self.num_channels))
        self.new_time = np.arange((i*self.points_per_channel)/2, (self.points_per_channel/2)*(i+1))
        self.new_time = [n*(1/self.rate) for n in self.new_time]
        self.new_data_plot = self.new_data[:,self.dict_sensors['Mikro']].tolist()
        if self.flag == True:
            self.yar1 = self.new_data_plot
            self.xar1 = self.new_time
            self.flag = False
        else:
            self.yar1 += self.new_data_plot
            self.xar1 += self.new_time
        self.line1.set_data(self.xar1, self.yar1)

        self.ax1.set_xlim(self.new_time[-1]-2,self.new_time[-1])

        self.ax1.set_ylim(np.min(self.yar1), np.max(self.yar1))
        if i>= 1000:
            exit()

    def start(self):
        self.plotcanvas = FigureCanvasTkAgg(self.fig, self.root)
        self.plotcanvas.get_tk_widget().grid(column=1, row=1)
        self.ani = animation.FuncAnimation(self.fig, self.animate, interval=50, blit=False)
        self.root.mainloop()
        self.test_data_reader.stop_process()
        self.root.destroy()
    

if __name__ == '__main__':
    my_test_reader = App_Test()
    my_test_reader.start()