import tkMessageBox, tkFileDialog
from ConfigParser import *

class SearchFile:
        """
        Class to manage the File Search
        Uses tkFileDialog
        """

        def __init__(self, root):
                """
                Constructor.
                @param root The master window.
                @type root Tk() or Toplevel
                """
                

                # define options for opening or saving a file
                self.file_opt = options = {}
                options['defaultextension'] = '' # couldn't figure out how this works
                options['filetypes'] = [('Music mp3', '.mp3')] # ('all files', '.*'), 
                options['initialdir'] = 'C:\\'
                options['initialfile'] = 'alarma.mp3'
                options['parent'] = root
                options['title'] = 'This is a title'


        def askOpenFile(self):
                """
                Open a File Dialog to select the music.
                @return A String with the file path.
                """
               
                return tkFileDialog.askopenfilename(**self.file_opt)





def loadConfig(pom, APPPATH, CONFIG):
        """
        Method to load the configuration.
        @param pom The Pomodoro to set the options
        @type pom Pomodoro

        @param APPPATH The path to the apply
        @type APPPATH String

        @param CONFIG The name of the config archive (*.cfg)
        @type CONFIG String
        """
        cfg = ConfigParser()
        
        cfg.read(APPPATH + '/' + CONFIG)
        pom.volume = cfg.getfloat("configuration", "volume")
        pom.set_Filemp3(cfg.get("configuration", "song"))


def save(pom, APPPATH, CONFIG):
        """
        Method to save the changes (volume, song,...) in the configuration file
        (By default pomfig.cfg)

        @param pom The Pomodoro to set the options
        @type pom Pomodoro

        @param APPPATH The path to the apply
        @type APPPATH String

        @param CONFIG The name of the config archive (*.cfg)
        @type CONFIG String
        """
        cfg = ConfigParser()

        cfg.read(APPPATH + '/' + CONFIG)

        cfg.set("configuration", "volume", pom.volume)
        if(pom.filemp3 != ""):
                cfg.set("configuration", "song", pom.filemp3)

        f = open(APPPATH + '/' + CONFIG, "w")
        cfg.write(f)
        f.close()




def saveAreYouSure():
        """
        Method to open a window to ask if it would save.\n
        Two options, Accept, Cancel.
        @return The value of True (accept) of False (cancel).
        """
        return tkMessageBox.askokcancel("Save", "Do you wanna save the changes?")



