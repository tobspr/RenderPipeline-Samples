
from direct.interval.LerpInterval import LerpPosInterval, LerpHprInterval, LerpScaleInterval
from direct.interval.LerpInterval import LerpPosHprInterval,LerpColorScaleInterval, LerpFunc
from direct.interval.MetaInterval import Sequence,Parallel
from direct.interval.FunctionInterval import Func,Wait

from direct.task.Task import Task
from panda3d.core import Vec3

from functools import partial
from random import random
from .CheckMove import *
from .Sound import *

class Cube:
    def __init__(self,level):
        self.level = level
        self.sounds = Sounds()
        self.cube = loader.loadModel("./models/Cuboid.bam")
        self.cube.setPythonTag("TilePos", [0,0,None,None] ) #tells us which 2 tiles the block is one, x1,y1,x2,y2. 
                                                            #x2 and y2 are NONE if it's standing upright
        self.cube.setPythonTag("Animated", False) # i so dont want to pass around global parameters
        self.cube.reparentTo(render)

        self.moves = 0
        self.falls = 0
        self.shard_node = render.attach_new_node("shards")
    
    def resetStats(self):
        self.moves = 0
        self.falls = 0
        
    def enableGameControl(self):
        """
        assigns the keyboard-events to the block's movement
        """
        base.accept("arrow_up",     self.rotateCube,   [  "up"     ])
        base.accept("arrow_down",   self.rotateCube,   [ "down"    ])
        base.accept("arrow_left",   self.rotateCube,   [ "left"    ])
        base.accept("arrow_right",  self.rotateCube,   [ "right"   ])
    
    def disableGameControl(self):
        """
        clears the keyboard-events so the keys can be used to navigate the menu or other stuff.
        """
        base.ignore("arrow_up")
        base.ignore("arrow_down")
        base.ignore("arrow_left")
        base.ignore("arrow_right")
    
    def setPos(self, x1,y1=None ):
        """
        sets the block to the position you desire.
        you can either throw in 2 integers which make the tile positions. or you pass a tuple/list with at least 2 items.
        in both cases the it is x y coordinates. the block will be roated into a standing position if it isn't already.
        """
        if type(x1) == list or type(x1) == tuple:
            y1=x1[1]
            x1=x1[0]
        if self.getCubeTiles()[3]:
            self.cube.setHpr(render,0,0,0)
        
        self.cube.setPos(render,x1,y1,1)
        self.setCubeTiles(x1,y1)            
    
    def getCube(self):
        """
        returns the cube's node path.
        """
        return self.cube

    def getCubeTiles(self):
        """
        internal convenience functions. returns a list with [x1,y1,x2,y2]
        """
        return self.cube.getPythonTag("TilePos")

    def setCubeTiles(self,x1,y1,x2=None,y2=None):
        """
        internal convenience-function which sets the tile coordinates for the tiles the block is on. inputs are x1,y1,x2,y2 . x2 and y2 are optional.
        """
        self.cube.setPythonTag("TilePos", [x1,y1,x2,y2] )

    def isAnimated(self):
        """
        returns True if the block is currently playing an animation.. DONT TOUCH IT while it is animated or it will turn into evil-rotation cube.
        """
        return self.cube.getPythonTag("Animated")

    def setAnimated(self,param):
        """
        internal function: sets and clears the "isAnimated" tag
        """
        self.cube.setPythonTag("Animated", param)

    def fadeInCube(self,duration = 2.5):
        """
        helper function. simply moves the block from above onto the map. using the duration specified as parameter.
        if no parameter is supplied, it will assume the default-time of 1.2 seconds or so.
        """
        self.setAnimated(True)
        x1,y1,x2,y2 = self.cube.getPythonTag("TilePos")
        #animate the cube, once finished clear the animation tag
        self.cube.setZ(render,15)
        self.cube.wrtReparentTo(render)

        print("Starting fade in sequence")
        Sequence( LerpPosInterval(self.cube, duration ,(x1, y1,1), blendType="easeOut"  ) , 
            Func(self.setAnimated,False), 
            Func(lambda:self.level.stopAnimatedTile(x1,y1) ) ).start()
        
    def animate(self,myInterval):
        """
        internal function which accepts an interval as input, plays it. and automatically resets the "animated" tag once it finished.
        you have to check yourself if the tag is set before playing the animation. use isAnimated() for that.
        """
        #print  "animating cube"
        seq = Sequence( myInterval , Func(self.setAnimated,False) )
        #seq.start()
        return seq
    
    def resetCube(self,task=None):
        """
        resets the cube to the statring position, including the fly-in-from-above animation.
        """
        print("Resetting cube")
        x,y,z = self.level.getPosFromTile(self.level.getStartTile())
        self.setPos(x,y)
        self.cube.setHpr(render,0,0,0)
        #self.level.stopAnimatedTile(x,y )
        print("Fading in cube")
        self.fadeInCube()
    
    def levelUp(self, task=None):
        """
        calls the levelClass to load the next level and resets the cube.
        """
        if self.level.loadLevel() == 0: #if level loaded successfully...
            self.resetCube()
        
        self.level.main.gui.set_stage(self.level.LevelNr + 1)

    def rotateCube(self,direction):
        """
        rotates the cube according to the direction passed as first argument. accepted values are "up" "down" "left" "right"
        """
        #first check if we are allowed to move the block at all..
        if self.isAnimated() : 
            print("canceling rotation of cube")
            return
            
        #cleaning up from last rotation (we cant clean those up at the end of this function cause the interval needs the dummynode for rotation)
        self.cube.wrtReparentTo(render)
        try:
            dummy.remove_node()
        except:
            pass

        self.setAnimated(True)
        duration = 0.2
        x1,y1,x2,y2 = self.getCubeTiles()
        
        self.level.animateTile(x1,y1)
        self.level.animateTile(x2,y2)
        
        dummy = render.attachNewNode("dummy")
        dummy.reparentTo(self.cube)
        dummy.setZ(render,0)
        dummy.wrtReparentTo(render)
        dummy.setHpr(0,0,0)
        dest_hpr = Vec3(0)
            
        if self.cube.getZ(render) > .7:
            #case1 : cube is standing upright
            #ok... since we rotate relative there are rounding errors... since there !might! be some uebernoob playing the game
            #needing one gazillion rotations to reach the goal it might happen those rounding errors actually get visible
            #so let him enjoy and reset the cube every-time it's standing straight-up.
            
            self.cube.setZ(render,1) #how comes this is one?.. well.. i know.. because of my learnings..
            self.cube.setX(render, round(self.cube.getX(render),0)  )
            self.cube.setY(render, round(self.cube.getY(render),0)  )
            self.cube.setH(render, round(self.cube.getH(render),0)  )
            self.cube.setP(render, round(self.cube.getP(render),0)  )
            self.cube.setR(render, round(self.cube.getR(render),0)  )


            if direction == "right":
                dummy.setY(dummy,.5)
                self.cube.wrtReparentTo(dummy) 
                dest_hpr = Vec3(0, -90, 0)
                self.setCubeTiles( x1, y1+1 ,x1 , y1+2 )
                
            if direction == "left":
                dummy.setY(dummy,-.5)
                self.cube.wrtReparentTo(dummy)
                dest_hpr = Vec3(0, 90, 0)
                self.setCubeTiles( x1, y1-2 ,x1 , y1-1 )
               
            if direction == "up":
                dummy.setX(dummy,-.5)
                self.cube.wrtReparentTo(dummy) 
                dest_hpr = Vec3(0, 0, -90)
                self.setCubeTiles( x1-2, y1 ,x1-1 , y1 )
                            
            if direction == "down":
                dummy.setX(dummy,.5)
                self.cube.wrtReparentTo(dummy) 
                dest_hpr = Vec3(0, 0, 90)
                self.setCubeTiles( x1+1, y1 ,x1+2 , y1 )          
            
        elif x1 == x2 :  #if aligned to y-axis
            if direction == "right":
                dummy.setY(dummy,1)
                self.cube.wrtReparentTo(dummy)
                dest_hpr = Vec3(0, -90, 0)
                self.setCubeTiles( x1, y1+2  )

            if direction == "left":
                dummy.setY(dummy,-1)
                self.cube.wrtReparentTo(dummy) 
                dest_hpr = Vec3(0, 90, 0)
                self.setCubeTiles( x1, y1-1)

            if direction == "up":
                dummy.setX(dummy,-.5)
                self.cube.wrtReparentTo(dummy) 
                dest_hpr = Vec3(0, 0, -90)
                self.setCubeTiles( x1-1, y1, x2-1, y2 )
                
            if direction == "down":
                dummy.setX(dummy,.5)
                self.cube.wrtReparentTo(dummy) 
                dest_hpr = Vec3(0, 0, 90)
                self.setCubeTiles( x1+1, y1, x2+1, y2 )


        elif y1==y2 : #if it is alligned to x-axis..

            if direction == "right":
                dummy.setY(dummy,.5)
                self.cube.wrtReparentTo(dummy)
                dest_hpr = Vec3(0, -90, 0)
                self.setCubeTiles( x1, y1+1, x2, y2+1 )
                
            if direction == "left":
                dummy.setY(dummy,-.5)
                self.cube.wrtReparentTo(dummy) 
                dest_hpr = Vec3(0, 90, 0)
                self.setCubeTiles( x1, y1-1, x2, y2-1 )
            
            if direction == "up":
                dummy.setX(dummy,-1)
                self.cube.wrtReparentTo(dummy) 
                dest_hpr = Vec3(0, 0, -90)
                self.setCubeTiles( x1-1, y1  )
                
            if direction == "down":
                dummy.setX(dummy,1)
                self.cube.wrtReparentTo(dummy) 
                dest_hpr = Vec3(0, 0, 90)
                self.setCubeTiles( x1+2, y1  )

        else:
            print("Invalid move. Waiting ..")


        print("Rotating!")
        anim = self.animate( LerpHprInterval(dummy, duration, dest_hpr,(0,0,0) ) )

        
        #this sorta.. doesnt belong here.. but i dunno where to put it yet.
        x1,y1,x2,y2 = self.getCubeTiles()
        # self.level.tintTile(x1,y1) #this is fun to play with if your cube is invisible...
        # self.level.tintTile(x2,y2)
        self.level.stopAnimatedTile(x1,y1) #stops the tile-animation for the tiles below the block
        self.level.stopAnimatedTile(x2,y2)
        
        #cheking what consequences your move had... muhahaa... if you get a 1 .. i've got bad news for you
        checkresult = checkMove(self.level.levelNode,self.getCubeTiles(),self.sounds)
        if checkresult == 1:
            self.falls +=1
            self.moves +=1

            # Force to the corner when the cuboid falls down
            side_force = 1.7

            force = Vec3(0, 0, 0)
            if direction == "up":
                force = Vec3(-side_force, 0, 0)
            elif direction == "down":
                force = Vec3(side_force, 0, 0)
            elif direction == "left":
                force = Vec3(0, -side_force, 0)
            elif direction == "right":
                force = Vec3(0, side_force, 0)

            dummy.set_hpr(render, Vec3(0, 0, 0))

            del anim

            self.setAnimated(True)
            final_hpr = dest_hpr * 3.0 + Vec3(random(), random(), random()) * 360.0 * 0.0
            anim = LerpFunc(self.animateCube, fromData=0, toData=1, duration=1.3, blendType='noBlend', extraArgs=[dummy.get_pos(render), Vec3(0), final_hpr, dummy, force])
            taskMgr.doMethodLater( anim.getDuration(), self.resetCube , "resetTask")

        elif checkresult == 2:

            #ok.. once reached the goal, move the block down, fading it out. thenload the new level etc.
            anim.pop()
            anim.append( Func(lambda: self.level.fadeOutLevel() ) )

            Sequence(Wait(0.3), Func(lambda *args: self.cube.hide())).start()

            taskMgr.doMethodLater( anim.getDuration()+2 , self.levelUp , "lvlup")
            taskMgr.doMethodLater( anim.getDuration()+2 , lambda *args: self.cube.show(), "show cube")
            taskMgr.doMethodLater( anim.getDuration()+2 , lambda *args: self.shard_node.node().remove_all_children(), "clear shards")
            
            Sequence(Wait(0.2), Func(lambda *args: self.sounds.playSound("finish.wav"))).start()

            self.moves = 0
            self.falls = 0

            cube_min, cube_max = Vec3(-0.5, -0.5, -1), Vec3(0.5, 0.5, 1)
            self.shard_node.set_pos(dummy.get_pos(render) + Vec3(-0.5, 0, 0))
            shard_size = (cube_max - cube_min) / 5.0

            self.shard_node.hide()
            Sequence(Wait(0.22), Func(lambda *args: self.shard_node.show())).start()

            for i in range(5):
                for j in range(5):
                    for k in range(5):
                        shard = loader.loadModel("models/CubeShard.bam")
                        shard.reparent_to(self.shard_node)
                        shard.set_x(i * shard_size.x + 0.1)
                        shard.set_y(j * shard_size.y + 0.1)
                        shard.set_z(k * shard_size.z + 0.2)
                        shard.set_scale(0.8 + random())

                        force = Vec3(i-2 - 0.15, j-2 - 0.15, k-2 + 2.6)
                        force.normalize()
                        force *= 12.0 * (1 + random() * 0.5)

                        d_hpr = Vec3(random(), random(), random()) * 360.0 * (3.0 + random())

                        shard_anim = Sequence(
                            Wait(0.22),
                            LerpFunc(self.animateShard, fromData=0, toData=2, duration=2.0, blendType='noBlend', extraArgs=[shard.get_pos(), d_hpr, shard, force]),
                            LerpHprInterval(shard, 1.0 + random(), d_hpr * 1.6, d_hpr, blendType='noBlend'),
                        )
                        shard_anim.start()

        elif checkresult == 0:
            #how lame... just a ..move..
            print("playing sound")
            self.moves += 1
            self.sounds.playSound("stonerotate.wav")
        print("moves:",self.moves ,"  falls:",self.falls)
        #last but not least.. we start the animation .. did you know that the pc knows you'r failing before you actually do? .. scary..
        anim.start()

    def animateShard(self, t, initial_pos, dest_hpr, shard, force):
        
        z_force = -(t**2) * 9.81 * 1.7
        regular_force = force * t

        dest_pos = initial_pos + regular_force + Vec3(0, 0, z_force)

        shard.set_pos(dest_pos)
        shard.set_hpr(dest_hpr * t)

    def animateCube(self, t, initial_pos, initial_hpr, dest_hpr, cube, force):
        z_force = -(t**2) * 9.81 * 1.7
        regular_force = force * t
        dest_pos = initial_pos + regular_force + Vec3(0, 0, z_force)
        cube.set_pos(render, dest_pos)
        cube.set_hpr(render, initial_hpr * (1 - t) + dest_hpr * t)
        # cube.set_hpr(render, initial_hpr)
