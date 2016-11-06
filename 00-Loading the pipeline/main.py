"""

Simplest possible application using the render pipeline.

This sample will not show any fancy rendering output, but you can base your own
applications on this skeleton.

This is the preferred way of initializing the pipeline, however you can find
alternative ways in the other included files.

"""

import sys
from direct.showbase.ShowBase import ShowBase


class Application(ShowBase):

    def __init__(self):
        # Notice that you must not call ShowBase.__init__ (or super), the
        # render pipeline does that for you. If this is unconvenient for you,
        # have a look at the other initialization possibilities.

        # Insert the pipeline path to the system path, this is required to be
        # able to import the pipeline classes. In case you placed the render
        # pipeline in a subfolder of your project, you have to adjust this.
        sys.path.insert(0, "../../")
        sys.path.insert(0, "../../RenderPipeline")

        # Import the main render pipeline class
        from rpcore import RenderPipeline

        # Construct and create the pipeline
        self.render_pipeline = RenderPipeline()
        self.render_pipeline.create(self)

        # Done! You can start setting up your application stuff as regular now.

Application().run()
