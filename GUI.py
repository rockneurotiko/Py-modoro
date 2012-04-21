#!/usr/bin/python

#GUI libraries
from Tkinter import *
import tkMessageBox, tkFileDialog

#Library to manipulate config archives
from ConfigParser import *

#Thread lib, this one let kill the thread
from libs.KThread import *

#sleep method
from time import sleep

#Necesary to make the path identifications and close the program if there is any error.
import os, inspect

#Some apps and methods to the program
from menuApps.InOut import SearchFile, loadConfig, save, saveAreYouSure



__author__ = "Rock Neurotiko" #: Author name
__copyright__= "Copyright 2012, Rock Neurotiko" #: Copyright of the code
__credits__ = ["Rock Neurotiko", ] #: The credits
__license__ = "GNU/GPL v3 (http://www.gnu.org/licenses/gpl-3.0.html)" #: The license of the code
__version__ = "0.3" #: The version of the app
__email__ = "miguelglafuente@gmail.com" #: The email to contact


class App(object):
        """
        Main window class. Creates the main app.
        """

        def __init__(self, master, pom):
                """
                Constructor of App class.
                @param master The master window.
                @type master Tk or Toplevel

                @param pom The Pomodoro instance.
                @type pom Pomodoro
                """
                self.errors = Errors()

                loadConfig(pom, APPPATH, CONFIG)

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


                start_image = PhotoImage(file=APPPATH + '/images/image.gif', master = self.frame)

                button_start = Button(self.frame, image = start_image, text="START", fg="green", command=self.start)
                button_start.img = start_image  #Store a reference to the image as an attribute of the widget
                button_start.grid(row=3, column=0)

                self.button_resume = Button(self.frame, text="RESUME", fg="blue", command=self.resume, state=DISABLED)
                self.button_resume.grid(row=3, column=1)

                self.button_stop = Button(self.frame, text= "STOP", fg="red", command=self.stop, state=DISABLED)
                self.button_stop.grid(row=3, column=2)




        def start(self):
                """
                Execute when "Start" button is pressed.
                Starts the count down.
                Always start a new count down.

                @except ValueError
                """
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
                """
                Continue the count down.
                Execute when "Resume" button is pressed.
                The count down must be stopped.

                @except ValueError
                """
                try:
                        self.pom.resume_pom()
                        global e
                        e = KThread(target = self.print_time)
                        e.start()

                        self.button_resume.config(state=DISABLED)
                except ValueError:
                        self.errors.ValueError()


                
        def stop(self):
                """
                Stops the count down.
                Execute when "Stop" button is pressed.
                """
                self.pom.interrupt_pom()
                e.kill()
                self.button_resume.config(state=ACTIVE)

        def end(self):
                """
                Finish the pomodoro (automatic).
                It runs when the count down is 0.
                """
                self.time.set("Congrats, you had already finish the pomodoro, take a break.")
                self.button_stop.config(state=DISABLED)


        def print_time(self):
                """
                Actualize the variable who controls the time in the window.
                This function just runs with a thread.
                """
                while(self.pom.segundos_trans < self.pom.tiempo and self.pom.estado == "START"):
                        self.time.set(self.pom.get_tiempo())
                        sleep(0.25)
                self.end()





class Config(object):
        """Class to open the configuration window, and save in the pomfig.cfg file"""

        def __init__(self, master):
                """
                Initialize the config window.
                @param master The window master to construct the configuration.
                @type master Tk or Toplevel.
                """

                self.master = master

                self.master.resizable(False, False)



                #Volume Config
                self.volume = DoubleVar()
                self.volume.set(pom.volume)

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
                """
                Execute when the "Accept" button is pressed.
                Ask if you want to save the changes, if the answer is yes, save it in pomfig.cfg
                """
                pom.volume = self.volume.get()
                if(saveAreYouSure()):
                        save(pom, APPPATH, CONFIG)
                self.master.destroy()

        def cancel(self):
                """
                Destroy the config window withouth changes
                """
                self.master.destroy()





