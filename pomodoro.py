#!/usr/bin/python

from time import sleep
import threading

from libs.KThread import *

import pygame

"""I don't use this library any more, I use pygame.mixer.music, who let's set the volume"""
#from libs.play_sound import *

"""If you want to play the music with winsound, uncomment this imports and check play_sound() method"""
#import sys #, osm inspect
#if sys.platform[:3] == "win":
#	import winsound





"""Old class and method to make the thread"""
#################################################
#												#
# class Temporizador(threading.Thread):			#
#												#
# 	def __init__ (self, time2):					#
#  		self.time = time2						#
#  		threading.Thread.__init__(self)			#
#  		global contador							#
#  		self.contador = 0						#
#												#
#  	def run (self):								#
#  		while self.contador < self.time:		#
#  			sleep(1)							#
#  			self.contador += 1					#
#												#
#  	def seconds(self):							#
#  		return self.time - self.contador		#
#												#
#################################################
#												#
#												#
#global f 										# 	
#f = Temporizador(time)							#
#f.start()    #Parte de otro metod0				#
# 												#
# Esta metodo ha sido eliminado para dar paso 	#
# al proporcionado por KThread, que permite 	#
#	matar el thread. 							#
#												#
#################################################


__author__ = "Rock Neurotiko"
__copyright__= "Copyright 2012, Rock Neurotiko"
__credits__ = ["Rock Neurotiko",]
__license__ = "GNU/GPL v3"
__version__ = "0.3"
__maintainer__ = "Rock Neurotiko"
__email__ = "miguelglafuente@gmail.com"

class Pomodoro(object):
	"""
	Main backend class. Contains all the back end methods to runs.
	"""

	def __init__(self):
		"""
		Constructor.
		Initialize control variables.
		"""

		self.ESTADO = "STOP" #STATES: STOP, START, PAUSE, END
		self.TIEMPO = 25*60
		self.INTERR = 0
		self.estado = self.ESTADO
		self.tiempo = self.TIEMPO
		self.interr = self.INTERR
		self.on = False
		self.segundos_trans = 0

		self.volume = 1.0
		self.filemp3 = "alarma.mp3"


	def crear_pom(self, time = 0):
		"""
		Method to create a pomodoro.
		If it's already started or paused, it will be interrupted and started again.
		Just makes the adjust to run, but the pomodoro doesn't start

		@param time The time selected to creates the pomodoro.
		@type time Integer
		"""

		if (self.estado=="START" or self.estado=="PAUSE"):
			self.interrupt_pom()
			self.segundos_trans = 0 #reboot the seconds

		self.estado="STOP"
		if time==0:
			time = 25*60
		self.tiempo = time


	def iniciar_pom(self):
		"""
		Method to start a pomodoro.
		If it's already started it will be interrupted and started again.
		"""
		#print("llama a iniciar")  #debug control

		if(self.estado =="START"):
			self.interrupt_pom()
			self.segundos_trans = 0 #reboot the seconds

		self.estado = "START"

		self.arrancar(self.tiempo)

		global e
		e = KThread(target = self.contador)
		e.start()

		self.interr = 0

	def resume_pom(self):
		"""
		Method to resume a pomodoro.
		"""
		#print("llama a resumir") #debug control

		self.estado = "START"

		self.arrancar(self.tiempo)

		global e
		e = KThread(target = self.contador)
		e.start()

		self.interr = 0

	def interrupt_pom(self):
		"""
		Method to STOP and pomodoro.
		Just works if it's already started.
		"""
		#print "Llama a parar"  #debug control

		if (self.estado=="STOP" or self.estado=="PAUSE"):
			print "No puedes parar algo no empezado"
		else:
			self.interr += 1
			print "Pomodoro parado quedando: " + self.get_tiempo()
			t.cancel() #kill the timer
			self.on = False #turn off the state of t
			e.kill() #kill the counter
			self.estado = "PAUSE" #put the state into PAUSE

	def arrancar(self, time):
		"""
		Method to control the finish of the pomodoro.
		Creates a timer threading.

		@param time The time selected of the pomodoro.
		@type time Integer
		"""
		global t
		if self.on == True:
			t.cancel()
			self.on == False
		t = threading.Timer(time, self.terminar)
		t.start()
		self.on = True

	def terminar(self):
		"""
		Method who is executed when the pomodoro is finished.
		This method is called from the Timer threading of arrancar method
		"""
		self.estado = "END"
		e.kill()
		self.on = False
		self.segundos_trans = 0
		print "Fin del pomodoro, puedes descansar.\n"
		self.play_sound()




	def contador(self):
		"""
		Method who controls the time.
		This method is called from the KThread instance.
		"""
		sleep(1)
		while (self.segundos_trans < self.tiempo and self.estado == "START"):
			self.segundos_trans += 1
			sleep(1)

	def get_interruptions(self):
		return self.interr


	def get_tiempo(self):
		"""
		Getter.
		@return The time parsed in a String.
		"""
		tiempo_local = self.seconds()

		if tiempo_local <= 60:
			return str(self.seconds()) + " " + "segundos."  

		elif tiempo_local <= 3600:
			segundos_local = tiempo_local - (tiempo_local/60)*60
			return str(tiempo_local/60)  + " " + "minutos, y " + str(segundos_local) + " " + "segundos."

		else:

			minutos_local = (tiempo_local - (tiempo_local - ((tiempo_local/3600)*3600)/60))/60
			segundos_local = tiempo_local - minutos_local - minutos_local*3600


			return (str(tiempo_local/3600) + " " + "hora/s, y " + str(minutos_local) + " " + 
			"minuto/s, y " + str(segundos_local) + " " + "segundo/s.")


	def seconds(self):
		"""
		Turns the time into seconds
		"""
		return self.tiempo - self.segundos_trans

	def play_sound(self):
		"""
		Play a song.
		Method called at the end of the pomodoro.
		"""

		#so_system = sys.platform

		pygame.mixer.init()
		#pygame.mixer.music.load('alarma.mp3')
		try:
			pygame.mixer.music.load(self.filemp3)
		except:
			pygame.mixer.music.load("alarma.mp3")
		pygame.mixer.music.set_volume(self.volume)
		pygame.mixer.music.play()


		# if(so_system[:3] == "win"):
		# 	winsound.PlaySound('alarma.wav', winsound.SND_FILENAME)
			

		# elif(so_system[:3] == "lin"):
		# 	play_sound.play(os.path.dirname(inspect.getfile(inspect.currentframe())) + "/alarma.wav")



	"""
	Getters and setters.
	"""

	def set_Filemp3(self, path):
		"""
		Set the filemp3 control variable of the Pomodoro instance.

		@param path The path of the song. (Not empty)
		@type path String
		"""
		if path!="":
			self.filemp3 = path
