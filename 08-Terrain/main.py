"""

Terrain Demo

Shows how to use the shader terrain mesh in the pipeline

"""

from __future__ import print_function

import os
import sys
from panda3d.core import Vec3, load_prc_file_data, ShaderTerrainMesh
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

from rpcore import RenderPipeline

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
            notify-level-linmath error
        """)

        self.render_pipeline = RenderPipeline()
        self.render_pipeline.create(self)

        # Set time of day
        self.render_pipeline.daytime_mgr.time = "04:25"

        # Add some environment probe to provide better reflections
        probe = self.render_pipeline.add_environment_probe()
        probe.set_pos(0, 0, 600)
        probe.set_scale(8192 * 2, 8192 * 2, 1000)

        self.terrain_np = render.attach_new_node("terrain")

        heightfield = loader.loadTexture("resources/heightfield.png")

        for x in range(3):
            for y in range(3):
                terrain_node = ShaderTerrainMesh()
                terrain_node.heightfield = heightfield
                terrain_node.target_triangle_width = 6.0
                terrain_node.generate()

                terrain_n = self.terrain_np.attach_new_node(terrain_node)
                terrain_n.set_scale(8192, 8192, 600)
                terrain_n.set_pos(-4096 + (x - 1) * 8192, -4096 + (y - 1) * 8192, 0)

        # Init movement controller
        self.controller = MovementController(self)
        self.controller.set_initial_position(Vec3(-12568, -11736, 697), Vec3(-12328, -11357, 679))
        self.controller.setup()

        self.accept("r", self.reload_shaders)
        self.reload_shaders()

    def reload_shaders(self):
        self.render_pipeline.reload_shaders()

        # Set the terrain effect
        self.render_pipeline.set_effect(self.terrain_np, "effects/terrain-effect.yaml", {}, 100)
        base.accept("l", self.tour)


    def tour(self):
        control_points = (
            (Vec3(2755.62084961, 6983.76708984, 506.219055176), Vec3(-179.09147644, 4.30751991272, 0.0)),
            (Vec3(3153.70068359, 5865.30859375, 560.780822754), Vec3(-225.239028931, 3.43641376495, 0.0)),
            (Vec3(2140.57080078, 5625.22753906, 598.345031738), Vec3(-196.022613525, 1.91196918488, 0.0)),
            (Vec3(2598.85961914, 3820.56958008, 627.692993164), Vec3(-272.410125732, 3.32752752304, 0.0)),
            (Vec3(1894.64526367, 3597.39257812, 647.455078125), Vec3(-198.227630615, 0.605303645134, 0.0)),
            (Vec3(1998.48425293, 1870.05358887, 639.38458252), Vec3(-121.682502747, 0.169744253159, 0.0)),
            (Vec3(3910.55297852, 2370.70922852, 518.356567383), Vec3(-130.42376709, 3.65418696404, -0.000583928485867)),
            (Vec3(4830.80761719, 1542.30749512, 501.019073486), Vec3(21.7212314606, 8.00974178314, 0.0)),
            (Vec3(4324.81982422, 2259.2409668, 713.095458984), Vec3(-19.1500263214, -1.68137300014, 0.0)),
            (Vec3(4584.38720703, 3417.75073242, 612.79510498), Vec3(-39.4675331116, -4.94804239273, 0.0)),
            (Vec3(4569.68261719, 4840.80908203, 540.924926758), Vec3(-83.4887771606, 4.08973407745, 0.0)),
            (Vec3(5061.6484375, 5490.93896484, 694.142578125), Vec3(-135.778717041, 0.605291008949, 0.0)),
            (Vec3(6273.03222656, 6343.10546875, 769.735290527), Vec3(-200.826278687, -1.35470712185, 0.0)),
            (Vec3(7355.02832031, 6314.39892578, 1164.65527344), Vec3(-262.645324707, -12.2435855865, 0.0)),
            (Vec3(6321.42431641, 4453.68310547, 898.895202637), Vec3(-322.574157715, -2.22581481934, 0.0)),
            (Vec3(4820.63916016, 4637.07128906, 793.165222168), Vec3(-330.291748047, 0.931967377663, 0.0)),
            (Vec3(2621.3125, 4790.99072266, 691.223144531), Vec3(-423.059020996, 3.10974740982, 0.0)),
            (Vec3(2166.64697266, 5683.75195312, 685.415039062), Vec3(-497.871612549, -1.57248008251, 0.0)),
            (Vec3(2426.64135742, 7216.48974609, 993.247558594), Vec3(-524.17388916, -6.69025611877, 0.0)),
            (Vec3(5014.83398438, 6712.60253906, 963.192810059), Vec3(-596.072387695, -3.31469583511, 0.00446693599224)),
            (Vec3(6107.69970703, 5460.03662109, 820.63104248), Vec3(-650.567199707, 1.04085958004, 0.0)),
        )
        self.controller.play_motion_path(control_points, 3.0)

Application().run()
