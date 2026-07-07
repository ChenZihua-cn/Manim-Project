# trunk-ignore(ruff/F403)
# pyright: ignore[reportWildcardImportFromLibrary]
from manim import *
import numpy as np

# 全局配置
config.frame_rate = 30
config.background_color = BLACK
config.pixel_width = 1920
config.pixel_height = 1080

# color norm
COLOR_PAULI = "#E53935"        # 泡利排斥力/势 - 红
COLOR_VDW = "#1E88E5"          # 范德华力 - 蓝
COLOR_EQUILIBRIUM = "#FFEB3B"  # 平衡点/高亮 - 黄
COLOR_DETECTOR = "#43A047"     # 探测器/信号 - 绿

# calculate the light reflection

def refelct_laser(incident_start, incident_direction, mirror):
    if """the incident laser not hit the mirror""":
        return None, None, False
    try:
        pass
    except np.linalg.LinAlgError:
        pass


class Scene1_(Scene):
    pass

class Scene2_(Scene):
    pass

class Scene3_(Scene):
    pass

class Scene4_FrequencyShiftDetection(Scene):
    pass

"""
    展示力-距曲线和探针在平衡点的振动
    画面中央显示探针和样品的局部模型，右侧弹出作用力表达式。
    公式出现后，曲线上的工作点进入接触区。
"""

# 中央出现局部模型
# 局部模型整体移动到左侧
# 右侧显示公式:F(D)=分段函数;D>a0时为范德华吸引项，D≤a0时加入接触排斥项。
# 公式移到上方，下方绘制力-曲线，一共三条曲线（已经写出函数）
# 随着探针移动，平衡点也在轴上移动