class TimePresets(object):
        """
        Class to gestionate the TimePresets window.
        """

        def __init__(self, master):
                """
                Constructor of TimePresets.
                @param master The master window.
                @type master Tk or Toplevel
                """
                self.master = master
                self.master.resizable(False, False)

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
                """
                Function to "Accept" button.
                Set the time in function of the option selected.
                """
                app.time_in_var.set(self.var.get())
                self.master.destroy()

        def cancel(self):
                """
                Function to "Cancel" button.
                Destroy the window and do nothing.
                """
                self.master.destroy()             







class Help(object):
        """
        Class to gestionate the help windows.
        """
        def __init__(self, master):
                """
                Initialize the window (master).
                @param master The master window.
                @type master Tk or Toplevel
                """
                self.master = master
                self.master.resizable(False, False)
                

        def whats(self):
                """
                Creates a text box (text about what is it?) in the window passed as parameter on the constructor if Help.
                """
                whats_text = Text(self.master, wrap=WORD, exportselection=0)
                
                var = """ Fellow pirate.
        Do you wanna know what a Pomodoro is?
        I'm gonna resume it, if you want a large explain search on the Internet."""

                whats_text.insert(INSERT, var)
                whats_text.config(state=DISABLED)
                self.master.geometry("600x300")

                whats_text.pack()

        def about(self):
                """
                Creates a text box (text about the program) in the window passed as parameter on the constructor of Help.
                """

                help_text = Text(self.master, wrap=WORD, exportselection=0)

                var = """ 
        Hello Pirate!

        This is the version """ + __version__ + """ of the Py-Modoro app.

        Author: """ + __author__ + """.
        Contact: """ + __email__ + """
        License: """ + __license__ + """. 

        """ + __copyright__ + """

        Cheers!
        """

                help_text.insert(INSERT, var)
                help_text.config(state=DISABLED)
                self.master.geometry("600x300")

                help_text.pack()


class Errors(object): #Class Errors
        """
        Class to gestionate the errors.
        """
        def __init__(self):
                """
                Empty, do nothing.
                """
                pass #Do nothing at create the instance of the class

        def ValueError(self):
                """
                Creates an error box.
                """
                tkMessageBox.showinfo("Check-out your input. " + " " * 20 + "Py-Modoro", "You must introduce an entire number (given in minutes)") #Already in use, but this creates a window with the error

        def ImportError(self):
                """
                Creates an error box because the pygame module is not installed.
                Destroy the app.
                """
                tkMessageBox.showerror("Error", "You must install the module pygame, check this link: http://www.pygame.org/download.shtml") #Window with the import error
                root.destroy() #Destroy the main app



#This function open the Search window (File>Select Music)
def openFile(*evento):
        """
        Create a new window (SearchFile).
        Calls the set_Filemp3 setter method of pom (Pomodoro instance), calls the askOpenFile method to select the mp3 file, and the atribute of set_Filemp3 is the path of the mp3 file selected.
        """
        searchClass = SearchFile(root) #Define the variable as SearchFile class (In packet InOut)
        pom.set_Filemp3(searchClass.askOpenFile()) #Use the method asOpenFile, who open a window to find a file, and save the path in the filemp3 variable of pom instance
        #print pom.filemp3  #debug print


#This function creates the configuration window (File>Configuration)
def configuration(*evento):
        """
        Create a new window (Toplevel) and makes an instance of Config class with the new window as atribute.
        """
        configwindow = Toplevel(root) #Define the new window
        Config(configwindow) #Call to the Config class


#This function open the Time Presets (File>Time Presets)
def timePresets(*evento):
        """
        Create a new window (Toplevel) and makes an instance of TimePresets class with the new window as atribute.
        """
        presetsWindow = Toplevel(root) #Define the new window
        TimePresets(presetsWindow) #Call to the TimePresets class


