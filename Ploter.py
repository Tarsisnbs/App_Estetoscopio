# Class Ploter V: 1.03
#Társis Natan B. Silva _ 13-01-2021
# - updated plotting frame shift logic
# - scaled x-axis with number of input signal samples
# - shift of the plot window changing the limits of the X axis (xmax and xmin)

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import queue

from numpy.ma.core import concatenate
class Ploter():

	def __init__(self):
		
		#self.sample_rate = 8000
		#self.t_sample = 1/self.sample_rate #criar método método 
		#self.total_samples  = int(self.window*self.sample_rate/(1000))
		self.q = queue.Queue()
		self.samp_rate = 8000
		self.samp_step = 1/self.samp_rate
		self.window = 40000
		self.window_t = self.window * self.samp_step
		self.time_interval = 10

		self.x = np.arange(0 , self.window_t , self.samp_step, dtype = float)
		self.y = np.zeros(self.window, dtype = float)

		self.x_vals = []
		self.y_vals = []
		self.fig,self.ax = plt.subplots(figsize=(8,4))
		self.ax.set_title("plot")
		self.ax.set_facecolor((1,1,1))
		self.ax.set_ylim(-1.1, 1.1)
		self.ax.set_xlim(0, self.window)
		self.ax.grid()

		self.fig,self.bx = plt.subplots(figsize=(8,4))
		self.bx.set_title("plot")
		self.bx.set_facecolor((1,1,1))
		self.bx.set_ylim(-1.1, 1.1)
		self.bx.set_xlim(0, self.window_t)
		self.bx.grid()

		self.ani  = FuncAnimation(self.fig,self.update_plt_list, interval=self.time_interval,blit=True, frames = 500)

		#self.ani  = FuncAnimation(self.fig,self.update_plt_list_time, interval=self.time_interval,blit=True, frames = 500)
		print("objeto Ploter instanciado : area de plot criada")

	def generate_data_p_sample(data):
		
		pass
	def generate_data_p_time(self, x_data):
		T = 1/(self.window)
		time = np.asarray(x_data)
		return print(time*0.000125, len(time))

		# y <- frame_data 
		# x <- tempo_frame 
		#del y[:size(frame_data)]
		#del x[:size(tempo_frame)]
		pass
	
		
	def update_plt_list(self, i):
		
		data = np.array(self.get_list())/32768
		shift = len(data)

		self.y = np.roll(self.y,-shift)
		self.y[-shift:] = data
		xmin, xmax = self.ax.get_xlim()
		self.x = np.roll(self.x,-shift)
		self.x[-shift:] = np.arange(xmax,xmax + shift)
		print(self.x)
		
		
		self.ax.set_xlim(xmin + shift ,xmax + shift)
		self.ax.figure.canvas.draw()	

		self.lines = self.ax.plot(self.x, self.y, color = (0,0,0), lw=0.5)
		return(self.lines)
	


	def update_plt_list_time(self, i):
		#get samples an frame size
		data = np.array(self.get_list())/32768
		shift = len(data)
		
		#refresh y axis
		self.y = np.roll(self.y,-shift)
		self.y[-shift:] = data
		
		#refresh x axis
		xmin, xmax = self.bx.get_xlim()
		self.x = np.roll(self.x,-shift)
		self.x[-shift:] = np.arange(xmax,xmax + shift*self.samp_step, self.samp_step)
		
		#refresh window plot limits
		self.bx.set_xlim(xmin + shift*self.samp_step ,xmax + shift*self.samp_step)
		self.bx.figure.canvas.draw()	
		
		#put all in to lines object
		self.lines = self.bx.plot(self.x, self.y, color = (0,0,0), lw=0.5)
		
		return(self.lines)

	def run_loop(self):
		
		plt.show()

	def get_list(self): 
		data = self.q.get() 
	
		return data

	def put_list(self, thing):
		self.q.put(thing)
