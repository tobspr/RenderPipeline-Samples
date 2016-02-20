"""

Simplest possible application using the render pipeline.

This sample will not show any fancy rendering output, but you can base your own
applications on this skeleton.

"""

import os, sys
from panda3d.core import load_prc_file_data
from direct.showbase.ShowBase import ShowBase

class Application(ShowBase):

    def __init__(self):
        # Notice that you must not call ShowBase.__init__ (or super), the render
        # pipeline does that for you.

        # Insert the pipeline path to the system path, this is required to be
        # able to import the pipeline classes. In case you placed the render
        # pipeline in a subfolder of your project, you have to adjust this.
        sys.path.insert(0, "../../")

        # Import render pipeline classes
        from rpcore import RenderPipeline, SpotLight

        # Construct and create the pipeline
        self.render_pipeline = RenderPipeline(self)
        self.render_pipeline.create()

        # Done! You can start setting up your application stuff as regular now.

Application().run()
