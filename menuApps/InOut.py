import tkMessageBox, tkFileDialog
from ConfigParser import *

class SearchFile:

        def __init__(self, root):
                

                # define options for opening or saving a file
                self.file_opt = options = {}
                options['defaultextension'] = '' # couldn't figure out how this works
                options['filetypes'] = [('Music mp3', '.mp3')] # ('all files', '.*'), 
                options['initialdir'] = 'C:\\'
                options['initialfile'] = 'alarma.mp3'
                options['parent'] = root
                options['title'] = 'This is a title'


        def askOpenFile(self):
               
                return tkFileDialog.askopenfilename(**self.file_opt)





def loadConfig(pom, APPPATH, CONFIG):
        cfg = ConfigParser()
        
        cfg.read(APPPATH + '/' + CONFIG)
        pom.volume = cfg.getfloat("configuration", "volume")
        pom.filemp3 = cfg.get("configuration", "song")


def save(pom, APPPATH, CONFIG):
        cfg = ConfigParser()

        cfg.read(APPPATH + '/' + CONFIG)

        cfg.set("configuration", "volume", pom.volume)
        cfg.set("configuration", "song", pom.filemp3)

        f = open(APPPATH + '/' + CONFIG, "w")
        cfg.write(f)
        f.close()




def saveAreYouSure():
        return tkMessageBox.askokcancel("Save", "Do you wanna save the changes?")



