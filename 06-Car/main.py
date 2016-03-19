
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
        self.controller.set_initial_position(Vec3(-5.2, -3, 1.1), Vec3(-3.5, -1.9, 1))
        self.controller.setup()


        base.accept("l", self.tour)

    def tour(self):
        """ Camera flythrough """
        # Motion path
        mopath = (
            (Vec3(4.87385797501, -0.344362914562, 5.48901510239), Vec3(628.874206543, -360.463439941, 0.0)),
            (Vec3(1.94719266891, 4.74504137039, 4.58151960373), Vec3(598.71282959, -361.878875732, 0.0)),
            (Vec3(-5.09015512466, 4.54550695419, 1.78752219677), Vec3(582.647644043, -365.798980713, 0.0)),
            (Vec3(-4.63440513611, -3.16596984863, 1.23839533329), Vec3(676.438964844, -366.016815186, 0.0)),
            (Vec3(2.48204016685, -4.05034923553, 0.648750066757), Vec3(754.165039062, -360.463592529, 0.0)),
            (Vec3(5.50842237473, 0.551185131073, 0.674605846405), Vec3(823.701416016, -362.423553467, 0.0)),
            (Vec3(0.640096724033, 4.76887559891, 1.36511325836), Vec3(893.788513184, -370.15447998, 0.0)),
            (Vec3(-4.85577774048, 2.92668414116, 1.66516792774), Vec3(950.724609375, -369.827819824, 0.0)),
            (Vec3(-3.50057959557, -1.54266178608, 1.3928374052), Vec3(1016.95355225, -369.501159668, 0.0)),
            (Vec3(6.04318237305, -1.61691939831, 3.41901898384), Vec3(1145.07922363, -380.389984131, 0.0)),
            (Vec3(3.70201969147, 6.61854076385, 4.2167596817), Vec3(1224.85327148, -378.974456787, 0.0)),
            (Vec3(1.37404370308, 8.29449462891, 5.3452501297), Vec3(1101.37268066, -357.197052002, 0.0)),
            (Vec3(5.87119197845, 9.08309459686, 5.25775766373), Vec3(968.127563477, -361.770324707, 0.0)),
            (Vec3(9.4000005722, -0.404727876186, 5.39594841003), Vec3(909.065124512, -361.661437988, 0.0)),
            (Vec3(8.2475271225, -7.25727844238, 5.25985813141), Vec3(805.115112305, -363.948059082, 0.0)),
            (Vec3(-3.06145167351, -8.31771564484, 2.68373322487), Vec3(768.574951172, -374.4012146, 0.0)),
            (Vec3(-9.58887481689, -0.730532109737, 1.76665329933), Vec3(640.606018066, -371.461273193, 0.0)),
            (Vec3(-2.96112918854, 1.59384298325, 0.857840240002), Vec3(587.292236328, -367.650115967, 0.0)),
            (Vec3(-2.96423792839, -1.67848885059, 1.00815808773), Vec3(673.129394531, -368.085754395, 0.0)),
            (Vec3(3.27399706841, -1.87560737133, 1.16455745697), Vec3(775.110717773, -367.105773926, 0.0)),
            (Vec3(3.19386529922, 2.00226211548, 1.16455745697), Vec3(854.726989746, -366.561340332, 0.0)),
            (Vec3(-1.50769126415, 2.34753108025, 0.566493868828), Vec3(897.252197266, -364.274749756, 0.0)),
            (Vec3(-3.38453054428, 0.0659308135509, 0.666721403599), Vec3(987.342102051, -367.4324646, 0.0)),
            (Vec3(-1.98923003674, 0.011309992522, 1.49845373631), Vec3(989.074523926, -394.872375488, 0.0)),
            (Vec3(0.0700719207525, -0.00889463722706, 1.77660727501), Vec3(988.601745605, -336.943603516, 0.0)),
            (Vec3(6.88837194443, -0.452337414026, 5.67470312119), Vec3(989.153198242, -359.701019287, 0.0)),
            (Vec3(3.92235994339, -0.507873833179, 5.65524291992), Vec3(989.704406738, -359.156585693, 0.0)),
        )
        self.controller.play_motion_path(mopath)

MainApp().run()
