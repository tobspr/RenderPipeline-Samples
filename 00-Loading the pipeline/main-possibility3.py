"""

This is an alternative possibility of initializing the RenderPipeline, which
uses the (deprecated!) DirectStart interface. This should not be used anymore,
except for fast prototyping.

"""

import sys

# Insert the pipeline path to the system path, this is required to be
# able to import the pipeline classes. In case you placed the render
# pipeline in a subfolder of your project, you have to adjust this.
sys.path.insert(0, "../../")
sys.path.insert(0, "../../RenderPipeline")

# Import render pipeline classes
from rpcore import RenderPipeline

# Construct and create the pipeline
render_pipeline = RenderPipeline()
render_pipeline.pre_showbase_init()

# Import (deprecated!) DirectStart interface
import direct.directbase.DirectStart
render_pipeline.create(base)

base.run()
