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
COLOR_DIFFRACTION = "#FF590083"
COLOR_ROUND_SPOT = "#FF4444"
COLOR_BLUE = "#0011FF"

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
        up_line = Line(chip.get_corner(UP + RIGHT), np.array([arrow_x, arrow_top_y, 0]))
        bot_line = Line(chip.get_corner(DOWN + RIGHT), np.array([arrow_x, arrow_bot_y, 0]))

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
            FadeOut(laser_group),
            FadeOut(block_note),
            run_time=0.8
        )
        self.wait(0.2)

class Scene1_2_afm_adjust(Scene):
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
        up_line = Line(chip.get_corner(UP + RIGHT), np.array([arrow_x, arrow_top_y, 0]))
        bot_line = Line(chip.get_corner(DOWN + RIGHT), np.array([arrow_x, arrow_bot_y, 0]))

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
        """
        # Phase 4: Laser appears in black area (outside structure)
        note_1 = Text("激光光点出现在视野中", font_size=26, color=YELLOW)
        note_1.to_edge(DOWN, buff=0.5)"""

        # Start from black area — upper-right of the structure
        x.set_value(5)
        y.set_value(3)
        self.play(FadeIn(laser_group, scale=0.5), 
                  # Write(note_1), 
                  run_time=1.0)
        self.wait(0.6)
        # self.play(FadeOut(note_1), run_time=0.5)

        # Phase 5: PID-style laser adjustment toward chip area
        self.add(trace)
        """
        adjust_note = Text("调节旋钮 → 激光向基片移动", font_size=24, color=WHITE)
        adjust_note.to_edge(DOWN, buff=0.5)
        self.play(Write(adjust_note), run_time=1.0)"""

        target = tipHolder.get_center()

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

        # self.play(FadeOut(adjust_note), run_time=0.4)
        """
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
        self.wait(1.2)"""

        # Phase 7: Fade out everything
        self.play(
            FadeOut(tipHolder), FadeOut(holder_label),
            FadeOut(chip), FadeOut(chip_label),
            FadeOut(cantilever), FadeOut(c_label),
            FadeOut(chip_annotation), FadeOut(dim_label),
            FadeOut(laser_group),
            # FadeOut(block_note),
            run_time=0.8
        )
        self.wait(0.2)

class Scene1_3_afm_adjust(Scene):
    def construct(self):
        holder_w, holder_h = 9.56, 1.89
        chip_w, chip_h = 4.44, 0.99
        cantilever_edge = 2.00
        """
        # ---1. Chip (created first so others can reference it) ---
        chip = Rectangle(width=chip_w, height=chip_h, color=GREY,
                        fill_opacity=0.6, stroke_width=1)
        chip
        chip_label = Text("玻璃基片 (Chip)", font_size=22, color=WHITE)
        chip_label.next_to(chip, LEFT, buff=0.6)

        framebox_chip = SurroundingRectangle(chip, color=BLUE, buff=0.1)"""

        # ---2. TipHolder (above chip) ---
        tipHolder = Rectangle(width=holder_w, height=holder_h, color=GREY,
                             fill_opacity=0.7, stroke_width=1)
        tipHolder.move_to(ORIGIN)
        # .next_to(chip, direction=UP, buff=0.015)

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
        cantilever.next_to(tipHolder, direction=DOWN, buff=0.01)

        c_label = Text("三角悬臂 (Cantilever)", font_size=22, color=WHITE)
        c_label.next_to(cantilever, DOWN, buff=0.2)

        framebox_cantilever = SurroundingRectangle(cantilever, color=BLUE, buff=0.15)
        """
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
        up_line = Line(chip.get_corner(UP + RIGHT), np.array([arrow_x, arrow_top_y, 0]))
        bot_line = Line(chip.get_corner(DOWN + RIGHT), np.array([arrow_x, arrow_bot_y, 0]))

        chip_annotation = VGroup(arrow_0, up_line, bot_line)"""

        # dim_label = MathTex(r"1{-}2\,\text{mm}", font_size=28, color=WHITE)
        # dim_label.next_to(chip_annotation, RIGHT, buff=0.2)

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
        all_geo = VGroup(tipHolder, 
                        # chip, 
                         cantilever)
        self.play(FadeIn(all_geo), run_time=1.2)
        self.wait(0.4)

        # Phase 2: Voiceover-style — highlight each part one by one
        # --- TipHolder ---
        self.play(Create(framebox_tipHolder), Write(holder_label), run_time=1.2)
        self.wait(0.6)
        self.play(FadeOut(framebox_tipHolder), run_time=0.4)
        """
        # --- Chip ---
        self.play(Create(framebox_chip), Write(chip_label), run_time=1.2)
        self.wait(0.6)
        self.play(FadeOut(framebox_chip), run_time=0.4)"""

        # --- Cantilever ---
        self.play(Create(framebox_cantilever), Write(c_label), run_time=1.2)
        self.wait(0.6)
        self.play(FadeOut(framebox_cantilever), run_time=0.4)

        # Phase 3: Dimension annotation
        # self.play(GrowFromCenter(chip_annotation), Write(dim_label), run_time=1.2)
        self.wait(0.5)
        """
        # Phase 4: Laser appears in black area (outside structure)
        note_1 = Text("激光光点出现在视野中", font_size=26, color=YELLOW)
        note_1.to_edge(DOWN, buff=0.5)"""

        # Start from black area — upper-right of the structure
        x.set_value(5)
        y.set_value(3)
        self.play(FadeIn(laser_group, scale=0.5), 
                  # Write(note_1), 
                  run_time=1.0)
        self.wait(0.6)
        # self.play(FadeOut(note_1), run_time=0.5)

        # Phase 5: PID-style laser adjustment toward chip area
        self.add(trace)
        """
        adjust_note = Text("调节旋钮 → 激光向基片移动", font_size=24, color=WHITE)
        adjust_note.to_edge(DOWN, buff=0.5)
        self.play(Write(adjust_note), run_time=1.0)"""

        target = tipHolder.get_center()

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

        # self.play(FadeOut(adjust_note), run_time=0.4)
        """
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
        self.wait(1.2)"""

        # Phase 7: Fade out everything
        self.play(
            FadeOut(tipHolder), FadeOut(holder_label),
            # FadeOut(chip), FadeOut(chip_label),
            FadeOut(cantilever), FadeOut(c_label),
            # FadeOut(chip_annotation), FadeOut(dim_label),
            FadeOut(laser_group),
            # FadeOut(block_note),
            run_time=0.8
        )
        self.wait(0.2)

