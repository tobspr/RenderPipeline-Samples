
# Disable the "xxx has no yyy member" error, pylint seems to be unable to detect
# the properties of a nodepath
# pylint: disable=E1101

from __future__ import print_function

import os
import sys
import math
from random import random, randint, seed
from panda3d.core import Vec3, load_prc_file_data, Material
from direct.showbase.ShowBase import ShowBase

# Switch into the current directory
os.chdir(os.path.realpath(os.path.dirname(__file__)))


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

        from render_pipeline_importer import RenderPipeline, SpotLight
        from code.util.movement_controller import MovementController

        self.render_pipeline = RenderPipeline(self)
        self.render_pipeline.create()

        # [Optional] use the default skybox, you can use your own skybox as well
        self.render_pipeline.create_default_skybox()

        # ------ End of render pipeline code, thats it! ------

        # Set time of day
        self.render_pipeline.daytime_mgr.time = 0.66

        # Light needs to be less-than-overpowering at night but bright at day
        is_day = 0.3 < self.render_pipeline.daytime_mgr.time < 0.63
        self.half_lumens = is_day and 250 or 20
        self.lamp_fov = is_day and 70 or 45
        self.lamp_radius = is_day and 10 or 7.5

        # Load the scene
        model = loader.loadModel("scene/Scene.bam")
        model.reparent_to(render)

        self._lights = []

        # Temperature lamps
        light_key = lambda light: int(light.get_name().split("LampLum")[-1])
        lumlamps = sorted(model.find_all_matches("**/LampLum*"), key=light_key)
        for lumlamp in lumlamps:
            lum = float(lumlamp.get_name()[len("LampLum"):])
            light = SpotLight()
            light.direction = (0, -1.5, -1)
            light.fov = self.lamp_fov
            light.set_color_from_temperature(lum * 1000.0)
            light.lumens = self.half_lumens
            light.pos = lumlamp.get_pos(self.render)
            light.radius = self.lamp_radius
            light.casts_shadows = True
            light.shadow_map_resolution = 512
            self.render_pipeline.add_light(light)

            # Put Pandas on the edges
            if lumlamp in lumlamps[0:2] + lumlamps[-2:]:
                panda = loader.loadModel("panda")
                panda.reparent_to(render)
                panda.set_material(Material("default"))
                panda.set_pos(light.pos)
                panda.set_z(0.65)
                panda.set_h(180 + randint(-60, 60))
                panda.set_scale(0.2)
                panda.set_y(panda.get_y() - 3.0)

            self._lights.append(light)

        # Init movement controller
        self.controller = MovementController(self)
        self.controller.set_initial_position(Vec3(3, 25, 8), Vec3(5, 0, 0))
        self.controller.setup()

        self.addTask(self.update, "update")

    def update(self, task):
        """ Update method """
        frame_time = globalClock.get_frame_time()
        # Make the lights glow
        for i, light in enumerate(self._lights):
            brightness = math.sin(0.4 * i + frame_time * 4.0)
            light.lumens = self.half_lumens / 2 + brightness * self.half_lumens

        return task.cont

MainApp().run()
