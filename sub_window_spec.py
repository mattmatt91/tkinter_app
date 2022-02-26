#import serial
from logging import root
from re import T
from tkinter import *
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from read_spec_live import Test_read_spec
import numpy as np

class App_Test_Spec():
    def __init__(self, rate):
        
        # setting params
        print('start spec')
        
        self.rate = rate
        self.integration_time = (1/self.rate)*1000000
        print(f'integration time in micros{self.integration_time}')

        self.child = Toplevel()
        self.child.title('Monitoring')
        self.child.geometry('1300x450')

        # init read data
        self.test_spec_reader = Test_read_spec(self.rate, self.integration_time)
        
        self.xar1 = []
        self.yar1 = []
        self.flag = True
        style.use('ggplot')
        self.fig = plt.figure(figsize=(14, 4.5), dpi=100)
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        self.line1, = self.ax1.plot(self.xar1, self.yar1)
        


    def animate(self,i):
        self.new_counts, self.new_wl = self.test_spec_reader.read_test_data()

        
        self.yar1 = self.new_counts
        self.xar1 = self.new_wl

        self.line1.set_data(self.xar1, self.yar1)

        self.ax1.set_xlim(np.min(self.xar1),np.max(self.xar1))

        self.ax1.set_ylim(np.min(self.yar1),np.max(self.yar1))

    def start(self):
        # try:
        self.plotcanvas = FigureCanvasTkAgg(self.fig, self.child)
        
        self.plotcanvas.get_tk_widget().grid(column=1, row=1)
        self.interval = self.integration_time/1000
        self.ani = animation.FuncAnimation(self.fig, self.animate, interval=self.interval, blit=False) #interval in ms
        # except Exception as e:
            # print(e)
            # self.stop()

    def stop(self):
        plt.close()
        self.test_data_reader.stop_process()
        self.child.destroy()

    

if __name__ == '__main__':
        root = Tk()
        root.title('This is my root window')
        root.geometry('1300x450')


        rate = 100
        my_test_reader = App_Test_Spec(rate)
        my_test_reader.start()

        root.mainloop()

        