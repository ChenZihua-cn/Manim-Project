"""
原子力显微镜微视频 - Manim Community Edition 完整脚本
五个镜头，总时长40秒
分辨率: 1920x1080, 帧率: 30fps
"""

# trunk-ignore(ruff/F403)
# pyright: ignore[reportWildcardImportFromLibrary]

from manim import *
import numpy as np

# =============================================================================
# 全局配置
# =============================================================================
config.frame_rate = 30
config.background_color = BLACK
config.pixel_width = 1920
config.pixel_height = 1080

# 颜色定义（按照规范）
COLOR_PROBABILITY = "#FFC107"  # 概率密度曲线 - 黄/橙
COLOR_CLOUD = "#1E88E5"        # 高斯云团 - 半透明蓝
COLOR_NODE = "#FFFFFF"         # 节点线 - 白
COLOR_PAULI = "#E53935"        # 泡利排斥力/势 - 红
COLOR_VDW = "#1E88E5"          # 范德华力 - 蓝
COLOR_LASER = "#FF0000"        # 激光 - 红
COLOR_DETECTOR = "#43A047"     # 探测器/信号 - 绿
COLOR_EQUILIBRIUM = "#FFEB3B"  # 平衡点/高亮 - 黄


# =============================================================================
# 镜头1：波函数的复数本质与概率诠释（7秒）
# =============================================================================
class Scene1_WaveFunctionComplex(Scene):
    """
    展示波函数的复数本质：复平面轨迹 + 概率密度转换
    时长：7秒
    """
    
    def phase_to_color(self, phase):
        """将相位 [-π, π] 映射为 RGB 色相"""
        hue = (phase + PI) / (2 * PI)  # 归一化到 [0,1]
        return ManimColor.from_hsv((hue, 1.0, 1.0))
    
    def construct(self):
        # 1. 标题（0-1秒）
        title = Text("波函数的复数本质", font_size=36, color=WHITE).to_edge(UP)
        self.play(Write(title), run_time=1)
        
        # 2. 复数平面（1-2秒）
        c_plane = ComplexPlane(
            x_range=[-3, 3], y_range=[-2, 2],
            background_line_style={"stroke_color": GREY, "stroke_width": 1}
        ).add_coordinates()
        c_plane.scale(0.9).shift(LEFT * 2 + UP * 0.5)
        
        # 添加坐标轴标签
        re_label = MathTex(r"\text{Re}", font_size=24, color=GREY).next_to(c_plane.x_axis, RIGHT)
        im_label = MathTex(r"\text{Im}", font_size=24, color=GREY).next_to(c_plane.y_axis, UP)
        
        self.play(Create(c_plane), Write(re_label), Write(im_label), run_time=1)
        
        # 3. 相位色轮图例（右上角）
        color_wheel = Circle(radius=0.6, color=WHITE, stroke_width=2)
        color_wheel.to_corner(UR).shift(LEFT * 1.5 + DOWN * 0.5)
        
        # 创建色轮填充
        wheel_sectors = VGroup()
        n_sectors = 36
        for i in range(n_sectors):
            angle_start = i * 2 * PI / n_sectors
            angle_end = (i + 1) * 2 * PI / n_sectors
            hue = i / n_sectors
            color = ManimColor.from_hsv((hue, 1.0, 1.0))
            sector = AnnularSector(
                inner_radius=0, outer_radius=0.6,
                angle=angle_end - angle_start,
                start_angle=angle_start,
                color=color, fill_opacity=1, stroke_width=0
            )
            wheel_sectors.add(sector)
        wheel_sectors.move_to(color_wheel)
        
        # 色轮标注
        phase_labels = VGroup(
            MathTex(r"0", font_size=20, color=WHITE).next_to(color_wheel, RIGHT, buff=0.1),
            MathTex(r"\pi", font_size=20, color=WHITE).next_to(color_wheel, LEFT, buff=0.1),
            MathTex(r"2\pi", font_size=20, color=WHITE).next_to(color_wheel, RIGHT, buff=0.1).shift(DOWN * 0.5)
        )
        
        self.play(Create(color_wheel), FadeIn(wheel_sectors), run_time=0.5)
        
        # 4. 复数波函数曲线（2-4秒）
        x_min, x_max = -3, 3
        x0, sigma, k = 0, 0.5, 4
        
        def complex_psi(x):
            envelope = np.exp(-((x - x0)**2) / (2 * sigma**2))
            phase = k * x
            return envelope * (np.cos(phase) + 1j * np.sin(phase))
        
        # 创建带相位颜色的曲线（分割为小段）
        n_segments = 100
        curve_segments = VGroup()
        colors = []
        points = []
        
        for i in range(n_segments + 1):
            t = x_min + (x_max - x_min) * i / n_segments
            psi_val = complex_psi(t)
            point = c_plane.coords_to_point(psi_val.real, psi_val.imag)
            points.append(point)
            phase = np.angle(psi_val)
            colors.append(self.phase_to_color(phase))
        
        for i in range(n_segments):
            line = Line(points[i], points[i+1], stroke_width=4)
            line.set_color(colors[i])
            curve_segments.add(line)
        
        phase_label = MathTex(r"\text{Phase } \phi(x)", font_size=28, color=WHITE)
        phase_label.next_to(c_plane, RIGHT, buff=0.8).shift(UP * 1.5)
        
        self.play(Create(curve_segments), Write(phase_label), run_time=2)
        self.wait(0.5)
        
        # 5. 转换到概率密度 |ψ|²（4-6秒）
        axes_real = Axes(
            x_range=[-3, 3], y_range=[0, 1.5],
            x_length=6, y_length=3,
            axis_config={"include_tip": False},
            x_axis_config={"numbers_to_include": np.arange(-3, 4, 1)},
            y_axis_config={"numbers_to_include": [0, 1]}
        ).shift(DOWN * 1.5)
        
        prob_curve = axes_real.plot(
            lambda x: np.exp(-((x - x0)**2) / sigma**2),
            x_range=[-3, 3],
            color=COLOR_PROBABILITY
        )
        
        fill = axes_real.get_area(prob_curve, x_range=(-1, 1), color=COLOR_PROBABILITY, opacity=0.3)
        
        # 先淡出复平面相关内容
        self.play(
            FadeOut(c_plane), FadeOut(re_label), FadeOut(im_label),
            FadeOut(curve_segments), FadeOut(phase_label),
            FadeOut(color_wheel), FadeOut(wheel_sectors),
            run_time=1.5
        )
        # 再淡入实数轴概率密度
        self.play(
            FadeIn(axes_real), Create(prob_curve), FadeIn(fill),
            run_time=1.5
        )
        
        # 6. 积分公式（6-7秒）
        integral = MathTex(
            r"P(a \leq x \leq b) = \int_a^b |\psi(x)|^2 dx",
            font_size=32, color=WHITE
        ).next_to(axes_real, UP, buff=0.5)
        
        self.play(Write(integral), run_time=0.5)
        
        # 高亮积分区域
        self.play(Indicate(fill, scale_factor=1.1, color=RED), run_time=0.5)
        self.wait(0.5)
        
        # 清理（用于转场）
        self.play(FadeOut(integral), run_time=0.3)
        self.play(
            FadeOut(title), FadeOut(axes_real), FadeOut(prob_curve), FadeOut(fill),
            run_time=0.5
        )


