"""

Benchmark

This is a benchmark to test the power of the GPU

"""

from __future__ import print_function, division

import os
import sys
import math
from random import random, randint, seed
from panda3d.core import Vec3, load_prc_file_data, Material, PNMImage
from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import Sequence

# Switch into the current directory
os.chdir(os.path.realpath(os.path.dirname(__file__)))

class MainApp(ShowBase):

    """ Main Testing Showbase """

    def __init__(self):

        # Setup window size, title and so on
        load_prc_file_data("", """
        win-size 1600 900
        window-title Render Pipeline - Benchmark
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
        self.render_pipeline.daytime_mgr.time = "17:41"

        model = loader.load_model("scene/Scene.bam")
        model.reparent_to(render)

        model.flatten_strong()

        num_rows = 32

        img = PNMImage("scene/lights.png")

        for x in range(num_rows):
            for y in range(num_rows):
                light = SpotLight()
                light.direction = (0, 0, -1)
                light.fov = 70
                # light.set_color_from_temperature(randint(2000, 20000))
                light.color = img.get_xel(x, y)
                light.energy = 35000
                light.pos = Vec3( -(x - num_rows//2) / num_rows * 300.0, (y - num_rows // 2) / num_rows * 300.0, 10)
                light.radius = 30
                light.casts_shadows = False
                light.shadow_map_resolution = 256
                self.render_pipeline.add_light(light)

        self.render_pipeline.prepare_scene(model)

        # Init movement controller
        self.controller = MovementController(self)
        self.controller.set_initial_position(Vec3(0, 450, 200), Vec3(0))
        self.controller.setup()

MainApp().run()