#This function creates another window (Help>What's pomodoro?)
def whatsPomodoro(*evento):
        """
        Create a new window (Toplevel) and makes an instance of Help class with the new window as atribute, and calls the whats method.
        """
        helpwindow = Toplevel(root) #Define the new window
        Help(helpwindow).whats() #Call to the whats method of the Help class, and the frame is helpwindow

#This function creates another window (Help>About...)
def aboutProgram(*evento):
        """
        Create a new window (Toplevel) and makes an instance of Help class with the new window as atribute, and calls the about method.
        """
        aboutwindow = Toplevel(root) #Define the new window
        Help(aboutwindow).about() #Call to the about method of the Help class, and the frame is helpwindow


#Defines the menu
def menu(root):
        """
        Creates the main menu.
        @return The menu created
        """
        menubar = Menu(root) #Start the Menu

        #Configuration menu
        configmenu = Menu(menubar, tearoff=0)
        configmenu.add_command(label="Select Music", accelerator = "CTRL+M", command=openFile)
        configmenu.add_command(label="Configuration", accelerator = "CTRL+X", command=configuration)
        configmenu.add_command(label="Time Presets", accelerator = "CTRL+T", command=timePresets)
        configmenu.add_separator()
        configmenu.add_command(label="Exit", accelerator = "CTRL+Q", command=callback)
        menubar.add_cascade(label="File", menu=configmenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="What's Pomodoro?", accelerator = "CTRL+W", command=whatsPomodoro)
        helpmenu.add_command(label="About...", accelerator = "CTRL+A", command=aboutProgram)
        menubar.add_cascade(label="Help", menu=helpmenu)

        #Defines the binds (accelerators)
        root.bind("<Control-KeyPress-m>", openFile)
        root.bind("<Control-KeyPress-x>", configuration)
        root.bind("<Control-KeyPress-t>", timePresets)
        root.bind("<Control-KeyPress-q>", callback)

        root.bind("<Control-KeyPress-w>", whatsPomodoro)
        root.bind("<Control-KeyPress-a>", aboutProgram)

        return menubar


#Function to ask if you really wanna close.
def callback(*evento):
        """
        Method to ask if you wanna close the app.
        If the answer is Yes, the window will destroy
        """
        if tkMessageBox.askokcancel("Quit" + " " * 20 + "Py-Modoro", "Are you sure you wanna close Py-Modoro?"): #Makes a Window with "Accept/Cancel" buttons, if accept, then destroy the window
                root.destroy() #Destroy the main app




def start():
        #GLOBAL VARIABLES
        global CONFIG
        global APPPATH
        global main_errors
        global pom
        global root
        global app



        CONFIG = "pomfig.cfg" #: Configuration name archive
        APPPATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) #: Path of the main app

        main_errors = Errors() #: main variable to call errors

        try: #Try to check if the import can be onde
                from pomodoro import Pomodoro #this import is right here to catch the possible exception.
        except ImportError: #If the pygame is not installed makes the next block
                main_errors.ImportError() #Call to the ImportError method of the Error class
                os._exit(0) #Close the program

        pom = Pomodoro() #: Creates the pomodoro class instance, this will have all the configurations and runs all the procedores

        #if __name__ == "__main__":
        
        root = Tk() #: initialize the Tk

        root.title("Py-Modoro v."+ __version__ + "  - By Rock Neurotiko") #: Put the title of the main window

        app = App(root, pom) #: Start the main app calling the App class

        menubar = menu(root) #: Set the menu in a variable


        root.protocol("WM_DELETE_WINDOW", callback) #If the window will close, it calls to callback, who will ask if you really wanna close
        root.config(menu=menubar) #Set the menubar in root
        root.geometry("450x150") #Set the size of the window
        root.resizable(False, False) #Set that the window can't be resizable

        root.mainloop()
