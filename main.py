# -*- coding: utf-8 -*-

# Plot live audio Eletronic Stethoscope 

#Conrado/Tarsis

#bibliotecas essenciais 
<<<<<<< HEAD
from PyQt5.QtGui import QDragEnterEvent, QDragMoveEvent
from matplotlib.backend_bases import Event
=======
from PyQt5.QtGui import QMouseEvent
from PyQt5.uic.properties import QtGui
from matplotlib.backend_bases import Event, MouseEvent
from matplotlib.backends.backend_qt5 import FigureCanvasQT
>>>>>>> newVers
import matplotlib.pyplot as plt
import sys 
import matplotlib
from numpy.lib.financial import rate 
matplotlib.use('Qt5Agg')
<<<<<<< HEAD


import matplotlib.ticker as ticker
=======
>>>>>>> newVers
import numpy as np
from PyQt5.QtCore import QEvent, pyqtSlot
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
import queue 
<<<<<<< HEAD

=======
from PyQt5 import  QtMultimedia   
>>>>>>> newVers
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

<<<<<<< HEAD

from scipy.fft import fft, fftfreq
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
=======
from scipy.fft import fft, fftfreq
>>>>>>> newVers
from matplotlib.figure import Figure
from matplotlib.widgets import SpanSelector
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar 
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
class BasePlotter(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100 ):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(BasePlotter, self).__init__(fig)
        toolbar = NavigationToolbar(self, self)
        box_toolbar = QtWidgets.QVBoxLayout()
        box_toolbar.addWidget(toolbar, 0)
        box_toolbar.addWidget(toolbar, 0)
        fig.tight_layout()


class Plotter (FigureCanvas):
    
    def __init__(self,event_select, obj=None, samp_rate=8000, parent=None, width=5, height=4, dpi=100 ):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
<<<<<<< HEAD
        super(Ploter, self).__init__(fig)
=======
        super(Plotter, self).__init__(fig)
>>>>>>> newVers
        self.samp_rate = samp_rate
        self.samp_step = 1/self.samp_rate
        self.window_t = 2
        self.window = self.window_t/self.samp_step
        self.cursor = self.axes.axvline((0), color='green')
        self.freq_dom = False

        self.freq_dom = False

        self.x, self.y = self.init_plot_axis(self.window_t, self.samp_rate)
        self.axes.set_xlim(0, self.window_t)
        fig.tight_layout()
        
        #self.span = SpanSelector(self.axes, self.onselect, 'horizontal', useblit=True,
        #rectprops=dict(alpha=0.5, facecolor='red'),span_stays = True)
        
        
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
<<<<<<< HEAD
        self.draw()

    def plot_mark_time(self, current_time):
        print("time: ", current_time)
        n = self.axes.axvline((current_time), color='green') 
        self.draw()
        plt.Axes.remove(n)

=======
        self.draw()

    def plot_mark_time(self, current_time):
        n = self.axes.axvline((current_time), color='green') 
        self.draw()
        plt.Axes.remove(n)
    
    def plot_cursor(self, current_time):
        plt.Axes.remove(self.cursor)
        self.cursor = self.axes.axvline((current_time), color='green') 
        self.draw()
        
