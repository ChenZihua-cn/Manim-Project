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
    展示AFM探针扫描成像原理：
    悬臂梁左端固定、右端探针接触表面，样品表面向左移动，
    探针随表面形貌起伏偏转，激光反射至四象限探测器，
    实时绘制形貌曲线。时长：~9秒
    """

    def construct(self):
        # ---- 表面形貌定义（延展范围供滚动） ----
        def surface_profile(x):
            h = 0.0
            h += 0.25 * np.exp(-((x - 1.5) ** 2) / 0.25)   # 左凸起
            h += 0.35 * np.exp(-((x - 3.3) ** 2) / 0.15)    # 中央尖峰
            h += 0.20 * np.exp(-((x - 5.0) ** 2) / 0.40)    # 右宽凸起
            h += 0.18 * np.exp(-((x - 6.5) ** 2) / 0.30)    # 尾部小凸起
            return h

        # ---- ValueTracker：表面左移量 ----
        surface_shift = ValueTracker(0)
        SCAN_RANGE = 6.0  # 总扫描距离

        # ========== 1. 动态表面 (0-1.5s) ==========
        # 表面曲线 — updater 每帧根据 surface_shift 重新计算点位
        surface = VMobject()
        surface.set_stroke(color=COLOR_DETECTOR, width=3)

        def update_surface(mob):
            shift = surface_shift.get_value()
            n = 200
            pts = []
            for i in range(n):
                sx = -4.0 + 8.0 * i / (n - 1)
                pts.append([sx, -0.4 + surface_profile(sx + shift), 0])
            mob.set_points_as_corners(pts)

        surface.add_updater(update_surface)

        # 表面下方半透明填充
        n_init = 200
        init_fill_pts = []
        for i in range(n_init):
            sx = -4.0 + 8.0 * i / (n_init - 1)
            init_fill_pts.append([sx, -0.4 + surface_profile(sx), 0])
        init_fill_pts = init_fill_pts + [[4.0, -3, 0], [-4.0, -3, 0]]

        surface_fill = Polygon(*init_fill_pts,
                               color=COLOR_DETECTOR, fill_opacity=0.12,
                               stroke_width=0)

        def update_surface_fill(mob):
            shift = surface_shift.get_value()
            n = 200
            pts = []
            for i in range(n):
                sx = -4.0 + 8.0 * i / (n - 1)
                pts.append([sx, -0.4 + surface_profile(sx + shift), 0])
            pts = pts + [[4.0, -3, 0], [-4.0, -3, 0]]
            mob.set_points_as_corners(pts)

        surface_fill.add_updater(update_surface_fill)

        surface_label = Text("样品表面", font_size=22, color=COLOR_DETECTOR)
        surface_label.to_edge(DOWN).shift(UP * 0.15)

        # 表面移动方向指示
        move_arrow = Arrow((-0.5, -2.2, 0), (-2.5, -2.2, 0),
                           color=WHITE, buff=0.1, stroke_width=2)
        move_label = Text("表面移动 ←", font_size=18, color=WHITE)
        move_label.next_to(move_arrow, DOWN, buff=0.1)

        self.add(surface, surface_fill)
        self.play(Write(surface_label), GrowArrow(move_arrow),
                  Write(move_label), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(move_arrow), FadeOut(move_label))

        # ========== 2. 悬臂梁 + 探针 (1.5-3s) ==========
        # 悬臂梁：左端固定在 (-3, 0)，右端在 (0, tip_y) 随表面起伏
        cantilever_base = Line((-3, 0, 0), (0, 0, 0), color=GREY, stroke_width=8)
        tip_shape = Polygon(
            (-0.12, 0, 0), (0.12, 0, 0), (0, -0.4, 0),
            color=GREY, fill_opacity=1
        )
        cantilever = VGroup(cantilever_base, tip_shape)

        
        # 激光路径（入射到悬臂梁反射点，反射点跟随振动）—— 初始隐藏
        laser_in = Arrow((-3.5, 1.5, 0), (0, 0.15, 0), color=COLOR_LASER, buff=0)
        laser_out = Arrow((0, 0.15, 0), (3, 1.8, 0), color=COLOR_LASER, buff=0)
        laser_in.set_stroke(opacity=0)
        laser_out.set_stroke(opacity=0)
        
        # 四象限探测器
        detector = Rectangle(width=1.2, height=1.2, color=COLOR_DETECTOR, stroke_width=2)
        detector.move_to((3, 1.8, 0))
        
        # 探测器分割线
        cross = VGroup(
            Line((3, 1.2, 0), (3, 2.4, 0), color=GREY),
            Line((2.4, 1.8, 0), (3.6, 1.8, 0), color=GREY)
        )
        
        # 探测器标签
        detector_label = Text("四象限探测器", font_size=20, color=COLOR_DETECTOR)
        detector_label.next_to(detector, UP, buff=0.2)
        
        self.add(cantilever, detector, cross, detector_label)

        # 2. 初始静止展示（0-1秒）—— 激光箭头不显示
        self.wait(1)

        # 3. 悬臂梁振动 + 激光 + 探针尖端表面波（1-3秒）
        vibrate = ValueTracker(0)

        def update_cantilever(mob):
            shift = surface_shift.get_value()
            tip_y = surface_profile(shift)
            new_base = Line((-3, 0, 0), (0, tip_y, 0),
                            color=GREY, stroke_width=8)
            new_tip = Polygon(
                (-0.12, tip_y, 0), (0.12, tip_y, 0), (0, tip_y - 0.4, 0),
                color=GREY, fill_opacity=1
            )
            mob.become(VGroup(new_base, new_tip))


        # 探针尖端不平整表面 —— 移动波 sin(ωt - kx)
        n_wave_pts = 25
        wave_k = 20
        wave_omega = 8 * PI
        wave_dots = VGroup()
        for i in range(n_wave_pts):
            dot = Dot(radius=0.015, color=COLOR_LASER, fill_opacity=0.8)
            wave_dots.add(dot)

        def update_wave(mob):
            t = vibrate.get_value()
            offset = 0.15 * np.sin(10 * t)
            for i, dot in enumerate(mob):
                frac = i / (n_wave_pts - 1)
                x = -0.11 + 0.22 * frac
                base_y = offset - 0.4 * (1 - abs(x) / 0.12)
                wave_y = 0.04 * np.sin(wave_omega * t - wave_k * x)
                dot.move_to(np.array([x, base_y + wave_y, 0]))

        wave_dots.add_updater(update_wave)

        cantilever.add_updater(update_cantilever)

        # 四象限探测器（右侧）
        detector = Rectangle(width=1.2, height=1.2,
                             color=COLOR_DETECTOR, stroke_width=2)
        detector.move_to((3, 1.8, 0))
        cross = VGroup(
            Line((3, 1.2, 0), (3, 2.4, 0), color=GREY, stroke_width=1),
            Line((2.4, 1.8, 0), (3.6, 1.8, 0), color=GREY, stroke_width=1)
        )
        detector_label = Text("四象限探测器", font_size=20, color=COLOR_DETECTOR)
        detector_label.next_to(detector, UP, buff=0.2)

        # 激光入射 — 从光源射向悬臂梁背面反射点
        laser_in = Arrow((-3.5, 1.5, 0), (0, 0.1, 0),
                         color=COLOR_LASER, buff=0, stroke_width=2)


        # 同时：淡入激光、显示表面波、振动悬臂梁
        self.play(
            FadeIn(laser_in), FadeIn(laser_out),
            FadeIn(wave_dots),
            vibrate.animate.set_value(2 * PI),
            run_time=2, rate_func=linear
        )
        cantilever.remove_updater(update_cantilever)
        wave_dots.remove_updater(update_wave)

        # 3. 频移公式（3-4秒）
        freq_shift = MathTex(
            r"\Delta f \approx -\frac{f_0}{2k} \frac{dF}{dz}",
            font_size=44, color=WHITE
        ).to_edge(UP)
        
        self.play(Write(freq_shift), run_time=1)
        
        # 高亮 dF/dz - use index instead of get_part_by_tex
        self.play(Indicate(freq_shift[0][6:9], color=RED, scale_factor=1.2), run_time=0.5)
        
        # 4. 光斑移动和信号显示（4-6秒）
        def update_laser_in(mob):
            shift = surface_shift.get_value()
            tip_y = surface_profile(shift)
            reflect = np.array([0, tip_y + 0.1, 0])
            mob.become(Arrow((-3.5, 1.5, 0), reflect,
                             color=COLOR_LASER, buff=0, stroke_width=2))

        laser_in.add_updater(update_laser_in)

        # 激光反射 — 从反射点射向探测器，偏转角度随悬臂梁倾斜变化
        laser_out = Arrow((0, 0.1, 0), (3, 1.8, 0),
                          color=COLOR_LASER, buff=0, stroke_width=2)

        def update_laser_out(mob):
            shift = surface_shift.get_value()
            tip_y = surface_profile(shift)
            reflect = np.array([0, tip_y + 0.1, 0])
            spot_y = 1.8 + tip_y * 1.0
            spot_y = np.clip(spot_y, 1.2, 2.4)
            mob.become(Arrow(reflect, (3, spot_y, 0),
                             color=COLOR_LASER, buff=0, stroke_width=2))

        laser_out.add_updater(update_laser_out)

        # 探测器上光斑
        spot = Dot((3, 1.8, 0), color=COLOR_EQUILIBRIUM, radius=0.08)

        def update_spot(mob):
            shift = surface_shift.get_value()
            tip_y = surface_profile(shift)
            spot_y = 1.8 + tip_y * 1.0
            spot_y = np.clip(spot_y, 1.2, 2.4)
            mob.move_to((3, spot_y, 0))

        spot.add_updater(update_spot)

        self.add(cantilever, detector, cross, detector_label)
        self.add(laser_in, laser_out, spot)
        self.wait(0.5)

        # ========== 3. 形貌追踪图 (3-3.5s) ==========
        topo_axes = Axes(
            x_range=[0, SCAN_RANGE, 1],
            y_range=[0, 0.6, 0.2],
            x_length=5.5, y_length=1.2,
            axis_config={"include_tip": False, "stroke_width": 1},
            x_axis_config={"numbers_to_include": [0, 2, 4, 6], "font_size": 16},
            y_axis_config={"numbers_to_include": [0, 0.3, 0.6], "font_size": 16}
        ).to_corner(DL).shift(RIGHT * 0.4 + UP * 0.3)

        topo_title = Text("形貌信号", font_size=18, color=WHITE)
        topo_title.next_to(topo_axes, UP, buff=0.05)

        topo_trace = VMobject()
        topo_trace.set_stroke(color=COLOR_EQUILIBRIUM, width=2.5)

        def update_topo(mob):
            shift = surface_shift.get_value()
            if shift <= 0.01:
                mob.set_points_as_corners([topo_axes.c2p(0, 0)])
                return
            n = max(2, int(shift / SCAN_RANGE * 150))
            pts = []
            for i in range(n + 1):
                tx = shift * i / max(n, 1)
                pts.append(topo_axes.c2p(tx, surface_profile(tx)))
            if len(pts) >= 2:
                mob.set_points_as_corners(pts)

        topo_trace.add_updater(update_topo)

        self.play(Create(topo_axes), Write(topo_title), run_time=0.5)
        self.add(topo_trace)

        # ========== 4. 表面左移扫描 (3.5-8s) ==========
        scan_label = Text("▶ 扫描中...", font_size=24, color=WHITE)
        scan_label.to_corner(UR).shift(LEFT * 0.5)
        self.add(scan_label)

        self.play(surface_shift.animate.set_value(SCAN_RANGE),
                  run_time=4.5, rate_func=linear)

        topo_trace.remove_updater(update_topo)

        done_label = Text("✓ 扫描完成", font_size=24, color=COLOR_EQUILIBRIUM)
        done_label.to_corner(UR).shift(LEFT * 0.5)
        self.play(Transform(scan_label, done_label), run_time=0.5)
        self.wait(0.5)

        # ========== 5. 转场淡出 ==========
        self.play(
            FadeOut(surface), FadeOut(surface_fill), FadeOut(surface_label),
            FadeOut(cantilever), FadeOut(detector), FadeOut(cross),
            FadeOut(detector_label),
            FadeOut(laser_in), FadeOut(laser_out), FadeOut(spot),
            FadeOut(scan_label),
            FadeOut(topo_axes), FadeOut(topo_title), FadeOut(topo_trace),
            FadeOut(cantilever), FadeOut(laser_in), FadeOut(laser_out),
            FadeOut(detector), FadeOut(cross), FadeOut(detector_label),
            FadeOut(wave_dots),
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
# 镜头6：AFM悬臂梁3D展示 (Termux 3D Scene)
# =============================================================================
class Scene6_Cuboid3D(ThreeDScene):
    """
    AFM悬臂梁3D: 固定基座 → 矩形主体 → 单坡屋脊尖端(tip_of_cantilever)
                   → 圆锥原子探针 → 样品表面
    边长 z(厚度) < y(宽度) < x(长度)
    摄像机 +x 轴朝向负x, 尖端+探针靠近镜头
    """

    LENGTH_X = 4.0
    LENGTH_Y = 1.5
    LENGTH_Z = 0.35
    TIP_LEN  = 0.6   # 尖端沿 x 长度
    ROOF_RISE = 0.18 # 右脊高出顶面
    PROBE_H  = 0.4   # 探针长度
    PROBE_R  = 0.22  # 探针底面半径

    def construct(self):
        self.set_camera_orientation(phi=0, theta=-PI / 2, zoom=0.85)

        hx = self.LENGTH_X / 2
        hy = self.LENGTH_Y / 2
        hz = self.LENGTH_Z / 2
        tl = self.TIP_LEN
        rr = self.ROOF_RISE

        face_style = dict(
            fill_color=BLUE_E, fill_opacity=1,
            stroke_color=WHITE, stroke_width=1.5,
        )

        # ── 1. 固定基座 ──────────────────────────────────────────
        base = Prism(
            dimensions=np.array([0.6, self.LENGTH_Y + 0.3, self.LENGTH_Z + 0.5]),
            fill_color=DARKER_GREY, fill_opacity=0.9,
            stroke_color=GREY_BROWN, stroke_width=1.5,
        ).move_to(np.array([-hx - 0.25, 0, 0]))
        self.play(Create(base), run_time=0.8)

        # ── 2. 悬臂梁主体 ────────────────────────────────────────
        body = Prism(
            dimensions=np.array([self.LENGTH_X - tl, self.LENGTH_Y, self.LENGTH_Z]),
            fill_color=BLUE_E, fill_opacity=1,
            stroke_color=WHITE, stroke_width=1,
        ).move_to(np.array([-tl / 2, 0, 0]))
        self.play(Create(body), run_time=0.6)

        # ── 3. tip_of_cantilever: 单坡尖端 ─────────────────────
        # 后端 (x0): 矩形 ABCD 接主体 — 前端 (x1): 左檐H平坦, 右脊I倾斜
        x0, x1 = hx - tl, hx

        A, B = np.array([x0, -hy, -hz]), np.array([x0, hy, -hz])
        C, D = np.array([x0,  hy,  hz]), np.array([x0, -hy, hz])
        E, F = np.array([x1, -hy, -hz]), np.array([x1, hy, -hz])
        H    = np.array([x1, -hy,  hz])       # 左檐 (平坦)
        I    = np.array([x1,  hy,  hz - rr])  # 右脊 (下切倾斜)

        tip_of_cantilever = VGroup(
            Polygon(A, B, F, E, **face_style),  # bottom
            Polygon(A, E, H, D, **face_style),  # left
            Polygon(B, F, I, C, **face_style),  # right (tall)
            Polygon(D, H, I, C, **face_style),  # roof
        )
        self.play(Create(tip_of_cantilever), run_time=0.6)

        # ── 4. 原子探针 (圆锥, 右脊正下方) ──────────────────────
        apex = np.array([(x1+x0)/2, 0, -hz - self.PROBE_H])
        tip_cone = Cone(
            base_radius=self.PROBE_R, height=self.PROBE_H,
            direction=IN, resolution=(32, 32),
            fill_color=YELLOW_E, fill_opacity=0.85,
            stroke_color=GOLD, stroke_width=1,
        ).move_to(np.array([(x1+x0)/2, 0, -hz - self.PROBE_H / 2]))

        tip_atom = Sphere(radius=0.06, fill_color=RED, fill_opacity=1).move_to(apex)
        orbit = Circle(
            radius=0.04, color=ORANGE, stroke_width=1.5,
        ).move_to(apex)

        self.add(tip_cone, tip_atom)


        # ── 7. 摄像机环绕 ────────────────────────────────────────
        self.move_camera(
            phi=70 * DEGREES, theta=-60 * DEGREES, zoom=0.6,
            run_time=5, rate_func=smooth,
        )
        self.wait(0.5)
        self.add(orbit)

        # ── 8. 样品表面上升 ──────────────────────────────────────
        def sample_surface_height(x, y):
            """2D高度场：高斯凸起模拟样品表面形貌"""
            h = 0.0
            h += 0.20 * np.exp(-(((x - 1.0)**2) / 0.4 + ((y - 0.3)**2) / 0.3))
            h += 0.30 * np.exp(-(((x - 2.0)**2) / 0.2 + ((y + 0.2)**2) / 0.25))
            h += 0.25 * np.exp(-(((x + 0.5)**2) / 0.5 + ((y - 0.4)**2) / 0.4))
            h += 0.22 * np.exp(-(((x + 1.5)**2) / 0.6 + ((y + 0.1)**2) / 0.35))
            h += 0.18 * np.exp(-(((x - 0.5)**2) / 0.7 + ((y + 0.6)**2) / 0.5))
            return h

        Z_BASE = -0.75
        surface = Surface(
            func=lambda u, v: np.array([u, v, Z_BASE + sample_surface_height(u, v)]),
            u_range=(-3, 3),
            v_range=(-1.5, 1.5),
            resolution=60,
            fill_color=COLOR_DETECTOR,
            fill_opacity=0.85,
            checkerboard_colors=False,
            stroke_color=ManimColor("#2E7D32"),
            stroke_width=0.3,
        )
        """
        surface_label = Text("样品表面", font_size=22, color=COLOR_DETECTOR)
        surface_label.to_corner(DL)"""

        # 表面从下方升入视野（沿Z轴上升）
        surface.shift(IN * 0.8)
        self.play(Create(surface))
        self.play(
            surface.animate.shift(OUT * 0.8),
            # Write(surface_label),
            run_time=1.5,
        )
        self.wait(1.0)


        # ── 8.5 原子级表面 — 模拟放大后的样品表面 ──────────────
        # 创建由小球组成的原子阵列平面（棋盘格排列）
        atom_spheres = VGroup()
        atom_colors_pair = [BLUE_D, BLUE_C]
        spacing = 0.32
        x_vals = np.arange(-2.56, 2.57, spacing)
        y_vals = np.arange(-1.12, 1.13, spacing)
        for i, x in enumerate(x_vals):
            for j, y in enumerate(y_vals):
                sphere = Sphere(
                    radius=0.10,
                    fill_color=atom_colors_pair[(i + j) % 2],
                    fill_opacity=1,
                    stroke_width=0.2,
                    stroke_color=GREY,
                    resolution=(10, 10),
                ).move_to(np.array([x, y, Z_BASE + 0.05]))
                atom_spheres.add(sphere)

        # 同步转场：样品表面淡出 → 原子形貌淡入
        self.play(
            FadeOut(surface),
            FadeIn(atom_spheres),
            run_time=1.5,
        )

        # ── 9. 淡出 ──────────────────────────────────────────────
        self.play(
            *[FadeOut(o) for o in (
                base, body, tip_of_cantilever,
                tip_cone, tip_atom, orbit,
                atom_spheres,
                # surface_label,
            )],
            run_time=1,
        )


# =============================================================================
# 主渲染入口（可选：用于连续渲染所有场景）
# =============================================================================
if __name__ == "__main__":
    # 可以在这里添加批量渲染逻辑
    pass
