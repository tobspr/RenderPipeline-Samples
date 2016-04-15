"""

Terrain Demo

Shows how to use the shader terrain mesh in the pipeline

"""

from __future__ import print_function

import os
import sys
from panda3d.core import Vec3, load_prc_file_data, ShaderTerrainMesh, Shader
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
            stm-max-chunk-count 2048
            gl-coordinate-system default
            stm-max-views 20
        """)

        self.render_pipeline = RenderPipeline()
        self.render_pipeline.create(self)

        # Set time of day
        self.render_pipeline.daytime_mgr.time = 0.76

        # Add some environment probe to provide better reflections
        # probe = self.render_pipeline.add_environment_probe()
        # probe.set_pos(0, 0, 5)
        # probe.set_scale(25, 25, 12)
         
        self.terrain_node = ShaderTerrainMesh()
        self.terrain_node.heightfield_filename = "resources/heightfield.png"
        self.terrain_node.target_triangle_width = 10.0
        self.terrain_node.generate()
         
        self.terrain_np = render.attach_new_node(self.terrain_node)
        self.terrain_np.set_scale(8192, 8192, 1000)

        # Init movement controller
        self.controller = MovementController(self)
        self.controller.set_initial_position(Vec3(0, 0, 1100), Vec3(100, 100, 1000))
        self.controller.setup()

        self.accept("r", self.reload_shaders)
        self.reload_shaders()

    def reload_shaders(self):
        self.render_pipeline.reload_shaders()

        # Set the terrain effect
        self.render_pipeline.set_effect(self.terrain_np, "effects/terrain-effect.yaml", {}, 100)


Application().run()
