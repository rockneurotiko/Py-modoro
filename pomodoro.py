from time import sleep
import threading
import play_sound
from KThread import *






# class Temporizador(threading.Thread):

# 	def __init__ (self, time2):
#  		self.time = time2
#  		threading.Thread.__init__(self)
#  		global contador
#  		self.contador = 0

#  	def run (self):
#  		while self.contador < self.time:
#  			sleep(1)
#  			self.contador += 1
 	
#  	def segundos(self):
#  		return self.time - self.contador




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
		play_sound.play("~/pomodoro/alarma.mp3")
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
		

	def iniciar_pom(self, time = 0):
		if time == 0:
			time = self.tiempo

		self.estado = "START"

		self.arrancar(time)

		#global f
		#f = Temporizador(time)
		#f.start()    #Parte de otro metodo

		global e
		e = KThread(target = self.contador)
		e.start()

		self.interr = 0

	
	def tiempo_pom(self, mins = 0):
		if mins == 0:
			self.tiempo = 25*60
		else:
			self.tiempo = mins*60

	def interrupt_pom(self):
		if self.estado=="STOP":
			print "No puedes parar algo no empezado"
		
		else:
			self.interr += 1
			t.cancel()
			e.kill()
			print "Pomodoro parado quedando: " + str(self.segundos())

	
	def saber_tiempo(self):
		print(self.segundos())


	
 	def cuenta_atras(self):

 		while self.estado == "START":
 			self.saber_tiempo()
 			sleep(1)
 			
 		self.promt_inicial()

 	
 	def quit(self):
 		self.interrupt_pom()
		

	

 	#INTERFAZ

 	def promt_iniciar(self):
 		time = input("Introduzca tiempo.(si introduces 0 es por defecto [25])  >: ")
 		self.tiempo_pom(time)
 		self.iniciar_pom()
 		self.promt_inicial()


 	def promt_inicial(self):


 		hacer = raw_input("Introduzca (h para ayuda): ")

 		if hacer == "h":
 			print """ 
 			Usted puede introducir:
 			iniciar -> Pasa a un promt donde introduces el tiempo para el pomodoro.
 			parar -> para el pomodoro iniciado
 			interrupciones -> muestra las interrupciones hechas al pomodoro.
 			h -> muestra esta ayuda
 			q -> salir
 			tiempo -> muestra el tiempo que llevas.


 			"""
 			self.promt_inicial()
		
 		elif hacer == "parar":
 			self.interrupt_pom()
 			self.promt_inicial()

 		elif hacer == "iniciar":
 			self.promt_iniciar()

 		elif hacer == "q":
 			self.quit()
 			e.kill()

 		elif hacer == "tiempo":
 			if self.estado == "START":
 				self.saber_tiempo()
 				self.promt_inicial()
 			else:
 				print "No has iniciado ningun pomodoro. \n"
 				self.promt_inicial()
 		
 		elif hacer == "cuenta":
 			self.cuenta_atras()

 		else:
 			print """
 			No ha introducido ningun comando valido.
 			Introduzca "h" para ver los comandos habilitados.
 			"""
 			self.promt_inicial()





pom = pomodoro()
pom.promt_inicial()
	