class Scene5_ForceCurve(Scene):
    Z_RANGE = (0.5, 3.0)          # 距离范围 (nm)
    FORCE_RANGE = (-2, 2)         # 力范围 (nN)，调整以更好展示曲线
    VDW_CUTOFF = (-3, 1)          # 范德华力显示截断范围
    DECAY_LEN = 0.3               # 泡利力衰减长度
    PAULI_AMPLITUDE = 5.0         # 泡利力幅值
    EQUILIBRIUM_Z = 0.85          # 平衡点位置
    VIBRATION_CYCLES = 2          # 振动周期数
    VIBRATION_AMPLITUDE = 0.05    # 振动幅度
    VDW_AMPLITUDE = 1.0              # 范德华力幅值 C
    VDW_CUTOFF_DIST = 0.5            # 短程截断距离（防止奇点）
    VDW_CUTOFF_VALUE = -100.0        # 截断处返回的力值
    VDW_CLIP_RANGE = (-3, 1)         # 绘图时力的显示裁剪范围

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vdw_amplitude = self.VDW_AMPLITUDE
        self.vdw_cutoff = self.VDW_CUTOFF_DIST
        self.vdw_cutoff_value = self.VDW_CUTOFF_VALUE
        self.vdw_clip_range = self.VDW_CLIP_RANGE
    
    def cantilever_model(self) -> VGroup:
        """悬臂梁+探针尖端+尖端原子，返回居中于 ORIGIN 的 VGroup"""
        beam = RoundedRectangle(
            width=3.5, height=0.15, corner_radius=0.06,
            color=GREY, fill_opacity=1, stroke_width=0
        )
        anchor = Rectangle(
            width=0.25, height=0.6,
            color=DARK_GREY, fill_opacity=1, stroke_width=0
        ).next_to(beam.get_left(), LEFT, buff=0)
        tip = Polygon(
            (-0.12, 0, 0), (0.12, 0, 0), (0, -0.5, 0),
            color=GREY, fill_opacity=1, stroke_width=0
        ).next_to(beam.get_right(), DOWN, buff=0).shift(LEFT*0.2)
        tip_atom = Dot(
            point=tip.get_bottom(),
            color=COLOR_VDW, radius=0.08
        )
        model = VGroup(beam, anchor, tip, tip_atom)
        model.move_to(ORIGIN)
        return model

    def sample_surface(self) -> VGroup:
        """样品表面：水平基底 + 原子阵列，居中于 ORIGIN"""
        base = Line(LEFT * 2, RIGHT * 2, color=GREY, stroke_width=3)
        atoms = VGroup()
        atom_colors = [BLUE_D, BLUE_C, BLUE_D, BLUE_C, BLUE_E,BLUE_D, BLUE_C, BLUE_D]
        for i, c in enumerate(atom_colors):
            atom = Dot(
                point=base.get_top() + UP * 0.12,
                color=c, radius=0.12
            ).shift(RIGHT * (i - len(atom_colors) / 2 + 0.5) * 0.35)
            atoms.add(atom)
        surface = VGroup(base, atoms)
        surface.move_to(ORIGIN)
        return surface

    def force_formula(self) -> MathTex:
        """统一力公式，初始位置在画面右侧"""
        formula = MathTex(
            r"F(z) = \begin{cases} "
            r"\dfrac{HR}{6(z+z_s)^2}, & z+z_s > a_0 \\[1em] "
            r"\dfrac{HR}{6a_0^2} + \dfrac{4}{3} E_{\rm eff} \sqrt{R}\, (a_0 - z - z_s)^{3/2}, & z+z_s \leq a_0 "
            r"\end{cases}",
            font_size=36, color=WHITE
            ).scale(0.8)
        formula.to_edge(RIGHT, buff=1.0)
        return formula

    def _vdw_force(self, z: float | np.ndarray) -> np.ndarray:
        z_arr = np.asarray(z)
        force = np.full_like(z_arr, self.vdw_cutoff_value, dtype=float)
        mask = z_arr > self.vdw_cutoff
        force[mask] = -self.vdw_amplitude / (z_arr[mask] ** 7)
        return force

    def pauli_force(self, z: float | np.ndarray) -> np.ndarray:
        z_arr = np.asarray(z)
        return self.PAULI_AMPLITUDE * np.exp(-2 * z_arr / self.DECAY_LEN)

    def total_force(self, z: float | np.ndarray) -> np.ndarray:
        return self.pauli_force(z) + self._vdw_force(z)

    def force_derivative(self, z: float, h: float = 0.001) -> float:
        """使用中心差分，但 h 取较小值，避免跨越截断边界"""
        # 可选的更鲁棒方法：若 z-h < cutoff，改用前向差分
        if z - h < self.vdw_cutoff:
            # 使用前向差分 (f(z+h) - f(z))/h
            result = (self.total_force(z + h) - self.total_force(z)) / h
        else:
            result = (self.total_force(z + h) - self.total_force(z - h)) / (2 * h)
        return float(result)
    
    def create_axes(self) -> tuple[Axes, VGroup]:
        """创建坐标轴和标签（仅坐标轴，不含曲线）"""
        axes = Axes(
            x_range=[*self.Z_RANGE, 0.5],
            y_range=[*self.FORCE_RANGE, 1],
            x_length=8, y_length=4,
            axis_config={"include_tip": False},
            x_axis_config={"numbers_to_include": [1, 2, 3]},
            y_axis_config={"numbers_to_include": [-2, -1, 0, 1, 2]}
        ).scale(0.8).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.5)
        
        labels = VGroup(
            MathTex(r"z \text{ (nm)}", font_size=24).next_to(axes.x_axis, RIGHT),
            MathTex(r"F \text{ (nN)}", font_size=24).next_to(axes.y_axis, UP)
        )
        return axes, labels
    
    def create_vdw_curve_group(self, axes: Axes) -> tuple[ParametricFunction, MathTex]:
        """创建范德华力曲线及其标签"""
        # 截断函数避免超出显示范围
        def vdw_clipped(z):
            f = self._vdw_force(z)
            return np.clip(f, self.VDW_CUTOFF[0], self.VDW_CUTOFF[1])
        
        # 生成 x 值数组
        x_values = np.linspace(0.7, 3, 100)
        # 计算对应的 y 值
        y_values = vdw_clipped(x_values)

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

    def create_region_labels(self, axes: Axes) -> VGroup:
        """非接触区 / 接触区 分界与标签"""
        divider = DashedLine(
            axes.c2p(self.EQUILIBRIUM_Z, self.FORCE_RANGE[0]),
            axes.c2p(self.EQUILIBRIUM_Z, self.FORCE_RANGE[1]),
            color=GREY, stroke_width=1, dash_length=0.12
        )
        non_contact = Text("非接触区", font_size=22, color=COLOR_VDW).scale(0.8)
        non_contact.move_to(axes.c2p(1.8, -1.2))
        contact = Text("接触区", font_size=22, color=COLOR_PAULI).scale(0.8)
        contact.move_to(axes.c2p(0.65, 1.2))
        return VGroup(divider, non_contact, contact)

    def create_probe(self, axes: Axes) -> Triangle:
        """曲线上工作点标记，初始位于非接触区"""
        z_start = 2.5
        f_start = np.clip(float(self.total_force(z_start)), self.FORCE_RANGE[0], self.FORCE_RANGE[1])
        probe = Triangle(color=GREY, fill_opacity=1)
        probe.scale(0.15)
        probe.move_to(axes.c2p(z_start, f_start))
        return probe
    
    def create_delta_f_display(self) -> tuple[DecimalNumber, MathTex]:
        """创建频率变化显示"""
        delta_f = DecimalNumber(0, num_decimal_places=2, color=COLOR_DETECTOR)
        delta_f.to_corner(DR).shift(LEFT * 0.5 + UP * 0.5)
        
        label = MathTex(r"\Delta f", font_size=30, color=WHITE)
        label.next_to(delta_f, LEFT, buff=0.2)
        return delta_f, label

    def animate_vibration(self, axes: Axes, probe: Triangle,
                          delta_f: DecimalNumber, duration: float) -> None:
        """工作点沿合力曲线从非接触区移动到接触区"""
        t = ValueTracker(2.5)
        z_end = self.EQUILIBRIUM_Z

        def update_probe(mob):
            z = t.get_value()
            f = np.clip(float(self.total_force(z)), self.FORCE_RANGE[0], self.FORCE_RANGE[1])
            mob.move_to(axes.c2p(z, f))

        def update_df(mob):
            z = t.get_value()
            slope = self.force_derivative(z)
            mob.set_value(slope * 0.1)

        probe.add_updater(update_probe)
        delta_f.add_updater(update_df)

        self.play(t.animate.set_value(z_end), run_time=duration, rate_func=smooth)

        probe.remove_updater(update_probe)
        delta_f.remove_updater(update_df)

        
    TIME_SCALE = 2.0 / 13 * 10              # 时间缩放因子（>1延长，<1缩短）
    def construct(self):
        ts = self.TIME_SCALE
        """
        # ---- 1. 中央创建悬臂模型 ----
        cantilever = self.cantilever_model()
        self.play(FadeIn(cantilever, shift=UP * 0.5), run_time=0.6 * ts)

        # ---- 2. 模型左移 ----
        self.play(cantilever.animate.shift(LEFT * 3.5), run_time=0.8 * ts)

        # ---- 3. 下方出现原子级样品表面 ----
        sample = self.sample_surface()
        sample.next_to(cantilever, DOWN, buff=0.8)
        self.play(FadeIn(sample, shift=DOWN * 0.3), run_time=0.5 * ts)
        """
        # ---- 4. 右侧弹出统一力公式 ----
        formula = self.force_formula()
        self.play(Write(formula), run_time=0.6 * ts)

        # ---- 5. 公式上移 ----
        self.play(formula.animate.to_edge(UP, buff=0.4), run_time=0.5 * ts)

        # ---- 6. 坐标轴 ----
        axes, axes_labels = self.create_axes()
        self.play(Create(axes), Write(axes_labels), run_time=0.5 * ts)

        # ---- 7. 范德华力曲线 ----
        vdw_curve, vdw_label = self.create_vdw_curve_group(axes)
        self.play(Create(vdw_curve), run_time=0.7 * ts)
        self.play(Write(vdw_label), run_time=0.3 * ts)

        # ---- 8. 泡利排斥力曲线 ----
        pauli_curve, pauli_label = self.create_pauli_curve_group(axes)
        self.play(Create(pauli_curve), run_time=0.7 * ts)
        self.play(Write(pauli_label), run_time=0.3 * ts)

        # ---- 9. 合力曲线 ----
        total_curve, total_label = self.create_total_curve_group(axes)
        self.play(Create(total_curve), run_time=0.35 * ts)
        self.play(Write(total_label), run_time=0.15 * ts)

        # ---- 10. 区域标签 ----
        region_labels = self.create_region_labels(axes)
        self.play(FadeIn(region_labels), run_time=0.5 * ts)

        # ---- 11. 平衡点标记 ----
        eq_point, eq_label = self.create_equilibrium_marker(axes)
        self.play(FadeIn(eq_point), Write(eq_label), run_time=0.5 * ts)

        # ---- 12. 工作点沿曲线从非接触区移动到接触区 ----
        probe = self.create_probe(axes)
        delta_f, delta_f_label = self.create_delta_f_display()
        self.play(FadeIn(probe), FadeIn(delta_f), Write(delta_f_label), run_time=0.4 * ts)
        self.animate_vibration(axes, probe, delta_f, duration=1.0 * ts)
        
class Scene5_AFMForseCurve(Scene):
    pass