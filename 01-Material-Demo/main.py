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

from rpcore import RenderPipeline, SpotLight

# This is a helper class for better camera movement - its not really
# a rendering element, but it included for convenience
from rpcore.util.movement_controller import MovementController

class Application(ShowBase):
    def __init__(self):

        # Setup window size, title and so on
        load_prc_file_data("", """
            win-size 1600 900
            window-title Render Pipeline by tobspr
        """)

        self.render_pipeline = RenderPipeline()
        self.render_pipeline.create(self)

        # Set time of day
        self.render_pipeline.daytime_mgr.time = 0.76

        # Load the scene
        model = loader.load_model("scene/TestScene.bam", callback=self.continue_init)

    def continue_init(self, model):
        """ Gets called when the async loading finished """
        model.reparent_to(render)

        # Enable parallax mapping on the floor
        self.render_pipeline.set_effect(model.find("**/FloorPlane"),
            "effects/default.yaml", {"parallax_mapping": True}, 100)

        # Add some environment probe to provide better reflections
        probe = self.render_pipeline.add_environment_probe()
        probe.set_pos(0, 0, 5)
        probe.set_scale(25, 25, 12)

        # Add some random lights
        num_lights = 2

        # Load some ies profile
        ies_profile = self.render_pipeline.load_ies_profile("defined.ies")
        for x in range(num_lights):
            for y in range(num_lights):
                light = SpotLight()
                light.direction = (0, 0, -1)
                light.fov = 110.0
                light.color = (1, 1, 1.5)
                light.lumens = 3.0
                pos_x, pos_y = (x-num_lights//2) * 7.0 + 5.0, (y-num_lights//2) * 7.0 + 5.0
                light.pos = (pos_x, pos_y, 12.0)
                light.radius = 35.0
                light.casts_shadows = True
                light.near_plane = 0.1
                light.shadow_map_resolution = 512
                light.ies_profile = ies_profile
                self.render_pipeline.add_light(light)

        # Init movement controller
        self.controller = MovementController(self)
        self.controller.set_initial_position(Vec3(16.9, -13.4, 5.7), Vec3(9.6, -2.5, 4.6))
        self.controller.setup()

Application().run()
