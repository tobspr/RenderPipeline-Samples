
# Disable the "xxx has no yyy member" error, pylint seems to be unable to detect
# the properties of a nodepath
# pylint: disable=E1101

from __future__ import print_function

import os
import sys
import math
from random import random, randint, seed
from panda3d.core import Vec3, load_prc_file_data
from direct.showbase.ShowBase import ShowBase

# Change to the current directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

class MainApp(ShowBase):
    def __init__(self):

        # Setup window size, title and so on
        load_prc_file_data("", """
            win-size 1600 900
            window-title Render Pipeline by tobspr
        """)

        # ------ Begin of render pipeline code ------

        # Insert the pipeline path to the system path, this is required to be
        # able to import the pipeline classes
        pipeline_path = "../../"

        # Just a special case for my development setup, so I don't accidentally
        # commit a wrong path. You can remove this in your own programs.
        if not os.path.isfile(os.path.join(pipeline_path, "setup.py")):
            pipeline_path = "../../RenderPipeline/"

        sys.path.insert(0, pipeline_path)

        from rpcore import RenderPipeline, SpotLight
        self.render_pipeline = RenderPipeline()
        self.render_pipeline.create(self)

        # This is a helper class for better camera movement - its not really
        # a rendering element, but it included for convenience
        from rpcore.util.movement_controller import MovementController

        # ------ End of render pipeline code, thats it! ------

        self.render_pipeline.daytime_mgr.time = 0.741

        # Load the scene
        model = loader.loadModel("scene/scene.bam")
        model.reparent_to(render)
        self.render_pipeline.prepare_scene(model)

        # Init movement controller
        self.controller = MovementController(self)
        self.controller.set_initial_position_hpr(Vec3(-4.8, 3.0, 1.0), Vec3(-127, -2.73, 0.0))
        self.controller.setup()


        base.accept("l", self.tour)

    def tour(self):
        """ Camera flythrough """
        # Motion path
        mopath = (
            (Vec3(4.03593730927, -0.544453799725, 5.40879201889), Vec3(990.020019531, -359.266845703, 0.0)),
            (Vec3(-0.542494595051, 4.81144475937, 2.80708742142), Vec3(947.809753418, -366.671142578, 0.0)),
            (Vec3(-6.29322004318, 2.77208423615, 1.3867855072), Vec3(964.741027832, -364.711120605, 0.0)),
            (Vec3(-2.4391644001, -5.62284660339, 1.32748699188), Vec3(1068.98181152, -366.344421387, 0.0)),
            (Vec3(5.65527534485, -1.16699492931, 1.44794154167), Vec3(1157.26049805, -368.086608887, 0.0)),
            (Vec3(-0.768297970295, 4.01399374008, 0.671069025993), Vec3(1273.73156738, -362.968933105, 0.0)),
            (Vec3(-3.23558425903, -0.0152323488146, 0.966191887856), Vec3(1352.24536133, -392.586700439, 0.0)),
            (Vec3(-1.55705070496, -2.53522276878, 0.555241346359), Vec3(1439.42150879, -363.295593262, 0.0)),
            (Vec3(0.116861321032, -0.427198320627, 1.08965158463), Vec3(1529.90490723, -375.055419922, 0.0)),
            (Vec3(0.065696850419, 1.65449047089, 1.21597766876), Vec3(1554.16015625, -373.095397949, 0.0)),
            (Vec3(0.0405929833651, 7.30522537231, 3.1753692627), Vec3(1576.20959473, -373.204223633, 0.0)),
            (Vec3(0.0514025650918, 7.97706985474, 3.62691926956), Vec3(1419.8125, -356.870941162, 0.0)),
            (Vec3(6.54702425003, 7.94502496719, 4.90251398087), Vec3(1295.93884277, -358.722045898, 0.0)),
            (Vec3(8.56750679016, -3.25144028664, 5.43005466461), Vec3(1255.38256836, -359.593139648, 0.0)),
            (Vec3(-2.68423557281, -8.50214195251, 3.08925223351), Vec3(1124.81530762, -377.124053955, 0.0)),
            (Vec3(-6.76232194901, 4.90780639648, 1.14179193974), Vec3(943.61138916, -361.87991333, 0.0)),
            (Vec3(-3.35591650009, -1.53063929081, 0.866183340549), Vec3(1025.6697998, -368.63092041, 0.0)),
            (Vec3(-3.45307064056, 1.96282124519, 0.866183340549), Vec3(945.344787598, -365.799865723, 0.0)),
            (Vec3(3.68962097168, 2.42984819412, 1.91770780087), Vec3(850.21484375, -383.875366211, 0.0)),
            (Vec3(2.15808415413, -3.19981098175, 2.81170415878), Vec3(739.886047363, -391.388549805, 0.0)),
            (Vec3(-4.64695215225, -0.159373953938, 0.814572036266), Vec3(631.841064453, -362.750976562, 0.0)),
            (Vec3(2.87521338463, 7.16097259521, 3.4908516407), Vec3(515.605957031, -377.450958252, 0.0)),
            (Vec3(8.59916305542, 0.0813773721457, 3.7681016922), Vec3(452.291168213, -379.846466064, 0.0)),
            (Vec3(5.76941871643, -1.32986474037, 5.50954580307), Vec3(631.920043945, -361.226593018, 0.0)),
            (Vec3(3.67592144012, -0.432737737894, 5.55842065811), Vec3(629.557556152, -360.573272705, 0.0)),
        )
        self.controller.play_motion_path(mopath, 2.3)

MainApp().run()
