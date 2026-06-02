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
        tipHolder = Rectangle(width=holder_w, height=holder_h)
        tipHolder.next_to(chip, direction=UP, aligned_edge=DOWN)
        
        framebox_tipHolder = SurroundingRectangle()

        # ---2. Chip ---
        chip = Rectangle(width=chip_w, height=chip_h)
        chip.move_to(ORIGIN)

        framebox_chip = SurroundingRectangle()

        # ---3. Cantilever ---
        cantilever_base = Triangle(color=WHITE).rotate(PI)
        cantilever_covered = Triangle(color=BLACK).rotate(PI)

        cantilever = VGroup(cantilever_base, cantilever_covered)

        cantilever.next_to(chip, direction=DOWN, aligned_edge=UP)
        
        framebox_cantilever = SurroundingRectangle()
        
        """ 1.2.3. is a Vgroup() , maybe would be use in the future """
        # ---4. Annotation ---
        arrow_top_y = tipHolder.get_bottom()[1]
        arrow_bot_y = chip.get_bottom()[1]
        arrow_x = chip.get_right() + 1.0
        
        arrow_0 = DoubleArrow(
                start=[arrow_x, arrow_top_y, 0],
                end=[arrow_x, arrow_bot_y, 0],
                color=WHITE, stroke_width=3,
                tip_shape=StealthTip, tip_length=0.15, buff=0
                )
        up_line = Line(chip.get_corner(UP+RIGHT), arrow_0.get_top())
        bot_line = Line(chip.get_corner(DOWN+RIGHT), arrow_0.get_bottom())

        chip_annotation = VGroup(arrow_0, up_line, bot_line)


        label_0 = MathTex(r"1{-}2\,\text{mm}", font_size=28, color=WHITE)
        label_0.next_to(chip_annotation, RIGHT, buff=0.2)






#
#
class Scene2_afm_adjust(Scene):
    pass

#
#
class Scene3_afm_adjust(Scene):
    pass

