"""

Lights sample

This sample shows how to setup multiple lights and load them from a .bam file.

"""

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
from direct.interval.IntervalGlobal import Sequence

# Switch into the current directory
os.chdir(os.path.realpath(os.path.dirname(__file__)))

class MainApp(ShowBase):

    """ Main Testing Showbase """

    def __init__(self):

        # Setup window size, title and so on
        load_prc_file_data("", """
        win-size 1600 900
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
        self.render_pipeline = RenderPipeline(self)
        self.render_pipeline.create()

        # This is a helper class for better camera movement - its not really
        # a rendering element, but it included for convenience
        from rpcore.util.movement_controller import MovementController

        # ------ End of render pipeline code, thats it! ------

        # Set time of day
        self.render_pipeline.daytime_mgr.time = 0.32
        self.half_lumens = 160
        # self.half_lumens = 20
        self.lamp_fov = 70
        self.lamp_radius = 10
        # Load the scene
        model = loader.loadModel("scene/Scene.bam")
        model.reparent_to(render)

        # Animate balls, this is for testing the motion blur
        blend_type = "noBlend"

        np = model.find("**/MBRotate")
        np.hprInterval(1.5, Vec3(360, 360, 0), Vec3(0, 0, 0), blendType=blend_type).loop()

        np = model.find("**/MBUpDown")
        np_pos = np.get_pos() - Vec3(0, 0, 2)
        Sequence(
            np.posInterval(0.15, np_pos + Vec3(0, 0, 6), np_pos, blendType=blend_type),
            np.posInterval(0.15, np_pos, np_pos + Vec3(0, 0, 6), blendType=blend_type)).loop()

        np = model.find("**/MBFrontBack")
        np_pos = np.get_pos() - Vec3(0, 0, 2)
        Sequence(
            np.posInterval(0.15, np_pos + Vec3(0, 6, 0), np_pos, blendType=blend_type),
            np.posInterval(0.15, np_pos, np_pos + Vec3(0, 6, 0), blendType=blend_type)).loop()

        np = model.find("**/MBScale")
        Sequence(
            np.scaleInterval(0.2, Vec3(1.5), Vec3(1), blendType=blend_type),
            np.scaleInterval(0.2, Vec3(1), Vec3(1.5), blendType=blend_type)).loop()

        # Generate temperature lamps
        self._lights = []
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
            light.casts_shadows = False
            light.shadow_map_resolution = 256
            self.render_pipeline.add_light(light)

            # Put Pandas on the edges
            if lumlamp in lumlamps[0:2] + lumlamps[-2:]:
                panda = loader.loadModel("panda")
                panda.reparent_to(render)
                panda_mat = Material("default")
                panda_mat.emission = 0
                panda.set_material(panda_mat)
                panda.set_pos(light.pos)
                panda.set_z(0.65)
                panda.set_h(180 + randint(-60, 60))
                panda.set_scale(0.2)
                panda.set_y(panda.get_y() - 3.0)

            self._lights.append(light)

        self.render_pipeline.prepare_scene(model)

        # Init movement controller
        self.controller = MovementController(self)
        self.controller.set_initial_position(Vec3(3, 25, 8), Vec3(5, 0, 0))
        self.controller.setup()

        self.day_time = 0.3
        self.time_direction = 0

        # Keys to modify the time, disabled in the demo
        self.accept("k", self.reset)
        self.accept("p", self.set_time_direction, [1,])
        self.accept("p-up", self.set_time_direction, [0,])
        self.accept("i", self.set_time_direction, [-1,])
        self.accept("i-up", self.set_time_direction, [0,])

        self.addTask(self.update, "update")

    def reset(self):
        self.day_time = 0.209

    def set_time_direction(self, direction):
        self.time_direction = direction

    def update(self, task):
        """ Update method """
        frame_time = globalClock.get_frame_time()
        # Make the lights glow
        for i, light in enumerate(self._lights):
            brightness = math.sin(0.4 * i + frame_time * 4.0)
            light.lumens = max(0, self.half_lumens / 2 + brightness * self.half_lumens)

        # Time control, disabled in the demo
        # self.day_time += globalClock.get_dt() / 40.0 * self.time_direction
        # self.render_pipeline.daytime_mgr.time = self.day_time

        return task.cont

MainApp().run()
