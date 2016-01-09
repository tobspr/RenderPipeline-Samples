

from panda3d.core import SamplerState
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectButton import DirectButton
from direct.interval.LerpInterval import LerpColorScaleInterval
from direct.interval.MetaInterval import Sequence
from direct.interval.FunctionInterval import Func
from direct.gui.DirectGuiBase import DGG
from sys import exit

class Menu(object):
    def __init__(self,main): 
        self.main=main

        wx = base.win.get_x_size()
        wy = base.win.get_y_size()
        kx = 1920
        ky = 1080
        self.myFrame = DirectFrame(frameColor=(1,1,1,1),
            frameSize=(0, kx,0, ky))

        menu_tex = loader.loadTexture("res/menu.png")
        menu_tex.set_minfilter(SamplerState.FT_nearest)
        menu_tex.set_magfilter(SamplerState.FT_linear)
        self.myFrame["frameTexture"] = menu_tex
        self.myFrame.reparentTo(base.pixel2d)
        self.myFrame.set_pos( (wx-kx) / 2, 0, -(wy+ky) / 2)
        self.myFrame.set_transparency(True)

        self.startButton = DirectButton(
                    text = "",  
                    text_scale=1.0,
                    text_fg=(0.2,0.2,0.2,1),
                    frameTexture="res/start_game.png",
                    frameColor=(1,1,1,1),
                    frameSize=(-64, 64, -20, 20),
                    command=self.main.startGame,
                    relief=DGG.FLAT,
                    rolloverSound=None,
                    clickSound=None,
                    parent=self.myFrame,
                    scale=2.0,
                    pos=(wx/2 + 160, 0, wy/2 + 50)
                    )
        self.startButton.setTransparency(1)

        self.exitButton = DirectButton(
                    text = ("Exit Game"),  
                    pos=(0,0,-.8),
                    text_scale=.1,
                    frameColor=(0,0,0,0),
                    relief=1,
                    frameVisibleScale=(2,3),
                    command=exit,
                    rolloverSound=None,
                    clickSound=None,
                    parent=self.myFrame,
                    )
        self.exitButton.setTransparency(1)
        
        self.resumeButton = DirectButton(
                    text = ("Resume"),  
                    pos=(.0,0,.3),
                    text_scale=.1,
                    frameColor=(0,0,0,0),
                    relief=1,
                    frameVisibleScale=(2,3),
                    command=self.main.resumeGame,
                    rolloverSound=None,
                    clickSound=None,
                    parent=self.myFrame,
                    )
        
        self.resumeButton.setTransparency(1)
        self.resumeButton.hide()
        
        self.selectFrame= DirectFrame( frameColor=(1,1,1,1) , frameSize=(-64, 64, -20, 20) , frameTexture="res/select.png")
        self.selectFrame.setTransparency(1)
        self.selectFrame.reparentTo(self.startButton)
        self.entries = [self.exitButton,self.startButton,self.resumeButton]
        self.activeEntry = 1


    
    
    def clearKeys(self):
        base.ignore("arrow_up")
        base.ignore("arrow_down")
        base.ignore("arrow_left")
        base.ignore("arrow_right")
        base.ignore("escape")
        base.ignore("enter")
    
    def execSelection(self):
        self.entries[self.activeEntry]["command"]()
      
        
    def selectDown(self):
        if self.activeEntry == 0:
            self.activeEntry = len(self.entries)-1
        else:
            self.activeEntry -=1
        
        if self.entries[self.activeEntry].isHidden():
            self.selectDown()
            return   
        self.selectFrame.reparentTo(self.entries[self.activeEntry])
        
    def selectUp(self):

        if self.activeEntry == len(self.entries)-1:
            self.activeEntry=0
        else:
            self.activeEntry +=1
        if self.entries[self.activeEntry].isHidden() :
            self.selectUp()
            return
        self.selectFrame.reparentTo(self.entries[self.activeEntry])

    def hideMenu(self):
        self.clearKeys()
        self.main.gui.show()
        seq= Sequence( LerpColorScaleInterval(self.myFrame, 0.4 ,(1,1,1,0)) , Func(self.myFrame.hide) )
        seq.start()
    
    def hideResume(self):
        seq= Sequence( LerpColorScaleInterval(self.resumeButton, .5 ,(1,1,1,0)) , Func(self.resumeButton.hide))
        seq.start()
     
    def showResume(self):
        self.resumeButton.show()
        #seq= Sequence(  LerpColorScaleInterval(self.resumeButton, 1 ,(1,1,1,1)) )
        #seq.start()
        
    def showMenu(self): 
        self.clearKeys()
        base.accept("arrow_up" , self.selectUp )
        base.accept("arrow_down" , self.selectDown )
        base.accept("escape", exit)
        base.accept("enter",self.execSelection)  
        self.myFrame.show()
        self.main.gui.hide()
        seq= Sequence( LerpColorScaleInterval(self.myFrame, .5 ,(1,1,1,1)) )
        seq.start()
