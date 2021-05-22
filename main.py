# -*- coding: utf-8 -*-

# Plot live audio Eletronic Stethoscope 

#Conrado/Tarsis

#bibliotecas essenciais 
from PyQt5.QtGui import QDragEnterEvent, QDragMoveEvent
from matplotlib.backend_bases import Event
import matplotlib.pyplot as plt
import sys 
import matplotlib
from numpy.lib.financial import rate 
matplotlib.use('Qt5Agg')


import matplotlib.ticker as ticker
import numpy as np
from PyQt5.QtCore import QEvent, pyqtSlot
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
import queue 

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


from scipy.fft import fft, fftfreq
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
class Ploter (FigureCanvas):
    
    def __init__(self,obj, samp_rate, parent=None, width=5, height=4, dpi=100 ):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(Ploter, self).__init__(fig)
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

    def plot_signal(self, signal): 
        if self.freq_dom == True:
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
    
    def plot_real_time (self,data): 
        self.process_plot(data)
        self.axes.set_facecolor((1,1,1))
        self.axes.set_ylim( ymin=-1, ymax=1)
        self.axes.plot(self.x, self.y, color = (0,0,0), lw=0.5)
        self.draw()

    def plot_mark_time(self, current_time):
        print("time: ", current_time)
        n = self.axes.axvline((current_time), color='green') 
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
        self.audio_to_play = []
        self.samp_rate = samp_rate
        self.time_player = 0
    
    def set_signal_to_play(self, s):
        if s == 2:
            self.audio_to_play = self.get_signal_filt_not_norm()
        else: 
            self.audio_to_play = self.audio_memorized

    def get_signal_to_play(self):
        try:
            s = np.array(self.audio_to_play)
            return s
        except: 
            print("nenhum sinal selecionado para enviar ao player")
            pass
   
    def get_signal_not_norm(self):
        audio_array = np.array(self.audio_memorized)
        return audio_array

    def get_signal_norm(self):
        audio_array = np.array(self.audio_memorized)/32768 #Audio NP Array NORM
        return audio_array
    
    def get_signal_filt_not_norm(self):
        audio_array = np.array(self.audio_f_memorized)*32768 #Audio NP Array NORM
        audio_array = audio_array.astype(np.int16)
        return audio_array

    def get_signal_filt_norm(self):
        audio_array = np.array(self.audio_f_memorized) #Audio NP Array NORM
        return audio_array

    def get_time_player(self): 
        return self.time_player

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

import pyaudio
class Player():
    WIDTH = 2
    CHANNELS = 1
    RATE = 8000
    def __init__(self):
        self.current_time = 0
        self.FRAME_SIZE = 1000
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.end_player = False
    
    def open_stream(self):
        self.stream = self.p.open(
                    format=self.p.get_format_from_width(self.WIDTH),
                    channels=self.CHANNELS,
                    rate=self.RATE,
                    input=True,
                    output=True,
                    frames_per_buffer = 1000,
                    )
    
    def rec(self):
        data_frame = self.stream.read(1000)
        time = self.play_frame(data_frame)
        return (np.frombuffer(data_frame, dtype=np.int16), time)
        
    def play_frame(self, data_frame):
        self.stream.write(data_frame, 1000)
        self.current_time = self.current_time + 1000
        return self.current_time
        
    def stop(self):
        print("stop")
        self.current_time = 0
        self.stream.stop_stream()
        self.stream.close()

