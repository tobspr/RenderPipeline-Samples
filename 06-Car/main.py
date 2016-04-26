
# Disable the "xxx has no yyy member" error, pylint seems to be unable to detect
# the properties of a nodepath
# pylint: disable=no-member

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
            window-title Render Pipeline - Car Demo
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

        self.render_pipeline.daytime_mgr.time = "20:08"

        # Load the scene
        model = loader.loadModel("scene/scene.bam")
        # model = loader.loadModel("scene2/Scene.bam")

        model.reparent_to(render)
        self.render_pipeline.prepare_scene(model)

        # Init movement controller
        self.controller = MovementController(self)
        self.controller.set_initial_position(
            Vec3(-7.5, -5.3, 1.8), Vec3(-5.9, -4.0, 1.6))
        self.controller.setup()

        base.accept("l", self.tour)

    def tour(self):
        """ Camera flythrough """
        mopath = (
            (Vec3(-10.8645000458, 9.76458263397, 2.13306283951), Vec3(-133.556228638, -4.23447799683, 0.0)),
            (Vec3(-10.6538448334, -5.98406457901, 1.68028640747), Vec3(-59.3999938965, -3.32706642151, 0.0)),
            (Vec3(9.58458328247, -5.63625621796, 2.63269257545), Vec3(58.7906494141, -9.40668964386, 0.0)),
            (Vec3(6.8135137558, 11.0153560638, 2.25509500504), Vec3(148.762527466, -6.41223621368, 0.0)),
            (Vec3(-9.07093334198, 3.65908527374, 1.42396306992), Vec3(245.362503052, -3.59927511215, 0.0)),
            (Vec3(-8.75390911102, -3.82727789879, 0.990055501461), Vec3(296.090484619, -0.604830980301, 0.0)),
        )
        self.controller.play_motion_path(mopath, 3.0)

MainApp().run()
