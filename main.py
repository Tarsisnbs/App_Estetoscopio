# -*- coding: utf-8 -*-

# Plot live audio Eletronic Stethoscope 

#Conrado/Tarsis

#bibliotecas essenciais 
from PyQt5.QtGui import QDragEnterEvent, QDragMoveEvent
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
import scipy.signal as signal
from scipy.signal import butter, lfilter, lfilter_zi, freqs

#Struct of State Machine with all the valid states and yor transictions (flag plus next state)
#the structure is a fork described by a list dictionary
#like: {VALID_STATE:[(flag_A, state_A), (flag_B, state_B)]} for a valid state with two possibles transictions (A and B)
struct_state_machine = {"INICIO":[("setup_end","ESPERANDO")], "ESPERANDO":[("rec_now","GRAVANDO"), ("filter_now","FILTRANDO"), ("save_now", "SALVANDO"), 
                        ("open_now", "CARREGANDO"), ("clear_now", "CLEARING"), ("play_now", "REPRODUZINDO")], "GRAVANDO":[("wait_now", "ESPERANDO")], 
                        "FILTRANDO":[("wait_now", "ESPERANDO")], "SALVANDO":[("wait_now", "ESPERANDO")], "CARREGANDO":[("wait_now", "ESPERANDO")], "CLEARING":[("wait_now", "ESPERANDO")], 
                        "REPRODUZINDO":[("wait_now", "ESPERANDO")], "PAUSE":[("wait_now", "ESPERANDO")]}

#Dictionary with the state of all flags of the system
flags_status = {"setup_end":False, "rec_now":False, "rec_end":False, "filter_now":False, "save_now":False, "open_now":False, "clear_now":False, "play_now":False, "pause_now":False, "wait_now":False}
'''
@staticmethod
def print_log(string=s):
    s = string
    l = sys.stdout.write("\r", s, "\n")
    sys.stdout.flush()
'''

class State():
    def __init__(self,current_state, next_state, condition_flag):
        self.state_name = current_state
        self.next_state = next_state
        self.condition_flag = condition_flag

    def check_flag(self, flag_status):
        if flag_status[self.condition_flag]:
            return self.next_state
        else: 
            return self.state_name
    def go_next_state(self):
        self.state_name = self.next_state

