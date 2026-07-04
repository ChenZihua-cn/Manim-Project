"""
AFM 幅度调制系统结构示意图动画
展示反馈控制系统的信号流向和工作原理
"""

# trunk-ignore(ruff/F403)
# pyright: ignore[reportWildcardImportFromLibrary]

from manim import *
import numpy as np

# 颜色定义
COLOR_BLOCK = "#2196F3"      # 功能模块 - 蓝色
COLOR_PROBE = "#FF5722"      # 探针 - 橙红色
COLOR_SIGNAL = "#FFC107"     # 信号流 - 黄色
COLOR_ERROR = "#E53935"      # 误差信号 - 红色
COLOR_FEEDBACK = "#43A047"   # 反馈 - 绿色
COLOR_COMPUTER = "#9C27B0"   # 计算机 - 紫色
COLOR_SCANNER = "#00BCD4"    # 扫描器 - 青色
COLOR_SURFACE = "#795548"    # 样品表面 - 棕色


class AFMSystemDiagram(Scene):
    """
    AFM幅度调制系统结构示意图动画
    对应 Mermaid 图:
      Probe → AmpDet → Comp ← Ref
      Comp → Error → FB ↔ Computer → Display
      FB → ScanCtrl / SpaceCtrl
      Exc → ScanCtrl / SpaceCtrl
      ScanCtrl → X,Y → Scanner → Sample -.-> Probe
      SpaceCtrl → Z  → Scanner
    """

    # ---- 布局常量 ----
    # 列 (x)
    X_PROBE = -5.5
    X_DETECT = -2.8
    X_COMP = 0.0
    X_FB = 2.8
    X_DIGITAL = 5.5
    X_SCAN = 0.5
    X_SPACE = 3.5
    X_SCANNER = -3.5
    X_EXC = 2.0

    # 行 (y)
    Y_MAIN = 2.0       # 主信号链
    Y_REF = 3.2        # 参考值标签
    Y_DISPLAY = 0.2    # 显示器
    Y_CTRL = -0.5      # 扫描/间距控制
    Y_SCANNER = -1.8   # 三维扫描器
    Y_EXC = -3.2       # 激励信号

    def construct(self):
        # ========== 0. 开场标题 ==========
        title = Text("幅度调制 AFM 系统结构", font_size=40, color=WHITE)
        title.to_edge(UP, buff=0.3)
        subtitle = Text("Amplitude Modulation AFM System", font_size=24, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.1)

        self.play(Write(title), FadeIn(subtitle), run_time=1.5)
        self.wait(0.5)
        self.play(FadeOut(subtitle), title.animate.scale(0.7).to_corner(UL), run_time=1)

        # ========== 1. 布局：列式排列 ==========
        #   Col1        Col2        Col3      Col4        Col5
        #   Probe  →  AmpDet  →  ((±))  →   FB    ↔  Computer
        #     ↑                                   ↓
        #     │            ScanCtrl  SpaceCtrl   Display
        #     │              ↓   ↘    ↙   ↓
        #     └──(反馈)── Scanner  ←───  Excitation

        probe_group = self.create_probe_system()
        probe_group.move_to([self.X_PROBE, self.Y_MAIN, 0])

        amp_detector = self.create_block("振幅检测", width=2.2, height=1)
        amp_detector.move_to([self.X_DETECT, self.Y_MAIN, 0])

        comparator = self.create_comparator()
        comparator.move_to([self.X_COMP, self.Y_MAIN, 0])

        ref_label = Text("参考值", font_size=20, color=WHITE)
        ref_label.next_to(comparator, UP, buff=0.5)

        error_label = Text("误差信号", font_size=20, color=COLOR_ERROR)
        error_label.next_to(comparator, DOWN, buff=0.5)

        feedback_ctrl = self.create_block("反馈控制器", width=2.2, height=1.2, color=COLOR_FEEDBACK)
        feedback_ctrl.move_to([self.X_FB, self.Y_MAIN, 0])

        computer = self.create_computer()
        computer.move_to([self.X_DIGITAL, self.Y_MAIN, 0])

        display = self.create_monitor()
        display.move_to([self.X_DIGITAL, self.Y_DISPLAY, 0])

        scan_ctrl = self.create_block("扫描控制\n信号处理", width=1.8, height=1.2, font_size=18)
        scan_ctrl.move_to([self.X_SCAN, self.Y_CTRL, 0])

        gap_ctrl = self.create_block("间距控制\n信号处理", width=1.8, height=1.2, font_size=18)
        gap_ctrl.move_to([self.X_SPACE, self.Y_CTRL, 0])

        scanner = self.create_scanner()
        scanner.move_to([self.X_SCANNER, self.Y_SCANNER, 0])

        excite_label = Text("激励信号", font_size=20, color=COLOR_SIGNAL)
        excite_label.move_to([self.X_EXC, self.Y_EXC, 0])

        # ========== 2. 逐步显示各组件 ==========
        self.play(FadeIn(probe_group), run_time=1)
        self.wait(0.2)
        self.play(FadeIn(amp_detector), run_time=0.6)
        self.play(FadeIn(comparator), Write(ref_label), run_time=0.6)
        self.play(Write(error_label), run_time=0.4)
        self.play(FadeIn(feedback_ctrl), run_time=0.6)
        self.play(FadeIn(computer), FadeIn(display), run_time=0.6)
        self.play(FadeIn(scan_ctrl), FadeIn(gap_ctrl), run_time=0.6)
        self.play(FadeIn(scanner), Write(excite_label), run_time=0.6)
        self.wait(0.3)

        # ========== 3. 绘制连接线 (曲线优先) ==========
        lines = self._create_all_connections(
            probe_group, amp_detector, comparator, ref_label,
            feedback_ctrl, computer, display,
            scan_ctrl, gap_ctrl, scanner, excite_label,
        )

        for line_group in lines:
            self.play(Create(line_group), run_time=0.6)

        self.wait(0.8)

        # ========== 4. 信号流动画 ==========
        self._animate_full_signal_flow(
            probe_group, amp_detector, comparator,
            feedback_ctrl, scan_ctrl, gap_ctrl, scanner,
        )

        # ========== 5. 文字说明 ==========
        self.play(*[FadeOut(obj) for obj in self.mobjects if obj is not title], run_time=1)

        desc_text = VGroup(
            Text("工作流程：", font_size=36, color=YELLOW),
            Text("1. 激励信号驱动扫描控制与间距控制", font_size=28, color=WHITE),
            Text("2. 探针振动 → 振幅检测 → 与参考值比较 → 误差信号", font_size=28, color=WHITE),
            Text("3. 反馈控制器处理误差，输出调节信号", font_size=28, color=WHITE),
            Text("4. 三维扫描器移动样品，探针-样品作用力闭环反馈", font_size=28, color=WHITE),
            Text("5. 计算机记录形貌并显示", font_size=28, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        desc_text.move_to(ORIGIN)

        self.play(Write(desc_text[0]), run_time=0.5)
        for i in range(1, len(desc_text)):
            self.play(Write(desc_text[i]), run_time=0.6)
            self.wait(0.15)

        self.play(FadeOut(title), run_time=0.5)
        self.wait(2.5)
        self.play(FadeOut(desc_text), run_time=1)

    # ========== 连接线 ==========

    def _create_all_connections(self, probe, amp_det, comp, ref_label,
                                 fb, computer, display,
                                 scan_ctrl, gap_ctrl, scanner, excite):
        """创建所有信号连接线，返回按绘制顺序排列的 VGroup 列表"""

        lines = []

        # ---- 主链 (同排，直箭头) ----

        # ① Probe → 振幅检测
        p_right = probe.get_right() + RIGHT * 0.1
        ad_left = amp_det.get_left() + LEFT * 0.1
        lines.append(VGroup(
            self.create_signal_line(p_right, ad_left, color=COLOR_SIGNAL),
            self.create_signal_line(p_right, ad_left, color=WHITE).set_opacity(0.25),
        ))

        # ② 振幅检测 → 比较器
        lines.append(self.create_signal_line(
            amp_det.get_right(), comp.get_left(), color=COLOR_SIGNAL
        ))

        # ③ 参考值 → 比较器
        lines.append(self.create_signal_line(
            ref_label.get_bottom(), comp.get_top(), color=WHITE
        ))

        # ④ 比较器 → 反馈控制器 (误差信号, 红色)
        lines.append(self.create_signal_line(
            comp.get_right(), fb.get_left() + UP * 0.2, color=COLOR_ERROR
        ))

        # ⑤ 反馈控制器 ↔ 计算机 (双向)
        lines.append(DoubleArrow(
            fb.get_right(), computer.get_left(),
            color=COLOR_FEEDBACK, buff=0.1, stroke_width=2, tip_length=0.15,
        ))

        # ⑥ 计算机 → 显示器
        lines.append(self.create_signal_line(
            computer.get_bottom(), display.get_top(), color=COLOR_COMPUTER
        ))

        # ---- 分支 (曲线) ----

        # ⑦ 反馈控制器 → 扫描控制 (左下弧线)
        lines.append(self.create_curved_signal_line(
            fb.get_left() + DOWN * 0.1,
            scan_ctrl.get_top() + UP * 0.1,
            angle=PI / 3.5, color=COLOR_FEEDBACK,
        ))

        # ⑧ 反馈控制器 → 间距控制 (右下弧线)
        lines.append(self.create_curved_signal_line(
            fb.get_bottom() + DOWN * 0.1,
            gap_ctrl.get_top() + UP * 0.1,
            angle=-PI / 3.5, color=COLOR_FEEDBACK,
        ))

        # ⑨ 激励信号 → 扫描控制 (左上弧线)
        lines.append(self.create_curved_signal_line(
            excite.get_top() + UP * 0.1 + LEFT * 0.2,
            scan_ctrl.get_bottom() + DOWN * 0.15,
            angle=-PI / 4, color=COLOR_SIGNAL,
        ))

        # ⑩ 激励信号 → 间距控制 (右上弧线)
        lines.append(self.create_curved_signal_line(
            excite.get_top() + UP * 0.1 + RIGHT * 0.2,
            gap_ctrl.get_bottom() + DOWN * 0.15,
            angle=PI / 4, color=COLOR_SIGNAL,
        ))

        # ⑪ 扫描控制 → 三维扫描器 (X, Y) (左弯弧线)
        line_xy = self.create_curved_signal_line(
            scan_ctrl.get_left() + LEFT * 0.1,
            scanner.get_right() + RIGHT * 0.1 + UP * 0.4,
            angle=PI / 3, color=COLOR_SIGNAL,
        )
        xy_label = MathTex(r"X,Y", font_size=16, color=WHITE).next_to(line_xy, UP, buff=0.1)
        lines.append(VGroup(line_xy, xy_label))

        # ⑫ 间距控制 → 三维扫描器 (Z) (弧线绕行)
        line_z = self.create_curved_signal_line(
            gap_ctrl.get_left() + LEFT * 0.1,
            scanner.get_right() + RIGHT * 0.1 + DOWN * 0.4,
            angle=-PI / 2.8, color=COLOR_SIGNAL,
        )
        z_label = MathTex(r"Z", font_size=16, color=WHITE).next_to(line_z, DOWN, buff=0.1)
        lines.append(VGroup(line_z, z_label))

        # ⑬ 三维扫描器 → 样品 → 探针 (物理反馈，虚线弧线)
        lines.append(self._create_feedback_dashed(scanner, probe))

        return lines

    # ---- 曲线/贝塞尔辅助 ----

    def create_curved_signal_line(self, start, end, angle=PI / 3, color=COLOR_SIGNAL):
        """使用 CurvedArrow 创建曲线信号线"""
        return CurvedArrow(start, end, angle=float(angle), color=color,
                           stroke_width=2, tip_length=0.15)

    def _create_feedback_dashed(self, scanner, probe):
        """扫描器 → 探针 的虚线物理反馈"""
        sc_left = scanner.get_left() + LEFT * 0.2
        probe_tip = probe[3].get_center()

        return DashedLine(
            sc_left + DOWN * 0.3,
            probe_tip,
            dash_length=0.15,
            color=COLOR_SCANNER,
            stroke_width=2,
        )

    # ========== 信号流动画 ==========

    def _animate_full_signal_flow(self, probe, amp_det, comp, fb, scan_ctrl, gap_ctrl, scanner):
        """展示完整信号流，跟随曲线路径"""
        # 各阶段信号灯动画已注释
        _ = (amp_det, comp, fb, scan_ctrl, gap_ctrl)

        # 阶段1: 探针 → 振幅检测 → 比较器
        # dot = Dot(color=COLOR_SIGNAL, radius=0.08)
        # path1 = VMobject()
        # path1.set_points_as_corners([
        #     probe.get_right() + RIGHT * 0.1,
        #     amp_det.get_left() + LEFT * 0.1,
        #     amp_det.get_right(),
        #     comp.get_left(),
        # ])
        # self.play(MoveAlongPath(dot, path1), run_time=2, rate_func=linear)
        # self.play(FadeOut(dot), run_time=0.15)

        # 阶段2: 比较器 → 反馈控制器 (误差信号)
        # dot2 = Dot(color=COLOR_ERROR, radius=0.08)
        # path2 = VMobject()
        # path2.set_points_as_corners([
        #     comp.get_right(),
        #     fb.get_left() + UP * 0.2,
        # ])
        # self.play(MoveAlongPath(dot2, path2), run_time=1.5, rate_func=linear)

        # 阶段3: 反馈控制器 分支 → 扫描控制 + 间距控制 (沿曲线)
        # dot3a = Dot(color=COLOR_FEEDBACK, radius=0.08)
        # dot3b = Dot(color=COLOR_FEEDBACK, radius=0.08)
        # path3a = CurvedArrow(
        #     fb.get_left() + DOWN * 0.1,
        #     scan_ctrl.get_top() + UP * 0.1,
        #     angle=PI / 3.5, color=COLOR_FEEDBACK, stroke_width=0,
        # )
        # path3b = CurvedArrow(
        #     fb.get_bottom() + DOWN * 0.1,
        #     gap_ctrl.get_top() + UP * 0.1,
        #     angle=-PI / 3.5, color=COLOR_FEEDBACK, stroke_width=0,
        # )
        # self.play(
        #     MoveAlongPath(dot3a, path3a),
        #     MoveAlongPath(dot3b, path3b),
        #     run_time=2, rate_func=linear,
        # )
        # self.play(FadeOut(dot3a), FadeOut(dot3b), FadeOut(dot2), run_time=0.2)

        # 阶段4: 扫描控制 → 三维扫描器
        # dot4 = Dot(color=COLOR_SIGNAL, radius=0.08)
        # path4 = CurvedArrow(
        #     scan_ctrl.get_left() + LEFT * 0.1,
        #     scanner.get_right() + RIGHT * 0.1 + UP * 0.4,
        #     angle=PI / 3, color=COLOR_SIGNAL, stroke_width=0,
        # )
        # self.play(MoveAlongPath(dot4, path4), run_time=1.2, rate_func=linear)
        # self.play(FadeOut(dot4), run_time=0.15)

        scanner_body = scanner[0]
        self.play(scanner_body.animate.set_fill(opacity=0.5).set_color(YELLOW), run_time=0.3)
        self.play(scanner_body.animate.set_fill(opacity=0.2).set_color(COLOR_SCANNER), run_time=0.3)

        # 阶段5: 物理反馈 (扫描器 → 探针)
        # dot5 = Dot(color=COLOR_SCANNER, radius=0.08)
        # sc_left = scanner.get_left() + LEFT * 0.2
        # probe_tip = probe[3].get_center()
        # feedback_path = Line(
        #     sc_left + DOWN * 0.3,
        #     probe_tip,
        #     stroke_width=0,
        # )
        # self.play(MoveAlongPath(dot5, feedback_path), run_time=1.2, rate_func=linear)
        # self.play(FadeOut(dot5), run_time=0.15)

        # 探针闪烁表示受到物理作用
        probe_tip_mobj = probe[3]
        self.play(probe_tip_mobj.animate.set_color(YELLOW), run_time=0.2)
        self.play(probe_tip_mobj.animate.set_color(COLOR_PROBE), run_time=0.2)

        self.wait(0.5)

    # ========== 辅助方法 ==========

    def create_block(self, text, width=2.0, height=1.0, color=COLOR_BLOCK, font_size=20):
        rect = Rectangle(width=float(width), height=float(height), color=color,
                         fill_opacity=0.2, stroke_width=2)
        label = Text(text, font_size=font_size, color=WHITE)
        label.move_to(rect.get_center())
        return VGroup(rect, label)

    def create_comparator(self):
        circle = Circle(radius=0.4, color=WHITE, stroke_width=2)
        minus = MathTex(r"-", font_size=24, color=WHITE).move_to(
            circle.get_center()).shift(UP * 0.15 + RIGHT * 0.15)
        plus = MathTex(r"+", font_size=20, color=WHITE).move_to(
            circle.get_center()).shift(DOWN * 0.15 + RIGHT * 0.15)
        return VGroup(circle, minus, plus)

    def create_probe_system(self):
        surface = Rectangle(width=2, height=0.3, color=COLOR_SURFACE, fill_opacity=0.5)
        surface.shift(DOWN * 1)
        surface_label = Text("样品", font_size=18, color=WHITE).next_to(surface, DOWN, buff=0.1)

        cantilever = Line((-0.8, 0.5, 0), (0, 0.5, 0), color=GREY, stroke_width=4)
        tip = Polygon((-0.05, 0.2, 0), (0.05, 0.2, 0), (0, 0, 0),
                      color=COLOR_PROBE, fill_opacity=1).next_to(cantilever, DOWN+RIGHT, buff=0)
        probe_label = Text("探针", font_size=18, color=COLOR_PROBE).next_to(cantilever, UP, buff=0.1)

        fixture = Rectangle(width=0.3, height=0.6, color=GREY, fill_opacity=0.5)
        fixture.move_to((-0.95, 0.5, 0))

        return VGroup(surface, surface_label, cantilever, tip, probe_label, fixture)

    def create_computer(self):
        case = Rectangle(width=1.2, height=1.5, color=COLOR_COMPUTER, fill_opacity=0.2, stroke_width=2)
        screen = Rectangle(width=1, height=0.6, color=WHITE, fill_opacity=0.1, stroke_width=1)
        screen.move_to(case.get_center()).shift(UP * 0.2)
        label = Text("计算机", font_size=18, color=WHITE)
        label.next_to(case, DOWN, buff=0.1)
        return VGroup(case, screen, label)

    def create_monitor(self):
        frame = Rectangle(width=1.8, height=1.2, color=COLOR_COMPUTER, fill_opacity=0.2, stroke_width=2)
        content = Rectangle(width=1.6, height=1, color=WHITE, fill_opacity=0.1, stroke_width=1)
        wave = FunctionGraph(
            lambda x: 0.2 * np.sin(3 * x) + 0.1 * np.sin(7 * x),
            x_range=(-0.7, 0.7),
            color=COLOR_SIGNAL, stroke_width=2,
        )
        wave.scale(0.5).move_to(content)
        base = Polygon((-0.2, -0.6, 0), (0.2, -0.6, 0), (0, -0.8, 0),
                       color=GREY, fill_opacity=0.5)
        label = Text("显示器", font_size=18, color=WHITE)
        label.next_to(frame, DOWN, buff=0.1).shift(DOWN * 0.3)
        return VGroup(frame, content, wave, base, label)

    def create_scanner(self):
        body = Rectangle(width=1.5, height=2, color=COLOR_SCANNER, fill_opacity=0.2, stroke_width=2)
        x_label = MathTex(r"X", font_size=20, color=WHITE).move_to(
            body.get_right() + RIGHT * 0.3 + UP * 0.5)
        y_label = MathTex(r"Y", font_size=20, color=WHITE).move_to(
            body.get_right() + RIGHT * 0.3)
        z_label = MathTex(r"Z", font_size=20, color=WHITE).move_to(
            body.get_right() + RIGHT * 0.3 + DOWN * 0.5)
        inner_text = Text("三维扫描器", font_size=16, color=WHITE)
        inner_text.move_to(body.get_center())
        return VGroup(body, x_label, y_label, z_label, inner_text)

    def create_signal_line(self, start, end, color=COLOR_SIGNAL, buff=0.1):
        return Arrow(start, end, color=color, buff=buff, stroke_width=2, tip_length=0.15)


class AFMSystemSimplified(Scene):
    """
    简化版AFM系统动画 - 更清晰的信号流展示
    时长：约20秒
    """

    def construct(self):
        # 标题
        title = Text("AFM 反馈控制系统", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1)

        # 核心组件位置
        positions = {
            'probe': LEFT * 4 + DOWN * 1,
            'detector': LEFT * 2 + UP * 1.5,
            'comparator': RIGHT * 0.5 + UP * 1.5,
            'feedback': RIGHT * 3 + UP * 0.5,
            'scanner': LEFT * 3 + DOWN * 2,
            'computer': RIGHT * 5 + UP * 0.5,
            'display': RIGHT * 5 + DOWN * 2
        }

        # 创建组件
        probe = self.create_probe_icon().move_to(positions['probe'])
        detector = self.create_block_icon("振幅检测").move_to(positions['detector'])
        comparator = self.create_circle_icon("-\n+").move_to(positions['comparator'])
        feedback = self.create_block_icon("反馈控制", color=COLOR_FEEDBACK).move_to(positions['feedback'])
        scanner = self.create_block_icon("扫描器", color=COLOR_SCANNER).move_to(positions['scanner'])
        computer = self.create_block_icon("计算机", color=COLOR_COMPUTER).move_to(positions['computer'])
        display = self.create_block_icon("显示", color=COLOR_COMPUTER).move_to(positions['display'])

        # 显示所有组件
        components = VGroup(probe, detector, comparator, feedback, scanner, computer, display)
        self.play(FadeIn(components), run_time=2)

        # 绘制连接线
        connections = self.create_connections(positions)
        self.play(Create(connections), run_time=2)

        # 信号流动画
        self.animate_workflow(positions)

        # 结束
        self.wait(2)

    def create_probe_icon(self):
        """探针图标"""
        cantilever = Line((-0.5, 0.3, 0), (0.3, 0.3, 0), color=GREY, stroke_width=3)
        tip = Triangle(color=COLOR_PROBE).scale(0.15).rotate(PI)
        tip.move_to((0.3, 0, 0))
        sample = Rectangle(width=1.2, height=0.2, color=COLOR_SURFACE, fill_opacity=0.5)
        sample.move_to((0, -0.4, 0))
        label = Text("探针", font_size=16, color=WHITE).next_to(cantilever, UP, buff=0.1)
        return VGroup(sample, cantilever, tip, label)

    def create_block_icon(self, text, color=COLOR_BLOCK, size=0.8):
        """方块图标"""
        rect = Square(side_length=size, color=color, fill_opacity=0.2, stroke_width=2)
        label = Text(text, font_size=16, color=WHITE)
        label.move_to(rect)
        return VGroup(rect, label)

    def create_circle_icon(self, text):
        """圆形图标（比较器）"""
        circle = Circle(radius=0.4, color=WHITE, stroke_width=2)
        label = MathTex(text, font_size=20, color=WHITE)
        label.move_to(circle)
        return VGroup(circle, label)

    def create_connections(self, pos):
        """创建连接线"""
        lines = VGroup()

        # 探针 -> 检测器
        lines.add(Arrow(pos['probe'] + UP * 0.5, pos['detector'] + LEFT * 0.4,
                       color=COLOR_SIGNAL, buff=0.1, stroke_width=2))

        # 检测器 -> 比较器
        lines.add(Arrow(pos['detector'] + RIGHT * 0.4, pos['comparator'] + LEFT * 0.4,
                       color=COLOR_SIGNAL, buff=0.1, stroke_width=2))

        # 比较器 -> 反馈控制
        lines.add(Arrow(pos['comparator'] + RIGHT * 0.4, pos['feedback'] + LEFT * 0.4,
                       color=COLOR_ERROR, buff=0.1, stroke_width=2))

        # 反馈控制 -> 计算机
        lines.add(Arrow(pos['feedback'] + RIGHT * 0.4, pos['computer'] + LEFT * 0.4,
                       color=COLOR_FEEDBACK, buff=0.1, stroke_width=2))

        # 计算机 <-> 显示
        lines.add(DoubleArrow(pos['computer'] + DOWN * 0.4, pos['display'] + UP * 0.4,
                             color=COLOR_COMPUTER, buff=0.1, stroke_width=2))

        # 反馈控制 -> 扫描器
        lines.add(Arrow(pos['feedback'] + DOWN * 0.4, pos['scanner'] + RIGHT * 0.4,
                       color=COLOR_FEEDBACK, buff=0.1, stroke_width=2))

        return lines

    def animate_workflow(self, pos):
        """工作流动画"""
        # 信号点
        signal = Dot(color=COLOR_SIGNAL, radius=0.1)

        # 路径1: 探针 -> 检测器 -> 比较器
        path1 = VMobject()
        path1.set_points_as_corners([
            pos['probe'] + UP * 0.5,
            pos['detector'] + LEFT * 0.4,
            pos['detector'] + RIGHT * 0.4,
            pos['comparator'] + LEFT * 0.4
        ])

        self.play(MoveAlongPath(signal, path1), run_time=2, rate_func=linear)

        # 路径2: 比较器 -> 反馈 -> 扫描器
        path2 = VMobject()
        path2.set_points_as_corners([
            pos['comparator'] + RIGHT * 0.4,
            pos['feedback'] + LEFT * 0.4,
            pos['feedback'] + DOWN * 0.4,
            pos['scanner'] + RIGHT * 0.4
        ])

        signal2 = Dot(color=COLOR_FEEDBACK, radius=0.1)
        self.play(MoveAlongPath(signal2, path2), run_time=2, rate_func=linear)

        # 扫描器动作示意
        scanner_rect = Square(side_length=0.8, color=COLOR_SCANNER, fill_opacity=0.2)
        scanner_rect.move_to(pos['scanner'])
        self.play(scanner_rect.animate.scale(1.2).set_color(YELLOW), run_time=0.5)
        self.play(scanner_rect.animate.scale(1/1.2).set_color(COLOR_SCANNER), run_time=0.5)

        self.wait(1)


# 渲染入口
if __name__ == "__main__":
    pass