"""
### 1. 核心物理主体 (反射物体)
这是一个侧视图
*   **外观**：图片中央有一个灰色的、具有厚度的块状物体（类似于一个梯形柱体或带斜面的底座）。
*   **结构**：
    *   顶部是一个水平的平坦面。
    *   左侧是一个倾斜的表面（斜面）。
    *   底部有一个指向下方的黑色小三角形（探针）。

### 2. 右侧光路 (光束 A)
*   **入射**：一束红色的激光（标有"Laser"）从右上方向左下方照射。
*   **接触点**：光束触及灰色物体的**顶部水平面**。
*   **反射**：根据反射定律（入射角等于反射角），光束向上方反射。
*   **终点**：反射光线指向标有字母 **A** 的位置。

### 3. 左侧光路 (光束 B)
*   **入射**：另一束红色的激光（标有"Laser"）从右上方偏右向左下方照射。
*   **接触点**：光束触及灰色物体的**左侧倾斜面**。
*   **反射**：同样遵循反射定律，光束在此斜面上产生反射。
*   **终点**：反射光线向左下方射出，指向标有字母 **B** 的位置。

"""
# 调节水平旋钮，使激光光点落在探针基片的中间位置；
# 调节垂直旋钮，使激光往悬臂方向移动。由于探针基片的边缘是一个梯形，有一定的倾斜度，
# 所以，激光落在探针基片的边缘时，反射的激光光点会落在探头的前方，
# 此时，稍微调节垂直旋钮，即可将激光调节到悬臂的区域附近。
class Scene2_afm_adjust(Scene):
    def construct(self):
        # ---1. Block Geometry ---

        top_left = np.array([-2, 1.5, 0])
        top_right = np.array([2, 1.5, 0])
        bot_left = np.array([-4, -0.8, 0])
        bot_right = np.array([2, -0.8, 0])

        block = Polygon(
                top_left, top_right, bot_right, bot_left,
                color=GRAY, fill_opacity=0.8, stroke_width=1
                )

        cantilever = Line(start=bot_right, end=bot_left+LEFT, color=WHITE)

        probe_tip = Triangle().scale(0.3).rotate(PI).next_to(
            cantilever, DOWN + LEFT, buff=0).shift(0.5*RIGHT)

        leftView = VGroup(block, cantilever, probe_tip)

        # ---2. Label ---

        framebox_block = SurroundingRectangle(block)

        block_label = Text("探针基片 (侧视图)", font_size=24, color=WHITE)
        block_label.next_to(block, UP, buff=0.4)

        top_surface_label = Text("顶部水平面", font_size=20, color=WHITE)
        top_surface_label.next_to(block.get_top(), UP, buff=0.15).shift(LEFT * 0.3)

        tip_label = Text("探针", font_size=18, color=WHITE)
        tip_label.next_to(probe_tip, DOWN, buff=0.15)

        # ---3. Laser Beam A (Top surface horizontal) ---
        inc_A_start = np.array([4.5, 3.2, 0])
        inc_A_hit = (top_left + top_right) / 2   # (0, 1.5, 0)

        inc_A_vec = inc_A_hit - inc_A_start
        inc_A_dir = inc_A_vec / np.linalg.norm(inc_A_vec)

        normal_top = np.array([0.0, 1.0, 0.0])
        ref_A_dir = inc_A_dir - 2 * np.dot(inc_A_dir, normal_top) * normal_top
        ref_A_end = inc_A_hit + ref_A_dir * 2.8

        laser_A_in = Arrow(inc_A_start, inc_A_hit, color=COLOR_LASER,
                           buff=0, stroke_width=2.5, tip_length=0.12)
        laser_A_out = Arrow(inc_A_hit, ref_A_end, color=COLOR_LASER,
                            buff=0, stroke_width=2.5, tip_length=0.12)

        label_A = MathTex(r"A", font_size=36, color=RED)
        label_A.move_to(ref_A_end + ref_A_dir * 0.3)

        # ---4. Laser Beam B (Left sloped surface) ---
        surf_B_vec = top_left - bot_left
        surf_B_dir = surf_B_vec / np.linalg.norm(surf_B_vec)
        normal_left = np.array([-surf_B_dir[1], surf_B_dir[0], 0])

        inc_B_hit = (top_left + bot_left) / 2    # (-3.25, 0.35, 0)
        inc_B_start = np.array([-3.5, 2.0, 0])

        inc_B_vec = inc_B_hit - inc_B_start
        inc_B_dir = inc_B_vec / np.linalg.norm(inc_B_vec)

        ref_B_dir = inc_B_dir - 2 * np.dot(inc_B_dir, normal_left) * normal_left
        ref_B_end = inc_B_hit + ref_B_dir * 2.2

        laser_B_in = Arrow(inc_B_start, inc_B_hit, color=COLOR_LASER,
                           buff=0, stroke_width=2.5, tip_length=0.12)
        laser_B_out = Arrow(inc_B_hit, ref_B_end, color=COLOR_LASER,
                            buff=0, stroke_width=2.5, tip_length=0.12)

        label_B = MathTex(r"B", font_size=36, color=RED)
        label_B.move_to(ref_B_end + ref_B_dir * 0.3)

        # --- Narration text (right side) ---
        narration_1 = Text(
            "调节水平旋钮\n→ 激光移至基片中间",
            font_size=22, color=WHITE, line_spacing=1.5
        )
        narration_1.to_edge(RIGHT, buff=0.6).shift(UP * 1.5)

        narration_2 = Text(
            "调节垂直旋钮\n→ 激光向悬臂移动",
            font_size=22, color=WHITE, line_spacing=1.5
        )
        narration_2.to_edge(RIGHT, buff=0.6).shift(UP * 1.5)

        narration_3 = Text(
            "斜面边缘反射\n→ 光点落在探头前方",
            font_size=22, color=WHITE, line_spacing=1.5
        )
        narration_3.to_edge(RIGHT, buff=0.6).shift(UP * 1.5)

        # --- Animation ---
        self.play(FadeIn(leftView), run_time=1.0)
        self.play(Write(block_label), run_time=0.8)
        self.play(Write(top_surface_label), run_time=0.8)
        self.play(Write(tip_label), run_time=0.8)
        self.wait(0.3)
        self.play(FadeOut(block_label, top_surface_label, tip_label), run_time=0.8)

        self.play(GrowArrow(laser_A_in), GrowArrow(laser_A_out),
                  Write(label_A), Write(narration_1), run_time=1.2)
        self.wait(0.5)
        self.play(FadeOut(narration_1), run_time=0.5)

        self.play(Write(narration_2), run_time=0.5)
        self.wait(0.5)
        self.play(FadeOut(narration_2), run_time=0.5)

        self.play(Write(narration_3),
                  GrowArrow(laser_B_in), GrowArrow(laser_B_out),
                  Write(label_B), run_time=1.2)
        self.wait(0.5)
       
        self.play(FadeOut(narration_3), run_time=0.5)
        self.wait(1.5)