# =============================================================================
# 镜头2：全同粒子与反对称化（13秒）
# =============================================================================
class Scene2_SlaterDeterminant(Scene):
    """
    展示全同粒子的不可区分性和Slater行列式
    时长：13秒
    """
    
    def construct(self):
        # 1. 初始化坐标轴和两个高斯云团（0-1秒）
        axes = Axes(
            x_range=[-3, 3], y_range=[-0.5, 2],
            x_length=8, y_length=3,
            axis_config={"include_numbers": False, "include_tip": False}
        ).shift(LEFT * 2 + DOWN * 0.5)
        
        self.add(axes)
        
        # 定义高斯函数
        def gaussian(x, center, sigma=0.5):
            return np.exp(-((x - center)**2) / (2 * sigma**2))
        
        # ValueTracker控制云团位置
        tracker1 = ValueTracker(-1.5)
        tracker2 = ValueTracker(1.5)
        
        # 动态云团曲线
        cloud1 = always_redraw(lambda: axes.plot(
            lambda x: gaussian(x, tracker1.get_value()),
            x_range=[-3, 3],
            color=COLOR_CLOUD, stroke_width=3
        ))
        
        cloud2 = always_redraw(lambda: axes.plot(
            lambda x: gaussian(x, tracker2.get_value()),
            x_range=[-3, 3],
            color=COLOR_CLOUD, stroke_width=3
        ))
        
        # 半透明填充 - 先创建静态曲线用于get_area
        cloud1_static = axes.plot(
            lambda x: gaussian(x, tracker1.get_value()),
            x_range=[-3, 3],
            color=COLOR_CLOUD, stroke_width=3
        )
        cloud2_static = axes.plot(
            lambda x: gaussian(x, tracker2.get_value()),
            x_range=[-3, 3],
            color=COLOR_CLOUD, stroke_width=3
        )
        fill1 = always_redraw(lambda: axes.get_area(
            cloud1_static, x_range=(-3, 3), opacity=0.4, color=COLOR_CLOUD
        ))
        fill2 = always_redraw(lambda: axes.get_area(
            cloud2_static, x_range=(-3, 3), opacity=0.4, color=COLOR_CLOUD
        ))
        
        self.add(cloud1, cloud2, fill1, fill2)
        
        # 2. 云团缓慢靠近（1-3秒）
        self.play(
            tracker1.animate.set_value(-0.5),
            tracker2.animate.set_value(0.5),
            run_time=2, rate_func=linear
        )
        
        # 3. Slater行列式（3-4.5秒）
        slater = MathTex(
            r"\Psi(\mathbf{r}_1,\mathbf{r}_2) = \frac{1}{\sqrt{2}}"
            r"\begin{vmatrix} \phi_a(\mathbf{r}_1) & \phi_a(\mathbf{r}_2) \\"
            r"\phi_b(\mathbf{r}_1) & \phi_b(\mathbf{r}_2) \end{vmatrix}",
            font_size=36, color=WHITE
        ).to_edge(UP).shift(LEFT * 1)
        
        # 自旋标注
        spin_label = Text("相同自旋 (↑↑)", font_size=24, color=RED).next_to(slater, RIGHT, buff=0.5)
        
        self.play(Write(slater), Write(spin_label), run_time=1.5)
        
        # 4. 展开行列式（4.5-6秒）
        expanded = MathTex(
            r"= \frac{1}{\sqrt{2}}\Big[ \phi_a(\mathbf{r}_1)\phi_b(\mathbf{r}_2) - \phi_a(\mathbf{r}_2)\phi_b(\mathbf{r}_1) \Big]",
            font_size=36, color=WHITE
        ).move_to(slater)
        
        self.play(TransformMatchingTex(slater, expanded), run_time=1.5)
        
        # 5. 云团继续靠近，出现节点线（6-7.5秒）
        self.play(
            tracker1.animate.set_value(-0.2),
            tracker2.animate.set_value(0.2),
            run_time=1.5, rate_func=linear
        )
        
        # 节点线
        node_line = DashedLine(
            start=axes.c2p(0, 0), end=axes.c2p(0, 1.5),
            color=COLOR_NODE, stroke_width=3
        )
        
        self.play(Create(node_line), run_time=0.5)
        
        # 6. 完全重合，显示Ψ=0（7.5-10秒）
        self.play(
            tracker1.animate.set_value(0),
            tracker2.animate.set_value(0),
            run_time=1.5, rate_func=linear
        )
        
        # 重叠区域变暗表示概率为零
        overlap_plot = axes.plot(lambda x: gaussian(x, 0), x_range=[-3, 3], color=BLACK)
        overlap_region = axes.get_area(
            overlap_plot,
            x_range=(-1, 1), color=BLACK, opacity=0.7
        )
        
        zero_eq = MathTex(r"\Psi = 0", font_size=48, color=RED)
        zero_eq.move_to(expanded)
        
        self.play(
            Transform(expanded, zero_eq),
            FadeIn(overlap_region),
            run_time=1
        )
        
        # 7. 节点线闪烁（10-10.5秒）
        self.play(Flash(node_line, color=YELLOW), run_time=0.5)
        
        # 8. 保持显示（10.5-13秒）
        self.wait(2.5)
        
        # 清理转场
        self.play(FadeOut(expanded), FadeOut(spin_label), run_time=0.3)
        self.play(
            FadeOut(axes), FadeOut(cloud1), FadeOut(cloud2),
            FadeOut(fill1), FadeOut(fill2), FadeOut(node_line), FadeOut(overlap_region),
            run_time=0.5
        )


