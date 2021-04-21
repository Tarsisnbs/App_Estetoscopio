# -*- coding: utf-8 -*-

# Plot live audio Eletronic Stethoscope 

#Conrado/Tarsis

#bibliotecas essenciais 
import matplotlib.pyplot as plt
import sys 
import matplotlib 
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import matplotlib.ticker as ticker
import numpy as np
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
import queue 
import pyaudio

from matplotlib.figure import Figure
class Ploter (FigureCanvas):
    
    def __init__(self,obj, samp_rate, parent=None, width=5, height=4, dpi=100 ):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(Ploter, self).__init__(fig)
        #atributos
        #regras de negocio (mudar de lugar)
        self.samp_rate = samp_rate
        self.samp_step = 1/self.samp_rate
        self.window_t = 2
        self.window = self.window_t/self.samp_step

        self.x, self.y = self.init_plot_axis(self.window_t, self.samp_rate)
        self.axes.set_xlim(0, self.window_t)
        fig.tight_layout()
    
    def init_plot_axis(self, window_t, samp_rate):
        samp_step = 1/samp_rate
        window_s = window_t*samp_rate
        x = np.arange(0 , window_t , samp_step, dtype = float)
        y = np.zeros(window_s, dtype=float)
        return (x,y)

    def plot_signal(self, signal): #public
        self.axes.clear()
        self.axes.plot(np.arange(0,len(signal)*self.samp_step,self.samp_step), signal, color = (0,1,0), lw=0.5)
        self.draw()
    
    def process_plot(self, data):
        shift = len(data)
        xmin, xmax = self.axes.get_xlim()
        if( self.x[0] < self.window_t): 
            self.y[:shift] = data
        else: 
            self.y = np.roll(self.y,-shift)
            self.y[-shift:] = data
            self.axes.set_xlim(xmin + shift*self.samp_step ,xmax + shift*self.samp_step)
        
        self.x = np.roll(self.x,-shift)
        self.x[-shift:] = np.arange(xmax,xmax + shift* self.samp_step, self.samp_step)

    def plot_real_time (self,data): #public
        self.process_plot(data)
        self.axes.set_facecolor((1,1,1))
        self.axes.set_ylim( ymin=-1, ymax=1)
        self.axes.plot(self.x, self.y, color = (0,1,0), lw=0.5)
        self.draw()
        
    def clear_plot(self): #Não testado
        self.axes.clear()
        pass
               
import soundfile as sf
class Registrador(): 
    def __init__(self, samp_rate):
        self.audio_memorized = []
        self.audio_f_memorized = []
        self.samp_rate = samp_rate
    
    def get_audio_signal_np(self):
        audio_array = np.array(self.audio_memorized)/32768 #Audio NP Array NORM
        return audio_array
    
    def get_audio_signal_filt_np(self):
        audio_array = np.array(self.audio_f_memorized)/32768 #Audio NP Array NORM
        return audio_array

    def set_signal_f(self, data):
        self.audio_f_memorized= data

    def extend_signal(self, data):
        self.audio_memorized.extend(data)

    def save_wav(self): 
        sf.write('audio_file.wav', self.audio_memorized, self.samp_rate, 'PCM_24') 
        sf.write('audio_f_file.wav', self.audio_f_memorized, self.samp_rate, 'PCM_24') 
        '''
        if(self.audio_f_memorized == []):
            pass
        else:
            sf.write('audio_f_file.wav', self.audio_f_memorized, self.samp_rate, 'PCM_24') 
        '''
    def load_wav(self): 
        self.audio_memorized = sf.read('audio_file.wav', self.audio_memorized, self.samp_rate, 'PCM_24')
        
    
    def clear_memory(self): #Não testado
        self.audio_memorized = [] 

from scipy.signal import butter, lfilter, lfilter_zi, freqs    
class Filter(): 
    def __init__(self, lowcut, highcut, samp_rate):
        self.b, self.a = self.butter_bandpass(lowcut, highcut, samp_rate)

    def butter_bandpass(self, lowcut, highcut, sRate):
        order=2
        nyq = 0.5 * sRate
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        w, h = freqs(a, b)
        print(a, b)
        return b, a

    def filtrar_sin(self, data):
        zi = lfilter_zi(self.b, self.a)
        y,zo = lfilter(self.b, self.a, data, zi=zi*data[0])
        return y

class PloterMpl(QtWidgets.QMainWindow):
    WIDTH = 2
    CHANNELS = 1
    RATE = 8000
    
    def __init__(self):

        #Flags
        self.GRAVANDO = False

        #plot props
        self.samp_rate = 8000
        
        self.canvas = Ploter(self, self.samp_rate, width=5, height=4, dpi=100)
        self.interval = 30

        #define new Qthread for pyaudio
        self.threadpool = QtCore.QThreadPool()	
        self.threadpool.setMaxThreadCount(1)

        #buffer
        self.q = queue.Queue()
        self.plot_now = False
        
        #Armazenamento
        self.registrador = Registrador(self.samp_rate)

        #Filtragem 
        self.filtro = Filter(500, 2000, self.samp_rate)

        QtWidgets.QMainWindow.__init__(self)
        self.resize(1024, 600)
        self.ui = uic.loadUi('main.ui', self)

        self.ui.gridLayout_3.addWidget(self.canvas, 0, 1, 2, 1)
        
        #timer for update plt
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.interval)
        self.timer.timeout.connect(self.gravar)
        self.timer.start()

        self.p = pyaudio.PyAudio()
        
        self.pushButton.clicked.connect(self.start_worker)
        self.pushButton_2.clicked.connect(self.stop_stream)
        self.pushButton_3.clicked.connect(self.clear_all)
        self.pushButton_4.clicked.connect(self.filtrar)
        self.pushButton_10.clicked.connect(self.salvar)
        self.worker = None
        print('Setup ok')


    def start_worker(self):
        self.GRAVANDO = True
        self.worker = Worker(self.start_audio, )
        self.threadpool.start(self.worker)	
        self.timer.setInterval(self.interval) 

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
        self.GRAVANDO = False
        self.canvas.plot_signal(self.registrador.get_audio_signal_np())
        
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def update_system(self):
        try:
            while True:
                QtWidgets.QApplication.processEvents()
                try: 
                    data_list = self.q.get_nowait()
                    data = np.array(data_list)/32768
                except queue.Empty:
            
                    break
                self.canvas.plot_real_time(data)
                self.registrador.extend_signal(data_list)
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

    def clear_all(self): 
        self.canvas.clear_plot
        self.registrador.clear_memory
        QtWidgets.QApplication.processEvents()

    def gravar(self): 
        
        try:
            while self.GRAVANDO == True:
                QtWidgets.QApplication.processEvents()
                try: 
                    data_list = self.q.get_nowait()
                    data = np.array(data_list)/32768
                except queue.Empty:
            
                    break
                self.canvas.plot_real_time(data)
                self.registrador.extend_signal(data_list)
            
        except Exception as e:
            print("Error:",e)
        pass
        pass

    def filtrar(self):
        sinal = self.registrador.get_audio_signal_np()
        sinal_f = self.filtro.filtrar_sin(sinal)
        self.registrador.set_signal_f(sinal_f) 
        self.canvas.plot_signal(sinal_f)
        pass 
    def play(): 
        pass 
    def salvar(self): 
        self.registrador.save_wav()
        pass
        
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


