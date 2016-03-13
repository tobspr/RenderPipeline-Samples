
from direct.task.Task import Task
from direct.interval.LerpInterval import LerpFunc

class CamControl:
    """
    All it does is taking the cubeclass-instance as input. And the camera will
    haunt the cube till all eternitiy.
    """
    def __init__(self,cube):
        base.disableMouse()
        self.cube=cube
        self.ZOOMLEVEL = .37
        base.camera.setX(25*self.ZOOMLEVEL)
        base.camera.setY(5*self.ZOOMLEVEL)
        taskMgr.add(self.cameraMovement,"CameraTask")

    def setZoom(self,zoomlevel):
        self.ZOOMLEVEL = zoomlevel

    def zoomIn(self):
        i = LerpFunc(self.setZoom, fromData = self.ZOOMLEVEL, toData = self.ZOOMLEVEL*0.7, duration = 1.0,blendType = "easeInOut")
        i.start()

    def zoomOut(self):
        i = LerpFunc(self.setZoom, fromData = self.ZOOMLEVEL, toData = self.ZOOMLEVEL*1.3, duration = 1.0,blendType = "easeInOut")
        i.start()

    def cameraMovement(self,task):
        x,y,z = self.cube.getCube().getPos(render)
        #smoothly follow the cube...
        base.camera.setX( base.camera.getX() - ((base.camera.getX()-x-18*self.ZOOMLEVEL)*.5*globalClock.getDt() ) )
        base.camera.setY( base.camera.getY() - ((base.camera.getY()-y+5*self.ZOOMLEVEL )*.5*globalClock.getDt() ) )
        base.camera.setZ(15*self.ZOOMLEVEL)
        base.camera.setHpr(75,-37,0)
        return Task.cont