from scipy.signal import butter, lfilter, lfilter_zi, freqs    
class Filter(): 
    def __init__(self, samp_rate):
        self.elip_filter = None
        self.fs = samp_rate 
        self.PA_pars = {"btype":"high", "order":5, "ftype":"ellip", "fc":100, "rp":1, "rs": 10 } 
        self.PB_pars = {"btype":"low", "order":5, "ftype":"ellip", "fc":100, "rp":1, "rs": 10 } 
        self.PNT_pars = {"fc":60, "q":10.0} 
    
    def set_PB_fc(self,fc):
        self.PB_pars["fc"] = fc
    
    def set_PA_fc(self,fc):
        self.PA_pars["fc"] = fc

    def set_PNT_fc(self, fc):
        self.PNT_pars["fc"] = fc

    def set_PA_pars(self, ftype, order, rp, rs):  
        self.PA_pars["order"] = order
        self.PA_pars["ftype"] = ftype
        self.PA_pars["rp"] = rp
        self.PA_pars["rs"] = rs

    def set_PB_pars(self, ftype, order, rp, rs):  
        self.PA_pars["order"] = order
        self.PB_pars["ftype"] = ftype
        self.PB_pars["rp"] = rp
        self.PB_pars["rs"] = rs

    def set_pars_NT(self, fc, q): 
        self.PNT_pars["fc"] = fc
        self.PNT_pars["q"] = q

    def get_PA_pars(self):
        pars = [self.PA_pars["btype"],self.PA_pars["order"], self.PA_pars["ftype"], self.PA_pars["fc"],
            self.PA_pars["rp"], self.PA_pars["rs"]]
        return pars

    def get_PB_pars(self):
        pars = [self.PB_pars["btype"],self.PB_pars["order"], self.PB_pars["ftype"], self.PB_pars["fc"],
            self.PB_pars["rp"], self.PB_pars["rs"]]
        return pars

    def filter_serie(self, data): 
        print("aplicando filtro serie")
        dataf1 = self.notch_filter_bandcut(data, self.PNT_pars["fc"], self.PNT_pars["q"], self.fs)
        dataf2 = self.irr_bandpass_filter_zi(dataf1, self.get_PB_pars())
        #filtro PA desativado
        dataf3 = self.irr_bandpass_filter_zi(dataf2, self.get_PA_pars())
        return dataf3
    
    def notch_filter_bandcut(self, data, f0, Q, fs):
        b, a = self.notch_filter(f0, Q, fs)
        zi = lfilter_zi(b, a)
        print(zi)
        y,zo = lfilter(b, a, data, zi=zi*data[0])
        return y

    def notch_filter(self, f0, Q, fs):
        b, a = signal.iirnotch(f0, Q, fs)
        print(b, "/", a)
        print("filtro Notch  implementado")
        return b, a

    def irr_bandpass_filter_zi(self, data, irr_pars):
    
        b, a = self.irr_filter_discrete(*irr_pars)
        print(b, "/", a)
        zi = lfilter_zi(b, a)
        y,zo = lfilter(b, a, data, zi=zi*data[0])
        return y

    def irr_filter_discrete(self, btype, order, ftype, fc, rp, rs):
        b, a = signal.iirfilter(order, fc,rp = rp, rs=rs,
                        btype=btype, analog=False, ftype=ftype, fs=self.fs)
        w, h = signal.freqz(b, a, fs= self.fs, worN= 40000)
        return b, a
    
