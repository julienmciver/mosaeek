#So as this stands, when I started writing this code, 
#I didn't know how to properly maniuplate the UI wiuthout
#referencing variables, so there are  a FUCKTON of variables here
#which have turned out to be completely unneccessary. I hope to imrpve this soon, 
#and if I ever get to the ponit where I will be hoping to push this to the app store
# I will be sure to fix this all.


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.properties import BooleanProperty
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.widget import Widget 
from kivy.graphics import Rectangle, Color 
from kivy.core.audio import SoundLoader
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button 
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.scatter import Scatter
from newProject import *
from mainMenu import *

from kivy.lang import Builder 
  
  
# Loading Multiple .kv files  
Builder.load_file('newPallette.kv') 
Builder.load_file('newProj.kv') 



import os #for listing directories
from kivy.uix.image import Image #for creating an ImageIcon class

def get_totPix():
        return int(split1[2])
        
def getPos_():
    return posFile
        
    
def getCoords():
    split2 = split1[1].split("#")
        
    coords = []
    cols = []
    temp = []
    
    for i in split2:
    
        temp = i.split("@")
        
        coords.append(temp[0])
        cols.append(temp[1])
    
    return [coords,cols]
def getPallette():
    split3 = split1[0].split(">")
    cols = []
    for i in split3:
        temp = i.split("!")
            
        cols.append([int(temp[0]), int(temp[1]), int(temp[2]), int(temp[3])])
    return cols
def getColCount():
    split4 = split1[3].split("$")
        
    colCount = []
    for i in split4:
        colCount.append(int(i))
    return colCount
    
def currentCoords():
        #return str(self.coords[self._pos])
        #         #print(str(self.coords[self._pos]))
    
    return "L"

def getCurrentCol():
    for i in pallette:
        
        if (str(i[3]) == currentCol):
           
            return [i[0]/255, i[1]/255, i[2]/255, 1]
            
            #return [1,1,1,1]
#TODO: put this all in a class so you can stop looking like a damn fool :*
def getFontColor():
    if (firstCol[0] + firstCol[1] + firstCol[2] > 0.7):
        return [0,0,0,1]
    else:
        return [1,1,1,0.9]

def getAmnt(pos_):
        #first, we get the last value in MosaicProj.txt
        #list that we need: colors
        tempPos = int(pos_)
        tempCount = 1
        side = not int(orientIndex)
        tempCoord = None
        if (tempPos +1 >= len(colors)):
            return 0
        while((colors[tempPos + 1] ==colors[tempPos] )):
            tempCoord = coords[tempPos+1].split(":")[side]
            if (tempCoord == "0"):
                break
            else:
                tempPos += 1
                tempCount += 1
            
        return tempCount
def makeShoppingList():
    tempString = ""
    for i in contentText_:
        if not (i == "$$$"):
            thing = i.split("}")
            tempString += thing[0] + ": " + thing[1] + "\n"

    return tempString

current_proj = open("currentProj.txt", "r").read().rstrip().split("$")

path = current_proj[0] + "/mosaicProj.txt"
file = open(path, "r").read()
path = current_proj[0] + "/pos.txt"
posFile_ = open(path, "r")
posFile = posFile_.read()

split1 = file.split("_")        

orientIndex = split1[4]
totPix = get_totPix()
coords = getCoords()[0]
colors = getCoords()[1]

colCount = getColCount()
pallette = getPallette()
pos__ = getPos_()
amnt = getAmnt(pos__)
currentCol = colors[int(posFile)]

firstCol = getCurrentCol()

fontCol = getFontColor()
path = current_proj[0] + "/shoppingList.txt"
contentText_ = open(path,'r').read().split("_")

class MiddleButton(ButtonBehavior, Widget):
    pressBool = False
    canvasCol = ListProperty([1,1,1,1])
    def __init__(self, **kwargs):
        super(MiddleButton, self).__init__(**kwargs)
        ButtonBehavior.__init__(self)

    def pressed_down(self):
        self.pressBool = True
    
    def pressed_up(self):
        if self.pressBool:
            self.pressBool = False
            
    def setCol(self, col):
        self.canvasCol = col

