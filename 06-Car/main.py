
# Disable the "xxx has no yyy member" error, pylint seems to be unable to detect
# the properties of a nodepath
# pylint: disable=E1101

from __future__ import print_function

import os
import sys
import math
from random import random, randint, seed
from panda3d.core import Vec3, load_prc_file_data
from direct.showbase.ShowBase import ShowBase

# Change to the current directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

class MainApp(ShowBase):
    def __init__(self):

        # Setup window size, title and so on
        load_prc_file_data("", """
            # win-size 1600 900
            # win-size 1920 1080
            win-size 2560 1440
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
        self.render_pipeline = RenderPipeline()
        self.render_pipeline.create(self)

        # This is a helper class for better camera movement - its not really
        # a rendering element, but it included for convenience
        from rpcore.util.movement_controller import MovementController

        # ------ End of render pipeline code, thats it! ------

        self.render_pipeline.daytime_mgr.time = 0.324

        # Load the scene
        model = loader.loadModel("scene/scene.bam")
        model.reparent_to(render)
        self.render_pipeline.prepare_scene(model)

        # Init movement controller
        self.controller = MovementController(self)
        self.controller.set_initial_position_hpr(Vec3(-9.67578792572, 7.44844293594, 1.32429432869), Vec3(-129.460510254, -0.0907380580902, 1.26570870531e-23))
        self.controller.setup()

        base.accept("l", self.tour)

    def tour(self):
        """ Camera flythrough """
        # Motion path
        mopath = (
            (Vec3(-9.67578792572, 7.44844293594, 1.32429432869), Vec3(-129.460510254, -0.0907380580902, 1.26570870531e-23)),
            (Vec3(5.6103014946, -0.101410590112, 5.6585893631), Vec3(-91.660446167, 0.181481957436, -3.11729687131e-24)),
            (Vec3(4.81058073044, -1.74531757832, 5.65214681625), Vec3(-79.1260299683, -0.272225618362, -1.74441508592e-19)),
            (Vec3(5.13469314575, 3.74600219727, 0.61830919981), Vec3(53.0427322388, -1.1796361208, -2.8006086609e-24)),
            (Vec3(-0.0783951580524, 3.54442477226, 0.828930497169), Vec3(49.7614631653, -5.60283660889e-06, 1.50736378563e-17)),
            (Vec3(-8.73009872437, 5.83314418793, 0.622094392776), Vec3(230.689590454, 2.08703565598, 4.24384004772e-14)),
            (Vec3(-4.61631393433, -2.05521035194, 1.45067763329), Vec3(220.189590454, -7.34999418259, 1.40663542825e-14)),
            (Vec3(2.08008670807, -2.08980798721, 1.40093314648), Vec3(194.464614868, -9.79998588562, -2.22346805105e-15)),
            (Vec3(7.70267629623, 1.77368688583, 0.635437190533), Vec3(171.167755127, 1.07288360596e-05, 2.3162429006e-12)),
            (Vec3(6.30877733231, 7.53235578537, 0.794994473457), Vec3(190.002166748, 2.08705019951, 1.40288061722e-17)),
            (Vec3(5.7558426857, 9.1334810257, 0.740567445755), Vec3(124.902160645, 1.81483018398, -1.0861217609e-16)),
            (Vec3(-6.59877824783, 4.19088554382, 3.07992815971), Vec3(227.539596558, -15.879611969, -4.85763932304e-17)),
            (Vec3(-1.43576622009, -3.85774421692, 1.27280509472), Vec3(355.967834473, -2.08702802658, 7.15576602465e-32)),
            (Vec3(5.06005096436, -5.574696064, 1.4792971611), Vec3(395.605377197, -0.635172724724, 5.28953236767e-09)),
            (Vec3(4.22867393494, 1.36209774017, 1.61565947533), Vec3(463.19921875, -1.17961061001, 1.56818256839e-14)),
            (Vec3(-8.61300468445, 2.81095552444, 5.51579141617), Vec3(574.236633301, -22.2314605713, -2.36885066853e-15)),
            (Vec3(-3.23688173294, -8.87144374847, 7.29551553726), Vec3(717.036315918, -38.1111068726, -3.89869733719e-12)),
            (Vec3(6.9931397438, 0.352610468864, 8.37956905365), Vec3(808.911071777, -37.9296264648, -2.14153172841e-17)),
            (Vec3(-3.67716407776, 2.42237210274, 1.25417733192), Vec3(920.801574707, -1.81480431557, -3.21062076827e-21)),
            (Vec3(-5.03519248962, -1.99267101288, 0.626431763172), Vec3(937.995361328, -1.72405970097, 9.73692151274e-21)),
            (Vec3(-7.88716125488, -9.81040000916, 0.671547889709), Vec3(694.198425293, 3.08520269394, -7.53577227204e-14)),
            (Vec3(-10.3637962341, 2.21844983101, 0.307416677475), Vec3(568.00189209, 6.89631128311, -1.281110413e-21)),
            (Vec3(-3.59259080887, 3.95971107483, 0.997548103333), Vec3(716.839477539, -10.7981367111, 5.64976517929e-18)),
            (Vec3(-2.23506236076, 3.88475131989, 0.997541606426), Vec3(716.839477539, -10.7981367111, 2.58575523189e-13)),
            (Vec3(-0.84736174345, 4.63475656509, 0.745338797569), Vec3(761.858337402, -7.25924110413, 1.03128511048e-13)),
            (Vec3(-0.545130074024, 7.36238718033, 0.988417208195), Vec3(596.942810059, -10.7981300354, -3.96466984676e-13)),
            (Vec3(3.96552157402, 3.9378631115, 0.888374686241), Vec3(759.889465332, -7.44072246552, 5.6630221515e-15)),
            (Vec3(6.83503675461, 5.07958745956, 1.35647082329), Vec3(522.392822266, -0.998126745224, -2.47028797418e-08)),
            (Vec3(0.820540785789, 0.197230920196, 7.56859731674), Vec3(448.696014404, -81.5759048462, 3.64362012784e-11)),
            (Vec3(-3.51800608635, 7.42211961746, 3.71423721313), Vec3(563.736328125, -9.34627246857, -6.10001746042e-15)),
            (Vec3(9.11974906921, 8.14447784424, 4.48866844177), Vec3(492.730163574, -11.9777460098, -1.0043676909e-13)),
            (Vec3(5.56226205826, 0.387885093689, 5.24619436264), Vec3(628.114135742, 1.54262781143, 1.8275872482e-10)),
            (Vec3(4.04775619507, -1.55904722214, 5.21813249588), Vec3(640.911010742, 1.63336586952, -1.44365598577e-13)),
            (Vec3(0.80768686533, -8.62872409821, 3.60759234428), Vec3(714.214111328, -12.9758872986, -2.56536921561e-14)),
            (Vec3(-9.24007701874, 2.4030418396, 1.03644263744), Vec3(682.386169434, -12.7036676407, 1.38730849725e-11)),
            (Vec3(-9.60101795197, 7.48619365692, 1.2708107233), Vec3(587.8203125, -1.08885848522, 4.64905796514e-22)),
        )
        self.controller.play_motion_path(mopath, 2.3)

MainApp().run()
