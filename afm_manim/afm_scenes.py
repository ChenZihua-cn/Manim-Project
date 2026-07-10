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
    Z_RANGE = (0.5, 2.0)          # 距离范围 (nm)
    FORCE_RANGE = (-2, 6)         # 力范围 (nN)
    A0 = 1.2                      # a₀ — 接触过渡距离 (z+z_s = a₀ 处分界)
    Z_S = 0.28                    # z_s — 距离偏移量
    VDW_COEFF = 0.5               # C = HR/6 — 范德华吸引系数
    CONTACT_COEFF = 20.0          # K = (4/3)E_eff √R — Hertz 排斥刚度
    EQUILIBRIUM_Z = 0.85          # 平衡点位置
    VIBRATION_CYCLES = 2          # 振动周期数
    VIBRATION_AMPLITUDE = 0.05    # 振动幅度

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.a0 = self.A0
        self.z_s = self.Z_S
        self.vdw_coeff = self.VDW_COEFF
        self.contact_coeff = self.CONTACT_COEFF
    
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

        # z+z_s = D

        formula = MathTex(
            r"F(z) = \begin{cases} "
            r"\dfrac{HR}{6(D)^2}, & D > a_0 \\[1em] "
            r"\dfrac{HR}{6a_0^2} + \dfrac{4}{3} E_{\rm eff} \sqrt{R}\, (a_0 - D)^{3/2}, & D \leq a_0 "
            r"\end{cases}",
            font_size=36, color=WHITE
            ).scale(0.8)
        formula.to_edge(RIGHT, buff=1.0)
        return formula

    def _vdw_component(self, z: float | np.ndarray) -> np.ndarray:
        """范德华吸引项: -C / (z + z_s)²"""
        d = np.asarray(z) + self.z_s
        return -self.vdw_coeff / (d ** 2)

    def _contact_component(self, z: float | np.ndarray) -> np.ndarray:
        """Hertz 接触排斥项: K · (a₀ - z - z_s)^(3/2)，仅接触区非零"""
        d = np.asarray(z) + self.z_s
        result = np.zeros_like(d, dtype=float)
        mask = d <= self.a0
        result[mask] = self.contact_coeff * (self.a0 - d[mask]) ** 1.5
        return result

    def total_force(self, z: float | np.ndarray) -> float | np.ndarray:
        """合力: 与 force_formula 完全一致的 piecewise 定义"""
        scalar = np.isscalar(z)
        d = np.atleast_1d(np.asarray(z) + self.z_s)
        vdw_at_a0 = self.vdw_coeff / (self.a0 ** 2)
        result = -self.vdw_coeff / (d ** 2)
        mask_contact = d <= self.a0
        result[mask_contact] = -vdw_at_a0 + self.contact_coeff * (self.a0 - d[mask_contact]) ** 1.5
        if scalar:
            return float(result[0])
        return result

    def force_derivative(self, z: float, h: float = 0.001) -> float:
        """中心差分数值求导"""
        return float((self.total_force(z + h) - self.total_force(z - h)) / (2 * h))
    
    def create_axes(self) -> tuple[Axes, VGroup]:
        """创建坐标轴和标签（仅坐标轴，不含曲线）"""
        axes = Axes(
            x_range=[*self.Z_RANGE, 0.5],
            y_range=[*self.FORCE_RANGE, 1],
            x_length=8, y_length=4,
            axis_config={"include_tip": False},
            x_axis_config={"numbers_to_include": [1, 2]},
            y_axis_config={"numbers_to_include": [-1, 0, 2, 4]}
        ).scale(0.8).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.5)
        
        labels = VGroup(
            MathTex(r"z \text{ (nm)}", font_size=24).next_to(axes.x_axis, RIGHT),
            MathTex(r"F \text{ (nN)}", font_size=24).next_to(axes.y_axis, UP)
        )
        return axes, labels
    
    def create_vdw_curve_group(self, axes: Axes) -> tuple[ParametricFunction, MathTex]:
        """创建范德华力曲线及其标签"""
        curve = axes.plot(
            lambda z: float(self._vdw_component(z)),
            x_range=[0.7, 2],
            color=COLOR_VDW,
            stroke_width=3
        )
        # 标签紧挨曲线（z=1.5附近，曲线y≈-0.17的位置）
        label = MathTex(r"F_{\text{vdW}} \propto -1/(z+z_s)^2", color=COLOR_VDW, font_size=26)
        label.move_to(axes.c2p(1.5, -0.45))

        return curve, label

    def create_contact_curve_group(self, axes: Axes) -> tuple[ParametricFunction, MathTex]:
        """创建 Hertz 接触排斥力曲线及其标签"""
        curve = axes.plot(
            lambda z: float(self._contact_component(z)),
            x_range=[0.5, 2],
            color=COLOR_PAULI,
            stroke_width=3
        )
        # 标签紧贴曲线上升段（z=0.7处）
        label = MathTex(r"F_{\text{Hertz}}"
                        r"\propto (a_0 - z - z_s)^{3/2}" , color=COLOR_PAULI, font_size=26)
        label.move_to(axes.c2p(0.75, 4.8)).shift(RIGHT*0.4)

        return curve, label

    def create_total_curve_group(self, axes: Axes) -> tuple[ParametricFunction, MathTex]:
        """创建合力曲线及其标签"""
        curve = axes.plot(
            lambda z: float(self.total_force(z)),
            x_range=[0.5, 2],
            color=WHITE,
            stroke_width=4
        )
        # 标签紧贴合力曲线右侧
        label = MathTex(r"F_{\text{total}}", color=WHITE, font_size=26)
        label.move_to(axes.c2p(1.6, 0.6))

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
        non_contact.move_to(axes.c2p(1.6, -1.0))
        contact = Text("接触区", font_size=22, color=COLOR_PAULI).scale(0.8)
        contact.move_to(axes.c2p(0.7, 4.5))
        return VGroup(divider, non_contact, contact)

    def create_probe(self, axes: Axes) -> Triangle:
        """曲线上工作点标记，初始位于非接触区"""
        z_start = 1.8
        f_start = np.clip(float(self.total_force(z_start)), self.FORCE_RANGE[0], self.FORCE_RANGE[1])
        probe = Triangle(color=GREY, fill_opacity=1).scale(0.6)
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
        t = ValueTracker(1.8)
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

        # ---- 8. Hertz 接触排斥力曲线 ----
        pauli_curve, pauli_label = self.create_contact_curve_group(axes)
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