"""

Shading Models

This shows the different shading models supported in the pipeline.

"""

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
            window-title Render Pipeline - Shading Models Demo
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

        # Set time of day
        self.render_pipeline.daytime_mgr.time = 0.769

        # Load the scene
        model = loader.loadModel("scene/TestScene.bam")
        model.reparent_to(render)

        self.render_pipeline.prepare_scene(model)

        # Init movement controller
        self.controller = MovementController(self)
        self.controller.set_initial_position(
            Vec3(6.6, -18.8, 4.5), Vec3(4.7, -16.7, 3.4))
        self.controller.setup()

        base.accept("l", self.tour)
        base.accept("r", self.reload_shaders)

    def reload_shaders(self):
        self.render_pipeline.reload_shaders()
        self.render_pipeline.prepare_scene(render)

    def tour(self):
        mopath = (
            (Vec3(3.97601628304, -15.5422525406, 1.73230814934), Vec3(49.2462043762, -11.7619161606, 0.0)),
            (Vec3(4.37102460861, -6.52981519699, 2.84148645401), Vec3(138.54864502, -15.7908058167, 0.0)),
            (Vec3(-5.88968038559, -13.9816446304, 2.44033527374), Vec3(302.348571777, -13.2863616943, 0.0)),
            (Vec3(5.23844909668, -18.1897411346, 4.54698801041), Vec3(402.91229248, -14.7019147873, 0.0)),
            (Vec3(-7.27328443527, -0.466051012278, 3.30696845055), Vec3(607.032165527, -19.6019115448, 0.0)),
            (Vec3(5.33415555954, 1.92750489712, 2.53945565224), Vec3(484.103546143, -11.9796953201, 0.0)),
            (Vec3(-0.283608138561, -6.86583900452, 1.43702816963), Vec3(354.63848877, -4.79302883148, 0.0)),
            (Vec3(-11.7576808929, 7.0855755806, 3.40899515152), Vec3(272.73840332, -12.959692955, 0.0)),
            (Vec3(7.75462722778, 13.220041275, 3.97876667976), Vec3(126.342140198, -19.4930171967, 0.0)),
            (Vec3(-2.10827493668, 4.78230571747, 1.27567899227), Vec3(-40.1353683472, -5.77301359177, 0.0)),
            (Vec3(8.67115211487, 16.9084873199, 3.72598099709), Vec3(89.5658569336, -10.9996757507, 0.0)),
            (Vec3(-8.1254825592, 26.6411190033, 3.21335697174), Vec3(268.092102051, -12.1974525452, 0.0)),
            (Vec3(7.89382314682, 45.8911399841, 4.47727441788), Vec3(498.199554443, -11.3263425827, 0.0)),
            (Vec3(-2.33054184914, 43.8977775574, 1.86498868465), Vec3(551.198242188, 13.6092195511, 0.0)),
            (Vec3(4.80335664749, 36.9664497375, 6.16300296783), Vec3(810.128417969, -10.6730031967, 0.0)),
            (Vec3(45.0654678345, 7.54712438583, 22.2645874023), Vec3(808.238586426, -17.5330123901, 0.0)),
            (Vec3(5.99377584457, -12.3760728836, 4.53536558151), Vec3(806.978820801, -2.39745855331, 0.0)),
            (Vec3(6.05853939056, -1.72227275372, 4.53848743439), Vec3(809.65637207, -2.39745855331, 0.0)),
            (Vec3(4.81568479538, 8.28769683838, 4.48393821716), Vec3(809.65637207, -2.39745855331, 0.0)),
            (Vec3(5.82831144333, 17.5230751038, 4.52401590347), Vec3(809.65637207, -2.39745855331, 0.0)),
            (Vec3(4.09594917297, 26.7909412384, 4.44915866852), Vec3(809.65637207, -2.39745855331, 0.0)),
            (Vec3(4.39108037949, 37.2143096924, 5.16932630539), Vec3(809.65637207, -2.39745855331, 0.0)),
        )
        self.controller.play_motion_path(mopath, 2.3)


MainApp().run()
