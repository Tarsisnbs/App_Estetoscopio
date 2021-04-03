# -*- coding: utf-8 -*-

# Plot live audio Eletronic Stethoscope 

#Conrado/Tarsis

#bibliotecas essenciais 
import matplotlib.pyplot as plt
import sys 
import matplotlib 
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as ticker
import numpy as np

from matplotlib.animation import FuncAnimation
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5 import uic
import time
import queue 
import pyaudio

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None , width =1, height=1, dpi=50 ):
        self.window = 40000
        
        #fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig, self.axes = plt.subplots(figsize=(8,4))
        
        self.x_vals = []
        self.y_vals = []
    
        self.axes.set_title("Original Sound")
        self.axes.set_ylim(-1.1, 1.1)
        self.axes.set_xlim(0, self.window)
        self.axes.set_facecolor((1,1,1))
        self.axes.grid()
        FigureCanvas.__init__(self, self.fig)
        

class PloterMpl(QtWidgets.QMainWindow):
    WIDTH = 2
    CHANNELS = 1
    RATE = 8000

    def __init__(self):
        self.time_interval = 20
        self.q = queue.Queue()
        self.canvas = MplCanvas(self, width=5, height=4, dpi=50)
        QtWidgets.QMainWindow.__init__(self)
        self.resize(1024, 600)
        self.ui = uic.loadUi('main.ui', self)
        self.ui.gridLayout_3.addWidget(self.canvas, 0, 1, 2, 1)
       
        print("objeto Ploter instanciado : area de plot criada")
        self.pushButton.clicked.connect(self.start_audio)
        self.pushButton_2.clicked.connect(self.stop_stream)
        
    
    def start_audio(self):
        #inicialização pyaudio
        self.pushButton.setEnabled(False)
        #self.ani  = FuncAnimation(self.fig, self.update_plt_list, interval=self.time_interval,blit=True, frames = 500)
        self.p = pyaudio.PyAudio()
        
        def callback(in_data, frame_count, time_info, status):
            self.put_list((np.frombuffer(in_data, dtype=np.int16)))
            return (in_data, pyaudio.paContinue)

        self.stream = self.p.open(format=self.p.get_format_from_width(self.WIDTH),
                    channels=self.CHANNELS,
                    rate=self.RATE,
                    input=True,
                    output=True,
                    frames_per_buffer = 1000,
                    stream_callback=callback)
        self.stream.start_stream()
        while self.stream.is_active():
                self.update_plt_list()

        
    
    def stop_stream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def update_plt_list(self):
        data = self.get_list()
        shift = len(data)
        self.canvas.y_vals.extend(data)
        self.canvas.x_vals = list(range(0, (len(self.canvas.y_vals))))
        xmin, xmax = self.canvas.axes.get_xlim()
        if len(self.canvas.x_vals)> self.canvas.window:
            #shift frame and signal
            del self.canvas.y_vals[:shift]
            del self.canvas.x_vals[:shift]
            self.canvas.axes.set_xlim(xmax,xmax + self.canvas.window)
            #redraw all
            self.canvas.axes.figure.canvas.draw()
            #update x axys
            for n in range (len(self.canvas.x_vals)):
                self.canvas.x_vals[n] = n + xmax
            ###########
        print(self.canvas.y_vals)
        self.lines = self.canvas.axes.plot(np.array(self.canvas.x_vals), np.array(self.canvas.y_vals)/32768, color = (0,0,0), lw=0.5)
        self.canvas.draw()

        
        #print("n samples:", len(self.y_vals), "n shift samp:", shift)
        return(self.lines)
    #def run_loop(self):
        
    def run_loop(self):
        plt.show()

    def get_list(self):  
        data = self.q.get() 
        return data

    def put_list(self, thing):
        self.q.put(thing)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow  = PloterMpl()
    MainWindow.show()
    sys.exit(app.exec_())