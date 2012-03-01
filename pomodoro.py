from time import sleep
import threading
import play_sound
from KThread import *




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
#  	def segundos(self):							#
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
__credits__ = ["Rock Neurotiko", "Who mades the module KThread", 
				"Who mades the module play_sound"]
__license__ = "GNU/GPL v3"
__version__ = "0.1.2"
__maintainer__ = "Rock Neurotiko"
__email__ = "miguelglafuente@gmail.com"

class pomodoro:

	def __init__(self):
		self.ESTADO = "STOP"
		self.TIEMPO = 25*60
		self.INTERR = 0
		self.estado = self.ESTADO
		self.tiempo = self.TIEMPO
		self.interr = self.INTERR
		self.on = False
		self.count_t = 0

	def contador(self):
		global segundos_trans
		segundos_trans = 0
		while segundos_trans < self.tiempo:
			segundos_trans += 1
			sleep(1)

	def segundos(self):
		return self.tiempo - segundos_trans

	def interruptions(self):
		return self.interr


	def terminar(self):
		self.estado = "END"
		self.on = False
		play_sound.play("/home/rock/Programacion/pomodoro/alarma.mp3")
		print "Fin del pomodoro, puedes descansar.\n"
		self.promt_inicial()


	def arrancar(self, time):
		global t
		if self.on == True:
			t.cancel()
			self.on == False
			self.count_t -= 1
		t = threading.Timer(time, self.terminar)
		t.start()
		self.count_t += 1
		self.on = True


	def crear_pom(self, time = 25*60):

		self.estado="STOP"
		self.tiempo = time
		

	def tiempo_pom(self, mins = 0):
		if mins == 0:
			self.tiempo = 25*60
		else:
			self.tiempo = mins*60


	def iniciar_pom(self):
		
		time = self.tiempo

		self.estado = "START"

		self.arrancar(time)

		global e
		e = KThread(target = self.contador)
		e.start()

		self.interr = 0

	

	def interrupt_pom(self):
		if self.estado=="STOP":
			print "No puedes parar algo no empezado"
		
		else:
			self.interr += 1
			t.cancel()
			e.kill()
			print "Pomodoro parado quedando: " + self.a_minutos()
			self.estado = "STOP"


	def a_minutos(self):
		tiempo_local = self.segundos()

		if tiempo_local <= 60:
			return self.segundos() + " " + "segundos."

		elif tiempo_local <= 3600:
			segundos_local = tiempo_local - (tiempo_local/60)*60
			return str(tiempo_local/60)  + " " + "minutos, y " + str(segundos_local) + " " + "segundos."

		else:

			minutos_local = (tiempo_local - (tiempo_local - ((tiempo_local/3600)*3600)/60))/60
			segundos_local = tiempo_local - minutos_local - minutos_local*3600


			return (str(tiempo_local/3600) + " " + "hora/s, y " + str(minutos_local) + " " + 
			"minuto/s, y " + str(segundos_local) + " " + "segundo/s.")

	def saber_tiempo(self):
		print "Quedan: " + self.a_minutos()



	
 	def cuenta_atras(self):

 		while self.estado == "START":
 			self.saber_tiempo()
 			sleep(1)
 			
 		self.promt_inicial()

 	
 	def quit(self):
 		if self.estado == "START":
 			self.interrupt_pom()
 		print "Espero que haya aprovechado el tiempo."
 		raw_input()
	

 	#INTERFAZ

 	def promt_iniciar(self):
 		time = input("Introduzca tiempo en minutos.(si introduces 0 es por defecto [25])  >: ")
 		self.tiempo_pom(time)
 		self.iniciar_pom()
 		self.promt_inicial()


 	def promt_inicial(self):


 		hacer = raw_input("Comando (h para ayuda): ")

 		if (hacer == "--help" or hacer == "h"):
 			print """ 
 			Usted puede introducir:
 			c -> muestra una cuenta atras del tiempo que queda(irreversible) [comando largo --cuenta]
 			h -> muestra esta ayuda (comando largo --help)
 			i -> Pasa a un promt donde introduces el tiempo para el pomodoro (comando largo --iniciar)
 			--interrupciones -> muestra las interrupciones hechas al pomodoro.
 			p -> para el pomodoro iniciado (comando largo --parar)
 			q -> salir (comando largo --quit)
 			t -> muestra el tiempo que queda de pomodoro (comando largo --tiempo)
 			


 			"""
 			self.promt_inicial()

 		elif (hacer == "--cuenta" or hacer == "c"):
 			self.cuenta_atras()

 		elif (hacer == "--iniciar" or hacer == "i"):
 			self.promt_iniciar()

		
 		elif (hacer == "--parar" or hacer == "p"):
 			self.interrupt_pom()
 			self.promt_inicial()


 		elif (hacer == "--quit" or hacer == "q"):
 			if self.estado == "START":
 				e.kill() 			
 			self.quit()

 		elif (hacer == "--tiempo" or hacer == "t"):
 			if self.estado == "START":
 				self.saber_tiempo()
 				self.promt_inicial()
 			else:
 				print "No has iniciado ningun pomodoro. \n"
 				self.promt_inicial()
 		


 		else:
 			print """
 			No ha introducido ningun comando valido.
 			Introduzca "h" para ver los comandos habilitados.
 			"""
 			self.promt_inicial()





pom = pomodoro()
pom.promt_inicial()
	