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

