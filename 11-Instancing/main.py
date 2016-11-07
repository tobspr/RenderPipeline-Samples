"""

Material Demo

This demonstrates the various materials the pipeline supports.
It is also a reference scene, for testing BRDF changes.

"""

from __future__ import print_function

import os
import sys
import struct
from panda3d.core import Vec3, load_prc_file_data, Texture, GeomEnums
from panda3d.core import OmniBoundingVolume
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

# Import the render pipeline class
from rpcore import RenderPipeline

# This is a helper class for better camera movement - see below.
from rpcore.util.movement_controller import MovementController


class Application(ShowBase):
    def __init__(self):
        # Setup window size and title
        load_prc_file_data("", """
            # win-size 1600 900
            window-title Render Pipeline - Instancing Example
        """)

        # Construct the render pipeline
        self.render_pipeline = RenderPipeline()
        self.render_pipeline.create(self)
        self.render_pipeline.daytime_mgr.time = "19:17"
        # self.render_pipeline.daytime_mgr.time = "12:00"

        # Load the scene
        model = self.loader.load_model("scene/Scene.bam")
        model.reparent_to(self.render)

        # Find the prefab object, we are going to in instance this object
        # multiple times
        prefab = model.find("**/InstancedObjectPrefab")

        # Collect all instances
        matrices = []
        for elem in model.find_all_matches("**/PREFAB*"):
            matrices.append(elem.get_mat(self.render))
            elem.remove_node()

        print("Loaded", len(matrices), "instances!")

        # Allocate storage for the matrices, each matrix has 16 elements,
        # but because one pixel has four components, we need amount * 4 pixels.
        buffer_texture = Texture()
        buffer_texture.setup_buffer_texture(len(matrices) * 4, Texture.T_float, Texture.F_rgba32, GeomEnums.UH_static)

        float_size = len(struct.pack("f", 0.0))
        floats = []

        # Serialize matrices to floats
        ram_image = buffer_texture.modify_ram_image()

        for idx, mat in enumerate(matrices):
            for i in range(4):
                for j in range(4):
                    floats.append(mat.get_cell(i, j))

        # Write the floats to the texture
        data = struct.pack("f" * len(floats), *floats)
        ram_image.set_subdata(0, len(data), data)

        # Load the effect
        self.render_pipeline.set_effect(prefab, "effects/basic_instancing.yaml", {})

        prefab.set_shader_input("InstancingData", buffer_texture)
        prefab.set_instance_count(len(matrices))

        # We have do disable culling, so that all instances stay visible
        prefab.node().set_bounds(OmniBoundingVolume())
        prefab.node().set_final(True)

        # Initialize movement controller, this is a convenience class
        # to provide an improved camera control compared to Panda3Ds default
        # mouse controller.
        self.controller = MovementController(self)
        self.controller.set_initial_position_hpr(
            Vec3(-23.2, -32.5, 5.3),
            Vec3(-33.8, -8.3, 0.0))
        self.controller.setup()

Application().run()
