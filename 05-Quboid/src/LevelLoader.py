
"""
i dont really know how to save maps in a best possible way. but i guess i'll just store the same informationas in the tags in clear-text.
<"Type"="tile","Pos"="12_2">
pos is the X_Y coordinate. Type can be lots of different types. "tile" would be the standard tile,
"weakTile" is one that only carries half the cuboid. "fragile" could be one that breaks after using it once
"switch" which triggers events... stuff like that. can be extended quite esily.

other tags are "Start" and "Goal" 
further tags could be "ID" which could come in handy when using switches.
notice the naming. tag names start capital, the values lowercase.

"""
from panda3d.core import NodePath, Vec3
from direct.showbase.Loader import Loader
from direct.interval.LerpInterval import LerpPosQuatInterval,LerpPosInterval, LerpHprInterval ,LerpPosHprInterval ,LerpColorScaleInterval
from direct.interval.LerpInterval import LerpFunc
from direct.interval.FunctionInterval import Func,Wait
from direct.interval.MetaInterval import Sequence
from random import random
from panda3d.core import AmbientLight,DirectionalLight
from panda3d.core import RigidBodyCombiner
from .Sound import *
from .LevelGenerator import LevelGenerator
from panda3d.core import OmniBoundingVolume

class Level:
    def __init__(self,main):
        self.main = main
        self.sounds = Sounds()
        self.loadBackground()
        self.levelGen = LevelGenerator()
        print("initializing levelnode")
        self.LevelNr = 0
        
    def loadBackground(self,background="./models/surrounding/Scene.bam"):
        base.setBackgroundColor(1,1,1)
        self.background = loader.loadModel(background)
        self.background.reparentTo(render)
        self.background.setZ(-10)
        self.background.setScale(.3)
        self.background.setH(-90)

    def loadLevel(self, levelnr=None):
        """
        will load the level with the nr. if no number is specified it will load lastlevelnumber+1.. or tries to do so.
        if it fails it will either generate a new level or return to the menue (havent decided yet)
        """
        if levelnr == None:
            self.LevelNr +=1
        else:
            self.LevelNr = levelnr
        print("trying to load level nr:",self.LevelNr)
        #handle unloading of the map here.
        try: 
            tiles = self.levelNode.findAllMatches("=Pos")
        except:
            tiles = []
            print("no tiles for removal found")
        for tile in tiles:
            x,y,z = self.getPosFromTile(tile)
            self.stopAnimatedTile(x,y)
            tile.remove_node()
        
        try:
            self.levelNode.remove_node()
        except:
            print("failed to remove old level node.. maybe there was none?")
        
        print("loading level....")
        
        try:
            data=open("./levels/level_"+str(self.LevelNr)).read()
        except:
            print("sorry, failed to load mapfile level"+str(self.LevelNr))
            
            #data = self.levelGen.generateLevel()
            #print ".... level generator should kick in here.. but it's not yet ready.."   
            self.main.levelEnd()  
            return 1
            
            #data=open("./levels/level_"+str(self.LevelNr-1)).read()
                #if self.newMap == None:
                #    self.createNewLevel(level)
                #data=open("./levels/level_temp").read()
                #return
                
            
           
        self.levelNode = self.loadLevelData( data )
        print(self.levelNode, "returning levelNode")
        self.levelNode.reparentTo(render)        
        self.fadeInLevel()
        return 0
        #return self.levelNode
                 
            #startPos = self.LevelNode.find("=Type=start").getTag("Pos")
            #startPos = startPos.split("_")
    
    def animateTile(self,x,y):
        """
        the floating animation of tiles.
        """
        Time = 2
        tile = self.getTileFromPos(x,y)
        if tile:
             if tile.getPythonTag("Seq").isPlaying() ==False:
                seq = Sequence( 
                        LerpPosInterval( tile, Time+(0.2*Time*random()),(x,y,.35),(x,y,0)  , blendType="easeInOut") ,  
                        LerpPosInterval( tile, Time+(0.2*Time*random()),(x,y, 0),(x,y,.35) , blendType="easeInOut")  )
                tile.setPythonTag("Seq", seq )
                seq.loop()  
                
                
    def stopAnimatedTile(self,x,y,now=None):
        tile = self.getTileFromPos(x,y)
        if tile:
            if tile.hasPythonTag("Seq") and now == None:
                sequence = tile.getPythonTag("Seq")
                sequence.pause()
                sequence = Sequence( Wait(.1), LerpPosQuatInterval(tile,.1,(x,y,0),(0,0,0),blendType='easeIn') )
                sequence.start()
                tile.setPythonTag("Seq",sequence)
            elif tile.hasPythonTag("Seq") and now != None:      
                sequence = tile.getPythonTag("Seq")
                sequence.pause()
                
    def animateTiles(self,task=None):
        """
        calls animateTile on all tiles. note the plural in the name
        """        
        tiles = self.levelNode.findAllMatches("=Pos")
        for tile in tiles:
            x,y,z = self.getPosFromTile(tile)
            self.animateTile(x,y)
            
      
    def loadTile(self,data):
        data = data.split(",")
        tile = None
        for i in data:
            #check for the type and load tile
            if i.startswith("Type="):
                i = i.split("=")
                tile = loader.loadModel("./models/"+i[1]+".bam")
                tile.setTag(i[0],i[1])
                break
                
        for i in data:
            if i.startswith("Pos=") and tile != None:
                i = i.split("=")
                tile.setTag(i[0], i[1])
                break
         
        if tile:
            if tile.hasTag("Pos") and tile.hasTag("Type"):
                return tile
            else:
                return None 
        else:
          return None


    def loadLevelData(self,inputData):
        """
        processes the level asloaded from the file. it seperates the input data until the data for each tile is ready.
        each tile data will be passed to loadTile().
        it returns a rigidNode optimized nodepath.
        """
        rigidNode = RigidBodyCombiner("LevelNode")
        levelNode = NodePath(rigidNode)
        #rigidNode.reparentTo(levelNode)
        #this looks heavy but all it does is deleting whitespaces and seperating the content for each tile into a list.
        inputData = inputData.replace("\n","").strip().replace(" ","").lstrip("<").rstrip(">").split("><")
        
        for tileData in inputData:
            tile = self.loadTile(tileData)
            if tile != None:
                tile.reparentTo(levelNode)
                tile.setPos( self.getPosFromTile(tile) )
                tile.setZ(tile,0.00000001) #workaround for rigid body combiner so it does not assume the (0,0) tile as static
            else:
                print("ERROR, could not load tile with data: ",tileData)
        rigidNode.collect()
        inode = rigidNode.getInternalScene().node() #workaround for a boundingvolume issue with rigidbodycombiner
        inode.setBounds(OmniBoundingVolume())  #still workaround
        inode.setFinal(True) #still workaround
        #levelNode.analyze()  
        return levelNode 
    
    def getTileFromPos(self,x,y):
        """
        returns the nodePath of a tile with the given tile number
        """
        if type(x) == list or type(x) == tuple:
            y=x[1]
            x=x[0]
        tile = self.levelNode.find("=Pos="+str(x)+"_"+str(y))
        if tile.isEmpty():
            return None
        else:
            return tile
    
    def getPosFromTile(self,tile):
        """
        returns the tile position given a tile's nodePath, or None if the nodepath has no position tags
        """
        if tile.hasTag("Pos"):
            pos = tile.getTag("Pos").split("_")
            x,y = int(pos[0]) , int(pos[1])
            return (x,y,0)
        else:
            print("ERROR, supplied tile has no 'Pos' tag")
            return None

    def getStartTile(self):
        tile = self.levelNode.find("=Type=start")
        if tile.isEmpty() == True:
            print("Start-Tile was not found.. I'm prediction an application crash within the next 50ms...")
            print("oh.. and feel free to add propper exception handling here so we get back to some menue or so, instead of crashin")
        return tile
    
    
    def fadeOutLevel(self,fadeTime=1):
        """
        the level-falls-apart animation.
        """
        tiles = self.levelNode.findAllMatches("=Pos")
        for tile in tiles:
            x,y,z = self.getPosFromTile(tile)
            self.stopAnimatedTile(x,y,True)
            tile.setPos(x,y,0)
            #tile.setHpr(random()*360,random()*360,random()*360)
            # seq = LerpPosHprInterval(tile,fadeTime+(0.3*fadeTime*random()),(x,y,-15),(random()*360 -180,random()*360-180,random()*360-180), blendType='easeIn')
            # seq.start()

            final_hpr = Vec3(random(), random(), random()) * 360.0
            force = (Vec3(random(), random(), random())-0.5) * 5.0
            force.z = 0
            seq = LerpFunc(self.tileGravityAnimation, fromData=0, toData=1, duration=1.0, blendType='noBlend', extraArgs=[tile.get_pos(render), Vec3(0), final_hpr, tile, force])
            tile.setPythonTag("Seq", seq)
            seq.start()


    def tileGravityAnimation(self, t, initial_pos, initial_hpr, dest_hpr, tile, force):
        """
        Animates a tile by applying gravity
        """
        z_force = -(t**2) * 9.81 * 1.7
        regular_force = force * t
        dest_pos = initial_pos + regular_force + Vec3(0, 0, z_force)
        tile.set_pos(render, dest_pos)
        tile.set_hpr(render, initial_hpr * (1 - t) + dest_hpr * t)
       
    def fadeInLevel(self, fadeTime = 1.6):
        """
        fade-in animation. the parameter it takes is the time in seconds.changing it might cause animation glitches with the cube-fade-in animation
        """
        self.sounds.playSound("nyon.wav")
        tiles = self.levelNode.findAllMatches("=Pos")
        for tile in tiles:
            
            x,y,z = self.getPosFromTile(tile)
            tile.setPos(x,y,-15)
            tile.setHpr(random()*360-180,random()*360-180,random()*360-180)
            seq =  LerpPosQuatInterval(tile,fadeTime+(0.3*fadeTime*random()),(x,y,0),(0,0,0),blendType='easeOut') 
            tile.setPythonTag("Seq", seq )
            seq.start()  
        Sequence(Wait(fadeTime*1.4), Func(lambda:self.animateTiles())).start() 
    
    def tintTile(self,x,y):
        """
        the 'i was so bored and was looking for something colorful' function. feel free to enable it in the Cube.py file
        """
        if x != None and y != None:
            tile=self.getTileFromPos(x,y)
            
            #tile.setColorScale(0,0,0,1)
            if tile != None:
                if tile.hasPythonTag("Colorlerp"):
                    tile.getPythonTag("Colorlerp").pause()
                seq = Sequence(
                    Wait(.1),
                    LerpColorScaleInterval(tile,.1,(random(),random(),random(),1) ), 
                    LerpColorScaleInterval(tile,10,(1,1,1,1) ) )
                tile.setPythonTag("Colorlerp",seq)
                seq.start()