>>>>>>> newVers
    def fft_transf(self, y, N, T):
        yf = fft(y)
        xf = fftfreq(N, T)[:N//2]
        return yf, xf
<<<<<<< HEAD

=======
        
>>>>>>> newVers
    def plot_freq(self,data):
        self.clear_plot()
        N = len(data)
        yf_freq, xf_freq = self.fft_transf(data, N, self.samp_step )
<<<<<<< HEAD
        self.axes.plot(xf_freq, 2.0/N * np.abs(yf_freq[0:N//2]))
        self.axes.grid()
        self.draw()

    def clear_plot(self): #Não testado
        self.axes.clear()
        self.draw
        pass
               
=======
        #self.axes.set_ylim( ymin=0, ymax=0.01)
        self.axes.plot(xf_freq, 1.0/N * np.abs(yf_freq[0:N//2]), color = (0,0,0))
        self.axes.grid()
        self.draw()
    
    def plot_wh(self,w_h):
        self.axes.semilogx(w_h[0] / (2*np.pi), 20 * np.log10(np.maximum(abs(w_h[1]), 1e-5)))
        self.draw()
    
    def clear_plot(self): 
        self.axes.clear()
        self.draw()
       
from tkinter import *
from tkinter import Scrollbar, filedialog
from tkinter.filedialog import asksaveasfilename, dialogstates      
>>>>>>> newVers
import soundfile as sf
class Registrador(): 
    def __init__(self, samp_rate):
        self.filters_memorized = {"PB":[], "PA":[], "NT":[]}
        self.audio_memorized = []
        self.audio_f_memorized = []
        self.audio_to_play = []
<<<<<<< HEAD
        self.samp_rate = samp_rate
        self.time_player = 0
=======
        self.audio_frag_selected = []
        self.samp_rate = samp_rate
        self.time_player_fs = (0,0)
>>>>>>> newVers
    
    def set_signal_to_play(self, s):
        if s == 2:
            self.audio_to_play = self.get_signal_filt_not_norm()
        else: 
            self.audio_to_play = self.audio_memorized
<<<<<<< HEAD

    def get_signal_to_play(self):
        try:
            s = np.array(self.audio_to_play)
=======
            
        self.set_time_player(0,len(self.audio_to_play))
        print(self.time_player_fs)
            
    def get_signal_to_play(self, norm = False):
        try:
            if norm:
                s = np.array(self.audio_to_play)/32768
            else:
                s = np.array(self.audio_to_play)
>>>>>>> newVers
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
<<<<<<< HEAD
        return audio_array

    def get_signal_filt_norm(self):
        audio_array = np.array(self.audio_f_memorized) #Audio NP Array NORM
        return audio_array

    def get_time_player(self): 
        return self.time_player

=======
        return audio_array

    def get_signal_filt_norm(self):
        audio_array = np.array(self.audio_f_memorized) #Audio NP Array NORM
        return audio_array

    def get_time_player(self): 
        return self.time_player_fs
    

    def make_signal_frag(self, xmin, xmax):
        #signal_selected = self.get_signal_to_play()
        #self.audio_frag_selected = signal_selected[int(xmin*8000): int(xmax*8000)]
        #self.audio_to_play = self.audio_frag_selected
        print("sinal cortado em: ", xmin, xmax)
        self.set_time_player(xmin, xmax)
        #return self.get_signal_to_play()/32768
        
    
>>>>>>> newVers
    def set_filters_memorized(self,a_b, filter=""):
        self.filters_memorized[filter] = a_b
        print(self.filters_memorized)

    def set_signal_f(self, data):
        self.audio_f_memorized= data

    def extend_signal(self, data):
        self.audio_memorized.extend(data)

<<<<<<< HEAD
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
=======
    def set_time_player(self, tini, tend): 
        self.time_player_fs = tini, tend

    def save_wav(self): 
        try:
            root = Tk()
            root.withdraw()
            self.filename = asksaveasfilename(initialdir="/", title="Save as",
                filetypes=(("audio file", "*.wav"), ("all files", "*.*")),
                defaultextension=".wav")
            #save stream as .wav file
            sf.write(self.filename, self.audio_memorized, self.samp_rate, 'PCM_24') 
            root.destroy()
        except:
            print("nenhum sinal de audio armazenado no sistema")
            
    def load_wav(self): 
        root = Tk()
        root.withdraw()
        _audio_file = filedialog.askopenfilename(initialdir="desktop/", title="Escolha um Arquivo", filetypes=(("wav files", "*.wav"),("all files", "*.*")))
        #self.audio_memorized = sf.read('audio_file.wav', self.audio_memorized, self.samp_rate, 'PCM_24')       
        filename = _audio_file
        self.data, self.fs = sf.read(filename, dtype=np.int16) 
        #sd.play(self.data, self.fs) 
        #self.duration = len(self.data)/self.fs
        #self.time = np.arange (0, self.duration , 1/self.fs)
    
        self.audio_memorized = np.array(self.data)     
        root.destroy()    
>>>>>>> newVers
    
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
        self.PA_pars = {"btype":"high", "order":5, "ftype":"ellip", "fc":100, "rp":1, "rs": 10, "tf":()} 
        self.PB_pars = {"btype":"low", "order":5, "ftype":"ellip", "fc":100, "rp":1, "rs": 10, "tf":() } 
        self.PNT_pars = {"fc":60, "q":10.0, "tf":()} 

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

    def get_w_h(self):
        tfPB = self.PB_pars["tf"]
        tfPA = self.PA_pars["tf"]
        tfPNT = self.PNT_pars["tf"]
        whPB = signal.freqz(tfPB[0], tfPB[1], fs= self.fs, worN= 40000)
        whPA = signal.freqz(tfPA[0], tfPA[1], fs= self.fs, worN= 40000)
        whPNT = signal.freqz(tfPNT[0], tfPNT[1], fs= self.fs, worN= 40000)
        return whPB, whPA, whPNT
    
    def filter_serie(self, data): 
        print("aplicando filtro serie")
        dataf1 = self.notch_filter_bandcut(data, self.PNT_pars["fc"], self.PNT_pars["q"], self.fs)
        dataf2 = self.irr_bandpass_filter_zi(dataf1, self.get_PB_pars())
        #filtro PA desativado
        dataf3 = self.irr_bandpass_filter_zi(dataf2, self.get_PA_pars())
        return dataf3
    
    def notch_filter_bandcut(self, data, f0, Q, fs):
        b, a = self.notch_filter(f0, Q, fs)
        self.PNT_pars["tf"] = (b,a)
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
        if irr_pars[0] == "low":
            self.PB_pars["tf"] = b,a
        elif irr_pars[0] == "high":
            self.PA_pars["tf"] = b,a
        else: 
            pass
        print(b, "/", a)
        zi = lfilter_zi(b, a)
        y,zo = lfilter(b, a, data, zi=zi*data[0])
        return y

<<<<<<< HEAD
class MainApp(QtWidgets.QMainWindow):
    WIDTH = 2
    CHANNELS = 1
    RATE = 8000
=======
    def irr_filter_discrete(self, btype, order, ftype, fc, rp, rs):
        b, a = signal.iirfilter(order, fc,rp = rp, rs=rs,
                        btype=btype, analog=False, ftype=ftype, fs=self.fs)
        
        w, h = signal.freqz(b, a, fs= self.fs, worN= 40000)
        return b, a
>>>>>>> newVers
    
class MainApp(QtWidgets.QMainWindow):

    def __init__(self):
<<<<<<< HEAD

=======
        self.estate_key={"GRAVANDO":self.gravando,"FILTRANDO":self.filtrando,"SALVANDO":self.salvando,
                            "CARREGANDO":self.carregando, "CLEARING":self.clearing, "REPRODUZINDO":self.reproduzindo,
                            "ESPERANDO":self.esperando}
      
    #Estado 0
>>>>>>> newVers
        self.current_state = "INICIO"

    #init GUI
        QtWidgets.QMainWindow.__init__(self)
        self.resize(1024, 600)
        self.ui = uic.loadUi('main.ui', self)

    #plot props
        self.samp_rate = 8000
<<<<<<< HEAD
        
        self.canvas1 = Ploter(self, self.samp_rate, width=5, height=4, dpi=100)
        self.canvas2 = Ploter(self, self.samp_rate, width=5, height=4, dpi=100)
        self.track_channel = [self.canvas1, self.canvas2]

        self.interval = 30
        #define new Qthread for pyaudio
=======
        self.interval = 30

    #init manipulador de threads
>>>>>>> newVers
        self.threadpool = QtCore.QThreadPool()	
        self.threadpool.setMaxThreadCount(1)

    #Flags de controle das Threads
        self.call_rec_td = False
        self.call_play_td = False

    #Plotters 
    
        self.canvas1 = Plotter(self, self.samp_rate, width=5, height=4, dpi=100)
        self.canvas2 = Plotter(self, self.samp_rate, width=5, height=4, dpi=100)
        
        self.span_ch1 = SpanSelector(self.canvas1.axes, self.onselect, 'horizontal', useblit=True,
                        rectprops=dict(alpha=0.5, facecolor='red'),span_stays = True)
        self.span_ch2 = SpanSelector(self.canvas2.axes, self.onselect, 'horizontal', useblit=True,
                        rectprops=dict(alpha=0.5, facecolor='red'),span_stays = True)
        self.track_channel = [self.canvas1, self.canvas2]
        self.ui.gridLayout_3.addWidget(self.canvas1, 0, 1, 2, 1)
        self.ui.gridLayout.addWidget(self.canvas2, 0, 1, 2, 1)
    
        
    #buffer
        self.q = queue.Queue()
        
    #Armazenamento
        self.registrador = Registrador(self.samp_rate)

    #Filtragem 
        self.filtros = Filter(self.samp_rate)

<<<<<<< HEAD
        self.ui.gridLayout_3.addWidget(self.canvas1, 0, 1, 2, 1)
        self.ui.gridLayout.addWidget(self.canvas2, 0, 1, 2, 1)
        
        #init sliders
=======
    #Audio I/O
        self.player = Player()
        
    #init sliders
>>>>>>> newVers
        val_pb = self.sliderPB.value()
        self.lab_PB.setText(str(val_pb))
        val_pa = self.sliderPB.value()
        self.lab_PA.setText(str(val_pa))
        val_nt = self.sliderPB.value()
        self.lab_NT.setText(str(val_nt))
<<<<<<< HEAD
        #timer for update SVM
=======

    #timer for update SVM
>>>>>>> newVers
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.interval)
        self.timer.timeout.connect(self.update_system)
        self.timer.start()
<<<<<<< HEAD
        
        self.player = Player()
        
        self.ch_selected = 1
        self.canvas1.mouseReleaseEvent =  lambda x:self.select_ch1()
        self.canvas2.mouseReleaseEvent =   lambda x:self.select_ch2()

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
        
        self.worker = None
=======
    
    #Eventos de seleção do canal com o clique do mouse
        #self.canvas1.mousePressEvent(None)
        self.canvas1.mousePressEvent =  lambda x:self.select_ch_n(1, self.selected_ch1)
        self.canvas2.mousePressEvent =   lambda x:self.select_ch_n(2, self.selected_ch2)
     #conexão dos sinais de entrada
        self.sliderPB.sliderReleased.connect(lambda: self.set_flag("filter_now"))
        self.sliderPA.sliderReleased.connect(lambda: self.set_flag("filter_now"))
        self.sliderNT.sliderReleased.connect(lambda: self.set_flag("filter_now"))
        
    # Botões
        self.actionOriginal_Sound.triggered.connect(lambda: self.set_flag("save_now"))
        self.actionOpen.triggered.connect(lambda: self.set_flag("open_now"))

        self.recButton.clicked.connect(lambda: self.set_flag ("rec_now"))
        self.playButton.clicked.connect(lambda: self.set_flag ("play_now"))
        self.stopButton.clicked.connect(lambda: self.set_flag("wait_now"))
        self.pauseButton.clicked.connect(lambda: self.set_flag("pause_now"))
        self.clearButton.clicked.connect(lambda: self.set_flag("clear_now"))
       
        self.exitButton.clicked.connect(lambda: self.exit())
        self.freqtime_toggButon.clicked.connect(lambda: self.switch_freq_time())
        self.refreshButton.clicked.connect(lambda: self.refresh_adv_pars())
        self.adv_pars_Buton.clicked.connect(lambda: self.hide_show_adv_menu())

    # Desativa/Ativa botões 
        self.recButton.setEnabled(True)
        self.playButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.pauseButton.setEnabled(False)
        self.clearButton.setEnabled(True)
        self.groupBox_2.setChecked(False)
        
        self.ui.adv_pars_Box.hide()
        #setup inicial: canal 1 selecionado
        self.worker = None
        self.ch_selected = 1
    #End Setup
>>>>>>> newVers
        self.set_flag("setup_end") 
        print('Setup ok')


    def refresh_adv_pars(self):
        map_dict = {"Butterworth":"butter", "Bessel":"bessel","Chebyshev I":"cheby1", "Chebyshev II":"cheby2","Elíptico":"ellip"}
        typefPA = self.ui.comboBox_tipoPA.currentText()
        typefPB = self.ui.comboBox_tipoPB.currentText()
        orderPB = self.ui.ordem_PB.value()
        orderPA = self.ui.ordem_PA.value()
        rpPB = self.ui.slider_rp_PB.value()
        rpPA = self.ui.slider_rp_PA.value()
        rsPB = self.ui.slider_rs_PB.value()
        rsPA = self.ui.slider_rs_PA.value()
        
        self.filtros.set_PA_pars(map_dict[typefPA],orderPA,rpPA,rsPA)
        self.filtros.set_PA_pars(map_dict[typefPB],orderPB,rpPB,rsPB)
    
        '''
        tf_filtros = self.filtros.get_w_h()
        self.canvas2.plot_wh(tf_filtros[0])
        self.canvas2.plot_wh(tf_filtros[1])
        self.canvas2.plot_wh(tf_filtros[2])
        '''
        
    def hide_show_adv_menu(self):
        if self.ui.adv_pars_Buton.isChecked(): 
            self.ui.adv_pars_Box.show()
        else: 
            self.ui.adv_pars_Box.hide()
     
    def select_ch_n(self, ch_n, selected_ch_n):
        self.ch_selected = ch_n
        print("canal ", ch_n, " selecionado.") 
        self.select_track_channel(self.ch_selected)
        
        
        selected_ch_n()
       
        
        
    def selected_ch1(self):
        self.ui.ch1.setStyleSheet("QGroupBox"
                                     "{"
                                     "border : 4px solid black;"
                                     "}"
                                     "QGroupBox::editable:on"
                                     "{"
                                     "border : 2px solid;"
                                     "border-color : red green blue yellow"
                                     "}")
        self.ui.ch2.setStyleSheet("QGroupBox"
                                     "{"
                                     "border : 0px solid black;"
                                     "}"
                                     "QGroupBox::editable:on"
                                     "{"
                                     "border : 0px solid;"
                                     "border-color : red green blue yellow"
                                     "}")
  
    
<<<<<<< HEAD
    def select_ch1(self): 
        self.ch_selected = 1
        print("canal 1 selecionado")   
    def select_ch2(self): 
        self.ch_selected = 2
        print("canal 2 selecionado")   
        
    
=======
    def selected_ch2(self): 
        self.ui.ch2.setStyleSheet("QGroupBox"
                                     "{"
                                     "border : 4px solid black;"
                                     "}"
                                     "QGroupBox::editable:on"
                                     "{"
                                     "border : 2px solid;"
                                     "border-color : red green blue yellow"
                                     "}")
        self.ui.ch1.setStyleSheet("QGroupBox"
                                     "{"
                                     "border : 0px solid black;"
                                     "}"
                                     "QGroupBox::editable:on"
                                     "{"
                                     "border : 0px solid;"
                                     "border-color : red green blue yellow"
                                     "}")
  

    #Altera a lista de flgs de entrada da maquina de estado       
>>>>>>> newVers
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
<<<<<<< HEAD
        
=======
    
    #Inicializa Thread para gravação
>>>>>>> newVers
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

<<<<<<< HEAD
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

    def start_rec_play(self):
        QtWidgets.QApplication.processEvents()
        end_time = 10*8000
        current_time = 0
        self.player.open_stream()
        while current_time < end_time :
=======
    #Loop principal onde e alterado o estado atual do sistema
    def update_system(self):
           try:
               print('ACTIVE THREADS:',self.threadpool.activeThreadCount(),end=" \r")
               while True:
                   QtWidgets.QApplication.processEvents()
                   #estado[i - 1] = estado [i]
                   self.current_state = self.state_machine_run(self.current_state)
                   
                   self.estate_key[self.current_state]()
           except Exception as e:
               print("Error: state swich",e)
##########################################################
    def gravando(self):
       if self.call_rec_td: 
           self.recButton.setEnabled(False)
           self.playButton.setEnabled(False)
           self.stopButton.setEnabled(True)
           self.pauseButton.setEnabled(False)
           self.clearButton.setEnabled(False)
           self.groupBox_2.setChecked(False)
           self.track_channel[self.ch_selected - 1].clear_plot()
           self.registrador.clear_memory()
           self.start_worker() 
       else:
            pass   
    
    def filtrando(self):
        self.filtrar()    
    
    def salvando(self):
       self.salvar()   
    
    def carregando(self):
       self.load_audio()   
    
    def clearing(self):
       self.clear_all()

    def reproduzindo(self):
       if self.call_play_td: 
           self.recButton.setEnabled(False)
           self.playButton.setEnabled(False)
           self.stopButton.setEnabled(True)
           self.pauseButton.setEnabled(True)
           self.clearButton.setEnabled(False)
           self.groupBox_2.setChecked(False)
           self.start_worker2()
       else: 
           pass
    
    def esperando(self):
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
##########################################################
    def start_rec_play(self):
        QtWidgets.QApplication.processEvents()
        end_time = 100000*8000
        current_time = 0
        self.player.open_stream()
        while self.current_state == "GRAVANDO":
>>>>>>> newVers
            print(current_time)
            data, current_time = self.player.rec()
            self.q.put((np.frombuffer(data, dtype=np.int16)))
            self.plot_rec()
<<<<<<< HEAD
            if self.current_state != "GRAVANDO":
                    print("stoping streaming")
=======
            if current_time > end_time :
                    print("end streaming")
                    self.set_flag('wait_now')
>>>>>>> newVers
                    break
            QtWidgets.QApplication.processEvents()
                    
        print("exiting streaming audio")
        self.player.stop()
        self.registrador.set_signal_to_play(1)
        self.end_rec()
    
    def start_play(self): 
         QtWidgets.QApplication.processEvents()
<<<<<<< HEAD
         self.select_track_channel(self.ch_selected)
         data = self.registrador.get_signal_to_play()
         end_time = len(data) ##
         current_time = 0
         
         self.player.open_stream()
        
         while(current_time < end_time):
             current_time = self.player.play_frame(data)
             data = data[1000:]
             current_time = current_time + 1000
             self.track_channel[self.ch_selected - 1].plot_mark_time(current_time/8000)
             if self.current_state != "REPRODUZINDO":
                 break
         self.player.stop()
         self.set_flag("wait_now")

    def clear_all(self): 
        self.canvas1.clear_plot
        self.registrador.clear_memory
        sys.exit(app.exec_())

    def filtrar(self):
        try:
            fs = 8000 ##
            fc_PB = self.sliderPB.value()
            fc_PA = self.sliderPA.value()
            fc_NT = self.sliderNT.value()
            self.lab_PB.setText(str(fc_PB))
            self.lab_PA.setText(str(fc_PA))
            self.lab_NT.setText(str(fc_NT))
            sinal = self.registrador.get_signal_norm()
            
            sinal_f = self.filter_serie(sinal, fs, fc_PB, fc_PA, fc_NT)
            
=======
         data = self.registrador.get_signal_to_play()
         tini,tend = self.registrador.get_time_player()
         end_time = tend ##
         current_time = tini
         data = data[tini:tend]
         self.player.open_stream()
         while(self.current_state == "REPRODUZINDO"):
             print(end_time, current_time)
             QtWidgets.QApplication.processEvents()
             l = self.player.play_frame(data)
             data = data[1000:]
             current_time = current_time + 1000
             self.track_channel[self.ch_selected - 1].plot_mark_time(current_time/8000)
             if current_time >= end_time:
                 self.set_flag("wait_now")
                 break
         self.player.stop()
         print(self.current_state)
        
    def clear_all(self): 
        self.track_channel[self.ch_selected - 1].clear_plot()
        self.registrador.clear_memory()
        self.set_flag("wait_now")
        
    def exit(self):
        sys.exit(app.exec_())
   
    def filtrar(self):
        try:
            fc_PB = self.sliderPB.value()
            fc_PA = self.sliderPA.value()
            fc_NT = self.sliderNT.value()

            sinal = self.registrador.get_signal_norm()
            
            self.filtros.set_PB_fc(fc=fc_PB)
            self.filtros.set_PA_fc(fc=fc_PA)
            self.filtros.set_PNT_fc(fc_NT)

            sinal_f = self.filtros.filter_serie(sinal)
            print("lol")
>>>>>>> newVers
            self.registrador.set_signal_f(sinal_f) 

            self.canvas2.plot_signal(sinal_f)####
            self.set_flag("wait_now")
        except Exception as e:
<<<<<<< HEAD
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

    def select_track_channel(self, ch): 
        self.registrador.set_signal_to_play(ch)
=======
            print("Erro ao filtrar:",e)
            self.set_flag("wait_now")
    
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
    
    def salvar(self): 
        self.registrador.save_wav()
        self.set_flag("wait_now")
    
    def load_audio(self):
        self.registrador.load_wav()
        self.canvas1.plot_signal(self.registrador.get_signal_norm())
        self.select_ch_n(1, self.selected_ch1)
        self.set_flag("wait_now")
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

    def open_new_window(self, singnal_frag):
        print("abrindo janela...")
        
        self.dialog = WindowDIalog(singnal_frag)
        #self.dialogs.append(dialog)
        self.dialog.show()
    def close_last_window(self):
            pass
    def onselect(self, xmin, xmax):
        print(xmin*8000, xmax*8000)
        self.track_channel[self.ch_selected-1].plot_cursor(xmin)
        
        self.registrador.make_signal_frag(int(8000*xmin), int(8000*xmax))
        singnal_frag = self.registrador.get_signal_to_play(norm=True)
        self.open_new_window(singnal_frag[int(8000*xmin):int(8000*xmax)])
        '''
        line2.set_data(thisx, thisy)
        ax2.set_xlim(thisx[0], thisx[-1])
        ax2.set_ylim(thisy.min(), thisy.max())
        fig.canvas.draw_idle()
        '''

    

    
class WindowDIalog(QtWidgets.QMainWindow):
    def __init__(self, singnal_frag, parent=None):
        super(WindowDIalog, self).__init__(parent)
        self.ui_ = uic.loadUi('form.ui', self)
        self.canvas_base = BasePlotter(self, width=50, height=40, dpi=100)
        self.ui_.verticalLayout.addWidget(self.canvas_base, 1)
        self.canvas_base.axes.plot(singnal_frag)
        self.canvas_base.draw
        
class AdvancedOptions():
    def __init__(self):
        self.PA_pars = {"btype":"high", "order":5, "ftype":"ellip", "fc":100, "rp":1, "rs": 10 }
>>>>>>> newVers

class Worker(QtCore.QRunnable):
	def __init__(self, function, *args, **kwargs):
		super(Worker, self).__init__()
		self.function = function
		self.args = args
		self.kwargs = kwargs

	@pyqtSlot()
	def run(self):

		self.function(*self.args, **self.kwargs)
<<<<<<< HEAD

app = QtWidgets.QApplication(sys.argv)
MainWindow  = MainApp()
MainWindow.show()
sys.exit(app.exec_())
=======
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow  = MainApp()
    MainWindow.showMaximized()
    sys.exit(app.exec_())
>>>>>>> newVers


