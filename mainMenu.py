from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget 
from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.core.image import Image
import math
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.popup import Popup
from kivy.uix.label import Label 
from kivy.uix.anchorlayout import AnchorLayout 
import os
import time
from kivy.clock import Clock
from kivy.cache import Cache
import gc
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.core.image import Image as CoreImage
import shutil
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import *
from kivy.graphics.transformation import Matrix


# To collect the coordinates after freehand drawing
from bresenham import bresenham

def parseFile(file):
    split1 = file.split("#")    
    colors_ = {'name':split1[1]}
    for i in split1[1:]:
        x = i.split("_")
        y = x[1][1:-1].split(", ")
        colors_[x[0]]= [float(y[0]), float(y[1]), float(y[2])]    
    

    return colors_

def normalise(num2, num1):
    return int(((num1-num2)/(abs(num1-num2))))

def sortAr(ar, index, cond):
    p = ar[0]
    if cond == 'min':

        for i in ar:
            if p[index] > i[index]:
                p = i
    elif cond == 'max':
        for i in ar:
            if p[index] < i[index]:
                p = i
    return p[index]
             

def distance(p1,p2):
    return (math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2))

class MainMenu(BoxLayout, Screen):
    def __init__(self, **kwargs):
        BoxLayout.__init__(self)
        self.__dict__.update(kwargs)
        self.name = 'MainMenu'

class Pallettes(Screen):
    s = False
    pop = None
    menuItems = []
    state = None
    def __init__(self, **kwargs):
            Screen.__init__(self)
            self.__dict__.update(kwargs)
            self.name = "Pallettes"
            #self.pop = ConfirmPop()
            #self.pop.modifyBtn.bind(on_release = lambda x: self.manager.get_screen("NewPallette").)
            
    def reloadItems(self):
        #shutil.rmtree('./Pallettes/' + nameStr)
        
        Clock.schedule_once(lambda x: self.pallettes.clear_widgets(), 0)
        Clock.schedule_once(lambda x:self.load(), 0)
    def load(self):
        self.pallettes.clear_widgets()
        
        path = './Pallettes'
        dirs = os.listdir(path)
        file = None
        #Okay, I need to make it so that a transparent canvas is drawn over the thing. I need to insdert this
        #over the im. Oay:
        tempNo = 0
        for c, i in enumerate(dirs):
            if not i == 'resources':
                try:
                    tempNo = c
                    file = open (path + "/" + i + "/pallette.txt").read()
                   
                    x = PalletteMenuItem(file, self.state, height = self.height)
                    
                    self.menuItems.append(x)

                    x.bind(on_release = lambda x: self.modify(x.pop.ar))
                    
                    if self.state == 'pallettes':
                        print('pallettes')
                        x.pop.btn2.bind(on_release= lambda t: self.switchScreen("NewPallette"))
                        x.pop.btn1.bind(on_release = lambda x: self.reloadItems())
                    elif self.state == 'newProj':
                        print('newProj')
                    elif self.state == 'pallettesNewProj':
                        print('pallettesNew')
                    self.pallettes.add_widget(x)
                    
                    #self.pallettes.add_widget(L())

                except Exception as e:
                    print(e, " HERE")
    
    
    def open_(self):
        self.pop.open_()
    
    def switchScreen(self, scrn):
        self.manager.current = scrn
    
    def modify(self, ar):
        self.manager.get_screen("NewPallette").populate(ar)
        self.manager.get_screen("NewPallette").modifyBool = True
#manager.get_screen('NewPallette').populate(file))#


class DeletePop(Popup):
    ar = None
    name_ = StringProperty("")
    doneBool = False
    def __init__(self, ar):
        Popup.__init__(self)
        self.name_ = ar[0].split("_")[1]
        self.ar = ar
        for i in ar[1:]:
            x = i.split("_")
            y = x[1][1:-1].split(", ")
            colors_ = [float(y[0]), float(y[1]), float(y[2])]    
            self.colors.add_widget(ColorBox(colors_, x[0]))
    #def delete(self):
     #   nameStr = self.name_
      #  shutil.rmtree('./Pallettes/' + nameStr)
       # self.doneBool = True