from scipy.fft import fft, fftfreq
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

        self.freq_dom = False

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
        
        if self.freq_dom == True:
            print("lol")
            self.plot_freq(signal)
            
        else:
            self.axes.clear()
            self.axes.grid()
            self.axes.plot(np.arange(0,len(signal)*self.samp_step,self.samp_step), signal, color = (0,0,0), lw=0.5)
            self.axes.set_ylim( ymin=-1, ymax=1)
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
        self.axes.plot(self.x, self.y, color = (0,0,0), lw=0.5)
        self.draw()

    def plot_mark_time(self, current_time):
        print("time: ", current_time)
        n = self.axes.axvline((current_time), color='green') #
        self.draw()
        plt.Axes.remove(n)

    def fft_transf(self, y, N, T):
        yf = fft(y)
        xf = fftfreq(N, T)[:N//2]
        return yf, xf

    def plot_freq(self,data):
        self.clear_plot()
        N = len(data)
        yf_freq, xf_freq = self.fft_transf(data, N, self.samp_step )
        self.axes.plot(xf_freq, 2.0/N * np.abs(yf_freq[0:N//2]))
        self.axes.grid()
        self.draw()

    def clear_plot(self): #Não testado
        self.axes.clear()
        self.draw
        pass
               
import soundfile as sf
class Registrador(): 
    def __init__(self, samp_rate):
        self.filters_memorized = {"PB":[], "PA":[], "NT":[]}
        self.audio_memorized = []
        self.audio_f_memorized = []
        self.samp_rate = samp_rate
        self.time_player = 0
    ##############
    def get_audio_signal_np(self):
        audio_array = np.array(self.audio_memorized)/32768 #Audio NP Array NORM
        return audio_array
    
    def get_audio_signal_filt_np(self):
        audio_array = np.array(self.audio_f_memorized)/32768 #Audio NP Array NORM
        return audio_array

    def get_time_player(self): 
        return self.time_player
    #############metodos de manipulação de sinais por canal

    def set_filters_memorized(self,a_b, filter=""):
        self.filters_memorized[filter] = a_b
        print(self.filters_memorized)

    def set_signal_f(self, data):
        self.audio_f_memorized= data

    def extend_signal(self, data):
        self.audio_memorized.extend(data)

    def set_time_player(self, time): 
        self.time_player = time/self.samp_rate

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

class Player():
    def __init__(self):
        self.current_time = 0
    def rec(self): 
        pass 
    def play_frame(self, data_frame):
        
        
        pass
    def stop():
        pass

class PloterMpl(QtWidgets.QMainWindow):
    WIDTH = 2
    CHANNELS = 1
    RATE = 8000
    
    def __init__(self):
        self.current_state = "INICIO"
        #Flags
        self.call_rec_td = False
        self.call_play_td = False
        #plot props
        self.samp_rate = 8000
        
        self.canvas = Ploter(self, self.samp_rate, width=5, height=4, dpi=100)
        self.canvas2 = Ploter(self, self.samp_rate, width=5, height=4, dpi=100)
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
        self.ui.gridLayout.addWidget(self.canvas2, 0, 1, 2, 1)
        
        #test sliders

        
        val_pb = self.sliderPB.value()
        self.lab_PB.setText(str(val_pb))
        val_pa = self.sliderPB.value()
        self.lab_PA.setText(str(val_pa))
        val_nt = self.sliderPB.value()
        self.lab_NT.setText(str(val_nt))
        #timer for update plt
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.interval)
        self.timer.timeout.connect(self.update_system)
        self.timer.start()
        
        self.p = pyaudio.PyAudio()
        
        self.sliderPB.sliderReleased.connect(lambda: self.set_flag("filter_now"))
        self.sliderPA.sliderReleased.connect(lambda: self.set_flag("filter_now"))
        self.sliderNT.sliderReleased.connect(lambda: self.set_flag("filter_now"))

        self.recButton.clicked.connect(lambda: self.set_flag ("rec_now"))
        self.playButton.clicked.connect(lambda: self.set_flag ("play_now"))
        self.stopButton.clicked.connect(lambda: self.set_flag("wait_now"))
        self.pauseButton.clicked.connect(lambda: self.set_flag("pause_now"))
        self.clearButton.clicked.connect(lambda: self.set_flag("clear_now"))
        self.freqtime_toggButon.clicked.connect(lambda: self.switch_freq_time())
        
        self.recButton.setEnabled(True)
        self.playButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.pauseButton.setEnabled(False)
        self.clearButton.setEnabled(True)
        self.groupBox_2.setChecked(False)
        
        #self.pushButton_9.clicked.connect(lambda: self.set_flag("filter_now"))
        self.worker = None
        flags_status["setup_end"] = True
        print('Setup ok')
   
    def set_flag(self, flag):
        flags_status[flag] = True

    def state_machine_run(self, current_state):
        for i in range (len(struct_state_machine[current_state])): # Percorre lista de flags de current_state 
            if flags_status[struct_state_machine[current_state][i][0]]: # Procura por flags ativas em current_state
                flags_status[struct_state_machine[current_state][i][0]] = False # desativa a respectiva flag
                current_state = struct_state_machine[current_state][i][1] # current_state = "next_state(flag = true)"
                break
        return current_state # Retorna o Próximo Estado (next_state ou current_state)
        
    def start_worker(self):
        print("instanciando worker...")
        self.worker = Worker(self.start_rec_play, )
        self.threadpool.start(self.worker)	
        self.timer.setInterval(self.interval) 
        self.call_rec_td = False # for don't call REC thread again 

    def start_worker2(self):
        print("instanciando worker 2...")
        self.worker = Worker(self.start_play, )
        self.threadpool.start(self.worker)	
        self.timer.setInterval(self.interval) 
        self.call_play_td = False # for don't call PLAY thread again 

    def start_rec_play(self):
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

            while self.stream.is_active():
                    QtWidgets.QApplication.processEvents()
                    self.gravar()
                    if self.current_state != "GRAVANDO":
                        print("stoping streaming")
                        break

            print("exiting streaming audio")
            self.stream.stop_stream()
            self.stream.close()
            self.end_rec()
            #self.p.terminate()	
        except Exception as e:
            print("ERROR: pyaudio ",e)
            pass

    def end_rec(self):
        try:
            self.canvas.plot_signal(self.registrador.get_audio_signal_np())
        except Exception as e: 
            print(e)
   
    def update_system(self):
        
        try:
            #print('ACTIVE THREADS:',self.threadpool.activeThreadCount(),end=" \r")
            while True:
                
                QtWidgets.QApplication.processEvents()
                self.current_state = self.state_machine_run(self.current_state)
                
                if self.current_state == "GRAVANDO": 
                    if self.call_rec_td: 
                        self.recButton.setEnabled(False)
                        self.playButton.setEnabled(False)
                        self.stopButton.setEnabled(True)
                        self.pauseButton.setEnabled(False)
                        self.clearButton.setEnabled(False)
                        self.groupBox_2.setChecked(False)
                        self.start_worker()
                
                elif self.current_state == "FILTRANDO":
                   # self.print_log("filtrando")
                    self.filtrar()
                elif self.current_state == "SALVANDO": 
                    #self.print_log("salvando")
                    self.salvar
                elif self.current_state == "CARREGANDO":
                   # self.print_log("carregando")
                    pass
                elif self.current_state == "CLEARING":
                   # self.print_log("clearing all")
                    self.clear_all()
                elif self.current_state == "REPRODUZINDO":
                   if self.call_play_td: 
                        self.recButton.setEnabled(False)
                        self.playButton.setEnabled(False)
                        self.stopButton.setEnabled(True)
                        self.pauseButton.setEnabled(True)
                        self.clearButton.setEnabled(False)
                        self.groupBox_2.setChecked(False)
                        self.start_worker2()

                elif self.current_state == "ESPERANDO":
                   # self.print_log("esperando...")
                    if self.call_rec_td == False: 
                        self.recButton.setEnabled(True)
                        self.playButton.setEnabled(True)
                        self.stopButton.setEnabled(False)
                        self.pauseButton.setEnabled(False)
                        self.clearButton.setEnabled(True)
                        self.groupBox_2.setChecked(True)
                        self.call_rec_td = True 
                    if self.call_play_td == False: 
                        self.recButton.setEnabled(True)
                        self.playButton.setEnabled(True)
                        self.stopButton.setEnabled(False)
                        self.pauseButton.setEnabled(False)
                        self.clearButton.setEnabled(True)
                        self.groupBox_2.setChecked(True)
                        self.call_play_td = True    
                else:                   
                    pass
        except Exception as e:
            print("Error: state swich",e)
        

    def get_list(self):  
        data = self.q.get_nowait() 
        return data

    def put_list(self, thing):
        self.q.put(thing)

    def clear_all(self): 
        self.canvas.clear_plot
        self.registrador.clear_memory
        sys.exit(app.exec_())

    def gravar(self): 
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
            print("Error 'gravando':",e)

    def filtrar(self):
        try:
            fs = 8000 ##
            fc_PB = self.sliderPB.value()
            fc_PA = self.sliderPA.value()
            fc_NT = self.sliderNT.value()
            self.lab_PB.setText(str(fc_PB))
            self.lab_PA.setText(str(fc_PA))
            self.lab_NT.setText(str(fc_NT))
            print("filtrando o sinal...")
            sinal = self.registrador.get_audio_signal_np()
            
            sinal_f = self.filter_serie(sinal, fs, fc_PB, fc_PA, fc_NT)
            
            self.registrador.set_signal_f(sinal_f) 

            self.canvas2.plot_signal(sinal_f)####
            self.set_flag("wait_now")
        except Exception as e:
            print("Error: state swich",e)
            exit()
             
############################################## Filter functions ##################################    
    def filter_serie(self, data, fs, fc_PB, fc_PA, fc_NT):
        q_NT = 10.0
        print("aplicando filtro serie")
        dataf1 = self.notch_filter_bandcut(data, fc_NT, q_NT, fs)
        dataf2 = self.elip_bandpass_filter_zi(dataf1, fs, fc_PB, type = 'low')
        #filtro PA desativado
        dataf3 = self.elip_bandpass_filter_zi(dataf2, fs, fc_PB, type = 'high')
        return dataf2
    
    def notch_filter_bandcut(self, data, f0, Q, fs):
        
        b, a = self.notch_filter(f0, Q, fs)
        self.registrador.set_filters_memorized((b,a), filter = "NT")
        print("1")
        zi = lfilter_zi(b, a)
        print(zi)
        y,zo = lfilter(b, a, data, zi=zi*data[0])
        return y

    def notch_filter(self, f0, Q, fs):
        b, a = signal.iirnotch(f0, Q, fs)
        print(b, "/", a)
        print("filtro Notch  implementado")
        return b, a

    def elip_bandpass_filter_zi(self, data, fs, fc, type):
        
        b, a = self.elip_filter(fs, fc, type)
        print(b, "/", a)
        if type == "low":
            self.registrador.set_filters_memorized((b,a), filter = "PB")
        else: 
            self.registrador.set_filters_memorized((b,a), filter = "PA")
        zi = lfilter_zi(b, a)
        y,zo = lfilter(b, a, data, zi=zi*data[0])
        return y

    def elip_filter(self, fs, fc, type):
        ordem = 5 
        rp = 1 
        rs = 10
        b, a = signal.ellip(ordem, rp, rs, fc, type, analog=False, fs = fs)
        print("filtro eliptico implementado")
        return b,a
#############################################################
    
    
    def start_play(self): 

        stream = self.p.open(format = pyaudio.paFloat32,
                channels = 1,
                frames_per_buffer = 1000,
                rate = 8000,
                output = True)
        
        data = self.registrador.get_audio_signal_np()
        i = 0
        self.registrador.set_time_player(i)
        while stream.is_active():
            if self.current_state != "REPRODUZINDO" or len(data) < 1000:
                self.registrador.set_time_player(0)
                self.canvas.plot_mark_time(self.registrador.get_time_player())
                break
            stream.write(data.astype(np.float32).tostring(), 1000)
            data = data[1000:]
            i = i + 1000
            self.registrador.set_time_player(i)
            self.canvas.plot_mark_time(self.registrador.get_time_player())
        
        stream.stop_stream()
        stream.close()
        self.set_flag("wait_now")
    
    def pausar(): 
        pass

    def salvar(self): 
        self.registrador.save_wav()
        pass
        
    def switch_freq_time(self):
        try:
            y = self.registrador.get_audio_signal_np()
            yf = self.registrador.get_audio_signal_filt_np()
            if self.ui.freqtime_toggButon.isChecked(): 
                self.canvas.freq_dom = True
                self.canvas.plot_signal(y)
                self.canvas2.freq_dom = True
                self.canvas2.plot_signal(yf)
            else:
                self.canvas.freq_dom = False
                self.canvas.plot_signal(y)
                self.canvas2.freq_dom = False
                self.canvas2.plot_signal(yf)
        except: 
            print("sem todos os dados necessários")
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