class MainApp(QtWidgets.QMainWindow):

    def __init__(self):
        #Estado 0
        self.current_state = "INICIO"

        #plot props
        self.samp_rate = 8000
        self.interval = 30

        #init manipulador de threads
        self.threadpool = QtCore.QThreadPool()	
        self.threadpool.setMaxThreadCount(1)

        #Flags de controle das Threads
        self.call_rec_td = False
        self.call_play_td = False

        #init GUI
        QtWidgets.QMainWindow.__init__(self)
        self.resize(1024, 600)
        self.ui = uic.loadUi('main.ui', self)

        #Plotters 
        self.canvas1 = Ploter(self, self.samp_rate, width=5, height=4, dpi=100)
        self.canvas2 = Ploter(self, self.samp_rate, width=5, height=4, dpi=100)
        self.track_channel = [self.canvas1, self.canvas2]
        self.ui.gridLayout_3.addWidget(self.canvas1, 0, 1, 2, 1)
        self.ui.gridLayout.addWidget(self.canvas2, 0, 1, 2, 1)

        #buffer
        self.q = queue.Queue()
        
        #Armazenamento
        self.registrador = Registrador(self.samp_rate)

        #Filtragem 
        self.filtros = Filter(self.samp_rate)

        #Audio I/O
        self.player = Player()
        
        #init sliders
        val_pb = self.sliderPB.value()
        self.lab_PB.setText(str(val_pb))
        val_pa = self.sliderPB.value()
        self.lab_PA.setText(str(val_pa))
        val_nt = self.sliderPB.value()
        self.lab_NT.setText(str(val_nt))

        #timer for update SVM
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.interval)
        self.timer.timeout.connect(self.update_system)
        self.timer.start()
        
        #Eventos de seleção do canal com o clique do mouse
        self.canvas1.mouseReleaseEvent =  lambda x:self.select_ch1()
        self.canvas2.mouseReleaseEvent =   lambda x:self.select_ch2()

        #conexão dos sinais de entrada
        self.sliderPB.sliderReleased.connect(lambda: self.set_flag("filter_now"))
        self.sliderPA.sliderReleased.connect(lambda: self.set_flag("filter_now"))
        self.sliderNT.sliderReleased.connect(lambda: self.set_flag("filter_now"))
        # Botões
        self.recButton.clicked.connect(lambda: self.set_flag ("rec_now"))
        self.playButton.clicked.connect(lambda: self.set_flag ("play_now"))
        self.stopButton.clicked.connect(lambda: self.set_flag("wait_now"))
        self.pauseButton.clicked.connect(lambda: self.set_flag("pause_now"))
        self.clearButton.clicked.connect(lambda: self.set_flag("clear_now"))
        self.freqtime_toggButon.clicked.connect(lambda: self.switch_freq_time())
        
        # Desativa/Ativa botões 
        self.recButton.setEnabled(True)
        self.playButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.pauseButton.setEnabled(False)
        self.clearButton.setEnabled(True)
        self.groupBox_2.setChecked(False)
        
        #setup inicial: canal 1 selecionado
        self.worker = None
        self.ch_selected = 1
        self.set_flag("setup_end") 
        print('Setup ok')
    
    def select_ch1(self): 
        self.ch_selected = 1
        print("canal 1 selecionado")   
    
    def select_ch2(self): 
        self.ch_selected = 2
        print("canal 2 selecionado")   

    #Altera a lista de flgs de entrada da maquina de estado       
    def set_flag(self, flag):
        if  flags_status[flag]:
            pass
        else:
            flags_status[flag] = True

    def state_machine_run(self, current_state):
        for i in range (len(struct_state_machine[current_state])): # Percorre lista de flags de current_state 
            if flags_status[struct_state_machine[current_state][i][0]]: # Procura por flags ativas em current_state
                flags_status[struct_state_machine[current_state][i][0]] = False # desativa a respectiva flag
                current_state = struct_state_machine[current_state][i][1] # current_state = "next_state(flag = true)"
                break
        return current_state # Retorna o Próximo Estado (next_state ou current_state)
    
    #Inicializa Thread para gravação
    def start_worker(self):
        print("instanciando worker...")
        self.worker = Worker(self.start_rec_play, )
        self.threadpool.start(self.worker)	
        self.timer.setInterval(self.interval) 
        self.call_rec_td = False 
    
    #Inicializa Thread para reprodução
    def start_worker2(self):
        print("instanciando worker 2...")
        self.worker = Worker(self.start_play, )
        self.threadpool.start(self.worker)	
        self.timer.setInterval(self.interval) 
        self.call_play_td = False 

    #Loop principal onde e alterado o estado atual do sistema
    def update_system(self):

           try:
               print('ACTIVE THREADS:',self.threadpool.activeThreadCount(),end=" \r")
               while True:
                   QtWidgets.QApplication.processEvents()
                   
                   #estado[i - 1] = estado [i]
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

                   # Na maior parte do tempo de execução o estado do sistema estará aqui
                   elif self.current_state == "ESPERANDO":
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

    def start_rec_play(self):
        QtWidgets.QApplication.processEvents()
        end_time = 10*8000
        current_time = 0
        self.player.open_stream()
        while current_time < end_time :
            print(current_time)
            data, current_time = self.player.rec()
            self.q.put((np.frombuffer(data, dtype=np.int16)))
            self.plot_rec()
            if self.current_state != "GRAVANDO":
                    print("stoping streaming")
                    break
            QtWidgets.QApplication.processEvents()
                    
        print("exiting streaming audio")
        self.player.stop()
        self.registrador.set_signal_to_play(1)
        self.end_rec()
    
    def start_play(self): 
         QtWidgets.QApplication.processEvents()
         self.select_track_channel(self.ch_selected)
         data = self.registrador.get_signal_to_play()
         end_time = len(data) ##
         current_time = 0
         
         self.player.open_stream()
         print("end time:", end_time)
         while(self.current_state == "REPRODUZINDO"):
             QtWidgets.QApplication.processEvents()
             current_time = self.player.play_frame(data)
             data = data[1000:]
             current_time = current_time + 1000
             self.track_channel[self.ch_selected - 1].plot_mark_time(current_time/8000)
             if current_time == end_time:
                 self.set_flag("wait_now")
                 break
         self.player.stop()
         print(self.current_state)
        
    def clear_all(self): 
        self.canvas1.clear_plot
        self.registrador.clear_memory
        sys.exit(app.exec_())

    def filtrar(self):
        try:
            fc_PB = self.sliderPB.value()
            fc_PA = self.sliderPA.value()
            fc_NT = self.sliderNT.value()
            self.lab_PB.setText(str(fc_PB))
            self.lab_PA.setText(str(fc_PA))
            self.lab_NT.setText(str(fc_NT))
            sinal = self.registrador.get_signal_norm()
            
            self.filtros.set_PB_fc(fc=fc_PB)
            self.filtros.set_PA_fc(fc=fc_PA)
            self.filtros.set_PNT_fc(fc_NT)

            sinal_f = self.filtros.filter_serie(sinal)
            
            self.registrador.set_signal_f(sinal_f) 

            self.canvas2.plot_signal(sinal_f)####
            self.set_flag("wait_now")
        except Exception as e:
            print("Erro ao filtrar:",e)
    
    def plot_rec(self): 
       try:
           while True:
               QtWidgets.QApplication.processEvents()
               try: 
                   data_list = self.q.get_nowait()
                   data = np.array(data_list)/32768
               except queue.Empty:
           
                   break
               self.canvas1.plot_real_time(data)
               self.registrador.extend_signal(data_list)
           
       except Exception as e:
           print("Error 'gravando':",e)
    
    def end_rec(self):
        try:
            self.canvas1.plot_signal(self.registrador.get_signal_norm())
        except Exception as e: 
            print(e)
    
    #não usadas por enquanto
    def end_play(self, i):
        self.recButton.setEnabled(True)
        self.playButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.pauseButton.setEnabled(False)
        self.clearButton.setEnabled(True)
        self.groupBox_2.setChecked(True)
        self.registrador.set_time_player(i)

    def salvar(self): 
        self.registrador.save_wav()

    #alterna o domínio dos graficos dos canais (tempo/frequencia) 
    def switch_freq_time(self):
        try:
            y = self.registrador.get_signal_norm()
            yf = self.registrador.get_signal_filt_norm()
            if self.ui.freqtime_toggButon.isChecked(): 
                self.canvas1.freq_dom = True
                self.canvas1.plot_signal(y)
                self.canvas2.freq_dom = True
                self.canvas2.plot_signal(yf)
            else:
                self.canvas1.freq_dom = False
                self.canvas1.plot_signal(y)
                self.canvas2.freq_dom = False
                self.canvas2.plot_signal(yf)
        except: 
            print("sem todos os dados necessários")
            pass

    #seleciona o canal ativo para reproduzir 
    def select_track_channel(self, ch): 
        self.registrador.set_signal_to_play(ch)

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
MainWindow  = MainApp()
MainWindow.show()
sys.exit(app.exec_())