class ConfirmPop(Popup):
    ar = None
    name_ = StringProperty("")
    doneBool = False
    def __init__(self, ar, *args):
        Popup.__init__(self)
        self.name_ = ar[0].split("_")[1]
        self.ar = ar
        for i in ar[1:]:
            x = i.split("_")
            y = x[1][1:-1].split(", ")
            colors_ = [float(y[0]), float(y[1]), float(y[2])]    
            self.colors.add_widget(ColorBox(colors_, x[0]))
        if args[0] == 'pallettes':
            self.btn1.text = "Delete"
            self.btn1.bind(lambda x: self.delete())
        elif args[0] == 'newProjPallette':
            self.btn1.text = "Cancel"
            self.btn2.text = 'Select'
        
    #confirmPop

    def delete(self):
        nameStr = self.name_
        shutil.rmtree('./Pallettes/' + nameStr)
        self.doneBool = True

    def open_(self, file):
        self.string = file
        print(file)
        #colors = parseFile(file)
        #self.string = colors['name']
        #for i, (k, v) in enumerate(colors.items()):
         #   print(k,v)
        #self.open()   
    
    #DeletePop

    #newProjPop

class NewPallettePop(Popup):
    string = ""
    def __init__(self, str_, **kwargs):
        super().__init__(**kwargs)
        self.string = str_


class PallettePopup(Popup):
    col = ListProperty([1,0,1])
    errorVis = ListProperty((1,0,0,1))
    def __init__(self, **kwargs):
            super().__init__(**kwargs)
        
    def setCol(self, col_):
        self.col = col_
    
    def setErrorVis(self, col_):
        self.errorVis = col_
        

class LabelButton(ButtonBehavior, Label):
    col = ListProperty([0.3,0.3,0.3,0.3])
    normalCol = ([.3,.3,.3,.3])
    def setBtnCols(self, btnCol):
        self.col = btnCol
    
        
        
class PalletteItem(ButtonBehavior, BoxLayout):
    col_ = ListProperty([1,0,0])
    name_ = StringProperty()
    
    def __init__(self, *args, **kwargs):
        
        ButtonBehavior.__init__(self)
        self.col_ = args[1]
        self.name_ = args[0]
    def getName(self):
        return str(self.name_)

class ColorBox(BoxLayout):
    col = ListProperty((0,0,0))
    def __init__(self, color, name_):
        BoxLayout.__init__(self)
        self.col = color
        self.txt.text =  name_
        

class NamePop(Popup):
    pass

class L(BoxLayout):
    pass



class PalletteMenuItem(ButtonBehavior, BoxLayout):
    col = ListProperty((.3,.3,.3,.3))
    pop = None
    def __init__(self, string, *args, **kwargs):
        ButtonBehavior.__init__(self)
        split1 = string.split("#")
        self.name_.text = split1[0].split("_")[1]
        
        self.pop = ConfirmPop(split1, args[0])
        
        
        for i in split1[1:]:
            x = i.split("_")
            
            y = x[1][1:-1].split(", ")
            colors_ = [float(y[0]), float(y[1]), float(y[2])]    
            self.colors.add_widget(ColorBox(colors_, x[0]))
      


class ModeBtns(BoxLayout):
    active = 'pointBtn'
    btns = {}
    activeCol = [0,1,0,0.5]
    inactiveCol = [.3,.3,.3,.3]
    def getActive(self):
        return self.active
    
    def btnClick(self, btn):
        
        self.setInactive()
        self.setActive(btn)
  

    def setActive(self, btn):
        self.btns[str(btn.name)].setBtnCols((0,1,1,1))
        self.btns[str(btn.name)].normalCol = self.activeCol
        self.active = btn.name

    
    def setInactive(self):
        self.btns[self.active].setBtnCols(self.inactiveCol)
        
class ZoomImage(RelativeLayout):
    pass 

