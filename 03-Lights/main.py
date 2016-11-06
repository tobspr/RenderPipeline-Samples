"""

Lights sample

This sample shows how to setup multiple lights and load them from a .bam file.

"""

# Disable the "xxx has no yyy member" error, pylint seems to be unable to detect
# the properties of a nodepath
# pylint: disable=no-member

from __future__ import print_function

import os
import sys
import math
from random import randint
from panda3d.core import Vec3, load_prc_file_data, Material
from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import Sequence

# Switch into the current directory
os.chdir(os.path.realpath(os.path.dirname(__file__)))


class MainApp(ShowBase):

    def __init__(self):
        # Setup window size and title
        load_prc_file_data("", """
        win-size 900 600
        window-title Render Pipeline - Lights demo
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

        # Import the movement controller, this is a convenience class
        # to provide an improved camera control compared to Panda3Ds default
        # mouse controller.
        from rpcore.util.movement_controller import MovementController

        # ------ End of render pipeline code, thats it! ------

        # Set time of day
        self.render_pipeline.daytime_mgr.time = "5:20"

        # Configuration variables
        self.half_energy = 5000
        self.lamp_fov = 70
        self.lamp_radius = 10

        # Load the scene
        model = self.loader.load_model("scene/Scene.bam")
        model.reparent_to(self.render)

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
        # This shows how to procedurally create lamps. In this case, we
        # base the lights positions on empties created in blender.
        self._lights = []
        light_key = lambda light: int(light.get_name().split("LampLum")[-1])
        lumlamps = sorted(model.find_all_matches("**/LampLum*"), key=light_key)
        for lumlamp in lumlamps:
            lum = float(lumlamp.get_name()[len("LampLum"):])
            light = SpotLight()
            light.direction = (0, -1.5, -1)
            light.fov = self.lamp_fov
            light.set_color_from_temperature(lum * 1000.0)
            light.energy = self.half_energy
            light.pos = lumlamp.get_pos(self.render)
            light.radius = self.lamp_radius
            light.casts_shadows = False
            light.shadow_map_resolution = 256
            self.render_pipeline.add_light(light)

            # Put Pandas on the edges
            if lumlamp in lumlamps[0:2] + lumlamps[-2:]:
                panda = self.loader.load_model("panda")
                panda.reparent_to(self.render)
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
        self.controller.set_initial_position(Vec3(23.9, 42.5, 13.4), Vec3(23.8, 33.4, 10.8))
        self.controller.setup()

        self.addTask(self.update, "update")

    def update(self, task):
        """ Update method """
        frame_time = self.taskMgr.globalClock.get_frame_time()

        # Make the lights glow
        for i, light in enumerate(self._lights):
            brightness = math.sin(0.4 * i + frame_time)
            light.energy = max(0, self.half_energy / 2.0 + brightness * self.half_energy)
        return task.cont

MainApp().run()
