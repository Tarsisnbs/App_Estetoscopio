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
from PyQt5.QtCore import pyqtSlot
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
        self.interval = 30
        self.time_interval = 20

        #define new Qthread
        self.threadpool = QtCore.QThreadPool()	
        self.threadpool.setMaxThreadCount(1)

        self.q = queue.Queue()
        self.canvas = MplCanvas(self, width=5, height=4, dpi=50)
        
        QtWidgets.QMainWindow.__init__(self)
        self.resize(1024, 600)
        
        self.ui = uic.loadUi('main.ui', self)
        self.ui.gridLayout_3.addWidget(self.canvas, 0, 1, 2, 1)
        

        self.p = pyaudio.PyAudio()
        print("objeto instanciado: p -> Pyaudio()")
        
        self.pushButton.clicked.connect(self.start_worker)
        self.pushButton_2.clicked.connect(self.stop_stream)
        self.worker = None
        print('Setup ok')
    
    def start_worker(self):
        # disable all user imputs
        #clear axes plot

        #self.canvas.axes.clear()
        #self.go_on = False

        #set thread with start_audio()
        self.worker = Worker(self.start_audio, )
        self.threadpool.start(self.worker)	
        
        #self.reference_plot = None
        #self.timer.setInterval(self.interval) 

    def new_method(self):
         self.lineEdit.setEnabled(False)#msec

    def start_audio(self):
        try:
            #process all events
            QtWidgets.QApplication.processEvents()

            #define callback and stream
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
            #process all events 4ever *
            while self.stream.is_active():
                    QtWidgets.QApplication.processEvents()
						
        except Exception as e:
            print("ERROR: ",e)
            pass


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


class Worker(QtCore.QRunnable):

	def __init__(self, function, *args, **kwargs):
		super(Worker, self).__init__()
		self.function = function
		self.args = args
		self.kwargs = kwargs

	@pyqtSlot()
	def run(self):

		self.function(*self.args, **self.kwargs)

app = QtWidgets.QApplication(sys.argv)
MainWindow  = PloterMpl()
MainWindow.show()
sys.exit(app.exec_())

