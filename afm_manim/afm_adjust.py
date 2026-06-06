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


#
class Scene1_afm_adjust(Scene):
    def construct(self):
        holder_w, holder_h = 9.56, 1.89
        chip_w, chip_h = 4.44, 0.99
        cantilever_edge = 2.00

        # ---1. Chip (created first so others can reference it) ---
        chip = Rectangle(width=chip_w, height=chip_h, color=GREY,
                        fill_opacity=0.6, stroke_width=1)
        chip.move_to(ORIGIN)
        chip_label = Text("玻璃基片 (Chip)", font_size=22, color=WHITE)
        chip_label.next_to(chip, LEFT, buff=0.6)

        framebox_chip = SurroundingRectangle(chip, color=BLUE, buff=0.1)

        # ---2. TipHolder (above chip) ---
        tipHolder = Rectangle(width=holder_w, height=holder_h, color=GREY,
                             fill_opacity=0.7, stroke_width=1)
        tipHolder.next_to(chip, direction=UP, buff=0.015)

        holder_label = Text("探针架 (Tip Holder)", font_size=22, color=WHITE)
        holder_label.next_to(tipHolder, UP, buff=0.025)

        framebox_tipHolder = SurroundingRectangle(tipHolder, color=BLUE, buff=0.1)

        # ---3. Cantilever (V-shape below chip) ---
        # Default triangle side = sqrt(3) * radius = sqrt(3) ≈ 1.732
        # Scale to match cantilever_edge
        tri_scale = cantilever_edge / np.sqrt(3)
        cantilever_base = Triangle(color=WHITE).rotate(PI).scale(tri_scale)
        cantilever_covered = Triangle(color=BLACK).rotate(PI).scale(tri_scale*0.3)
        cantilever = VGroup(cantilever_base, cantilever_covered)
        cantilever.next_to(chip, direction=DOWN, buff=0.01)

        c_label = Text("三角悬臂 (Cantilever)", font_size=22, color=WHITE)
        c_label.next_to(cantilever, DOWN, buff=0.2)

        framebox_cantilever = SurroundingRectangle(cantilever, color=BLUE, buff=0.15)

        # ---4. Dimension annotation (chip length: 1-2 mm) ---
        arrow_top_y = chip.get_top()[1]
        arrow_bot_y = chip.get_bottom()[1]
        arrow_x = chip.get_right()[0] + 1.0

        arrow_0 = DoubleArrow(
            start=[arrow_x, arrow_top_y, 0],
            end=[arrow_x, arrow_bot_y, 0],
            color=WHITE, stroke_width=3,
            tip_length=0.15, buff=0
        )
        up_line = Line(chip.get_corner(UP + RIGHT), [arrow_x, arrow_top_y, 0])
        bot_line = Line(chip.get_corner(DOWN + RIGHT), [arrow_x, arrow_bot_y, 0])

        chip_annotation = VGroup(arrow_0, up_line, bot_line)

        dim_label = MathTex(r"1{-}2\,\text{mm}", font_size=28, color=WHITE)
        dim_label.next_to(chip_annotation, RIGHT, buff=0.2)

        # ---5. Laser dot with traced path ---
        laser = Dot(color=RED, radius=0.08)
        laser_glow = Dot(color=RED, radius=0.14, fill_opacity=0.3)
        laser_group = VGroup(laser_glow, laser)

        trace = TracedPath(laser.get_center, stroke_color=YELLOW, stroke_width=2)

        x = ValueTracker(5)
        y = ValueTracker(3)
        laser.add_updater(lambda d: d.move_to((x.get_value(), y.get_value(), 0)))
        laser_glow.add_updater(lambda g: g.move_to(laser.get_center()))

        # ============================================================
        # Animation sequence
        # ============================================================

        # Phase 1: Show entire structure at once (no frameboxes yet)
        all_geo = VGroup(tipHolder, chip, cantilever)
        self.play(FadeIn(all_geo), run_time=1.2)
        self.wait(0.4)

        # Phase 2: Voiceover-style — highlight each part one by one
        # --- TipHolder ---
        self.play(Create(framebox_tipHolder), Write(holder_label), run_time=1.2)
        self.wait(0.6)
        self.play(FadeOut(framebox_tipHolder), run_time=0.4)

        # --- Chip ---
        self.play(Create(framebox_chip), Write(chip_label), run_time=1.2)
        self.wait(0.6)
        self.play(FadeOut(framebox_chip), run_time=0.4)

        # --- Cantilever ---
        self.play(Create(framebox_cantilever), Write(c_label), run_time=1.2)
        self.wait(0.6)
        self.play(FadeOut(framebox_cantilever), run_time=0.4)

        # Phase 3: Dimension annotation
        self.play(GrowFromCenter(chip_annotation), Write(dim_label), run_time=1.2)
        self.wait(0.5)

        # Phase 4: Laser appears in black area (outside structure)
        note_1 = Text("激光光点出现在视野中", font_size=26, color=YELLOW)
        note_1.to_edge(DOWN, buff=0.5)

        # Start from black area — upper-right of the structure
        x.set_value(5)
        y.set_value(3)
        self.play(FadeIn(laser_group, scale=0.5), Write(note_1), run_time=1.0)
        self.wait(0.6)
        self.play(FadeOut(note_1), run_time=0.5)

        # Phase 5: PID-style laser adjustment toward chip area
        self.add(trace)

        adjust_note = Text("调节旋钮 → 激光向基片移动", font_size=24, color=WHITE)
        adjust_note.to_edge(DOWN, buff=0.5)
        self.play(Write(adjust_note), run_time=1.0)

        target = chip.get_center()

        for _ in range(50):
            error_x = target[0] - x.get_value()
            error_y = target[1] - y.get_value()

            jitter = 0.25 * (abs(error_x) + abs(error_y)) / 8

            new_x = x.get_value() + error_x * 0.12 + np.random.uniform(-jitter, jitter)
            new_y = y.get_value() + error_y * 0.12 + np.random.uniform(-jitter, jitter)

            self.play(
                x.animate.set_value(new_x),
                y.animate.set_value(new_y),
                run_time=0.1,
                rate_func=linear
            )

        # Final snap to chip center
        self.play(
            x.animate.set_value(target[0]),
            y.animate.set_value(target[1]),
            run_time=0.4
        )
        self.play(FadeOut(trace))

        self.play(FadeOut(adjust_note), run_time=0.4)

        # Phase 6: Laser lands on chip — bright spot visible from front
        success_note = Text("正面观察可见明亮激光光点", font_size=26, color=GREEN)
        success_note.to_edge(DOWN, buff=0.5)
        self.play(Write(success_note), run_time=1.0)
        self.wait(0.8)
        self.play(FadeOut(success_note), run_time=0.4)

        # Blocked note — laser on opaque holder, no transmission below
        block_note = Text("激光完全被遮挡，下方无透射光斑", font_size=26, color=RED)
        block_note.to_edge(DOWN, buff=0.5)
        self.play(Write(block_note), run_time=1.2)
        self.wait(1.2)

        # Phase 7: Fade out everything
        self.play(
            FadeOut(tipHolder), FadeOut(holder_label),
            FadeOut(chip), FadeOut(chip_label),
            FadeOut(cantilever), FadeOut(c_label),
            FadeOut(chip_annotation), FadeOut(dim_label),
            FadeOut(laser_group), FadeOut(success_note),
            FadeOut(block_note),
            run_time=0.8
        )


#
#
class Scene2_afm_adjust(Scene):
    # ---1. Block Geometry ---

    top_left = np.array([-3, 1.5, 0])
    top_right = np.array([3, 1.5, 0])
    bot_left = np.array([-3.5, -0.8, 0])
    bot_right = np.array([3.5, -0.8, 0])
    
    block = Polygon(
            top_left, top_right, bot_left, bot_right,
            color=GRAY, fill_opacity=0.8, stroke_width=1
            )

    cantilever = Line().next_to(block, DOWN, buff=0)

    tip = Triangle().next_to(cantilever, DOWN + LEFT, buff=0)

    leftView = VGroup(block, cantilever, tip)

    # ---2. Label ---

    framebox_block = SurroundingRectangle(block)

    label_block = Text("探针基片")
    

    # ---3. Laser Beam A (Top surface horizontal) ---



    # ---4. Laser Beam B (Lefr surface linear) ---





#
#
class Scene3_afm_adjust(Scene):
    pass

