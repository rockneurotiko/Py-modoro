#!/usr/bin/python

from Tkinter import *
import tkMessageBox, tkFileDialog
from KThread import *
from time import sleep
import os



__author__ = "Rock Neurotiko"
__copyright__= "Copyright 2012, Rock Neurotiko"
__credits__ = ["Rock Neurotiko", ]
__license__ = "GNU/GPL v3"
__version__ = "0.2"
__maintainer__ = "Rock Neurotiko"
__email__ = "miguelglafuente@gmail.com"

class App:

        def __init__(self, master, pom):
                self.errors = Errors()

                self.pom = pom
                self.time_in_var = IntVar()
                self.time_in_var.set(25)
                self.time = StringVar()
                self.time.set("There is no Pomodoro started.")

                self.frame = Frame(master)
                self.frame.pack()

                label_time_input = Label(self.frame, text="Input the time.")
                label_time_input.grid(row=2, column=0)

                self.label_time = Label(self.frame, textvariable = self.time, cursor = "pirate")
                self.label_time.grid(row=1, column=1)


                scale_time = Scale(self.frame, variable = self.time_in_var, from_=1, to=60, resolution = 1.0)
                scale_time.grid(column=3)


                entry_time = Spinbox(self.frame, textvariable= self.time_in_var, width=15, from_=1, to=60)
                entry_time.grid(row=2, column=1)

                button_start = Button(self.frame, text="START", fg="green", command=self.start)
                button_start.grid(row=3, column=0)

                self.button_resume = Button(self.frame, text="RESUME", fg="blue", command=self.resume, state=DISABLED)
                self.button_resume.grid(row=3, column=1)

                self.button_stop = Button(self.frame, text= "STOP", fg="red", command=self.stop, state=DISABLED)
                self.button_stop.grid(row=3, column=2)




        def start(self):
                try:
                        self.pom.crear_pom(self.time_in_var.get() * 60)
                        self.pom.iniciar_pom()
                        global e
                        e = KThread(target = self.print_time)
                        e.start()

                        self.button_stop.config(state=ACTIVE)
                        self.button_resume.config(state=DISABLED)
                except ValueError:
                        self.errors.ValueError()

        def resume(self):
                try:
                        self.pom.resume_pom()
                        global e
                        e = KThread(target = self.print_time)
                        e.start()

                        self.button_resume.config(state=DISABLED)
                except ValueError:
                        self.errors.ValueError()


                
        def stop(self):
                self.pom.interrupt_pom()
                e.kill()
                self.button_resume.config(state=ACTIVE)

        def end(self):
                self.time.set("Congrats, you had already finish the pomodoro, take a break.")
                self.button_stop.config(state=DISABLED)


        def print_time(self):
                while(self.pom.segundos_trans < self.pom.tiempo and self.pom.estado == "START"):
                        self.time.set(self.pom.get_tiempo())
                        sleep(0.25)
                self.end()





class Config:

        def __init__(self, master):
                self.master = master



                #Volume Config
                self.volume = DoubleVar()
                self.volume.set(1.0)

                volume_label = Label(master, text="Volume: ")
                volume_label.grid(row=1, column=0)

                volume_scale = Scale(master, variable = self.volume, from_=0.0, to=1.0, resolution = 0.1, orient=HORIZONTAL)
                volume_scale.grid(row=1, column=1)


                #Buttons to accept/deny the changes.
                accept_button = Button(master, text="Accept", command = self.accept)
                accept_button.grid(row=2, column=0)

                cancel_button = Button(master, text="Cancel", command = self.cancel)
                cancel_button.grid(row=2, column=1)

        def accept(self):
                pom.volume = self.volume.get()
                self.master.destroy()

        def cancel(self):
                self.master.destroy()