class NewPallette(Screen):
    mode = 'rect'
    
    
    col = ListProperty([0,0,0,0])
    refIndex = 0
    m = Image.load('./resources/x.png', keep_data= True)
    pallette = {'name':''}
    palletteName = StringProperty(pallette['name'])
    pop = None
    namePop = None
    palletteList = None
    modifyBool = False
    imBool = True
    damnBool = True
    resourceList =[]
    uploadCount = 0
    prevPoint = None
    prevPointIm = None
    state = ''
    firstPos = None
    borderImList = []

    freeHandDims = [0,0,0,0]

    def __init__(self, **kwargs):
        Screen.__init__(self)
        self.__dict__.update(kwargs)
        self.name = "NewPallette"
     #   self.pop.addText.bind(on_release = lambda: self.addItem())
        self.modeBtns.pointBtn.setBtnCols(self.modeBtns.activeCol)
        self.modeBtns.btns = {'pointBtn': self.modeBtns.pointBtn, 'rectBtn': self.modeBtns.rectBtn, 'circBtn':self.modeBtns.circBtn, 'freeBtn':self.modeBtns.freeBtn}
        v = Image(self.im.source)
        v.save("A1.png")
        self.pop = PallettePopup()
        self.pop.addBtn.bind(on_release = lambda x: self.addItem())
        self.namePop = NamePop()
        self.namePop.confirmBtn.bind(on_release = lambda x: self.saveName())
        self.namePop.cancelBtn.bind(on_release = lambda x: self.cancelBtn())

    def cancelBtn(self):
        self.manager.current = 'Pallettes'
    def saveName(self):
        if not self.namePop.txt.text in os.listdir('./Pallettes'):
            self.pallette['name'] = self.namePop.txt.text
            self.palletteName = self.pallette['name']
            self.namePop.txt.text = ""
            self.namePop.dismiss()
        else:
            pass

    def presss(self):
        coords = self.coords()
        if coords == None:
            self.initCanvas()

    def onLeave(self):
        self.refIndex = 0
        self.col = (0,0,0,0)
        Clock.schedule_once(lambda x: self.changeSource('./resources/x.png'),0)
        #self.im.source = './resources/x.png'
        Cache.print_usage()
        Cache.remove('kv.image')
        #self.m = Image.remove_from_cache(self.m)
    def onEnter(self):
        #Clock.schedule_once(lambda x: self.export(), 0)
        #self.refIndex = 0
        self.initCanvas()
        Clock.schedule_once(lambda x: self.changeSource(self.path()),0)

        Clock.schedule_once(lambda x: self.export(),0)
        Cache.remove('kv.image')
        self.m = Image.remove_from_cache(self.m)
        self.m = Image.load("A" + str(int(self.imBool)) + ".png", keep_data = True)
    


    #---------------------------_ZOOM ON TOUCH_----------------------------

    #----------------------------------------------------------------------

    def addImgWidget(self):
        img = ZoomImage()
        img.size = self.colBox.size
        #img.pos = self.colBox.pos
        #img.imgScatter.pos = self.colBox.pos
        #img.img.scale = 100
        img.img.source = self.path()
        coords = self.getPosOnImage()
        I = img.scatter.transform
        
        self.colBox.add_widget(img)

    #----------------------------------------------------------------------

    #----------------------------------------------------------------------


    def touchDown(self):
        self.state = self.modeBtns.getActive()
        if self.state == 'pointBtn':
            self.mousePos()
        elif self.state == 'rectBtn' or self.state == 'circBtn':
            self.drawPoint()
        elif self.state == 'freeBtn':
            #self.addImgWidget()
            self.drawPoint(1)
        


    def addToBorder(self, *args):
        
        

        if not len(self.borderImList):
            self.firstPos = self.coords()
            firstPosIm = self.getPosOnImage(self.firstPos)
            self.freeHandDims = [firstPosIm[0],firstPosIm[1],firstPosIm[0],firstPosIm[0]]

        if len(args):
                if args[0][0] < self.freeHandDims[0]:
                    self.freeHandDims[0] = args[0][0]
                   
                elif args[0][0] > self.freeHandDims[1]:
                    self.freeHandDims[1] = args[0][0]
                    
                
                if args[0][1] < self.freeHandDims[2]:
                    self.freeHandDims[2] = args[0][1]
                   
                elif args[0][1] > self.freeHandDims[3]:
                    self.freeHandDims[3] = args[0][1]
                   


                self.borderImList.append(args[0]) 
                
                return

        
        else:
            temp = self.getPosOnImage()
            self.borderImList.append(temp)
        
            

    def touchMove(self):
        if self.state == 'pointBtn':
            self.mousePos()
        elif self.state == 'rectBtn':
            coords = self.coords()
            self.drag()
        elif self.state == 'circBtn':
            #self.addToBorder()    
            self.drag()
        elif self.state == 'freeBtn':
            self.addToBorder()    
            self.drag()


    def populate(self, string):
        
        self.menu.clear_widgets()
        self.palletteName = string[0].split("_")[1]
        self.pallette.clear()
        self.pallette['name'] = self.palletteName
        path = './Pallettes/' + self.pallette['name'] + '/resources '
        self.resourceList = os.listdir(path)
        self.resourceList.sort()
        if (len(self.resourceList)):
            imSource = path + '/' + self.resourceList[0]
        else:
            imSource = "./resources/x.png"
        self.refIndex = 0
        self.initCanvas()
        Clock.schedule_once(lambda x: self.changeSource(imSource),0)
        #self.im.source = imSource
        self.damnBool = False
        self.uploadCount = len(self.resourceList)
        #self.imBool = False
        for i in string[1:]:
            x = i.split("_")
            y = x[1][1:-1].split(", ")
            colors_ = [float(y[0]), float(y[1]), float(y[2])]    
            item = PalletteItem(x[0], colors_)
            item.bind(on_release=lambda item: self.removeItem(item))
            self.pallette[x[0]] = colors_
            self.menu.add_widget(item)
    def export(self):
        os.remove("A" + str(int(self.imBool)) + ".png")
        self.imBool = not self.imBool
        self.k.export_to_png("A" + str(int(self.imBool)) + ".png")
       # self.onEnter()
    def changePic(self, dir_):

        if not self.path() == './resources/x.png':
            try:
                if (self.refIndex + dir_ >= 0 and self.refIndex + dir_ < len(self.resourceList)):
                    self.refIndex += dir_
                    self.initCanvas()
                    
                    Clock.schedule_once(lambda x: self.changeSource(self.path()),0)
                    
                    #self.im.source = path + "/" + self.resourceList[self.refIndex]
                    #self.im.reload()
                    Clock.schedule_once(lambda x: self.export(), 0)
                    Cache.remove('kv.image')
                    self.m = Image.remove_from_cache(self.m)
                    self.damnBool = False
                    self.m = Image.load("A" + str(int(self.imBool)) + ".png", keep_data = True)
                    

            except Exception as e:
                print(e)

    #************************Start of crop work
    def coords(self):
        if self.im.collide_point(Window.mouse_pos[0],Window.mouse_pos[1] ):
            x_ = Window.mouse_pos[0]
            y_ = Window.mouse_pos[1]
            return [x_,y_]
        return None
    def drawPoint(self, *args):
        if self.im.collide_point(Window.mouse_pos[0],Window.mouse_pos[1]) and not self.path() == './resources/x.png':
            if not self.damnBool:
                self.m = Image.load("A" + str(int(self.imBool)) + ".png", keep_data = True)
                self.damnBool = True
            self.prevPoint = [Window.mouse_pos[0], Window.mouse_pos[1]]
            self.prevPointIm = self.getPosOnImage()
            self.drag()
    def drawRect(self, coords):
        
        with self.im.canvas:
            Color(1,1,1)
            size_ = [coords[0] - self.prevPoint[0], coords[1] - self.prevPoint[1]]
            #4 lines
            points = [self.prevPoint[0], self.prevPoint[1], self.prevPoint[0], coords[1]]
            Line(points = points, width = 2.2)
            Color(0,0,0,1)
            Line(points = points, width = 1.3)
            Color(1,1,1,1)
            points = [self.prevPoint[0], coords[1], coords[0], coords[1]]
            Line(points = points, width = 2.2)
            Color(0,0,0,1)
            Line(points = points, width = 1.3)
            Color(1,1,1,1)
            points = [coords[0], self.prevPoint[1], coords[0], coords[1]]
            Line(points = points, width = 2.2)
            Color(0,0,0,1)
            Line(points = points, width = 1.3)
            Color(1,1,1,1)
            points = [self.prevPoint[0], self.prevPoint[1], coords[0], self.prevPoint[1]]
            Line(points = points, width = 2.2)
            Color(0,0,0,1)
            Line(points = points, width = 1.3)
            
            #Rectangle(pos = (self.prevPoint), size = (size_))
    def drawCirc(self, coords):
        
        with self.im.canvas:
            Color(1,1,1,1)
            size = [coords[0] - self.prevPoint[0], coords[1] - self.prevPoint[1]]
            Line(ellipse = (self.prevPoint[0], self.prevPoint[1], size[0]+2, size[1]+2), width = 2, pos = (self.prevPoint[0], self.prevPoint[1]))
            Color(0,0,0,1)
            Line(ellipse = (self.prevPoint[0], self.prevPoint[1], size[0]+1.3, size[1]+1.3), width = 1.3, pos = (self.prevPoint[0], self.prevPoint[1]))
            #Ellipse(pos = (0,0), size = (200,200))

    def line(self, x1, y1, x2, y2):
        with self.im.canvas:
            Color(0,0,0,1)
            Line(points = (x1,y1, x2,y2), width = 2)
            Color(1,1,1,1)
            Line(points = (x1,y1, x2,y2), width = 0.5)
 

    def getCoordsAlongLine(self):
        #first calculate m: 
        coords = self.coords()

        
        point1 = [math.floor(self.firstPos[0]), math.floor(self.firstPos[1])]
        point2 = [math.floor(coords[0]), math.floor(coords[1])]
        self.line (point1[0], point1[1], point2[0], point2[1])
        x = list(bresenham(point1[0], point1[1], point2[0], point2[1]))
        
        
        
        for i in x:
            
            temp = self.getPosOnImage(i)
            self.addToBorder(temp)
            
        
        

        
        
        
        
        
          #iterating through the thing
        #1st, get the boundary lines. 

        
        
        # f(x) = m*x + c
        
        
                  

    def calcCoords(self):
        if not self.state == 'pointBtn' and not self.path() == './resources/x.png':
            if self.state == 'freeBtn':
                
                
                self.getCoordsAlongLine()
                left = sortAr(self.borderImList, 0, 'min') - 1
                right = sortAr(self.borderImList, 0, 'max') + 1
                top = sortAr(self.borderImList, 1, 'min') -1
                down = sortAr(self.borderImList, 1, 'max') + 1

                
                
                count = 0
                pixelSwitch1 = False
                pixelSwitch2 = False
                x = 0
                totCol = [0,0,0,1]
                tempTot = [0,0,0]
                for y in range(top, down):
                    pixelSwitch1 = False
                    pixelSwitch2 = False
                    
                    for x in range(left, right):
                        if (x,y) in self.borderImList:
                            if pixelSwitch1 == pixelSwitch2:
                                pixelSwitch1 = not pixelSwitch1
                        else:
                            if not pixelSwitch1 == pixelSwitch2:
                                pixelSwitch2 = pixelSwitch1
                        
                        if pixelSwitch1 and pixelSwitch2:
                                
                            tempCol = self.m.read_pixel(x,y)
                            tempTot[0] += tempCol[0]
                            tempTot[1] += tempCol[1]
                            tempTot[2] += tempCol[2]
                            count += 1
                            
                        if x == right-1 and not pixelSwitch1:
                            totCol[0] += tempTot[0]
                            totCol[1] += tempTot[1]
                            totCol[2] += tempTot[2]
                            
                            tempTot.clear()
                            tempTot = [0,0,0]
                            
                col_ = [totCol[0]/count, totCol[1]/count, totCol[2]/count, 1]
                self.col = col_
                self.borderImList.clear()
                self.firstPos = None
                
                return



            if self.im.collide_point(Window.mouse_pos[0],Window.mouse_pos[1]) and not self.path() == './resources/x.png':
                coords = self.getPosOnImage()
                #if points['name'] == 'rect':
                gridDims = [int(abs(coords[0] - self.prevPointIm[0])), int(abs(coords[1] - self.prevPointIm[1]))]
                minCoords = [min(coords[0], self.prevPointIm[0]), min(coords[1], self.prevPointIm[1])]
                tot = [0, 0, 0, 1]  
                
                if self.state == 'circBtn':
                    dims = [0.5*gridDims[0], 0.5*gridDims[1]]
                    angleInc =  (math.pi)/(gridDims[1])
                    temp = 0
                    param = [0,0]
                    switch = False
                    counter = 0
                    
                    
                    for i in range(gridDims[1]):
                        
                        #check the working here
                        
                        theta = math.pi/2 + angleInc*i
                        
                        xx = 1/((1/(dims[0]**2)) + ((math.tan(theta)**2)/(dims[1]**2)))
                        yy = xx*(math.tan(theta)**2)
                        r = math.sqrt(xx + yy)
                        insidePixels = round(abs(r*math.cos(theta)*2))
                        M = (gridDims[0] - insidePixels)/2
                        param[0] = M
                        param[1] = insidePixels
                        temp = 0
                        for c in range(gridDims[0]):
                            
                            if (temp <= param[int(switch)]):
                                temp += 1
                                if switch:
                                    tempCol = self.m.read_pixel(minCoords[0] + c, minCoords[1]+i)
                                    tot[0] += tempCol[0]
                                    tot[1] += tempCol[1]
                                    tot[2] += tempCol[2]
                                    counter += 1
                                         
                            else:
                                switch = not switch
                                temp = 0
                                
                if self.state == 'rectBtn':
                    for i in range(gridDims[1]):
                        for c in range(gridDims[0]):
                            tempCol = self.m.read_pixel(minCoords[0] + c, minCoords[1]+i)
                            tot[0] += tempCol[0]
                            tot[1] += tempCol[1]
                            tot[2] += tempCol[2]
                try:
                    if self.state == 'rectBtn':
                        noPix = gridDims[0]*gridDims[1]
                    elif self.state == 'circBtn':
                        noPix = counter
                    tot[0] /= noPix
                    tot[1] /= noPix
                    tot[2] /= noPix
                    self.col = tot       
                except Exception as e:
                    print(e)

    def path(self, *args):
        if not len(self.resourceList):
            return './resources/x.png'    
        if self.modifyBool:
            return './Pallettes/{}/resources /{}'.format(self.pallette['name'], self.resourceList[self.refIndex]) 
        if len(os.listdir('./temp')):
    
            return './temp/{}'.format(self.resourceList[self.refIndex])
        return './resources/x.png'
    def drawLine(self, coords):
        with self.im.canvas:
            Color(0,0,0,1)
            Line(points=[coords[0], coords[1], self.prevPoint[0], self.prevPoint[1]], width = 2)
            Color(1,1,1,1)
            Line(points = (coords[0], coords[1], self.prevPoint[0], self.prevPoint[1]), width = 0.5)
        temp = list(bresenham(int(coords[0]), int(coords[1]), int(self.prevPoint[0]), int(self.prevPoint[1])))
        temp2 = []
        for i in temp:
            temp3 = self.getPosOnImage(i)
            temp2.append(temp3)
        return temp2
        

    def initCanvas(self):
        with self.im.canvas:
     
            self.im.canvas.clear()
            Color(1,1,1,1)
            Rectangle(size = self.im.size, pos = self.im.pos, source = self.path())
         
                
                #Rectangle(pos = (self.pos), size = (self.size), source = ('Mario-PNG-Image.png'))
        return
 
    def drag(self):
        if self.im.collide_point(Window.mouse_pos[0],Window.mouse_pos[1]) and not self.path() == './resources/x.png':
            
            coords = self.coords()
            
            if (self.state == 'freeBtn'):
                line = self.drawLine(coords)
                for i in line:
                    self.addToBorder(i)
            elif self.state == 'rectBtn':
                self.im.canvas.clear()            
                self.initCanvas()
                self.drawRect(coords)
                return
            elif self.state == 'circBtn':
                self.im.canvas.clear()
                self.initCanvas()
                self.drawCirc(coords)
                return
            self.prevPoint = coords
    #**************************END of crop work

 #   def pressed(self):

    def getPosOnImage(self, *args):
        
        if len(args):
    
            if (args[0][0] >= self.im.pos[0]) and (args[0][0] <= self.im.pos[0] + self.im.width) and (args[0][1] >= self.im.pos[1]) and (args[0][1] <= self.im.pos[1] + self.im.height):
                x_ = args[0][0] - math.floor(self.im.pos[0])
                #if (x_ > self.m.size[0]):
                 #   x_  = self.m.size[0] -1 #whyyyy -1??
                if x_ < 0:
                    x_ = 0
                y_ = abs(((args[0][1] - math.floor(self.im.pos[1]) - self.im.size[1])))
                        
                if (y_ > self.m.size[1]):
                    y_ = self.im.size[1] -10 #dude why did you hard code in a -10 here wtf man what is this about >:(
                elif y_ < 0:
                    y_ = 0

                return (int(x_), int(y_))

        if (Window.mouse_pos[0] >= self.im.pos[0]) and (Window.mouse_pos[0] <= self.im.pos[0] + self.im.width) and (Window.mouse_pos[1] >= self.im.pos[1]) and (Window.mouse_pos[1] <= self.im.pos[1] + self.im.height):
            x_ = Window.mouse_pos[0] - math.floor(self.im.pos[0])
            if (x_ > self.m.size[0]):
                x_  = self.m.size[0] -1 #whyyyy -1??
            if x_ < 0:
                x_ = 0
            
            y_ = abs(((Window.mouse_pos[1] - math.floor(self.im.pos[1]) - self.im.size[1])))
                    
            if (y_ > self.m.size[1]):
                y_ = self.im.size[1] -10 #dude why did you hard code in a -10 here wtf man what is this about >:(
            elif y_ < 0:
                y_ = 0

            return (int(x_), int(y_))
    def mousePos(self):
        if not self.path() == './resources/x.png':
            if not self.damnBool:
                self.m = Image.load("A" + str(int(self.imBool)) + ".png", keep_data = True)
                self.damnBool = True
          
                
            try:
                    
                x_,y_ = self.getPosOnImage()
                self.col = self.m.read_pixel(x_, y_)
                if (len(self.col) == 3):
                    self.col.append(1)
                
            except Exception as e:
                print(e)
    
    def removeItem(self, item):
        self.menu.remove_widget(item)
        self.pallette.pop(item.getName(), None)
        #self.menu.clear_widgets()

    def openPop(self):
        if not self.col == [0,0,0,0]:
          
            if not (self.col in self.pallette.values()):
                self.pop.setCol(self.col)
                self.pop.open()
                self.pop.name_.text = ""
                self.pop.setErrorVis([1,0,0,0])
                self.pop.name_.focus = True

    def addItem(self):
        y = self.pop.name_.text
        if not y in self.pallette:
            x = PalletteItem(y, list(self.col))
            x.bind(on_release=lambda x: self.removeItem(x))
            self.pallette[y] = self.col
            self.menu.add_widget(x)
            self.pop.dismiss()
        else:
            self.pop.setErrorVis((1,0,0,1))
            self.pop.errorText.text = "Can't do duplicate names"
    
    def changeSource(self, source):
        #self.initCanvas()
        with self.im.canvas:
            Color(1,1,1,1)
            Rectangle(size = self.im.size, pos = self.im.pos, source = source)
                
    def deleteResource(self):
        if not self.path() == './resources/x.png':
         
            os.remove(self.path())
            
            path = None
            if not self.modifyBool:
                
                path = './temp'
                self.resourceList = os.listdir(path)
                self.resourceList.sort()
            else:
                path = './Pallettes/' + self.pallette['name'] + "/resources "
                self.resourceList = os.listdir(path)
                self.resourceList.sort()
              
            if self.refIndex < len(self.resourceList):
         
                self.initCanvas()
                Clock.schedule_once(lambda x: self.changeSource(path + "/" + self.resourceList[self.refIndex]),0)
                #self.im.source = path + "/" + self.resourceList[self.refIndex]
            elif len(self.resourceList) > 0:
           
                self.refIndex = len(self.resourceList) - 1
                self.initCanvas()
                Clock.schedule_once(lambda x: self.changeSource(path + "/" + self.resourceList[len(self.resourceList)-1]),0)
