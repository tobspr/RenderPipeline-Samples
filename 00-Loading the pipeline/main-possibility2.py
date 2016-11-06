"""

This is an alternative possibility of initializing the RenderPipeline, which
makes it possible to construct the ShowBase object manually

"""

import sys
from direct.showbase.ShowBase import ShowBase

# Insert the pipeline path to the system path, this is required to be
# able to import the pipeline classes. In case you placed the render
# pipeline in a subfolder of your project, you have to adjust this.
sys.path.insert(0, "../../RenderPipeline")
sys.path.insert(0, "../../")

# Import render pipeline classes
from rpcore import RenderPipeline

# Construct and create the pipeline
render_pipeline = RenderPipeline()
render_pipeline.pre_showbase_init()

# Construct and create the ShowBase
base = ShowBase()
render_pipeline.create(base)

base.run()