"""
这两张图展示了一个**悬臂（Cantilever）的放大图及其与激光光路校准的原理说明**。

第一张是悬臂的结构示意图，第二张是**激光打在不同位置时，观察到的结果记录表**。

### 1. 激光完全没有照射到悬臂上（透射无阻）
*   **位置 A、I**：激光在悬臂外侧，直接穿过。
*   **位置 E**：激光穿过 V 型悬臂中间的**空隙**。
*   **结果**：纸条上都是**无光斑**。

### 2. 激光照射在悬臂的边缘（衍射效应）
*   **位置 B、H、D、F**：激光刚好打在悬臂黑白交界的地方。
*   **结果**：光发生了**衍射**，纸条上的光斑会变窄、变长，呈现出倾斜或带状的图案。

### 3. 激光完全照射在悬臂平坦部分（全反射）
*   **位置 C、G**：位于悬臂宽大的支架上。
*   **结果**：激光被镜面反射，纸条上呈现**较圆、明亮且集中的光斑**。

### 4. 激光打在悬臂尖端背面（关键位置）
*   **位置 J**：位于 V 型悬臂的最底端针尖位置。
*   **结果**：虽然这里是尖端，但激光打在它的**背面**，同样能产生全反射，纸条上会观察到**较圆的激光光斑**。

---

目标就是**让激光精准地打在位置 J，并调整反射镜，让那个"较圆的光斑"准确进入探测器中心**。
"""