# =============================================================================
# 镜头3：从量子原理到指数排斥势（8秒）
# =============================================================================
class Scene3_ExponentialPauliRepulsion(Scene):
    """
    展示波函数节点与动能增加，引出指数排斥势
    时长：8秒
    """
    
    def construct(self):
        # 1. 波函数节点示意图（0-2秒）
        axes = Axes(
            x_range=[-2, 2], y_range=[-0.5, 1.5],
            x_length=6, y_length=3,
            axis_config={"include_numbers": False, "include_tip": False}
        ).shift(LEFT * 3 + UP * 1)
        
        # 有节点的波函数: ψ(x) = |x| * exp(-x²)
        psi_with_node = axes.plot(
            lambda x: np.abs(x) * np.exp(-x**2),
            x_range=[-2, 2],
            color=COLOR_CLOUD
        )
        
        # 节点标记
        node_dot = Dot(axes.c2p(0, 0), color=RED, radius=0.08)
        node_label = MathTex(r"\text{Node}", font_size=24, color=RED).next_to(node_dot, DOWN).shift(RIGHT * 0.7)
        
        # 曲率标注
        curvature_arrow = CurvedArrow(
            axes.c2p(0.5, 0.3), axes.c2p(1.2, 0.8),
            color=YELLOW, angle=-PI/4
        )
        curvature_text = MathTex(r"\text{High curvature} \Rightarrow \text{High } E_k", font_size=26, color=WHITE)
        curvature_text.next_to(axes, RIGHT, buff=0.5)
        
        self.play(Create(axes), Create(psi_with_node), run_time=1)
        self.play(FadeIn(node_dot), Write(node_label), run_time=0.5)
        self.play(Create(curvature_arrow), Write(curvature_text), run_time=0.5)
        
        # 2. 指数势公式（2-4秒）
        V_formula = MathTex(
            r"V(z) = A e^{-2z / \lambda}",
            font_size=48, color=WHITE
        ).to_edge(DOWN).shift(UP * 1)
        
        # 高亮参数
        V_formula.set_color_by_tex("A", YELLOW)
        V_formula.set_color_by_tex("\\lambda", BLUE)
        
        self.play(Write(V_formula), run_time=2)
        
        # 3. 力公式（4-5秒）
        F_formula = MathTex(
            r"F(z) = -\frac{dV}{dz} = \frac{2A}{\lambda} e^{-2z / \lambda}",
            font_size=42, color=WHITE
        ).next_to(V_formula, DOWN, buff=0.5)
        
        self.play(Write(F_formula), run_time=1)
        
        # 4. 力曲线小图（5-7秒）
        small_axes = Axes(
            x_range=[0, 2], y_range=[0, 5],
            x_length=4, y_length=2.5,
            axis_config={"include_tip": False},
            x_axis_config={"numbers_to_include": [0, 1, 2]},
            y_axis_config={"numbers_to_include": [0, 2, 4]}
        ).to_corner(DR).shift(LEFT * 0.5 + UP * 0.5)
        
        small_axes_labels = VGroup(
            MathTex(r"z", font_size=20).next_to(small_axes.x_axis, RIGHT),
            MathTex(r"F", font_size=20).next_to(small_axes.y_axis, UP)
        )
        
        # 力曲线 (λ = 0.3)
        decay_len = 0.3  # 避免使用lambda作为变量名
        force_curve = small_axes.plot(
            lambda z: 2 * np.exp(-2 * z / decay_len),
            x_range=[0, 2],
            color=COLOR_PAULI
        )
        
        self.play(Create(small_axes), Write(small_axes_labels), Create(force_curve), run_time=1.5)
        
        # 5. 标注短程性（7-8秒）
        range_arrow = DoubleArrow(
            small_axes.c2p(0, 0.3), small_axes.c2p(0.6, 0.3),
            color=COLOR_EQUILIBRIUM, buff=0
        ).scale(0.7)
        range_label = MathTex(r"\text{Short range: } z \gtrsim 2\lambda", font_size=22, color=WHITE)
        range_label.next_to(range_arrow, UP, buff=0.1).shift(RIGHT * 1)
        
        self.play(GrowArrow(range_arrow), Write(range_label), run_time=1)
        
        # 转场准备：将公式移到右上角
        V_target = V_formula.copy().scale(0.5).to_corner(UR)
        self.play(Transform(V_formula, V_target), run_time=0.5)
        
        self.wait(0.5)
        
        # 清理
        self.play(
            FadeOut(axes), FadeOut(psi_with_node), FadeOut(node_dot), FadeOut(node_label),
            run_time=0.4
        )
        self.play(
            FadeOut(curvature_arrow), FadeOut(curvature_text),
            FadeOut(F_formula), FadeOut(V_formula),
            run_time=0.4
        )
        self.play(
            FadeOut(small_axes), FadeOut(small_axes_labels),
            FadeOut(force_curve), FadeOut(range_arrow), FadeOut(range_label),
            run_time=0.4
        )


