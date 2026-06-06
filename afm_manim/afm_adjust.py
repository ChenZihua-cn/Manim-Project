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
COLOR_LASER = "#FF0000"
COLOR_LASER_SPOT = "#FF4444"
COLOR_TIP_HOLDER = "#555555"
COLOR_CHIP = "#999999"
COLOR_CANTILEVER = "#666666"
COLOR_BLOCK = "#888888"
COLOR_PROBE_TIP = "#222222"
COLOR_PAPER = "#EEEEEE"
COLOR_DIFFRACTION = "#FFC107"
COLOR_ROUND_SPOT = "#FF4444"
COLOR_GREEN = "#43A047"

"""
这是一张关于原子力显微镜探针的结构示意图

图片包含以下主要元素和标注，从上到下依次为：

1. **探针架 (TipHolder)**：最上方的深灰色矩形块，用于固定装置。
2. **玻璃体 (Chip)**：中间较浅灰色的矩形块，位于探针架下方。
3. **三角悬臂 (Cantilever)**：最下方一个向下突出的"V"字型结构，通常带有微小的探针尖端。
4. **尺寸标注**：右侧有一个双向箭头，标明了玻璃体底端到悬臂最底端之间的距离为 **1-2mm**。

图片整体采用黑、白、灰三种颜色，用简单的几何图形和文字表示器件的层级关系及尺寸结构。
"""

# 这里是先将激光光点调节至探针架区域，一开始不在这三个元素的任何一个上
# 顺时针旋转激光器位置垂直调节旋钮，直到激光落到探针架或探针基片上。
# 用random和updater模拟光路调节的微扰
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

        # ---5. Laser ---
        laser = Dot(color=RED, radius=0.08)
        
        # 添加路径轨迹
        trace = TracedPath(laser.get_center, stroke_color=YELLOW, stroke_width=2)
        
        x = ValueTracker(5)   # 起始偏移
        y = ValueTracker(3)
        laser.add_updater(lambda d: d.move_to((x.get_value(), y.get_value(), 0)))
        # Changed [...] to (...)
        # a tuple satisfies tuple[float, float, float] in Manim's Point3DLike union type
        self.add(laser, trace)
                
        # PID 控制风格的校准
        for _ in range(80):
            error_x = -x.get_value()
            error_y = -y.get_value()
            
            # 抖动随误差减小而减小（越接近越稳定）
            jitter = 0.3 * (abs(error_x) + abs(error_y)) / 10
            
            new_x = x.get_value() + error_x * 0.15 + np.random.uniform(-jitter, jitter)
            new_y = y.get_value() + error_y * 0.15 + np.random.uniform(-jitter, jitter)
            
            self.play(
                x.animate.set_value(new_x),
                y.animate.set_value(new_y),
                run_time=0.05,
                rate_func=linear
            )
        
        # 最终稳定在靶心
        self.play(
            x.animate.set_value(0),
            y.animate.set_value(0),
            run_time=0.5
        )

#
#
class Scene2_afm_adjust(Scene):
    pass

#
#
class Scene3_afm_adjust(Scene):
    pass

