"""

Material blending sample

This shows how to use the material blend effect which comes with the pipeline,
and supports blending for up to 4 materials.

"""

from __future__ import print_function

import os
import sys
from panda3d.core import Vec3, load_prc_file_data, TextureAttrib
from direct.showbase.ShowBase import ShowBase

# Switch into the current directory
os.chdir(os.path.realpath(os.path.dirname(__file__)))

class Application(ShowBase):

    """ Main Testing Showbase """

    def __init__(self):

        # Setup window size, title and so on
        load_prc_file_data("", """
        win-size 1600 900
        window-title Render Pipeline - Material blending example
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
        self.render_pipeline.daytime_mgr.time = "6:43"

        # Load the scene
        model = loader.loadModel("scene/Scene.bam")
        model.reparent_to(render)

        # Set the material blending effect on the terrain
        terrain = model.find("**/Terrain")
        self.render_pipeline.set_effect(terrain, "effects/material_blend4.yaml", {
                "parallax_mapping": False, # Not supported
                "alpha_testing": False,
                "normal_mapping": False, # The effect does its own normal mapping
            }, 100)

        # Configure the effect
        terrain.set_shader_input("detail_scale_factor", 4.0)

        # Detailmap blending factors.
        # Blending is calculated as  (detailmap + <add>) ^ <pow>
        # The base map has no blending since it is used as a filling material
        # and blending the base map would cause spots with no material at all.
        terrain.set_shader_input("material_0_pow", 10.0)
        terrain.set_shader_input("material_0_add",  0.5)
        terrain.set_shader_input("material_1_pow", 10.0)
        terrain.set_shader_input("material_1_add",  0.5)
        terrain.set_shader_input("material_2_pow", 10.0)
        terrain.set_shader_input("material_2_add",  0.5)

        # Init movement controller
        self.controller = MovementController(self)
        self.controller.set_initial_position(Vec3(-15.2, -9.0, 11.8), Vec3(-12.3, -7.0, 9.7))
        self.controller.setup()

Application().run()
