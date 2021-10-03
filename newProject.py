from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
import os
from mainMenu import *
#first, make the main menu screen switch:

class NewProj(BoxLayout, Screen):
    menuItems = []
    projPallette = []
    dims = [0,0]
    pop = None
    projIm = None
    #get a floatlayout to sit on top of the pallette box when there are no pallettes selected
    

    #make it so that when you click select pallette, it takes you to the pallette page, except clicking on a pallette menu item gives you the option to
    #modify, use a pallette, delete a pallette or make a new pallette.
    
    def popOpen(self):
        pass

    def load(self):
        self.pallettes.clear_widgets()
        
        path = './Pallettes'
        dirs = os.listdir(path)
        file = None
        #Okay, I need to make it so that a transparent canvas is drawn over the thing. I need to insdert this
        #over the im. Oay:
        tempNo = 0
        print("HHHH")
        for c, i in enumerate(dirs):
            if not i == 'resources':
                try:
                    tempNo = c
                    file = open (path + "/" + i + "/pallette.txt").read()
                    x = PalletteMenuItem(file, 1, height = self.height)
                    
                    self.menuItems.append(x)
                   
                    #x.bind(on_release = lambda x: self.modify(x.pop.ar))
                    #x.pop.modifyBtn.bind(on_release= lambda t: self.switchScreen("NewPallette"))
                    #x.pop.deleteBtn.bind(on_release = lambda x: self.reloadItems())
                    self.pallettes.add_widget(x)
                    
                    #self.pallettes.add_widget(L())

                except Exception as e:
                    print(e)