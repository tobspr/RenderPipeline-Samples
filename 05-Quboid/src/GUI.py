

from panda3d.core import TextNode, Vec4
from direct.interval.LerpInterval import LerpColorScaleInterval
from direct.interval.MetaInterval import Sequence,Parallel
from direct.interval.FunctionInterval import Func,Wait

class GUI(object):

    """ Handles the gui elements like showing the current stage """

    def __init__(self, control):

        self.control = control
        self.gui_node = pixel2d.attach_new_node("GUI")
        self.gui_node.hide()
        self.gui_node.set_transparency(True)

        roboto_light = loader.loadFont("res/Roboto-Light.ttf")
        roboto_light.set_scale_factor(1)
        roboto_light.set_pixels_per_unit(120)

        self.text_stage = TextNode("TextStage")
        self.text_stage.set_text("Stage 1")
        self.text_stage.set_align(TextNode.A_left)
        self.text_stage.set_text_color(1, 1, 1, 1)
        self.text_stage.set_font(roboto_light)
        self.text_stage_np = self.gui_node.attach_new_node(self.text_stage)
        self.text_stage_np.set_scale(80.0)
        self.text_stage_np.set_pos(60, 0, -120)

        self.anim = None

    def show(self):
        self.gui_node.show()
        if self.anim is not None:
            self.anim.finish()
        self.anim = Sequence(
            LerpColorScaleInterval(self.gui_node, 0.2, Vec4(1), Vec4(1, 1, 1, 0), blendType="easeInOut")
        )
        self.anim.start()

    def hide(self):
        self.gui_node.hide()
        if self.anim is not None:
            self.anim.finish()
        self.anim = Sequence(
            LerpColorScaleInterval(self.gui_node, 0.2, Vec4(1, 1, 1, 0), Vec4(1), blendType="easeInOut")
        )
        self.anim.start()


    def set_stage(self, stage_nr):
        print(("Setting stage", stage_nr))

        Sequence(
            LerpColorScaleInterval(self.text_stage_np, 0.4, Vec4(1, 1, 1, 0), Vec4(1), blendType="easeInOut"),
            Func(lambda *args: self.text_stage.set_text("Stage " + str(stage_nr))),
            LerpColorScaleInterval(self.text_stage_np, 0.4, Vec4(1), Vec4(1, 1, 1, 0), blendType="easeInOut"),
        ).start()
