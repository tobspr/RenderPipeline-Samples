
# Disable the "xxx has no yyy member" error, pylint seems to be unable to detect
# the properties of a nodepath
# pylint: disable=E1101

from __future__ import print_function

import os
import sys
import math
from random import random, randint, seed
from panda3d.core import Vec3, load_prc_file_data, TextureAttrib
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
        win-size 1600 900
        window-title Render Pipeline by tobspr 
        icon-filename Data/GUI/icon.ico
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

        from __init__ import RenderPipeline, SpotLight
        from Code.Util.MovementController import MovementController

        self.render_pipeline = RenderPipeline(self)
        self.render_pipeline.create()

        # [Optional] use the default skybox, you can use your own skybox as well
        self.render_pipeline.create_default_skybox()

        # ------ End of render pipeline code, thats it! ------

        # Load ground plane
        plane = self.loader.loadModel("Data/BuiltinModels/Plane/Plane.bam")
        plane.set_scale(10.0)
        plane.reparent_to(self.render)

        # Load the scene
        model = loader.loadModel("scene/Scene.bam")
        model.reparent_to(render)
        model.set_z(1)

        self.render_pipeline.set_effect(model, "Effects/MaterialBlend4.yaml", {
                "parallax_mapping": False, # Not supported
                "alpha_testing": False,
                "normal_mapping": False, # The effect does its own normal mapping
            })

        # Init movement controller
        self.controller = MovementController(self)
        self.controller.set_initial_position(Vec3(0, 10, 8), Vec3(0, 0, 0))
        self.controller.setup()
        
MainApp().run()
