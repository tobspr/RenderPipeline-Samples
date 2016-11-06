
import os
import sys


from direct.showbase.ShowBase import ShowBase
from panda3d.core import load_prc_file_data

from .Cube import Cube
from .Menu import Menu
from .LevelLoader import Level
from .CamControl import CamControl
from .GUI import GUI

class GameControl(ShowBase):
    """
    controlling the game itself, menu, editors level selection... it's sorta a fake-fsm.
    did i mention i dont like fsm's and prefer totaly whicked logic instead?
    """
    def __init__(self):

        load_prc_file_data("", "textures-power-2 none")
        load_prc_file_data("", "win-size 1600 900")
        # load_prc_file_data("", "fullscreen #t")
        load_prc_file_data("", "window-title cuboid")
        load_prc_file_data("", "icon-filename res/icon.ico")

        # I found openal works better for me
        load_prc_file_data("", "audio-library-name p3openal_audio")

         # ------ Begin of render pipeline code ------

        # Insert the pipeline path to the system path, this is required to be
        # able to import the pipeline classes
        pipeline_path = "../../"

        # Just a special case for my development setup, so I don't accidentally
        # commit a wrong path. You can remove this in your own programs.
        if not os.path.isfile(os.path.join(pipeline_path, "setup.py")):
            pipeline_path = "../../RenderPipeline/"

        sys.path.insert(0, pipeline_path)

        # Use the utility script to import the render pipeline classes
        from rpcore import RenderPipeline

        self.render_pipeline = RenderPipeline()
        # self.render_pipeline.mount_mgr.mount()
        # self.render_pipeline.load_settings("/$$rpconfig/pipeline.yaml")
        # self.render_pipeline.settings["pipeline.display_debugger"] = False
        # self.render_pipeline.set_empty_loading_screen()
        self.render_pipeline.create(self)

        # [Optional] use the default skybox, you can use your own skybox as well
        # self.render_pipeline.create_default_skybox()

        # ------ End of render pipeline code, thats it! ------


        # Set time of day
        self.render_pipeline.daytime_mgr.time = 0.812

        self.menu = Menu(self)
        self.level = Level(self)
        self.cube = Cube(self.level)
        self.camControl = CamControl(self.cube)
        self.gui = GUI(self)
        self.menu.showMenu()
        base.accept("i",self.camControl.zoomIn)
        base.accept("o",self.camControl.zoomOut)

    def startGame(self,level=0):
        #debug purpose only: to directly play a certian lvl number
        from sys import argv
        if len(argv) >1:
            level = int(argv[1])

        self.menu.hideMenu()
        self.level.loadLevel(level)
        self.cube.resetCube()
        self.cube.resetStats()
        self.cube.enableGameControl()
        base.accept("escape", self.pauseGame)

    def pauseGame(self):
        self.cube.disableGameControl()
        self.menu.showMenu()
        self.menu.showResume()
        #base.accept("escape", self.resumeGame )

    def resumeGame(self):
        self.menu.hideMenu()
        self.menu.hideResume()
        self.cube.enableGameControl()
        base.accept("escape", self.pauseGame)

    def levelEnd(self):
        self.cube.disableGameControl()
        self.menu.showMenu()

