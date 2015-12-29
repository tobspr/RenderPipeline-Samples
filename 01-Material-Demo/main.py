
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
os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__))))

# Append the current directory to the path
sys.path.insert(0, os.getcwd())


class MainApp(ShowBase):

    """ Main Testing Showbase """

    def __init__(self):

        # Setup window size, title and so on
        load_prc_file_data("", """
        win-size 1920 1080
        window-title Render Pipeline by tobspr 
        icon-filename Data/GUI/icon.ico
        """)

        # ------ Begin of render pipeline code ------

        # Insert the pipeline path to the system path, this is required to be
        # able to import the pipeline classes
        pipeline_path = "../../"
        # pipeline_path = "../../RenderPipeline/"
        sys.path.insert(0, pipeline_path)

        from __init__ import RenderPipeline, SpotLight
        from Code.Util.MovementController import MovementController

        self.render_pipeline = RenderPipeline(self)
        self.render_pipeline.create()

        # [Optional] use the default skybox, you can use your own skybox as well
        self.render_pipeline.create_default_skybox()

        # ------ End of render pipeline code, thats it! ------


        # Set time of day
        self.render_pipeline.get_daytime_mgr().set_time(0.651)

        # Load the scene
        model = loader.loadModel("scene/TestScene.bam")
        model.reparent_to(render)

        # Load some fancy ies profile
        ies_profile = self.render_pipeline.load_ies_profile("Data/IESProfiles/Defined.ies")
        
        # Add some random lights
        sqr = 3
        seed(3)
        for x in range(sqr):
            for y in range(sqr):
                light = SpotLight()
                light.set_direction(0, 0, -1)
                light.set_fov(110)
                light.set_color(Vec3(1, 1, 1.5) * 200.0)
                pos_x, pos_y = (x-sqr//2) * 7.0 + 5.0, (y-sqr//2) * 7.0
                light.set_pos(Vec3(pos_x, pos_y, 7.0))
                light.set_radius(25.0)
                light.set_casts_shadows(True)
                light.set_shadow_map_resolution(1024)
                light.set_ies_profile(ies_profile)
                self.render_pipeline.add_light(light)

        # Init movement controller
        self.controller = MovementController(self)
        self.controller.set_initial_position(Vec3(0, 25, 6), Vec3(0))
        self.controller.setup()
        
MainApp().run()