# =============================================================================
# 镜头4：频移检测原理（7秒）
# =============================================================================
class Scene4_FrequencyShiftDetection(Scene):
    """
    展示AFM探针在样品表面扫描成像：
    探针沿表面行进，悬臂梁随形貌起伏偏转，
    激光反射至四象限探测器，实时绘制形貌曲线。
    时长：~8秒
    """

    def construct(self):
        # ---- 表面形貌定义 ----
        def surface_profile(x):
            """样品表面：多个不同高度和宽度的特征"""
            h = 0.0
            h += 0.25 * np.exp(-((x + 1.5) ** 2) / 0.25)   # 左凸起
            h += 0.35 * np.exp(-((x - 0.3) ** 2) / 0.15)    # 中央尖峰
            h += 0.20 * np.exp(-((x - 2.0) ** 2) / 0.40)    # 右宽凸起
            return h

        # ========== 1. 样品表面 (0-1.5s) ==========
        n_pts = 300
        pts = []
        for i in range(n_pts):
            sx = -4.0 + 8.0 * i / (n_pts - 1)
            pts.append([sx, -1.0 + surface_profile(sx), 0])

        surface = VMobject()
        surface.set_points_as_corners(pts)
        surface.set_stroke(color=COLOR_DETECTOR, width=3)

        fill_pts = pts + [[4.0, -3, 0], [-4.0, -3, 0]]
        surface_fill = Polygon(*fill_pts, color=COLOR_DETECTOR,
                               fill_opacity=0.12, stroke_width=0)

        surface_label = Text("样品表面", font_size=22, color=COLOR_DETECTOR)
        surface_label.to_edge(DOWN).shift(UP * 0.15)

        scan_arrow = Arrow((-3.5, -2.2, 0), (-1.5, -2.2, 0),
                           color=WHITE, buff=0.1, stroke_width=2)
        scan_dir_label = Text("扫描方向 →", font_size=18, color=WHITE)
        scan_dir_label.next_to(scan_arrow, DOWN, buff=0.1)

        self.play(Create(surface), FadeIn(surface_fill),
                  Write(surface_label), run_time=1)
        self.play(GrowArrow(scan_arrow), Write(scan_dir_label), run_time=0.5)

        # ========== 2. 探针 + 探测器系统 (1.5-3s) ==========
        scan_x = ValueTracker(-3.0)

        def make_cantilever():
            x = scan_x.get_value()
            sy = -1.0 + surface_profile(x)
            base = np.array([x - 1.0, 0.0, 0])
            tip_contact = np.array([x, sy, 0])
            beam = Line(base, tip_contact, color=GREY, stroke_width=6)
            tip = Polygon(
                (x - 0.06, sy + 0.08, 0),
                (x + 0.06, sy + 0.08, 0),
                (x, sy, 0),
                color=GREY, fill_opacity=1
            )
            return VGroup(beam, tip)

        cantilever = always_redraw(make_cantilever)

        # 四象限探测器
        detector = Rectangle(width=1.0, height=1.4,
                             color=COLOR_DETECTOR, stroke_width=2)
        detector.move_to((5.0, 1.8, 0))
        cross_h = Line((4.5, 1.8, 0), (5.5, 1.8, 0),
                       color=GREY, stroke_width=1)
        cross_v = Line((5.0, 1.1, 0), (5.0, 2.5, 0),
                       color=GREY, stroke_width=1)
        det_label = Text("四象限\n探测器", font_size=16,
                         color=COLOR_DETECTOR, line_spacing=0.5)
        det_label.next_to(detector, UP, buff=0.1)

        # 激光光路
        def make_laser_in():
            x = scan_x.get_value()
            sy = -1.0 + surface_profile(x)
            reflect = np.array([x, sy + 0.04, 0])
            return Arrow((-2, 3.0, 0), reflect,
                         color=COLOR_LASER, buff=0, stroke_width=2,
                         max_tip_length_to_length_ratio=0.08)

        def make_laser_out():
            x = scan_x.get_value()
            sy = -1.0 + surface_profile(x)
            reflect = np.array([x, sy + 0.04, 0])
            deflection = surface_profile(x)
            spot_y = 1.8 + deflection * 2.0
            spot_y = np.clip(spot_y, 1.15, 2.45)
            return Arrow(reflect, (5.0, spot_y, 0),
                         color=COLOR_LASER, buff=0, stroke_width=2,
                         max_tip_length_to_length_ratio=0.08)

        def make_spot():
            x = scan_x.get_value()
            deflection = surface_profile(x)
            spot_y = 1.8 + deflection * 2.0
            spot_y = np.clip(spot_y, 1.15, 2.45)
            return Dot((5.0, spot_y, 0),
                       color=COLOR_EQUILIBRIUM, radius=0.08)

        laser_in = always_redraw(make_laser_in)
        laser_out = always_redraw(make_laser_out)
        spot = always_redraw(make_spot)

        self.play(
            FadeIn(detector), FadeIn(cross_h), FadeIn(cross_v),
            Write(det_label), run_time=0.5
        )
        self.add(cantilever, laser_in, laser_out, spot)
        self.wait(0.5)

        # ========== 3. 形貌追踪图 (3-3.5s) ==========
        topo_axes = Axes(
            x_range=[-3, 3, 1], y_range=[0, 0.6, 0.2],
            x_length=5.5, y_length=1.2,
            axis_config={"include_tip": False, "stroke_width": 1},
            x_axis_config={"numbers_to_include": [-3, 0, 3], "font_size": 16},
            y_axis_config={"numbers_to_include": [0, 0.3, 0.6], "font_size": 16}
        ).to_corner(DL).shift(RIGHT * 0.4 + UP * 0.3)

        topo_title = Text("形貌信号", font_size=18, color=WHITE)
        topo_title.next_to(topo_axes, UP, buff=0.05)

        topo_trace = VMobject()
        topo_trace.set_stroke(color=COLOR_EQUILIBRIUM, width=2.5)

        def update_topo(mob):
            x = scan_x.get_value()
            n = max(2, int((x + 3) / 6 * 120))
            trace_pts = []
            for i in range(n + 1):
                tx = -3.0 + 6.0 * i / max(n, 1)
                trace_pts.append(topo_axes.c2p(tx, surface_profile(tx)))
            if len(trace_pts) >= 2:
                mob.set_points_as_corners(trace_pts)

        topo_trace.add_updater(update_topo)

        self.play(Create(topo_axes), Write(topo_title), run_time=0.5)
        self.add(topo_trace)

        # ========== 4. 扫描行进 (3.5-7.5s) ==========
        scan_label = Text("▶ 扫描中...", font_size=24, color=WHITE)
        scan_label.to_corner(UR).shift(LEFT * 0.5)
        self.add(scan_label)

        self.play(scan_x.animate.set_value(3.0),
                  run_time=4, rate_func=linear)

        topo_trace.remove_updater(update_topo)

        done_label = Text("✓ 扫描完成", font_size=24, color=COLOR_EQUILIBRIUM)
        done_label.to_corner(UR).shift(LEFT * 0.5)
        self.play(Transform(scan_label, done_label), run_time=0.5)
        self.wait(0.5)

        # ========== 5. 转场淡出 ==========
        self.play(
            FadeOut(surface), FadeOut(surface_fill), FadeOut(surface_label),
            FadeOut(scan_arrow), FadeOut(scan_dir_label),
            FadeOut(cantilever), FadeOut(detector),
            FadeOut(cross_h), FadeOut(cross_v), FadeOut(det_label),
            FadeOut(laser_in), FadeOut(laser_out), FadeOut(spot),
            FadeOut(scan_label),
            FadeOut(topo_axes), FadeOut(topo_title), FadeOut(topo_trace),
            run_time=0.5
        )


