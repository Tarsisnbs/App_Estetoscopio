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
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
import queue 
import pyaudio
import soundfile as sf

class Ploter (FigureCanvas):
    
    def __init__(self, window_t, samp_step, parent=None, width=5, height=4, dpi=100 ):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(Ploter, self).__init__(fig)
        #plot props just copied, need check*
        self.samp_step = 1/8000
        self.window_t = 2
        self.window = 16000
        self.axes.set_xlim(0, self.window_t)
        self.time_interval = 30 

        #define np arrays data x and y
        self.x = np.arange(0 , self.window_t , self.samp_step, dtype = float)
        self.y = np.zeros(self.window, dtype = float)
        fig.tight_layout()
    
    pass
    def plot_signal(self, signal, samp_step):
        self.axes.clear()
        self.axes.plot(np.arange(0,len(signal)*samp_step,samp_step), signal, color = (0,1,0), lw=0.5)
        self.draw()
        
    def plot_real_time (self,data, samp_step, window_t):
        shift = len(data)
        
        xmin, xmax = self.axes.get_xlim()
        
        if( self.x[0] < window_t): 
            self.y[:shift] = data
            print("buffering x:", self.x[0])
        else: 
            self.y = np.roll(self.y,-shift)
            self.y[-shift:] = data
            self.axes.set_xlim(xmin + shift*samp_step ,xmax + shift*samp_step)
        
        self.x = np.roll(self.x,-shift)
        self.x[-shift:] = np.arange(xmax,xmax + shift* self.samp_step, self.samp_step)
        
        self.axes.set_facecolor((1,1,1))
        self.axes.set_ylim( ymin=-1, ymax=1)
        self.axes.plot(self.x, self.y, color = (0,1,0), lw=0.5)
        print(self.x)
        self.draw()       

class Registrador(): 
    def __init__(self):
        pass
    def save_wav(audio_array): 
        sf.write('stereo_file.wav', audio_array, 8000, 'PCM_24') 

    def load_wav(): 
        pass
    
    pass

class PloterMpl(QtWidgets.QMainWindow):
    WIDTH = 2
    CHANNELS = 1
    RATE = 8000
    
    def __init__(self):

        #plot props just copied, need check*
        self.samp_rate = 8000
        self.samp_step = 1/self.samp_rate
        self.window = 16000
        self.window_t = self.window * self.samp_step
        self.time_interval = 30 
        
        self.canvas = Ploter(self, self.samp_step, self.window_t, width=5, height=4, dpi=100)
        self.interval = 30

        #define new Qthread for pyaudio
        self.threadpool = QtCore.QThreadPool()	
        self.threadpool.setMaxThreadCount(1)

        #buffer
        self.q = queue.Queue()
        self.plot_now = False
        
        #self.audio_array = np.arange(0, self.audio_size*self.samp_rate, dtype = float)
        self.audio_list = []
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
        sf.write('audio_file.wav', np.array(self.audio_list)/32768, 8000) 
        self.canvas.plot_signal(np.array(self.audio_list)/32768, self.samp_step)
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def update_plt_list(self):
        try:
            #print('ACTIVE THREADS:',self.threadpool.activeThreadCount(),end=" \r")
            
            while True:
            
                QtWidgets.QApplication.processEvents()
            
                try: 
                    data_list = self.q.get_nowait()
                    data = np.array(data_list)/32768

                except queue.Empty:
            
                    break
                self.canvas.plot_real_time(data, self.samp_step, self.window_t)
                self.audio_list.extend(data_list)
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