class NavBtn(ButtonBehavior, Widget):
    col = ListProperty([0.3,0.3,0.3,.3])
    def __init__(self, **kwargs):
        super(NavBtn, self).__init__(**kwargs)
        ButtonBehavior.__init__(self)
    
    def buttonDown(self):
        self.col = [1,1,1,1]

    def buttonUp(self):
        self.col = [0.3,0.3,0.3,.3]
    

       

class posDisplay(Widget):
    #a label above another label. The label will be changed 
    #when nextClicked is clicked.

    def __init__(self, **kwargs):
        Widget.__init__(self)
        self.__dict__.update(**kwargs)
        self.gridId.text = self.colOrRow
        self.pos.text = self.pos_
    
    def setTxt(self, newText):
        self.pos.text = newText
    

class ImagePop(Popup):
    imgIcon = None
    def __init__(self, img, **kwargs):
        super().__init__(**kwargs)
        self.imgIcon = StringProperty(img)

#has a row inputbox and a column input box and a jump to button and a cancel button
class JumpWindow(Popup):
    _row = ObjectProperty()

class ShoppingList(Popup):   
    pass   
    
class ShoppingListItem(ButtonBehavior, GridLayout):
    def __init__(self, **kwargs):
        ButtonBehavior.__init__(self)
        self.__dict__.update(kwargs)
            
        tempCan = CanvasWidget(color = (int(self.color[0])/255, int(self.color[1])/255, int(self.color[2])/255,1))
        tempCan.col_()
        self.can.add_widget(tempCan)
        self.colLabel.text = self.name
        #self.colLabel.bind(size=self.colLabel.setter('texture_size'))
        self.amntLabel.text = self.amount
        
class CanvasWidget(Widget):
    col = ListProperty((1,0,0,1))
    def __init__(self, **kwargs):
        super(CanvasWidget,self).__init__()
        self.__dict__.update(kwargs)
    def col_(self):
        self.col = self.color
        

class ProjectsPopup(Popup):
    pass


class ProjectsBtn(ButtonBehavior,GridLayout):
    
    def __init__(self, **kwargs):
        ButtonBehavior.__init__(self)
        
        self.__dict__.update(kwargs)
        
        self.image.source = self.path + "/image.png"
        self.projName.text = self.path.split("/")[2]
        split_ = open(self.path + "/mosaicProj.txt", "r").read().split("_")
        
        self.mediumName.text = split_[5]
        self.progress.text = str(round(int((open(self.path + "/pos.txt", "r").read()))/int(split_[2])*100))+ "%"
        split2 = split_[-5].split("#")[-1].split("@")[0].split(":")
        self.dimensions.text = str(int(split2[0]) + 1) + " x " + str(int(split2[1]) + 1)
        
    
    def pressed(self): 
        return self.path
        

class IconImage(ButtonBehavior, Image):
    pass