# =============================================================================
# 镜头5：力曲线与工作模式（5秒）
# =============================================================================
class Scene5_AFMForceCurve(Scene):
    """
    展示力-距曲线和探针在平衡点的振动
    时长：通过 time_scale 参数可调，默认约 10 秒
    """
    
    # ========== 物理参数 ==========
    Z_RANGE = (0.5, 3.0)          # 距离范围 (nm)
    FORCE_RANGE = (-2, 2)         # 力范围 (nN)，调整以更好展示曲线
    VDW_CUTOFF = (-3, 1)          # 范德华力显示截断范围
    DECAY_LEN = 0.3               # 泡利力衰减长度
    PAULI_AMPLITUDE = 5.0         # 泡利力幅值
    EQUILIBRIUM_Z = 0.85          # 平衡点位置
    
    # ========== 动画参数 ==========
    TIME_SCALE = 2.0              # 时间缩放因子（>1延长，<1缩短）
    VIBRATION_CYCLES = 2          # 振动周期数
    VIBRATION_AMPLITUDE = 0.05    # 振动幅度
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 预计算物理函数
        self._vdw_force = np.vectorize(self._vdw_force_scalar)
    
    # ========== 物理模型函数 ==========
    @staticmethod
    def _vdw_force_scalar(z: float) -> float:
        """范德华力: F_vdw ∝ -1/z^7"""
        return -1.0 / (z ** 7) if z > 0.5 else -100
    
    def pauli_force(self, z: float | np.ndarray) -> float | np.ndarray:
        """泡利排斥力: F_pauli ∝ exp(-2z/λ)"""
        return self.PAULI_AMPLITUDE * np.exp(-2 * z / self.DECAY_LEN)
    
    def total_force(self, z: float | np.ndarray) -> float | np.ndarray:
        """合力 = 范德华力 + 泡利力"""
        return self.pauli_force(z) + self._vdw_force(z)
    
    def force_derivative(self, z: float, h: float = 0.01) -> float:
        """计算力在z处的导数（中心差分）"""
        result = (self.total_force(z + h) - self.total_force(z - h)) / (2 * h)
        return float(result)
    
    # ========== 场景构建模块 ==========
    def create_axes(self) -> tuple[Axes, VGroup]:
        """创建坐标轴和标签（仅坐标轴，不含曲线）"""
        axes = Axes(
            x_range=[*self.Z_RANGE, 0.5],
            y_range=[*self.FORCE_RANGE, 1],
            x_length=8, y_length=4,
            axis_config={"include_tip": False},
            x_axis_config={"numbers_to_include": [1, 2, 3]},
            y_axis_config={"numbers_to_include": [-2, -1, 0, 1, 2]}
        ).shift(DOWN * 0.5)
        
        labels = VGroup(
            MathTex(r"z \text{ (nm)}", font_size=24).next_to(axes.x_axis, RIGHT),
            MathTex(r"F \text{ (nN)}", font_size=24).next_to(axes.y_axis, UP)
        )
        return axes, labels
    
    def create_vdw_curve_group(self, axes: Axes) -> tuple[ParametricFunction, MathTex]:
        """创建范德华力曲线及其标签"""
        # 截断函数避免超出显示范围
        def vdw_clipped(z):
            f = self._vdw_force_scalar(z)
            return np.clip(f, self.VDW_CUTOFF[0], self.VDW_CUTOFF[1])
        
        curve = axes.plot(
            vdw_clipped,
            x_range=[0.7, 3],
            color=COLOR_VDW,
            stroke_width=3
        )
        # 标签紧挨曲线（z=1.4附近，曲线y≈-0.35的位置）
        label = MathTex(r"F_{\text{vdW}} \propto -1/z^7", color=COLOR_VDW, font_size=26)
        label.move_to(axes.c2p(1.5, -0.6))
        
        return curve, label
    
    def create_pauli_curve_group(self, axes: Axes) -> tuple[ParametricFunction, MathTex]:
        """创建泡利排斥力曲线及其标签"""
        def pauli_float(z: float) -> float:
            return float(self.pauli_force(z))
        curve = axes.plot(
            pauli_float,
            x_range=[0.5, 3],
            color=COLOR_PAULI,
            stroke_width=3
        )
        # 标签紧贴曲线上升段（z=0.7处）
        label = MathTex(r"F_{\text{Pauli}} \propto e^{-2z/\lambda}", color=COLOR_PAULI, font_size=26)
        label.move_to(axes.c2p(0.85, 1.5))
        
        return curve, label
    
    def create_total_curve_group(self, axes: Axes) -> tuple[ParametricFunction, MathTex]:
        """创建合力曲线及其标签"""
        def total_clipped(z: float) -> float:
            f = self.total_force(z)
            clipped = np.clip(f, self.FORCE_RANGE[0], self.FORCE_RANGE[1])
            return float(clipped)
        
        curve = axes.plot(
            total_clipped,
            x_range=[0.7, 3],
            color=WHITE,
            stroke_width=4
        )
        # 标签紧贴合力曲线右侧
        label = MathTex(r"F_{\text{total}}", color=WHITE, font_size=22)
        label.move_to(axes.c2p(1.6, 1.2))
        
        return curve, label
    
    def create_equilibrium_marker(self, axes: Axes) -> tuple[Dot, MathTex]:
        """创建平衡点标记"""
        point = Dot(axes.c2p(self.EQUILIBRIUM_Z, 0), color=COLOR_EQUILIBRIUM, radius=0.1)
        label = MathTex(r"\text{Equilibrium}", font_size=24, color=COLOR_EQUILIBRIUM)
        label.next_to(point, UR, buff=0.1)
        return point, label
    
    def create_probe(self, axes: Axes) -> Triangle:
        """创建探针图标"""
        probe = Triangle(color=GREY, fill_opacity=1)
        probe.scale(0.05)
        probe.rotate(PI)
        probe.move_to(axes.c2p(self.EQUILIBRIUM_Z, 0))
        return probe
    
    def create_delta_f_display(self) -> tuple[DecimalNumber, MathTex]:
        """创建频率变化显示"""
        delta_f = DecimalNumber(0, num_decimal_places=2, color=COLOR_DETECTOR)
        delta_f.to_corner(DR).shift(LEFT * 0.5 + UP * 0.5)
        
        label = MathTex(r"\Delta f", font_size=30, color=WHITE)
        label.next_to(delta_f, LEFT, buff=0.2)
        return delta_f, label
    
    # ========== 动画模块 ==========
    def animate_vibration(self, axes: Axes, probe: Triangle, 
                          delta_f: DecimalNumber, duration: float) -> None:
        """探针振动动画"""
        t = ValueTracker(0)
        z0 = self.EQUILIBRIUM_Z
        omega = self.VIBRATION_CYCLES * 2 * PI / duration
        
        def update_probe(mob):
            z = z0 + self.VIBRATION_AMPLITUDE * np.sin(omega * t.get_value())
            mob.move_to(axes.c2p(z, 0))
        
        def update_df(mob):
            slope = self.force_derivative(z0)
            mob.set_value(slope * 0.1 * np.sin(omega * t.get_value()))
        
        probe.add_updater(update_probe)
        delta_f.add_updater(update_df)
        
        self.play(t.animate.set_value(duration), run_time=duration, rate_func=linear)
        
        probe.remove_updater(update_probe)
        delta_f.remove_updater(update_df)
    
    def animate_transition_out(self, scene_objects: list, scan_text: Text) -> None:
        """转场淡出动画"""
        fade_outs = [FadeOut(obj) for obj in scene_objects]
        self.play(*fade_outs, Write(scan_text), run_time=0.5 * self.TIME_SCALE)
    
    # ========== 主构建流程 ==========
    def construct(self):
        ts = self.TIME_SCALE  # 时间缩放简写
        
        # ---- 1. 坐标轴（独立创建，不绑定曲线） ----
        axes, axes_labels = self.create_axes()
        self.play(Create(axes), Write(axes_labels), run_time=0.5 * ts)
        
        # ---- 2. 范德华力曲线：先画线，再写标签 ----
        vdw_curve, vdw_label = self.create_vdw_curve_group(axes)
        self.play(Create(vdw_curve), run_time=0.7 * ts)
        self.play(Write(vdw_label), run_time=0.3 * ts)
        
        # ---- 3. 泡利排斥力曲线：先画线，再写标签 ----
        pauli_curve, pauli_label = self.create_pauli_curve_group(axes)
        self.play(Create(pauli_curve), run_time=0.7 * ts)
        self.play(Write(pauli_label), run_time=0.3 * ts)
        
        # ---- 4. 合力曲线：先画线，再写标签 ----
        total_curve, total_label = self.create_total_curve_group(axes)
        self.play(Create(total_curve), run_time=0.35 * ts)
        self.play(Write(total_label), run_time=0.15 * ts)
        
        # ---- 5. 平衡点标记 ----
        eq_point, eq_label = self.create_equilibrium_marker(axes)
        self.play(FadeIn(eq_point), Write(eq_label), run_time=0.5 * ts)
        
        # ---- 6. 探针振动 ----
        probe = self.create_probe(axes)
        delta_f, delta_f_label = self.create_delta_f_display()
        
        self.add(probe, delta_f, delta_f_label)
        self.animate_vibration(axes, probe, delta_f, duration=2.0 * ts)
        
        # ---- 7. 转场 ----
        scan_text = Text("逐点扫描 → 表面形貌", font_size=36, color=WHITE).to_edge(UP)
        scene_objects = [
            axes, axes_labels, vdw_curve, vdw_label, pauli_curve, pauli_label,
            total_curve, total_label, eq_point, eq_label, probe, delta_f, delta_f_label
        ]
        self.animate_transition_out(scene_objects, scan_text)
        
        # ---- 8. 扫描占位符 ----
        placeholder = Rectangle(width=8, height=4, color=BLUE, fill_opacity=0.2)
        scan_label = Text("Scanning...", font_size=32, color=BLUE)
        scan_group = VGroup(placeholder, scan_label)
        
        self.play(FadeIn(scan_group), run_time=0.3 * ts)
        self.wait(0.2 * ts)
        
        # 最终淡出
        self.play(FadeOut(scan_text), FadeOut(scan_group), run_time=0.5 * ts)


# =============================================================================
# 主渲染入口（可选：用于连续渲染所有场景）
# =============================================================================
if __name__ == "__main__":
    # 可以在这里添加批量渲染逻辑
    pass
