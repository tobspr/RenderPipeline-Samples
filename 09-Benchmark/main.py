"""

Benchmark

This is a benchmark to test the power of the GPU

"""

from __future__ import print_function, division

import os
import sys
from panda3d.core import Vec3, load_prc_file_data, PNMImage
from direct.showbase.ShowBase import ShowBase

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

        from rpcore import RenderPipeline, PointLight
        self.render_pipeline = RenderPipeline()
        self.render_pipeline.create(self)

        # This is a helper class for better camera movement - its not really
        # a rendering element, but it included for convenience
        from rpcore.util.movement_controller import MovementController

        # ------ End of render pipeline code, thats it! ------

        # Set time of day
        self.render_pipeline.daytime_mgr.time = "17:41"

        self.camLens.set_fov(90)

        model = self.loader.load_model("scene/Scene.bam")
        model.reparent_to(self.render)

        model.flatten_strong()
        num_rows = 255

        img = PNMImage("scene/lights.png")

        for x in range(num_rows):
            for y in range(num_rows):
                light = PointLight()
                # light.direction = (0, 0, -1)
                # light.fov = 60
                # light.set_color_from_temperature(randint(2000, 20000))
                light.color = img.get_xel(x * 1, y * 1)
                light.energy = 5000 * (x / num_rows)
                light.pos = Vec3(-(x - num_rows // 2) / num_rows * 1000.0,
                                 (y - num_rows // 2) / num_rows * 1000.0, 2)
                light.radius = 4
                light.inner_radius = 0.5
                light.casts_shadows = False
                light.shadow_map_resolution = 256
                self.render_pipeline.add_light(light)

        self.render_pipeline.prepare_scene(model)

        # Init movement controller
        self.controller = MovementController(self)
        self.controller.set_initial_position(Vec3(0, 450, 200), Vec3(0))
        self.controller.setup()

        self.accept("l", self.benchmark)

    def benchmark(self):
        mopath = (
            (Vec3(0.0, 450.0, 200.0), Vec3(180.0, -23.9624938965, 0.0)),
            (Vec3(-190.848297119, 304.510772705, 90.5852050781), Vec3(209.767547607, -19.2802791595, 0.0)),
            (Vec3(-220.74269104, 10.6886262894, 38.7188148499), Vec3(278.595062256, -16.6669464111, -0.00123210949823)),
            (Vec3(-51.2080802917, -188.072463989, 50.2380104065), Vec3(364.747375488, -22.7647132874, 0.0)),
            (Vec3(211.633651733, -190.621276855, 216.169631958), Vec3(413.887451172, -40.1869468689, -0.000118153897347)),
            (Vec3(320.780090332, 303.404388428, 341.834014893), Vec3(495.000030518, -41.1669464111, 0.00174981483724)),
            (Vec3(125.150436401, 294.57989502, 218.834960938), Vec3(444.363800049, 3.80416536331, 0.0)),
            (Vec3(-355.501434326, 153.010559082, 68.0701370239), Vec3(611.234924316, -11.5491724014, 0.000359044410288)),
            (Vec3(-118.283355713, -115.640907288, 6.09887886047), Vec3(637.222473145, -8.82695007324, 0.0)),
            (Vec3(80.3096160889, 12.4637413025, 26.0630741119), Vec3(676.439758301, -24.3980617523, 0.0)),
            (Vec3(69.6195449829, 152.581176758, 14.8633785248), Vec3(881.898925781, -15.3602952957, 0.0)),
            (Vec3(-202.29776001, 109.818962097, 94.7222290039), Vec3(962.381530762, -27.7736206055, 0.00155594921671)),
            (Vec3(6.89826059341, -412.195037842, 221.591659546), Vec3(1080.42749023, -31.1491756439, 0.0)),
            (Vec3(362.657867432, -34.1290054321, 216.362884521), Vec3(1166.81677246, -35.0691833496, 0.0)),
            (Vec3(-0.339450836182, 452.040649414, 199.996627808), Vec3(180.0, -23.9624938965, 0.0)),
        )
        self.controller.play_motion_path(mopath, 3.0)

MainApp().run()
