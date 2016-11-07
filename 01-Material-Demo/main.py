"""

Material Demo

This demonstrates the various materials the pipeline supports.
It is also a reference scene, for testing BRDF changes.

"""

from __future__ import print_function

import os
import sys
from panda3d.core import Vec3, load_prc_file_data
from direct.showbase.ShowBase import ShowBase

# Change to the current directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Insert the pipeline path to the system path, this is required to be
# able to import the pipeline classes
pipeline_path = "../../"

# Just a special case for my development setup, so I don't accidentally
# commit a wrong path. You can remove this in your own programs.
if not os.path.isfile(os.path.join(pipeline_path, "setup.py")):
    pipeline_path = "../../RenderPipeline/"

sys.path.insert(0, pipeline_path)

# Import the render pipeline class
from rpcore import RenderPipeline

# This is a helper class for better camera movement - see below.
from rpcore.util.movement_controller import MovementController


class Application(ShowBase):
    def __init__(self):
        # Setup window size and title
        load_prc_file_data("", """
            # win-size 1600 900
            window-title Render Pipeline - Material Sample
        """)

        # Construct the render pipeline
        self.render_pipeline = RenderPipeline()
        self.render_pipeline.create(self)
        self.render_pipeline.daytime_mgr.time = "19:17"
        # self.render_pipeline.daytime_mgr.time = "12:00"

        # Load the scene
        model = self.loader.load_model("scene/TestScene.bam")
        model.reparent_to(self.render)

        self.render_pipeline.prepare_scene(model)

        # Enable parallax mapping on the floor
        # self.render_pipeline.set_effect(
        #     model.find("**/FloorPlane"),
        #     "effects/default.yaml", {"parallax_mapping": True}, 100)

        # Initialize movement controller, this is a convenience class
        # to provide an improved camera control compared to Panda3Ds default
        # mouse controller.
        self.controller = MovementController(self)
        self.controller.set_initial_position_hpr(
            Vec3(-17.2912578583, -13.290019989, 6.88211250305),
            Vec3(-39.7285499573, -14.6770210266, 0.0))
        self.controller.setup()

Application().run()