class MainLayout(BoxLayout, Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__dict__.update(shoppingList = ShoppingList(), projBtns = {})
        self.pop = ProjectsPopup()
        #self.shoppingList = ShoppingList()
        self.buildShoppingList()
        self.pop_projects()
        self.mainBtn.amount.text = str(amnt)
        self.mainBtn.setCol(firstCol)
        self.mainBtn.colorText.text = str(contentText_[int(currentCol)].split("}")[0])
            
        #self.overlayBg = (NewRowOverlayBG())

    #overlayBg = None
    
    column = StringProperty(str(int(coords[int(posFile)].split(":")[1])+1))
    row = StringProperty(str(int(coords[int(posFile)].split(":")[0])+1))

    bgBool = [False, False]
    shoppingList = None
    Projbtns = {}
    current_proj = current_proj[0]
    pop  = None
    pos_ = StringProperty(pos__)
    coords = coords
    amnt = amnt
    _fontCol = fontCol
    fontCol_ = ListProperty(_fontCol)   
    _pos = int(pos__)
    currentCol = colors[_pos]
    colCount = colCount
    orientation_ = True
    totalPixels = totPix
    mainCoords = StringProperty(coords[int(posFile)])
    currentCol_ = StringProperty(str(contentText_[int(currentCol)].split("}")[0]))
    currentRGB = ListProperty(firstCol)
    #a new
    contentText_ = open(path,'r').read().split("_")
    colors = colors
    totString = ("/" + str(totalPixels))
    mod_posString = str(_pos + 1)
    posString = StringProperty(mod_posString + totString)
    percString_ = str(round((_pos*100)/int(totalPixels))) + "%"
    percString = StringProperty(percString_)
    fontColor = ListProperty(getFontColor())
    skipCount = StringProperty(str(amnt))
    projBool = True
    imgIcon = StringProperty(current_proj + "/image.png")
    pallette = pallette
    maxJump = 0
    def setup(self):
        #resetting all starting values
        
        path = self.current_proj + "/mosaicProj.txt"
        file = open(path, "r").read()
        path = self.current_proj + "/pos.txt"
        posFile_ = open(path, "r")
        posFile = posFile_.read()

        split1_ = file.split("_")        

        orientIndex = split1_[4]
        self.totalPixels = int(split1_[2])
        self.coords = self.getCoords(split1_)[0]
        
        self.mainCoords = self.coords[int(posFile)]
        
        self.column = (str(int(self.coords[int(posFile)].split(":")[1])+1))
        self.row = (str(int(self.coords[int(posFile)].split(":")[0])+1))
        
        self.colors = self.getCoords(split1_)[1]
        self.colCount = self.getColCount(split1_)
        
        
        self.pos_ = posFile
        self.amnt = self.getAmnt(1)
        

        path = self.current_proj + "/shoppingList.txt"
        self.contentText_ = open(path,'r').read().split("_")
        self.pos_ = posFile
        self._pos = int(self.pos_)
        self.currentCol = self.colors[int(self.pos_)]
        self.currentcol = self.getCurrentCol()
        self.currentCol_ = str(self.contentText_[int(self.currentCol)].split("}")[0])
        self.currentRGB = self.getCurrentCol()
        self.fontCol = self.getFontColor_()
            
        
        self._fontCol = self.fontCol
        self.fontCol_ = self._fontCol   
        #self.currentCol = self.colors[self._pos]
        self.pallette = self.getPallette(split1_)
        self.orientation_ = True
        self.totalPixels = int(split1_[2])
        self.mainCoords = self.coords[int(posFile)]
        
        self.firstCol = self.getCurrentCol()
        self.currentRGB = self.firstCol
        self.totString = ("/" + str(self.totalPixels))
        self.mod_posString = str(self._pos + 1)
        self.posString = self.mod_posString + self.totString
        self.percString_ = str(round((self._pos*100)/int(self.totalPixels))) + "%"
        self.percString =self. percString_
        self.fontColor = self.getFontColor_()
        self.skipCount = str(self.amnt)
        self.imgIcon = self.current_proj + "/image.png"
        self.mainBtn.amount.text = str(self.amnt)
        self.mainBtn.setCol(self.firstCol)
        self.mainBtn.colorText.text = str(self.contentText_[int(self.currentCol)].split("}")[0])
            
        posFile_.close()
    def getPallette(self, split1_):
        split3 = split1_[0].split(">")
        cols = []
        for i in split3:
            temp = i.split("!")
                
            cols.append([int(temp[0]), int(temp[1]), int(temp[2]), int(temp[3])])
        return cols

    def getCoords(self, split1_):
        split2 = split1_[1].split("#")
            
        coords_ = []
        cols_ = []
        temp_ = []

        for i in split2:
        
            temp = i.split("@")
            
            coords_.append(temp[0])
            cols_.append(temp[1])
        
        return [coords_,cols_]
    def getColCount(self, split1_):
        split4 = split1_[3].split("$")
            
        colCount = []
        for i in split4:
            colCount.append(int(i))
        return colCount

    #percString = StringProperty(percString)
    def getCurrentCol(self):
        for i in self.pallette:
            if (str(i[3]) == self.currentCol):
           
                return [i[0]/255, i[1]/255, i[2]/255, 1]

    def buttonDown(self):
        self.mainBtn.btn.size = (self.mainBtn.btn.width/1.05, self.mainBtn.btn.height/1.05)


    def nextClicked(self, amnt, cond, *args):
        
        if ((Window.mouse_pos[0] >= self.mainBtn.pos[0]) and (Window.mouse_pos[0] <= (self.mainBtn.width + self.mainBtn.pos[0]))) and ((Window.mouse_pos[1] >= self.mainBtn.pos[1]) and (Window.mouse_pos[1] <= (self.mainBtn.height + self.mainBtn.pos[1]))) or (args[0]):
            if not (int(self.pos_) >= int(self.totalPixels)):
                #update pos_

                self.pos_ = (str(int(self.pos_) + amnt))
                
                posFile__ = open(self.current_proj + "/pos.txt", 'w')
                posFile__.write(self.pos_)
                posFile__.close()     
                #update coords
                #self.mainCoords = self.coords[int(self.pos_)]
                self.row = str(int(self.coords[int(self.pos_)].split(":")[0]) + 1)
                self.column = str(int(self.coords[int(self.pos_)].split(":")[1]) +1)
                #update percentage
                tempPos_ = int(self.pos_)
                tempPercString_ = str(round((tempPos_)*100/int(self.totalPixels))) + "%"
                
                self.percString = tempPercString_
                #update color
                self.currentCol = self.colors[int(self.pos_)]
                self.currentcol = self.getCurrentCol()
                self.currentCol_ = str(self.contentText_[int(self.currentCol)].split("}")[0])
                #self.currentRGB = self.getCurrentCol()
                #update totString
                temptotString = str(tempPos_+1) + "/" + str(totPix)
                self.posString = temptotString
                #update fontCol
                self. amnt = self.getAmnt(1)
                self.pop_projects()
                self.mainBtn.amount.text = str(self.amnt)
                self.mainBtn.setCol(self.getCurrentCol())
                self.mainBtn.colorText.text = str(self.contentText_[int(self.currentCol)].split("}")[0])
                self.fontCol_ = self.getFontColor_()
                if (cond == 0):
                    self.mainBtn.btn.size = (self.mainBtn.btn.width*1.05, self.mainBtn.btn.height*1.05)

                if (self.checkNewRow(cond)):
                    print("New Row")
        else:
            self.mainBtn.btn.size = (self.mainBtn.btn.width*1.05, self.mainBtn.btn.height*1.05)



    def backClicked(self):
        
        if not (int(self.pos_) == 0):
    
            self.pos_ = (str(int(self.pos_) - 1))
        
            posFile__ = open("pos.txt", 'w')
            posFile__.write(self.pos_)
            posFile__.close()     
            #update coords
            self.mainCoords = coords[int(self.pos_)]
            #update percentage
            tempPos_ = int(self.pos_)
            tempPercString_ = str(round((tempPos_)*100/int(self.totalPixels))) + "%"
            
            self.percString = tempPercString_
            #update color
            
            self.currentCol = colors[int(self.pos_)]
            self.currentCol_ = str(int(self.currentCol) + 1)
            self.currentRGB = self.getCurrentCol()
            
            #update totString
            temptotString = str(tempPos_+1) + "/" + str(totPix)
            
            self.posString = temptotString
            #update fontCol
           
            self.getAmnt(1)
            self.fontCol_ = self.getFontColor_()
    def getFontColor_(self):
        RGBVals = self.getCurrentCol()
        
        if (RGBVals[0] + RGBVals[1] + RGBVals[2] > 0.7):
      
            return [0,0,0,1]
        else:
     
            return [1,1,1,0.9]
  
        #builds a shopping list from shoppinglist.txt and stores it in widgets
    def buildShoppingList(self):        
        tempCount = 0
        text_ = open(self.current_proj + "/shoppingList.txt",'r').read().split("_")
        lenVar = len(text_)
        for c,i in enumerate(text_):
            
            if not (i == "$$$"):
                thing1 = i.split("}")
                thing = thing1[1].split("#")
                if not (c == lenVar -1):
                    col = thing[1].split(",")
                    self.shoppingList.grid.add_widget(ShoppingListItem(name = thing1[0].split(":")[1], color = col, amount = thing[0]))
                    tempCount += 1
                else:
                    self.shoppingList.totText1.text = "Elements: " + thing1[1]
                    self.shoppingList.totText2.text = "Colors: " + str(tempCount)

    
    def shoppingListOpen(self):
                
        self.shoppingList.open()




    def imageOpen(self, img):
        pop = ImagePop(img)
        pop.src.source = img
        pop.open()


    def getAmnt(self, cond):
        #first, we get the last value in MosaicProj.txt
        #list that we need: colors
        tempPos = int(self.pos_)
        tempCount = 1
        side = not int(orientIndex)
        tempCoord = None
        if cond:
            if not (int(tempPos) >= len(self.colors) -1):
                while((self.colors[tempPos + 1] ==self.colors[tempPos] )):
                    tempCoord = self.coords[tempPos+1].split(":")[side]
                    if (tempCoord == "0"):
                        break
                    else:
                        tempPos += 1
                        
                        if (tempPos == len(self.colors) -1):
                            print("u won da game")
                            return tempCount
                        tempCount += 1
                            
                self.skipCount = str(tempCount)
                if self.maxJump:
                    if (tempCount >= self.maxJump):
                        return maxJump

            else:
                tempCount = 0

            return tempCount

        else:
            tempCount = 0
            while((self.colors[tempPos - 2] ==self.colors[tempPos -1] )):
                tempCoord = self.coords[tempPos-1].split(":")[side]
                
                if (tempCoord == "0") or tempPos == 0:
                    
                    break
                else:
                    tempPos -= 1
                    tempCount += 1
            
            self.skipCount = str(-tempCount)
       
            if (tempCount == 0):
                return -1
            return -tempCount-1
    
    #TODO: this is ugly and weird. Must fix
    def backtoStart(self):
        if not (int(self.pos_) == 0):
            side = not int(orientIndex)
            tempCoord = self.coords[int(self.pos_)].split(":")[side]
            self.nextClicked(self.getAmnt(0), 1,1)
    
    def jumpTo(self):
        #a popup that asks you where you want to go
        pop = JumpWindow(title="Jump to:")
        pop.open()
    
    def pop_projects(self, *args):
        #self.pop = ProjectsPopup()
        if self.projBool:
            projects = os.listdir("./Mosaic Projects")
            projects.sort()
            for v,i in enumerate(projects):
                cPath = "./Mosaic Projects/" + i
                self.projBtns[cPath] = ProjectsBtn(path = cPath)
                self.projBtns[cPath].bind(on_release = lambda a: self.newProj(ProjectsBtn.pressed(a)))
                self.pop.grid.add_widget(self.projBtns[cPath])
                self.projBool = False
        else:
            #update the percentage on the current proj's percentage
            self.projBtns[self.current_proj].progress.text = str(self.percString)
            
            
        #self.pop.open()
        
    def newProj(self, path):
        if path == self.current_proj:
            self.pop.dismiss()
            return
        projFile = open("currentProj.txt", "w")
        projFile.write(path)
        projFile.close()
        self.current_proj = path
        self.shoppingList = ShoppingList()
        self.buildShoppingList() 
        self.pop.dismiss()
        self.setup()

    def updateLoadingScreen(self, perc):
        pass

    #extract row and column from a given pos
    def coordsGet(self, pos):
        tempCoords = self.coords[pos]
        tempCoords = tempCoords.split(":")
        x =  {"row" : int(tempCoords[0]),
                "col": int(tempCoords[1])}
        return x
    #Finishing a row function. opens a popup, animates it

    
    def checkNewRow(self, backClicked):
        if not backClicked:
            if self.bgBool[0] == False:
                coords_ = self.coordsGet(int(self.pos_))
                if not (coords_["col"] and not int(self.pos_) == 0):
                    return True
                else:
                    return False
    

class Manager(ScreenManager):
    pass
            
class MosaeekApp(App):
    def build(self):
        v = Manager(transition=FadeTransition())
        v.add_widget(MainMenu(name = 'MainMenu'))
        v.add_widget(MainLayout(name = 'current_proj'))
        v.add_widget(Pallettes(name = 'Pallettes'))
        v.add_widget(NewPallette(name = "NewPallette"))
        v.add_widget(NewProj(name = 'NewProj'))
        
        return v    

MosaeekApp().run()



        
