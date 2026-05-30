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
这是一个俯视图
这是一张关于某种探针或显微器件（很可能是原子力显微镜或近场光学显微镜的探针）的结构示意图。

图片包含以下主要元素和标注，从上到下依次为：

1. **探针架 (TipHolder)**：最上方的深灰色矩形块，用于固定装置。
2. **玻璃体 (Chip)**：中间较浅灰色的矩形块，位于探针架下方。
3. **三角悬臂 (Cantilever)**：最下方一个向下突出的"V"字型结构，通常带有微小的探针尖端。
4. **尺寸标注**：右侧有一个双向箭头，标明了玻璃体底端到悬臂最底端之间的距离为 **1-2mm**。

图片整体采用黑、白、灰三种颜色，用简单的几何图形和文字表示器件的层级关系及尺寸结构。
"""

# 这里是先将激光光点调节至探针架区域
# 顺时针旋转激光器位置垂直调节旋钮，直到激光落到探针架或探针基片上。
# 此时在探头正面观察，可看到一个很亮的激光光点。
# 由于激光完全被遮挡，提起探头观察，探头下方没有透射的激光光斑。
class Scene1_afm_adjust(Scene):
    def construct(self):
        # ---- Color / size constants ----
        holder_w, holder_h = 3.0, 0.9
        chip_w, chip_h = 2.6, 0.8
        cantilever_w, cantilever_h = 1.8, 1.2
        gap = 0.15

        # ---- 1. TipHolder (top) ----
        tip_holder = Rectangle(width=holder_w, height=holder_h,
                               color=COLOR_TIP_HOLDER, fill_opacity=0.85, stroke_width=1)
        tip_holder.move_to(UP * 1.5)

        holder_label = Text("探针架 (Tip Holder)", font_size=22, color=WHITE)
        holder_label.next_to(tip_holder, UP, buff=0.25)

        # ---- 2. Chip (middle) ----
        chip = Rectangle(width=chip_w, height=chip_h,
                        color=COLOR_CHIP, fill_opacity=0.75, stroke_width=1)
        chip.next_to(tip_holder, DOWN, buff=gap)

        chip_label = Text("玻璃基片 (Chip)", font_size=22, color=WHITE)
        chip_label.next_to(chip, LEFT, buff=0.6).shift(UP * 0.1)

        # ---- 3. Cantilever (V-shape, bottom) ----
        c_top_y = chip.get_bottom()[1] - gap
        c_tip_y = c_top_y - cantilever_h
        c_half_w = cantilever_w / 2

        cantilever_poly = Polygon(
            [-c_half_w, c_top_y, 0],
            [c_half_w, c_top_y, 0],
            [0, c_tip_y, 0],
            color=COLOR_CANTILEVER, fill_opacity=0.8, stroke_width=1.5
        )

        c_label = Text("三角悬臂 (Cantilever)", font_size=22, color=WHITE)
        c_label.next_to(cantilever_poly, DOWN, buff=0.25)

        # ---- 4. Dimension annotation (right side) ----
        arrow_top_y = chip.get_bottom()[1]
        arrow_bot_y = c_tip_y
        arrow_x = chip.get_right()[0] + 1.0

        dim_arrow = DoubleArrow(
            start=[arrow_x, arrow_top_y, 0],
            end=[arrow_x, arrow_bot_y, 0],
            color=WHITE, stroke_width=3,
            tip_length=0.15, buff=0
        )

        dim_label = MathTex(r"1{-}2\,\text{mm}", font_size=28, color=WHITE)
        dim_label.next_to(dim_arrow, RIGHT, buff=0.2)

        # ---- 5. Laser spot ----
        laser_dot = Dot(radius=0.1, color=COLOR_LASER_SPOT)
        laser_glow = Dot(radius=0.2, color=COLOR_LASER_SPOT, fill_opacity=0.3)
        laser = VGroup(laser_glow, laser_dot)

        # Start laser on tip holder
        laser.move_to(tip_holder.get_center())

        # ---- Animation sequence ----
        # Fade in structure
        self.play(FadeIn(tip_holder), Write(holder_label), run_time=0.8)
        self.play(FadeIn(chip), Write(chip_label), run_time=0.8)
        self.play(FadeIn(cantilever_poly), Write(c_label), run_time=0.8)

        # Dimension arrow
        self.play(GrowFromCenter(dim_arrow), Write(dim_label), run_time=1.0)
        self.wait(0.3)

        # Laser appears on TipHolder
        laser.move_to(tip_holder.get_center() + DOWN * 0.1)
        self.play(FadeIn(laser, scale=0.5), run_time=0.6)
        self.wait(0.3)

        # Laser blocked note
        block_note = Text("激光完全被遮挡\n下方无透射光斑", font_size=26,
                         color=COLOR_LASER, line_spacing=0.5)
        block_note.to_edge(DOWN, buff=0.6)
        self.play(Write(block_note), run_time=1.2)
        self.wait(0.8)
        self.play(FadeOut(block_note), run_time=0.5)

        # Laser moves down to chip
        self.play(laser.animate.move_to(chip.get_center()), run_time=1.5)

        # Bright spot note
        bright_note = Text("正面观察: 可见明亮激光光点", font_size=26, color=COLOR_GREEN)
        bright_note.to_edge(DOWN, buff=0.6)
        self.play(Write(bright_note), run_time=1.0)
        self.wait(1.0)

        # Fade out
        self.play(
            FadeOut(tip_holder), FadeOut(holder_label),
            FadeOut(chip), FadeOut(chip_label),
            FadeOut(cantilever_poly), FadeOut(c_label),
            FadeOut(dim_arrow), FadeOut(dim_label),
            FadeOut(laser), FadeOut(bright_note),
            run_time=0.8
        )


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
        # ---- Block geometry (trapezoid side view) ----
        # Corners of the trapezoidal block
        top_left = np.array([-1.0, 1.5, 0])
        top_right = np.array([2.0, 1.5, 0])
        bot_right = np.array([2.0, -0.8, 0])
        bot_left = np.array([-1.8, -0.8, 0])

        block = Polygon(
            top_left, top_right, bot_right, bot_left,
            color=COLOR_BLOCK, fill_opacity=0.7, stroke_width=2
        )

        # Probe tip (small triangle at bottom)
        tip_apex = np.array([-0.2, -1.6, 0])
        tip_left = np.array([-0.5, -0.85, 0])
        tip_right = np.array([0.1, -0.85, 0])
        probe_tip = Polygon(
            tip_left, tip_right, tip_apex,
            color=COLOR_PROBE_TIP, fill_opacity=0.9, stroke_width=1
        )

        # ---- Labels ----
        block_label = Text("探针基片 (侧视图)", font_size=24, color=WHITE)
        block_label.next_to(block, UP, buff=0.4)

        top_surface_label = Text("顶部水平面", font_size=20, color=WHITE)
        top_surface_label.next_to(block.get_top(), UP, buff=0.15).shift(LEFT * 0.3)

        left_surface_label = Text("斜面", font_size=20, color=WHITE)
        left_surface_label.move_to([-2.3, 0.35, 0])

        tip_label = Text("探针", font_size=18, color=WHITE)
        tip_label.next_to(probe_tip, DOWN, buff=0.15)

        # ---- Laser Beam A (top surface, horizontal) ----
        # Incident from upper-right to top surface
        inc_A_start = np.array([2.8, 2.5, 0])
        inc_A_hit = np.array([0.5, 1.5, 0])
        inc_A_vec = inc_A_hit - inc_A_start
        inc_A_dir = inc_A_vec / np.linalg.norm(inc_A_vec)

        # Top surface normal = (0, 1)
        normal_top = np.array([0.0, 1.0, 0.0])
        ref_A_dir = inc_A_dir - 2 * np.dot(inc_A_dir, normal_top) * normal_top
        ref_A_end = inc_A_hit + ref_A_dir * 2.8

        laser_A_in = Arrow(inc_A_start, inc_A_hit, color=COLOR_LASER,
                          buff=0, stroke_width=2.5, tip_length=0.12)
        laser_A_out = Arrow(inc_A_hit, ref_A_end, color=COLOR_LASER,
                           buff=0, stroke_width=2.5, tip_length=0.12)

        label_A = MathTex(r"A", font_size=36, color=RED)
        label_A.move_to(ref_A_end + ref_A_dir * 0.3)

        # ---- Laser Beam B (left sloped surface) ----
        # Surface from bot_left to top_left
        surf_vec = top_left - bot_left  # (0.8, 2.3)
        surf_len = np.linalg.norm(surf_vec)
        surf_dir = surf_vec / surf_len
        # Outward normal (pointing left)
        normal_left = np.array([-surf_dir[1], surf_dir[0], 0])

        # Hit point on left surface
        inc_B_hit = np.array([-1.35, 0.4, 0])
        inc_B_start = np.array([2.5, 2.2, 0])
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

        laser_label_A = Text("Laser", font_size=20, color=COLOR_LASER)
        laser_label_A.next_to(laser_A_in, RIGHT, buff=0.1).shift(UP * 0.3)

        # ---- Animation: Block + Probe ----
        self.play(FadeIn(block), run_time=1.0)
        self.play(Write(block_label), run_time=0.5)
        self.play(Write(top_surface_label), Write(left_surface_label), run_time=0.8)
        self.play(FadeIn(probe_tip), Write(tip_label), run_time=0.8)
        self.wait(0.3)

        # ---- Show Beam A ----
        self.play(GrowArrow(laser_A_in), GrowArrow(laser_A_out),
                 Write(laser_label_A), run_time=1.2)
        self.play(Write(label_A), run_time=0.5)
        self.wait(0.5)

        # ---- Show Beam B ----
        laser_label_B = Text("Laser", font_size=20, color=COLOR_LASER)
        laser_label_B.next_to(laser_B_in, RIGHT, buff=0.1)
        self.play(GrowArrow(laser_B_in), GrowArrow(laser_B_out),
                 Write(laser_label_B), run_time=1.2)
        self.play(Write(label_B), run_time=0.5)
        self.wait(0.8)

        # ---- Adjustment explanation ----
        adj_text_1 = Text("调节水平旋钮 → 激光移至基片中间", font_size=26, color=WHITE)
        adj_text_1.to_edge(DOWN, buff=0.5)

        self.play(
            FadeOut(laser_A_in), FadeOut(laser_A_out), FadeOut(label_A),
            FadeOut(laser_B_in), FadeOut(laser_B_out), FadeOut(label_B),
            FadeOut(laser_label_A), FadeOut(laser_label_B),
            run_time=0.6
        )

        self.play(Write(adj_text_1), run_time=1.0)
        self.wait(0.5)
        self.play(FadeOut(adj_text_1), run_time=0.4)

        # Show reflected spot and animate movement
        first_hit = top_left + (top_right - top_left) * 0.8
        first_src = np.array([3.0, 3.0, 0])
        first_vec = first_hit - first_src
        first_dir = first_vec / np.linalg.norm(first_vec)
        first_ref_dir = first_dir - 2 * np.dot(first_dir, normal_top) * normal_top
        first_ref = first_hit + first_ref_dir * 2.0
        spot_dot = Dot(first_ref, radius=0.1, color=COLOR_LASER_SPOT)
        self.play(FadeIn(spot_dot), run_time=0.5)

        # Animate spot moving toward cantilever edge
        edge_hit = top_left + (top_right - top_left) * 0.3
        edge_vec = edge_hit - first_src
        edge_dir = edge_vec / np.linalg.norm(edge_vec)
        edge_ref_dir = edge_dir - 2 * np.dot(edge_dir, normal_top) * normal_top
        edge_ref = edge_hit + edge_ref_dir * 2.0
        self.play(spot_dot.animate.move_to(edge_ref), run_time=2.5, rate_func=linear)

        # Laser near cantilever region
        edge_note = Text("激光移至悬臂边缘区域", font_size=26, color=COLOR_GREEN)
        edge_note.to_edge(DOWN, buff=0.5)
        self.play(Write(edge_note), run_time=0.8)

        # Reflection now goes downward in front of probe
        front_dot = Dot([-0.5, -2.2, 0], radius=0.12, color=COLOR_LASER_SPOT)
        self.play(FadeIn(front_dot), run_time=0.5)

        front_label = Text("反射光斑落在探头前方", font_size=22, color=WHITE)
        front_label.next_to(front_dot, DOWN, buff=0.2)
        self.play(Write(front_label), run_time=0.8)
        self.wait(1.0)

        # Fade all
        self.play(
            FadeOut(block), FadeOut(block_label),
            FadeOut(top_surface_label), FadeOut(left_surface_label),
            FadeOut(probe_tip), FadeOut(tip_label),
            FadeOut(spot_dot), FadeOut(edge_note),
            FadeOut(front_dot), FadeOut(front_label),
            run_time=0.8
        )


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
        v_left_top = np.array([-2.2, 1.2, 0])
        v_right_top = np.array([2.2, 1.2, 0])
        arm_width = 0.25  # thickness of each arm

        # Left arm polygon (approximate a thick line as a narrow polygon)
        left_dir = v_tip - v_left_top
        left_dir_n = left_dir / np.linalg.norm(left_dir)
        left_perp = np.array([-left_dir_n[1], left_dir_n[0], 0]) * arm_width

        left_arm = Polygon(
            v_left_top + left_perp,
            v_left_top - left_perp,
            v_tip - left_perp,
            v_tip + left_perp,
            color=COLOR_CANTILEVER, fill_opacity=0.85, stroke_width=1.5
        )

        # Right arm polygon
        right_dir = v_tip - v_right_top
        right_dir_n = right_dir / np.linalg.norm(right_dir)
        right_perp = np.array([-right_dir_n[1], right_dir_n[0], 0]) * arm_width

        right_arm = Polygon(
            v_right_top + right_perp,
            v_right_top - right_perp,
            v_tip - right_perp,
            v_tip + right_perp,
            color=COLOR_CANTILEVER, fill_opacity=0.85, stroke_width=1.5
        )

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
        positions = {
            "A": left_arm_pos(0.05),
            "B": left_arm_pos(0.25),
            "C": left_arm_pos(0.55),
            "D": left_arm_pos(0.82),
            "E": np.array([0.0, 0.2, 0]),   # gap center
            "F": right_arm_pos(0.82),
            "G": right_arm_pos(0.55),
            "H": right_arm_pos(0.25),
            "I": right_arm_pos(0.05),
            "J": v_tip + np.array([0.0, -0.05, 0]),
        }

        # Spot types
        no_spot_positions = {"A", "E", "I"}
        diffraction_positions = {"B", "D", "F", "H"}
        round_spot_positions = {"C", "G", "J"}

        # ---- Create position dots and labels ----
        pos_dots = {}
        pos_labels = {}
        for name, pos in positions.items():
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
        paper.move_to([3.8, -0.3, 0])
        paper_label = Text("白纸 / 光屏", font_size=20, color=BLACK)
        paper_label.next_to(paper, UP, buff=0.15)

        # Spot patterns on paper (created dynamically per position)

        # No-spot indicator
        no_spot_text = Text("无光斑", font_size=22, color=BLACK)
        no_spot_text.move_to(paper.get_center())

        # ---- Laser scanning dot ----
        laser_dot = Dot(positions["A"], radius=0.1, color=COLOR_LASER_SPOT)
        laser_glow_dot = Dot(positions["A"], radius=0.18, color=COLOR_LASER_SPOT, fill_opacity=0.25)
        laser_group = VGroup(laser_glow_dot, laser_dot)

        # ---- Animation sequence ----
        # Draw cantilever
        self.play(FadeIn(cantilever_group), Write(cantilever_label), run_time=1.2)

        # Draw position labels
        self.play(FadeIn(all_dots), Write(all_labels), run_time=1.5)
        self.wait(0.3)

        # Draw paper screen
        self.play(FadeIn(paper), Write(paper_label), run_time=1.0)

        # Title
        scan_title = Text("激光扫描悬臂校准", font_size=28, color=WHITE)
        scan_title.to_edge(UP, buff=0.3)
        self.play(Write(scan_title), run_time=0.8)

        # ---- Step through positions A → J ----
        scan_order = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

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
                new_pattern.rotate(PI / 6).move_to(paper.get_center())
            elif name in round_spot_positions:
                glow = Dot(paper.get_center(), radius=0.2,
                          color=COLOR_ROUND_SPOT, fill_opacity=0.3)
                spot = Dot(paper.get_center(), radius=0.12, color=COLOR_ROUND_SPOT)
                new_pattern = VGroup(glow, spot)

            # Animate laser moving + pattern update
            anims = [laser_group.animate.move_to(target_pos)]
            if current_pattern_mob is not None:
                anims.append(FadeOut(current_pattern_mob, run_time=0.3))
            self.play(*anims, run_time=0.6)

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
                note = Text("全反射 → 明亮圆光斑", font_size=20, color=COLOR_GREEN)
                if name == "J":
                    note = Text("尖端背面全反射 → 明亮圆光斑 ✓", font_size=20, color=COLOR_GREEN)

            if note:
                note.to_edge(DOWN, buff=0.4)
                self.play(Write(note), run_time=0.5)
                self.wait(0.4)
                self.play(FadeOut(note), run_time=0.3)

            self.wait(0.2)

        # ---- Summary ----
        summary = VGroup(
            Text("校准完成：激光精准对准悬臂尖端 (J)", font_size=28, color=COLOR_GREEN),
            Text("明亮圆光斑 → 进入探测器中心", font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.3)
        summary.to_edge(DOWN, buff=0.5)

        self.play(Write(summary), run_time=1.5)
        self.wait(2.0)

        # Fade out
        self.play(
            FadeOut(cantilever_group), FadeOut(cantilever_label),
            FadeOut(all_dots), FadeOut(all_labels),
            FadeOut(paper), FadeOut(paper_label),
            FadeOut(laser_group), FadeOut(scan_title),
            FadeOut(summary),
            run_time=0.8
        )
        if current_pattern_mob is not None:
            self.play(FadeOut(current_pattern_mob), run_time=0.3)
