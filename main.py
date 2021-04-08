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
	def __init__(self, parent=None, width=5, height=4, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)
		super(MplCanvas, self).__init__(fig)
		fig.tight_layout()

class PloterMpl(QtWidgets.QMainWindow):
    WIDTH = 2
    CHANNELS = 1
    RATE = 8000
    
    def __init__(self):

        #plot props just copied, need check*
        self.samp_rate = 8000
        self.samp_step = 1/self.samp_rate
        self.window = 160000
        self.window_t = self.window * self.samp_step
        self.time_interval = 10 

        #define np arrays data x and y
        self.x = np.arange(0 , self.window_t , self.samp_step, dtype = float)
        self.y = np.zeros(self.window, dtype = float)
        self.plotdata = np.zeros(self.window, dtype = float)
        #define fig to plot
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)   

        #timer plot refresh interval (ms)
        self.interval = 30

        #define new Qthread for pyaudio
        self.threadpool = QtCore.QThreadPool()	
        self.threadpool.setMaxThreadCount(1)

        #buffer
        self.q = queue.Queue()
        
        self.plot_now = False
        
        
        QtWidgets.QMainWindow.__init__(self)
        self.resize(1024, 600)
        self.ui = uic.loadUi('main.ui', self)

        self.ui.gridLayout_3.addWidget(self.canvas, 0, 1, 2, 1)
        
        #timer for update plt
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.interval) #msec
        self.timer.timeout.connect(self.update_plt_list)
        self.timer.start()
        self.reference_plot = None
        self.p = pyaudio.PyAudio()
        
        self.pushButton.clicked.connect(self.start_worker)
        self.pushButton_2.clicked.connect(self.stop_stream)
        self.worker = None
        print('Setup ok')


    def start_worker(self):
        # disable all user imputs
        #clear axes plot

        #self.canvas.axes.clear()
        #self.go_on = False
        self.canvas.axes.clear()
        #set thread with start_audio()
        self.worker = Worker(self.start_audio, )
        self.threadpool.start(self.worker)	
        
        self.reference_plot = None
        self.timer.setInterval(self.interval) 

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
        try:
            #print('ACTIVE THREADS:',self.threadpool.activeThreadCount(),end=" \r")
            
            while True:
            
                QtWidgets.QApplication.processEvents()
            
                try: 
            
                    #self.data = self.q.get_nowait()
            
                    data = np.array(self.q.get_nowait())/32768


            
                except queue.Empty:
            
                    break
                shift = len(data)
                self.canvas.axes.set_facecolor((0,0,0))
                self.plotdata = np.roll(self.plotdata,-shift) 
                self.plotdata[-shift:] = data
                self.y = self.plotdata[:]
                xmin, xmax = self.canvas.axes.get_xlim()
                self.x = np.roll(self.x,-shift)
                self.x[-shift:] = np.arange(xmax,xmax + shift* self.samp_step, self.samp_step)

                #self.y = data[:]
                self.canvas.axes.set_facecolor((1,1,1))
                self.canvas.axes.set_xlim(xmin + shift*self.samp_step ,xmax + shift*self.samp_step)
                

            self.canvas.axes.plot(self.x, self.y, color=(0,1,0.29))
            self.canvas.axes.set_ylim( ymin=-1, ymax=1)
            self.canvas.axes.yaxis.grid(True,linestyle='--')
            #self.canvas.axes.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
            
            self.canvas.draw()
        except Exception as e:
            print("Error:",e)
        pass



    def run_loop(self):
        plt.show()

    def get_list(self):  
        data = self.q.get_nowait() 
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

