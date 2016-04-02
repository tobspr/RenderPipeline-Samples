
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
            # win-size 1920 1080
            # win-size 2560 1440
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

        self.render_pipeline.daytime_mgr.time = 0.324

        # Load the scene
        model = loader.loadModel("scene/scene.bam")
        model.reparent_to(render)
        self.render_pipeline.prepare_scene(model)

        # Init movement controller
        self.controller = MovementController(self)
        self.controller.set_initial_position_hpr(Vec3(-10.6577367783, 7.90177536011, 1.27759826183), Vec3(-124.781364441, -0.544444441795, 0.0))
        self.controller.setup()

        base.accept("l", self.tour)

    def tour(self):
        """ Camera flythrough """
        # Motion path
        mopath = (
            (Vec3(-10.6577367783, 7.90177536011, 1.27759826183), Vec3(-124.781364441, -0.544444441795, 0.0)),
            (Vec3(-7.65479278564, 0.0209505427629, 1.05313777924), Vec3(-89.737663269, -0.27222442627, 1.34704433107e-15)),
            (Vec3(-3.99910902977, -7.02601861954, 1.71959364414), Vec3(-22.4064388275, -4.083340168, 4.93751155212e-17)),
            (Vec3(6.26898050308, -3.36650061607, 2.03177428246), Vec3(60.2154464722, -9.25556755066, -6.9021957889e-31)),
            (Vec3(5.37619447708, 3.81517601013, 2.33564043045), Vec3(127.874809265, -14.1555652618, -1.15121531646e-16)),
            (Vec3(-4.69762516022, 4.4881401062, 1.52477109432), Vec3(224.277877808, -6.26112127304, -1.65300641197e-27)),
            (Vec3(-5.3909740448, -0.0537432208657, 1.51055192947), Vec3(271.265258789, -10.9796419144, 9.87861237988e-15)),
            (Vec3(-6.39123868942, -3.96498560905, 2.85282707214), Vec3(302.896453857, -17.2407493591, 2.80525623493e-24)),
            (Vec3(6.05632543564, -5.66745996475, 4.01503515244), Vec3(403.171386719, -21.3240966797, -3.6682122493e-18)),
            (Vec3(5.87886714935, 5.13238430023, 2.82238030434), Vec3(494.586883545, -15.5166826248, 3.56255043715e-23)),
            (Vec3(-5.31576871872, 6.54800033569, 3.08319950104), Vec3(574.452575684, -14.9722414017, 4.96358130717e-17)),
            (Vec3(-10.4141635895, 0.0291149001569, 1.03256857395), Vec3(630.496704102, 0.0907283425331, 1.39374427294e-19)),
            (Vec3(-8.28491401672, -7.7529001236, 4.71980524063), Vec3(673.612609863, -19.8722362518, 4.73844675336e-19)),
            (Vec3(7.3855805397, -2.54302930832, 7.36575078964), Vec3(791.671875, -42.3759384155, 1.51329226927e-11)),
            (Vec3(3.1763086319, 6.56667995453, 5.32609605789), Vec3(875.737365723, -32.8482055664, -2.51912936729e-28)),
            (Vec3(-6.92491197586, 4.5765786171, 5.74722957611), Vec3(952.255859375, -32.9389877319, -3.6138474062e-19)),
            (Vec3(-11.1667308807, 6.47304964066, 1.58364403248), Vec3(957.637084961, -2.0871360302, -3.48538045745e-27)),
            (Vec3(-10.5598182678, -6.87400054932, 1.66387891769), Vec3(1027.59313965, -2.72232580185, -2.79300474621e-14)),
            (Vec3(7.59017276764, -8.01403331757, 1.76548790932), Vec3(1122.74951172, -3.72047281265, -4.64680637718e-12)),
            (Vec3(7.71055221558, 9.09056854248, 1.69482588768), Vec3(1222.1060791, -3.53899049759, 1.99654495986e-15)),
            (Vec3(-10.6483020782, 8.15358829498, 1.33072710037), Vec3(1310.0435791, -2.35936117172, 1.85199434049e-15)),
            (Vec3(-10.6483020782, 8.15358829498, 1.33072710037), Vec3(1310.0435791, -2.35936117172, -1.8811227633e-23)),
            (Vec3(-10.6483020782, 8.15358829498, 1.33072710037), Vec3(1310.0435791, -2.35936117172, -6.01001974479e-30)),
        )
        self.controller.play_motion_path(mopath, 3.0)

MainApp().run()