# 剪一小白纸放置在"激光接收器的下方"（出射光线处），调节水平方向旋钮（保持垂直方向旋钮不动），
# 观察反射到白纸上的光斑，可判断激光落在悬臂的位置。
# 一步步微调是激光光点沿V型悬臂呈现阶梯下降到V型最尖端的过程，可以展示光点从V的左端开始，一级一级阶梯下降。
class Scene3_afm_adjust(Scene):
    def construct(self):
        # ---- V-shaped cantilever geometry ----
        # Two arms forming a V opening upward
        v_tip = np.array([0.0, -1.8, 0])
        # ±45° arms: left arm at 135° (up-left), right arm at 45° (up-right)
        # With tip at y=-1.8 and top at y=1.2, height=3.0 → half-width at top = 3.0
        v_left_top = np.array([-3.0, 1.2, 0])
        v_right_top = np.array([3.0, 1.2, 0])
        arm_width = 0.25  # thickness of each arm

        # Left arm polygon (approximate a thick line as a narrow polygon)
        left_dir = v_tip - v_left_top
        left_dir_n = left_dir / np.linalg.norm(left_dir)
        left_perp = np.array([-left_dir_n[1], left_dir_n[0], 0]) * arm_width

        ArmShift = 0.18

        left_arm = Polygon(
            v_left_top + left_perp,
            v_left_top - left_perp,
            v_tip - left_perp,
            v_tip + left_perp,
            color=COLOR_CANTILEVER, fill_opacity=1, stroke_width=1.5
        ).shift(ArmShift*(RIGHT+DOWN))

        # Right arm polygon
        right_dir = v_tip - v_right_top
        right_dir_n = right_dir / np.linalg.norm(right_dir)
        right_perp = np.array([-right_dir_n[1], right_dir_n[0], 0]) * arm_width

        right_arm = Polygon(
            v_right_top + right_perp,
            v_right_top - right_perp,
            v_tip - right_perp,
            v_tip + right_perp,
            color=COLOR_CANTILEVER, fill_opacity=1, stroke_width=1.5
        ).shift(ArmShift*(LEFT+DOWN))

        cantilever_group = VGroup(left_arm, right_arm)
        cantilever_label = Text("V型悬臂 (放大)", font_size=24, color=WHITE)
        cantilever_label.next_to(cantilever_group, UP, buff=0.5)

        # ---- Position dots A-J along the V ----
        # Left arm: A(top) -> B -> C -> D(near tip)
        # Gap:   E (center gap)
        # Right arm: F(near tip) -> G -> H -> I(top)
        # Tip:   J (V-tip)

        def left_arm_pos(t):
            """t: 0=top, 1=tip"""
            return v_left_top + t * (v_tip - v_left_top)

        def right_arm_pos(t):
            """t: 0=top, 1=tip"""
            return v_right_top + t * (v_tip - v_right_top)

        # Position definitions
        # Main positions on the centerline of each arm
        # Edge positions AB/BC/CD/DJ are on the interior-facing edge of the left arm
        # (centerline + left_perp), where the laser hits the cantilever boundary → diffraction
        positions = {
            "A": left_arm_pos(0.05),
            "AB": left_arm_pos(0.15) + left_perp,
            "B": left_arm_pos(0.25),
            "BC": left_arm_pos(0.40) + left_perp,
            "C": left_arm_pos(0.55),
            "CD": left_arm_pos(0.685) + left_perp,
            "D": left_arm_pos(0.82),
            "DJ": left_arm_pos(0.91) - left_perp,
            "JF": right_arm_pos(0.91) + right_perp,
            "E": np.array([0.0, 0.2, 0]),   # gap center
            "F": right_arm_pos(0.82),
            "G": right_arm_pos(0.55),
            "H": right_arm_pos(0.25),
            "I": right_arm_pos(0.05),
            "J": v_tip + np.array([0.0, -0.05, 0]),
            "VTIP": v_tip+ np.array([0.0, -0.4, 0]),
        }

        # Spot types
        no_spot_positions = {"E"}
        diffraction_positions = {"AB", "BC", "CD", "DJ", "JF"}
        round_spot_positions = {"A", "B", "C", "D", "J", "F"}
        cross_spot_positions = {"VTIP"}

        # ---- Create position dots and labels ----
        # Edge points (AB, BC, CD, DJ) are transition waypoints — not shown
        pos_dots = {}
        pos_labels = {}
        for name, pos in positions.items():
            if name in {"AB", "BC", "CD", "DJ", "JF", "VTIP"}:
                continue
            dot = Dot(pos, radius=0.06, color=WHITE)
            label = Text(name, font_size=16, color=WHITE)
            # Place labels offset from the dot
            if name in {"A", "B", "C", "D"}:
                label.next_to(dot, LEFT, buff=0.12)
            elif name in {"F", "G", "H", "I"}:
                label.next_to(dot, RIGHT, buff=0.12)
            elif name == "E":
                label.next_to(dot, UP, buff=0.12)
            else:  # J
                label.next_to(dot, DOWN, buff=0.12)
            pos_dots[name] = dot
            pos_labels[name] = label

        all_dots = VGroup(*pos_dots.values())
        all_labels = VGroup(*pos_labels.values())

        # ---- Paper screen (right side) ----
        paper = Rectangle(width=1.8, height=2.2, color=COLOR_PAPER,
                         fill_opacity=0.9, stroke_width=2)
        paper.move_to(np.array([4.2, -0.3, 0]))
        paper_label = Text("白纸 / 光屏", font_size=20, color=BLACK)
        paper_label.next_to(paper, UP, buff=0.15)
        # Spot patterns on paper (created dynamically per position)

        # No-spot indicator
        no_spot_text = Text("无光斑", font_size=22, color=BLACK)
        no_spot_text.move_to(paper.get_center())

        # ---- Laser scanning dot ----
        x = ValueTracker(positions["D"][0])
        y = ValueTracker(positions["D"][1])
        laser_dot = Dot((x.get_value(), y.get_value(), 0), radius=0.1, color=COLOR_LASER_SPOT)
        laser_glow_dot = Dot((x.get_value(), y.get_value(), 0), radius=0.18, color=COLOR_LASER_SPOT, fill_opacity=0.25)
        laser_dot.add_updater(lambda d: d.move_to((x.get_value(), y.get_value(), 0)))
        laser_glow_dot.add_updater(lambda g: g.move_to(laser_dot.get_center()))
        laser_group = VGroup(laser_glow_dot, laser_dot)

        # ---- Animation sequence ----
        # Draw cantilever
        self.play(FadeIn(cantilever_group), Write(cantilever_label), run_time=0.5)

        # Draw position labels
        self.play(FadeIn(all_dots), Write(all_labels), run_time=0.5)
        self.wait(0.3)

        # Draw paper screen
        self.play(FadeIn(paper), Write(paper_label), run_time=0.5)

        # Title
        scan_title = Text("激光扫描悬臂校准", font_size=28, color=WHITE)
        scan_title.to_edge(UP, buff=0.3)
        self.play(Write(scan_title), run_time=0.8)
        self.play(FadeIn(laser_group), run_time=0.5)

        trace = TracedPath(laser_dot.get_center, stroke_color=YELLOW, stroke_width=2)
        # self.add(trace)

        # ---- Step through positions ----
        scan_order = ["D", "DJ", "J", "JF", "F", "VTIP", "J"]

        # Track the current pattern mobject
        current_pattern_mob = None

        for name in scan_order:
            target_pos = positions[name]

            # Prepare spot pattern for this position
            new_pattern = None
            if name in no_spot_positions:
                new_pattern = no_spot_text.copy()
            elif name in diffraction_positions:
                new_pattern = Ellipse(width=0.12, height=0.5, color=COLOR_DIFFRACTION,
                                     fill_opacity=0.9, stroke_width=0)
                if name == "JF":
                    new_pattern.rotate(PI / 4).move_to(paper.get_center())
                else:
                    new_pattern.rotate(-PI / 4).move_to(paper.get_center())
            elif name in round_spot_positions:
                glow = Dot(paper.get_center(), radius=0.2,
                          color=COLOR_ROUND_SPOT, fill_opacity=0.3)
                spot = Dot(paper.get_center(), radius=0.12, color=COLOR_ROUND_SPOT)
                new_pattern = VGroup(glow, spot)
            elif name in cross_spot_positions:
                dj_ellipse = Ellipse(width=0.12, height=0.5, color=COLOR_DIFFRACTION,
                                     fill_opacity=0.9, stroke_width=0)
                dj_ellipse.rotate(-PI / 4)
                jf_ellipse = Ellipse(width=0.12, height=0.5, color=COLOR_DIFFRACTION,
                                     fill_opacity=0.9, stroke_width=0)
                jf_ellipse.rotate(PI / 4)
                new_pattern = VGroup(dj_ellipse, jf_ellipse).move_to(paper.get_center())

            # Fade out old pattern
            if current_pattern_mob is not None:
                self.play(FadeOut(current_pattern_mob, run_time=0.3))

            # PID-style movement toward target with jitter
            for _ in range(18):
                error_x = target_pos[0] - x.get_value()
                error_y = target_pos[1] - y.get_value()
                jitter = 0.25 * (abs(error_x) + abs(error_y)) / 8
                new_x = x.get_value() + error_x * 0.15 + np.random.uniform(-jitter, jitter)
                new_y = y.get_value() + error_y * 0.15 + np.random.uniform(-jitter, jitter)
                self.play(
                    x.animate.set_value(new_x),
                    y.animate.set_value(new_y),
                    run_time=0.06,
                    rate_func=linear
                )

            # Final snap to exact target
            self.play(
                x.animate.set_value(target_pos[0]),
                y.animate.set_value(target_pos[1]),
                run_time=0.3
            )

            if new_pattern is not None:
                self.play(FadeIn(new_pattern), run_time=0.4)

            current_pattern_mob = new_pattern

            # Add note for special positions
            note = None
            if name in no_spot_positions:
                note = Text("激光未照射悬臂 → 无光斑", font_size=20, color=GREY)
            elif name in diffraction_positions:
                note = Text("边缘衍射 → 长条状光斑", font_size=20, color=COLOR_DIFFRACTION)
            elif name in round_spot_positions:
                note = Text("全反射 → 明亮圆光斑", font_size=20, color=GREEN)
                if name == "J":
                    note = Text("尖端背面全反射 → 明亮圆光斑 ✓", font_size=20, color=GREEN)
            elif name in cross_spot_positions:
                note = Text("尖端十字光斑 → 精准对准", font_size=20, color=COLOR_DIFFRACTION)

            if note:
                note.to_edge(DOWN, buff=0.4)
                self.play(Write(note), run_time=0.5)
                self.wait(0.4)
                self.play(FadeOut(note), run_time=0.3)

            self.wait(0.2)

        # ---- Summary ----
        summary = VGroup(
            Text("校准完成：激光精准对准悬臂尖端", font_size=28, color=GREEN),
            Text("十字光斑 → 精准对准 ✓", font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.3)
        summary.to_edge(DOWN, buff=0.5)

        self.play(Write(summary), run_time=1.5)
        self.wait(1.0)

        # Fade out
        self.play(
            FadeOut(cantilever_group), FadeOut(cantilever_label),
            FadeOut(all_dots), FadeOut(all_labels),
            FadeOut(paper), FadeOut(paper_label),
            FadeOut(laser_group),
            #  FadeOut(trace), 
            FadeOut(scan_title),
            FadeOut(summary),
            run_time=0.8
        )
        if current_pattern_mob is not None:
            self.play(FadeOut(current_pattern_mob), run_time=0.3)

class Scene3_1_afm_adjust(Scene):
    """Scene 3 的另一种视频实现形式"""
    def construct(self):
        # ---- V-shaped cantilever geometry ----
        # Two arms forming a V opening upward
        v_tip = np.array([0.0, -1.8, 0])
        # ±45° arms: left arm at 135° (up-left), right arm at 45° (up-right)
        # With tip at y=-1.8 and top at y=1.2, height=3.0 → half-width at top = 3.0
        v_left_top = np.array([-3.0, 1.2, 0])
        v_right_top = np.array([3.0, 1.2, 0])
        arm_width = 0.25  # thickness of each arm

        # Left arm polygon (approximate a thick line as a narrow polygon)
        left_dir = v_tip - v_left_top
        left_dir_n = left_dir / np.linalg.norm(left_dir)
        left_perp = np.array([-left_dir_n[1], left_dir_n[0], 0]) * arm_width

        ArmShift = 0.18

        left_arm = Polygon(
            v_left_top + left_perp,
            v_left_top - left_perp,
            v_tip - left_perp,
            v_tip + left_perp,
            color=COLOR_CANTILEVER, fill_opacity=1, stroke_width=1.5
        ).shift(ArmShift*(RIGHT+DOWN))

        # Right arm polygon
        right_dir = v_tip - v_right_top
        right_dir_n = right_dir / np.linalg.norm(right_dir)
        right_perp = np.array([-right_dir_n[1], right_dir_n[0], 0]) * arm_width

        right_arm = Polygon(
            v_right_top + right_perp,
            v_right_top - right_perp,
            v_tip - right_perp,
            v_tip + right_perp,
            color=COLOR_CANTILEVER, fill_opacity=1, stroke_width=1.5
        ).shift(ArmShift*(LEFT+DOWN))

        cantilever_group = VGroup(left_arm, right_arm)
        cantilever_label = Text("V型悬臂 (放大)", font_size=24, color=WHITE)
        cantilever_label.next_to(cantilever_group, UP, buff=0.5)

        # ---- Position dots A-J along the V ----
        # Left arm: A(top) -> B -> C -> D(near tip)
        # Gap:   E (center gap)
        # Right arm: F(near tip) -> G -> H -> I(top)
        # Tip:   J (V-tip)

        def left_arm_pos(t):
            """t: 0=top, 1=tip"""
            return v_left_top + t * (v_tip - v_left_top)

        def right_arm_pos(t):
            """t: 0=top, 1=tip"""
            return v_right_top + t * (v_tip - v_right_top)

        # Position definitions
        # Main positions on the centerline of each arm
        # Edge positions AB/BC/CD/DJ are on the interior-facing edge of the left arm
        # (centerline + left_perp), where the laser hits the cantilever boundary → diffraction
        positions = {
            "A": left_arm_pos(0.05),
            "AB": left_arm_pos(0.15) + left_perp,
            "B": left_arm_pos(0.25),
            "BC": left_arm_pos(0.40) + left_perp,
            "C": left_arm_pos(0.55),
            "CD": left_arm_pos(0.685) + left_perp,
            "D": left_arm_pos(0.82),
            "DJ": left_arm_pos(0.91) - left_perp,
            "JF": right_arm_pos(0.91) + right_perp,
            "E": np.array([0.0, 0.2, 0]),   # gap center
            "F": right_arm_pos(0.82),
            "G": right_arm_pos(0.55),
            "H": right_arm_pos(0.25),
            "I": right_arm_pos(0.05),
            "J": v_tip + np.array([0.0, -0.05, 0]),
            "VTIP": v_tip+ np.array([0.0, -0.4, 0]),
        }

        # Spot types
        no_spot_positions = {"E"}
        diffraction_positions = {"AB", "BC", "CD", "DJ", "JF"}
        left_arm_diffraction = {"AB", "BC", "CD", "DJ"}
        right_arm_diffraction = {"JF"}

        round_spot_positions = {"A", "B", "C", "D", "J", "F"}
        cross_spot_positions = {"VTIP"}

        # ---- Create position dots and labels ----
        # Edge points (AB, BC, CD, DJ) are transition waypoints — not shown
        pos_dots = {}
        pos_labels = {}
        for name, pos in positions.items():
            if name in {"AB", "BC", "CD", "DJ", "JF", "VTIP"}:
                continue
            dot = Dot(pos, radius=0.06, color=WHITE)
            label = Text(name, font_size=16, color=WHITE)
            # Place labels offset from the dot
            if name in {"A", "B", "C", "D"}:
                label.next_to(dot, LEFT, buff=0.12)
            elif name in {"F", "G", "H", "I"}:
                label.next_to(dot, RIGHT, buff=0.12)
            elif name == "E":
                label.next_to(dot, UP, buff=0.12)
            else:  # J
                label.next_to(dot, DOWN, buff=0.12)
            pos_dots[name] = dot
            pos_labels[name] = label

        all_dots = VGroup(*pos_dots.values())
        all_labels = VGroup(*pos_labels.values())

        """
        # ---- Paper screen (right side) ----
        paper = Rectangle(width=1.8, height=2.2, color=COLOR_PAPER,
                         fill_opacity=0.9, stroke_width=2)
        paper.move_to(np.array([4.2, -0.3, 0]))
        paper_label = Text("白纸 / 光屏", font_size=20, color=BLACK)
        paper_label.next_to(paper, UP, buff=0.15)
        # Spot patterns on paper (created dynamically per position)
        
        # No-spot indicator
        no_spot_text = Text("无光斑", font_size=22, color=BLACK)
        no_spot_text.move_to(paper.get_center())
        """
        # ---- Laser scanning dot ----
        x = ValueTracker(positions["D"][0])
        y = ValueTracker(positions["D"][1])
        laser_dot = Dot((x.get_value(), y.get_value(), 0), radius=0.1, color=COLOR_LASER_SPOT)
        laser_glow_dot = Dot((x.get_value(), y.get_value(), 0), radius=0.18, color=COLOR_LASER_SPOT, fill_opacity=0.25)
        laser_dot.add_updater(lambda d: d.move_to((x.get_value(), y.get_value(), 0)))
        laser_glow_dot.add_updater(lambda g: g.move_to(laser_dot.get_center()))
        laser_group = VGroup(laser_glow_dot, laser_dot)

        # ---- Animation sequence ----
        # Draw cantilever
        self.play(FadeIn(cantilever_group), Write(cantilever_label), run_time=0.5)

        # Draw position labels
        self.play(FadeIn(all_dots), Write(all_labels), run_time=0.5)
        self.wait(0.3)
        """
        # Draw paper screen
        self.play(FadeIn(paper), Write(paper_label), run_time=0.5)
        """
        # Title
        scan_title = Text("激光扫描悬臂校准", font_size=28, color=WHITE)
        scan_title.to_edge(UP, buff=0.3)
        self.play(Write(scan_title), run_time=0.8)
        self.play(FadeIn(laser_group), run_time=0.5)

        # trace = TracedPath(laser_dot.get_center, stroke_color=YELLOW, stroke_width=2)
        # self.add(trace)

        # ---- Step through positions ----
        scan_order = ["D", "DJ", "VTIP", "J"]

        # Track the current pattern mobject
        current_pattern_mob = None

        for name in scan_order:
            target_pos = positions[name]

            # Prepare spot pattern for this position
            new_pattern = None
            if name in no_spot_positions:
                """
                new_pattern = no_spot_text.copy()
                """
                no_spot_text = Text("无光斑", font_size=22, color=BLACK).move_to(np.array([4.2, -0.3, 0]))
                new_pattern = no_spot_text
            elif name in diffraction_positions:
                new_pattern = Ellipse(width=0.12, height=0.5, color=COLOR_BLUE,
                                     fill_opacity=0.9, stroke_width=0)
                if name == "JF":
                    # new_pattern.rotate(PI / 4).move_to(paper.get_center())
                    new_pattern.rotate(PI/4).move_to(positions["JF"])
                else:
                    # new_pattern.rotate(-PI / 4).move_to(paper.get_center())
                    new_pattern.rotate(-PI / 4).move_to(positions[name])
            elif name in round_spot_positions:
                if name != "J":
                    """
                    glow = Dot(paper.get_center(), radius=0.2,
                            color=COLOR_ROUND_SPOT, fill_opacity=0.3)
                    spot = Dot(paper.get_center(), radius=0.12, color=COLOR_ROUND_SPOT)
                    new_pattern = VGroup(glow, spot)"""
                    glow = Dot(positions[name], radius=0.2,
                            color=COLOR_BLUE, fill_opacity=0.3)
                    spot = Dot(positions[name], radius=0.12, color=COLOR_BLUE)
                    new_pattern = VGroup(glow, spot)

                else:
                    """
                    glow = Dot(paper.get_center(), radius=0.2,
                            color=COLOR_ROUND_SPOT, fill_opacity=0.3)
                    spot = Dot(paper.get_center(), radius=0.12, color=COLOR_ROUND_SPOT)
                    new_pattern = VGroup(glow, spot)"""
                    J_pattern_shift = 0.2*DOWN
                    glow = Dot(positions[name] + J_pattern_shift, radius=0.2,
                            color=COLOR_BLUE, fill_opacity=0.3)
                    spot = Dot(positions[name] + J_pattern_shift, radius=0.12, color=COLOR_BLUE)
                    new_pattern = VGroup(glow, spot)

            elif name in cross_spot_positions:
                dj_ellipse = Ellipse(width=0.12, height=0.5, color=COLOR_BLUE,
                                     fill_opacity=0.9, stroke_width=0)
                dj_ellipse.rotate(-PI / 4)
                jf_ellipse = Ellipse(width=0.12, height=0.5, color=COLOR_BLUE,
                                     fill_opacity=0.9, stroke_width=0)
                jf_ellipse.rotate(PI / 4)
                # new_pattern = VGroup(dj_ellipse, jf_ellipse).move_to(paper.get_center())
                new_pattern = VGroup(dj_ellipse, jf_ellipse).move_to(positions["VTIP"])

            # Fade out old pattern
            if current_pattern_mob is not None:
                self.play(FadeOut(current_pattern_mob, run_time=0.3))

            """
            # PID-style movement toward target with jitter
            for _ in range(18):
                error_x = target_pos[0] - x.get_value()
                error_y = target_pos[1] - y.get_value()
                jitter = 0.25 * (abs(error_x) + abs(error_y)) / 8
                new_x = x.get_value() + error_x * 0.15 + np.random.uniform(-jitter, jitter)
                new_y = y.get_value() + error_y * 0.15 + np.random.uniform(-jitter, jitter)
                self.play(
                    x.animate.set_value(new_x),
                    y.animate.set_value(new_y),
                    run_time=0.06,
                    rate_func=linear
                )

            # Final snap to exact target
            self.play(
                x.animate.set_value(target_pos[0]),
                y.animate.set_value(target_pos[1]),
                run_time=0.3
            )
            """

            if new_pattern is not None:
                self.play(FadeIn(new_pattern), run_time=0.4)

            current_pattern_mob = new_pattern

            # Add note for special positions
            note = None
            if name in no_spot_positions:
                note = Text("激光未照射悬臂 → 无光斑", font_size=20, color=GREY)
            elif name in diffraction_positions:
                note = Text("边缘衍射 → 长条状光斑", font_size=20, color=COLOR_DIFFRACTION)
            elif name in round_spot_positions:
                note = Text("全反射 → 明亮圆光斑", font_size=20, color=GREEN)
                if name == "J":
                    note = Text("尖端背面全反射 → 明亮圆光斑 ✓", font_size=20, color=GREEN)
            elif name in cross_spot_positions:
                note = Text("尖端十字光斑 → 精准对准", font_size=20, color=COLOR_DIFFRACTION)

            if note:
                note.to_edge(DOWN, buff=0.4)
                self.play(Write(note), run_time=0.5)
                self.wait(0.4)
                self.play(FadeOut(note), run_time=0.3)

            self.wait(0.2)

        # ---- Summary ----
        summary = VGroup(
            Text("校准完成：激光精准对准悬臂尖端", font_size=28, color=GREEN),
            Text("十字光斑 → 精准对准 ✓", font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.3)
        summary.to_edge(DOWN, buff=0.5)

        self.play(Write(summary), run_time=1.5)
        self.wait(1.0)

        # Fade out
        self.play(
            FadeOut(cantilever_group), FadeOut(cantilever_label),
            FadeOut(all_dots), FadeOut(all_labels),
            # FadeOut(paper), FadeOut(paper_label),
            FadeOut(laser_group),
            #  FadeOut(trace), 
            FadeOut(scan_title),
            FadeOut(summary),
            run_time=0.8
        )
        if current_pattern_mob is not None:
            self.play(FadeOut(current_pattern_mob), run_time=0.3)

class Scene3_2_afm_adjust(Scene):
    def construct(self):
        # ---- V-shaped cantilever geometry ----
        # Two arms forming a V opening upward
        v_tip = np.array([0.0, -1.8, 0])
        # ±45° arms: left arm at 135° (up-left), right arm at 45° (up-right)
        # With tip at y=-1.8 and top at y=1.2, height=3.0 → half-width at top = 3.0
        v_left_top = np.array([-3.0, 1.2, 0])
        v_right_top = np.array([3.0, 1.2, 0])
        arm_width = 0.25  # thickness of each arm

        # Left arm polygon (approximate a thick line as a narrow polygon)
        left_dir = v_tip - v_left_top
        left_dir_n = left_dir / np.linalg.norm(left_dir)
        left_perp = np.array([-left_dir_n[1], left_dir_n[0], 0]) * arm_width

        ArmShift = 0.18

        left_arm = Polygon(
            v_left_top + left_perp,
            v_left_top - left_perp,
            v_tip - left_perp,
            v_tip + left_perp,
            color=COLOR_CANTILEVER, fill_opacity=1, stroke_width=1.5
        ).shift(ArmShift*(RIGHT+DOWN))

        # Right arm polygon
        right_dir = v_tip - v_right_top
        right_dir_n = right_dir / np.linalg.norm(right_dir)
        right_perp = np.array([-right_dir_n[1], right_dir_n[0], 0]) * arm_width

        right_arm = Polygon(
            v_right_top + right_perp,
            v_right_top - right_perp,
            v_tip - right_perp,
            v_tip + right_perp,
            color=COLOR_CANTILEVER, fill_opacity=1, stroke_width=1.5
        ).shift(ArmShift*(LEFT+DOWN))

        cantilever_group = VGroup(left_arm, right_arm)
        cantilever_label = Text("V型悬臂 (放大)", font_size=24, color=WHITE)
        cantilever_label.next_to(cantilever_group, UP, buff=0.5)

        # ---- Position dots A-J along the V ----
        # Left arm: A(top) -> B -> C -> D(near tip)
        # Gap:   E (center gap)
        # Right arm: F(near tip) -> G -> H -> I(top)
        # Tip:   J (V-tip)

        def left_arm_pos(t):
            """t: 0=top, 1=tip"""
            return v_left_top + t * (v_tip - v_left_top)

        def right_arm_pos(t):
            """t: 0=top, 1=tip"""
            return v_right_top + t * (v_tip - v_right_top)

        # Position definitions
        # Main positions on the centerline of each arm
        # Edge positions AB/BC/CD/DJ are on the interior-facing edge of the left arm
        # (centerline + left_perp), where the laser hits the cantilever boundary → diffraction
        positions = {
            "A": left_arm_pos(0.05),
            "AB": left_arm_pos(0.15) + left_perp,
            "B": left_arm_pos(0.25),
            "BC": left_arm_pos(0.40) + left_perp,
            "C": left_arm_pos(0.55),
            "CD": left_arm_pos(0.685) + left_perp,
            "D": left_arm_pos(0.82),
            "DJ": left_arm_pos(0.91) - left_perp,
            "JF": right_arm_pos(0.91) + right_perp,
            "E": np.array([0.0, 0.2, 0]),   # gap center
            "F": right_arm_pos(0.82),
            "G": right_arm_pos(0.55),
            "H": right_arm_pos(0.25),
            "I": right_arm_pos(0.05),
            "J": v_tip + np.array([0.0, -0.05, 0]),
            "VTIP": v_tip+ np.array([0.0, -0.4, 0]),
        }

        # Spot types
        no_spot_positions = {"E"}
        diffraction_positions = {"AB", "BC", "CD", "DJ", "JF"}
        round_spot_positions = {"A", "B", "C", "D", "J", "F"}
        cross_spot_positions = {"VTIP"}

        # ---- Create position dots and labels ----
        # Edge points (AB, BC, CD, DJ) are transition waypoints — not shown
        pos_dots = {}
        pos_labels = {}
        for name, pos in positions.items():
            if name in {"AB", "BC", "CD", "DJ", "JF", "VTIP"}:
                continue
            dot = Dot(pos, radius=0.06, color=WHITE)
            label = Text(name, font_size=16, color=WHITE)
            # Place labels offset from the dot
            if name in {"A", "B", "C", "D"}:
                label.next_to(dot, LEFT, buff=0.12)
            elif name in {"F", "G", "H", "I"}:
                label.next_to(dot, RIGHT, buff=0.12)
            elif name == "E":
                label.next_to(dot, UP, buff=0.12)
            else:  # J
                label.next_to(dot, DOWN, buff=0.12)
            pos_dots[name] = dot
            pos_labels[name] = label

        all_dots = VGroup(*pos_dots.values())
        all_labels = VGroup(*pos_labels.values())

        # ---- Paper screen (right side) ----
        paper = Rectangle(width=1.8, height=2.2, color=COLOR_PAPER,
                         fill_opacity=0.9, stroke_width=2)
        paper.move_to(np.array([4.2, -0.3, 0]))
        paper_label = Text("白纸 / 光屏", font_size=20, color=BLACK)
        paper_label.next_to(paper, UP, buff=0.15)
        # Spot patterns on paper (created dynamically per position)

        # No-spot indicator
        no_spot_text = Text("无光斑", font_size=22, color=BLACK)
        no_spot_text.move_to(paper.get_center())

        # ---- Laser scanning dot ----
        x = ValueTracker(positions["D"][0])
        y = ValueTracker(positions["D"][1])
        laser_dot = Dot((x.get_value(), y.get_value(), 0), radius=0.1, color=COLOR_LASER_SPOT)
        laser_glow_dot = Dot((x.get_value(), y.get_value(), 0), radius=0.18, color=COLOR_LASER_SPOT, fill_opacity=0.25)
        laser_dot.add_updater(lambda d: d.move_to((x.get_value(), y.get_value(), 0)))
        laser_glow_dot.add_updater(lambda g: g.move_to(laser_dot.get_center()))
        laser_group = VGroup(laser_glow_dot, laser_dot)

        # ---- Animation sequence ----
        # Draw cantilever
        self.play(FadeIn(cantilever_group), Write(cantilever_label), run_time=0.5)

        # Draw position labels
        self.play(FadeIn(all_dots), Write(all_labels), run_time=0.5)
        self.wait(0.3)

        # Draw paper screen
        self.play(FadeIn(paper), Write(paper_label), run_time=0.5)

        # Title
        scan_title = Text("激光扫描悬臂校准", font_size=28, color=WHITE)
        scan_title.to_edge(UP, buff=0.3)
        self.play(Write(scan_title), run_time=0.8)
        self.play(FadeIn(laser_group), run_time=0.5)

        trace = TracedPath(laser_dot.get_center, stroke_color=YELLOW, stroke_width=2)
        # self.add(trace)

        # ---- Step through positions ----
        scan_order = ["D", "DJ","VTIP", "J"]

        # Track the current pattern mobject
        current_pattern_mob = None

        for name in scan_order:
            target_pos = positions[name]

            # Prepare spot pattern for this position
            new_pattern = None
            if name in no_spot_positions:
                new_pattern = no_spot_text.copy()
            elif name in diffraction_positions:
                new_pattern = Ellipse(width=0.12, height=0.5, color=COLOR_DIFFRACTION,
                                     fill_opacity=0.9, stroke_width=0)
                if name == "JF":
                    new_pattern.rotate(PI / 4).move_to(paper.get_center())
                else:
                    new_pattern.rotate(-PI / 4).move_to(paper.get_center())
            elif name in round_spot_positions:
                glow = Dot(paper.get_center(), radius=0.2,
                          color=COLOR_ROUND_SPOT, fill_opacity=0.3)
                spot = Dot(paper.get_center(), radius=0.12, color=COLOR_ROUND_SPOT)
                new_pattern = VGroup(glow, spot)
            elif name in cross_spot_positions:
                dj_ellipse = Ellipse(width=0.12, height=0.5, color=COLOR_DIFFRACTION,
                                     fill_opacity=0.9, stroke_width=0)
                dj_ellipse.rotate(-PI / 4)
                jf_ellipse = Ellipse(width=0.12, height=0.5, color=COLOR_DIFFRACTION,
                                     fill_opacity=0.9, stroke_width=0)
                jf_ellipse.rotate(PI / 4)
                new_pattern = VGroup(dj_ellipse, jf_ellipse).move_to(paper.get_center())

            # Fade out old pattern
            if current_pattern_mob is not None:
                self.play(FadeOut(current_pattern_mob, run_time=0.3))

            # PID-style movement toward target with jitter
            for _ in range(18):
                error_x = target_pos[0] - x.get_value()
                error_y = target_pos[1] - y.get_value()
                jitter = 0.25 * (abs(error_x) + abs(error_y)) / 8
                new_x = x.get_value() + error_x * 0.15 + np.random.uniform(-jitter, jitter)
                new_y = y.get_value() + error_y * 0.15 + np.random.uniform(-jitter, jitter)
                self.play(
                    x.animate.set_value(new_x),
                    y.animate.set_value(new_y),
                    run_time=0.06,
                    rate_func=linear
                )

            # Final snap to exact target
            self.play(
                x.animate.set_value(target_pos[0]),
                y.animate.set_value(target_pos[1]),
                run_time=0.3
            )

            if new_pattern is not None:
                self.play(FadeIn(new_pattern), run_time=0.4)

            current_pattern_mob = new_pattern
            """
            # Add note for special positions
            note = None
            if name in no_spot_positions:
                note = Text("激光未照射悬臂 → 无光斑", font_size=20, color=GREY)
            elif name in diffraction_positions:
                note = Text("边缘衍射 → 长条状光斑", font_size=20, color=COLOR_DIFFRACTION)
            elif name in round_spot_positions:
                note = Text("全反射 → 明亮圆光斑", font_size=20, color=GREEN)
                if name == "J":
                    note = Text("尖端背面全反射 → 明亮圆光斑 ✓", font_size=20, color=GREEN)
            elif name in cross_spot_positions:
                note = Text("尖端十字光斑 → 精准对准", font_size=20, color=COLOR_DIFFRACTION)

            if note:
                note.to_edge(DOWN, buff=0.4)
                self.play(Write(note), run_time=0.5)
                self.wait(0.4)
                self.play(FadeOut(note), run_time=0.3)

            self.wait(0.2)
            """
        """ 
        # ---- Summary ----
        summary = VGroup(
            Text("校准完成：激光精准对准悬臂尖端", font_size=28, color=GREEN),
            Text("十字光斑 → 精准对准 ✓", font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.3)
        summary.to_edge(DOWN, buff=0.5)
        
        self.play(Write(summary), run_time=1.5)
        self.wait(1.0)"""

        # Fade out
        self.play(
            FadeOut(cantilever_group), FadeOut(cantilever_label),
            FadeOut(all_dots), FadeOut(all_labels),
            FadeOut(paper), FadeOut(paper_label),
            FadeOut(laser_group),
            #  FadeOut(trace), 
            FadeOut(scan_title),
            # FadeOut(summary),
            run_time=0.8
        )
        if current_pattern_mob is not None:
            self.play(FadeOut(current_pattern_mob), run_time=0.3)