#                self.im.source = path + "/" + self.resourceList[len(self.resourceList)-1]
                
            else:
                self.initCanvas()
                Clock.schedule_once(lambda x: self.changeSource('./resources/x.png'),0)
                #self.im.source = './resources/x.png'
            self.uploadCount -=1
                
    def save(self):
        if not len(self.pallette) <= 1:
            directory = self.pallette['name']
            path = './Pallettes' + "/" + directory
            if not self.modifyBool:
                os.mkdir(path)
                os.mkdir(path + "/resources ")
            
                sourcePath = './temp'
                targetPath = path + '/resources '
                for i in os.listdir(sourcePath):
                    
                    dest = shutil.move(sourcePath + "/" + i, targetPath)

            palletteFile = open(path + "/pallette.txt", 'w')
            tempString = ""
            for i, (k,v) in enumerate(self.pallette.items()):
                tempString += "{}_{}#".format(k,v)
                
            palletteFile.write(tempString[0:-1])
            palletteFile.close()
            self.menu.clear_widgets()
            self.palletteName = ""
            self.modifyBool = False
    
    def getName(self):
        if not self.modifyBool:
            self.namePop.open()
            self.namePop.txt.focus = True
            self.pallette.clear()
            self.menu.clear_widgets()
            Clock.schedule_once(lambda x: self.changeSource('./resources/x.png'),0)
            #self.im.source = './resources/x.png'

    def upload(self):
        self.show_load()
    
    def show_load(self):
        content = LoadDialog(load= lambda x: self.load(), cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def dismiss_popup(self):
        self._popup.dismiss()

    def deleteImg(self):
        #delete the image
        pass

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
        savePath = None
    def load(self, path, filename):

        path_ = None
        savePath = None
        if self.modifyBool:    
            path_ = './Pallettes/' + self.pallette['name'] + '/resources ' 

        else:
            path_ = './temp'
        try:
    
            img_ = CoreImage(filename[0]).save(path_ + '/' + str(self.uploadCount) + "_" + filename[0].split('/')[-1])
        except:
         
            img_ = CoreImage('./resources/corrupted.png').save(path_ + '/' + str(self.uploadCount) + "_" + filename[0].split('/')[-1])
                
        savePath = path_ + '/' + str(self.uploadCount) + "_" + filename[0].split('/')[-1]
        self.uploadCount +=1
   
        
            
        self.resourceList = os.listdir(path_)
        self.resourceList.sort()
        self.refIndex = len(self.resourceList) -1
        self.initCanvas()
        Clock.schedule_once(lambda x: self.changeSource(savePath),0)
        #self.im.source = savePath
        self.im.reload()
        Clock.schedule_once(lambda x: self.export(), 0)
        Cache.remove('kv.image')
        self.m = Image.remove_from_cache(self.m)
        self.damnBool = False
        self.m = Image.load("A" + str(int(self.imBool)) + ".png", keep_data = True)
        self.dismiss_popup()

    def save_(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.text_input.text)

        self.dismiss_popup()
class SourceImages(Image):
    pass
            
        
            
class ColorDisplay(Widget):
    pass




class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    def isPng(self, directory, filename):
        return '.png' in filename

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

   


Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)
