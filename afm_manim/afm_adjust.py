"""
Here is the left part (Position) of a 16:9 video 

It shows how to adjust the afm 

"""


from manim import *
import numpy as np

# Global Config
# 1920*1080  | 30fps black | background
config.frame_rate = 30
config.background_color = BLACK
config.pixel_width = 1920
config.pixel_height = 1080

# Color definitions


# 
#
class Scene1_afm_adjust(Scene):
    # The constructure of the TipHolder, Chip, Cantilever
    def construct(self):
        holder_w, holder_h = 9.56, 1.89
        chip_w, chip_h = 4.44, 0.99
        cantilever_edge = 2.00

        # ---1. TipHolder ---
        TipHolder = Rectangle(width=holder_w, height=holder_h)


        # ---2. Chip ---
        Chip = Rectangle(width=chip_w, height=chip_h)

        # ---3. Cantilever ---
        Cantilever = Triangle(color=WHITE).rotate(PI)
        Cantilever_covered = Triangle(color=BLACK).rotate(PI)

        # ---4. Annotation ---






#
#
class Scene2_afm_adjust(Scene):
    pass

#
#
class Scene3_afm_adjust(Scene):
    pass