class TimePresets:

        def __init__(self, master):
                self.master = master
                self.var = IntVar()

                normal_pom_time = Radiobutton(master, text="Normal Pomodoro (25')", variable=self.var, value=25)
                normal_pom_time.grid(row=0, column=1)

                short_break = Radiobutton(master, text="Short Break (5')", variable=self.var, value=5)
                short_break.grid(row=1, column=1)

                long_break = Radiobutton(master, text="Long Break (15')", variable=self.var, value=15)
                long_break.grid(row=2, column=1)

                #Buttons to accept/deny the changes.
                accept_button = Button(master, text="Accept", command = self.accept)
                accept_button.grid(row=3, column=0)

                cancel_button = Button(master, text="Cancel", command = self.cancel)
                cancel_button.grid(row=3, column=2)

        def accept(self):
                app.time_in_var.set(self.var.get())
                self.master.destroy()

        def cancel(self):
                self.master.destroy()             







class Help:
        def __init__(self, master):
                help_text_var = StringVar()
                help_text = Text(master, wrap=WORD, exportselection=0)
                
#                 help_text_var.set(""" Fellow pirate.
# Do you wanna know what a Pomodoro is?
# I'm gonna resume it, if you want a large explain search on the Internet""")
                var = """ Fellow pirate.
Do you wanna know what a Pomodoro is?
I'm gonna resume it, if you want a large explain search on the Internet"""

                help_text.insert(INSERT, var)
                help_text.config(state=DISABLED)

                help_text.pack()




class SearchFile:

        def __init__(self):
                

                # define options for opening or saving a file
                self.file_opt = options = {}
                options['defaultextension'] = '' # couldn't figure out how this works
                options['filetypes'] = [('Music mp3', '.mp3')] # ('all files', '.*'), 
                options['initialdir'] = 'C:\\'
                options['initialfile'] = 'myfile.txt'
                options['parent'] = root
                options['title'] = 'This is a title'


                self.dir_opt = options = {}
                options['initialdir'] = 'C:\\'
                options['mustexist'] = False
                options['parent'] = root
                options['title'] = 'This is a title'

        def askOpenFile(self):
                return tkFileDialog.askopenfile(mode='r', **self.file_opt)



class Errors:
        def __init__(self):
                pass

        def ValueError(self):
                tkMessageBox.showinfo("Check-out your input. " + " " * 20 + "Py-Modoro", "You must introduce an entire number (given in minutes)")

        def ImportError(self):
                tkMessageBox.showerror("Error", "You must install the module pygame, check this link: http://www.pygame.org/download.shtml")
                root.destroy()





#Function to ask if you really wanna close.
def callback():
        if tkMessageBox.askokcancel("Quit" + " " * 20 + "Py-Modoro", "Are you sure you wanna close Py-Modoro?"):
                root.destroy()



#This function creates the configuration window (File>Configuration)
def configuration(*evento):
        configwindow = Toplevel(root)
        Config(configwindow)


def timePresets():
        presetsWindow = Toplevel(root)
        TimePresets(presetsWindow)


#This function creates another window (Help>What's pomodoro?)
def whatsPomodoro():
        helpwindow = Toplevel(root) #Define the new window
        Help(helpwindow) #Call to the class Help and pass the new window created.

def openFile():
        
        searchClass = SearchFile()
        filemp3 = searchClass.askOpenFile()



#Defines the menu
def menu(root):
        menubar = Menu(root)

        configmenu = Menu(menubar, tearoff=0)
        configmenu.add_command(label="Open file", command=openFile)
        configmenu.add_command(label="Configuration", accelerator = "CTRL+X", command=configuration)
        configmenu.add_command(label="Time Presets", command=timePresets)
        menubar.add_cascade(label="File", menu=configmenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="What's Pomodoro?", command=whatsPomodoro)
        helpmenu.add_command(label="About...", command=whatsPomodoro)
        menubar.add_cascade(label="Help", menu=helpmenu)

        root.bind("<Control-KeyPress-x>", configuration)

        return menubar


root = Tk()

main_errors = Errors()
try:
        from pomodoro import pomodoro #this import is right here to catch the possible exception.
except ImportError:
        main_errors.ImportError()
        os._exit(0)

pom = pomodoro()

root.title("Py-Modoro v.0.2  - By Rock Neurotiko")


app = App(root, pom)

menubar = menu(root)



root.protocol("WM_DELETE_WINDOW", callback)
root.config(menu=menubar)
root.geometry("500x500")

root.mainloop()