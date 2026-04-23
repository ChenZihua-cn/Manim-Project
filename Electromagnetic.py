"""
电磁场炫技动画 - 洛伦兹力之舞
展示带电粒子在交叉电磁场中的优美运动轨迹

运行命令:
    manimgl Experimental/Electromagnetic.py LorentzDance
    manimgl Experimental/Electromagnetic.py LorentzDance -w --hd  # 导出高清视频
"""

from manimlib import *
import numpy as np


# =============================================================================
# 物理参数配置
# =============================================================================

class PhysicsConfig:
    """物理参数配置类"""
    # 电磁场 (使用统一单位制)
    E_FIELD = np.array([0.0, 0.0, 2.0])      # 电场 (z方向)
    B_FIELD = np.array([0.0, 2.0, 0.0])      # 磁场 (y方向)
    
    # 粒子参数
    Q_POSITIVE = 1.0                         # 正电荷
    Q_NEGATIVE = -1.0                        # 负电荷
    MASS = 1.0                               # 质量
    
    # 初始速度
    V0_BASE = np.array([1.0, 0.0, 0.5])      # 基础初速度
    
    # 模拟参数
    T_MAX = 10.0                             # 模拟总时间
    DT = 0.02                                # 时间步长
    
    # 可视化参数
    PARTICLE_RADIUS = 0.08
    TRAIL_LENGTH = 2.0                       # 尾迹持续时间


# =============================================================================
# 轨迹计算
# =============================================================================

def lorentz_force(state, q, m, E, B):
    """
    计算洛伦兹力
    state: [x, y, z, vx, vy, vz]
    返回: [vx, vy, vz, ax, ay, az]
    """
    v = state[3:]
    F_electric = q * E
    F_magnetic = q * np.cross(v, B)
    F_total = F_electric + F_magnetic
    acceleration = F_total / m
    return np.concatenate([v, acceleration])


def compute_trajectory(q, m, v0, r0, E, B, t_max, dt=0.02):
    """
    使用RK4数值积分计算粒子轨迹
    
    返回:
        points: 位置数组 (N, 3)
        velocities: 速度数组 (N, 3)
        times: 时间数组 (N,)
    """
    n_steps = int(t_max / dt) + 1
    times = np.linspace(0, t_max, n_steps)
    
    # 状态: [x, y, z, vx, vy, vz]
    state = np.concatenate([r0, v0])
    states = [state.copy()]
    
    for i in range(n_steps - 1):
        # RK4积分
        k1 = lorentz_force(state, q, m, E, B)
        k2 = lorentz_force(state + 0.5 * dt * k1, q, m, E, B)
        k3 = lorentz_force(state + 0.5 * dt * k2, q, m, E, B)
        k4 = lorentz_force(state + dt * k3, q, m, E, B)
        
        state = state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
        states.append(state.copy())
    
    states = np.array(states)
    points = states[:, :3]
    velocities = states[:, 3:]
    
    return points, velocities, times


def get_analytical_trajectory(q, m, v0, r0, E, B, t_max, dt=0.02):
    """
    获取解析解轨迹（用于均匀电磁场）
    适用于 E ⊥ B 的情况
    """
    n_steps = int(t_max / dt) + 1
    times = np.linspace(0, t_max, n_steps)
    
    B_mag = np.linalg.norm(B)
    B_hat = B / B_mag
    
    # 漂移速度 v_d = E×B / B²
    v_drift = np.cross(E, B) / (B_mag ** 2)
    
    # 回旋频率
    omega = q * B_mag / m
    
    # 相对漂移系的速度
    v_rel = v0 - v_drift
    
    # 将相对速度分解为平行和垂直于B的分量
    v_parallel = np.dot(v_rel, B_hat) * B_hat
    v_perp = v_rel - v_parallel
    v_perp_mag = np.linalg.norm(v_perp)
    
    # 圆周运动半径
    r_cyclotron = m * v_perp_mag / (abs(q) * B_mag)
    
    # 构造垂直于B的平面上的基向量
    if v_perp_mag > 1e-10:
        e1 = v_perp / v_perp_mag
        e2 = np.cross(B_hat, e1)
    else:
        # 如果v_perp=0，选择任意垂直于B的基
        arbitrary = np.array([1.0, 0.0, 0.0]) if abs(B_hat[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
        e1 = np.cross(B_hat, arbitrary)
        e1 = e1 / np.linalg.norm(e1)
        e2 = np.cross(B_hat, e1)
    
    # 计算轨迹
    points = []
    for t in times:
        # 漂移运动
        r_drift = r0 + v_drift * t + v_parallel * t
        
        # 圆周运动 (回旋)
        if q > 0:
            r_gyro = r_cyclotron * (np.sin(omega * t) * e1 + (1 - np.cos(omega * t)) * e2)
        else:
            r_gyro = r_cyclotron * (np.sin(omega * t) * e1 - (1 - np.cos(omega * t)) * e2)
        
        points.append(r_drift + r_gyro)
    
    return np.array(points), times


# =============================================================================
# 带电粒子类
# =============================================================================

class ChargedParticle(Group):
    """带电粒子，包含球体、光晕和电荷标记"""
    
    def __init__(self, charge=1.0, mass=1.0, color=YELLOW, 
                 radius=0.08, show_sign=True, **kwargs):
        super().__init__(**kwargs)
        
        self.charge = charge
        self.mass = mass
        self.radius = radius
        
        # 主体球体
        self.sphere = Sphere(radius=radius, resolution=(25, 13))
        self.sphere.set_color(color)
        self.sphere.set_gloss(0.8)
        self.sphere.set_shading(0.3, 0.5, 0.2)
        
        # 光晕效果 (外圈)
        self.glow = Sphere(radius=radius * 1.5, resolution=(15, 8))
        self.glow.set_color(color)
        self.glow.set_opacity(0.2)
        
        self.add(self.sphere, self.glow)
        
        # 电荷标记 (+/-)
        if show_sign:
            sign = "+" if charge > 0 else "-"
            self.sign_text = Text(sign, font_size=24, color=WHITE)
            self.sign_text.move_to(self.get_center())
            self.add(self.sign_text)
    
    def update_sign_position(self):
        """更新符号位置到球心"""
        if hasattr(self, 'sign_text'):
            self.sign_text.move_to(self.get_center())


# =============================================================================
# 主场景
# =============================================================================

class LorentzDance(ThreeDScene):
    """
    洛伦兹力之舞 - 带电粒子在电磁场中的运动
    """
    
    def construct(self):
        # 设置背景
        from manimlib.utils.color import color_to_rgba
        self.camera.background_rgba = list(color_to_rgba("#0a0a15", 1.0))
        
        # 设置初始摄像机角度
        self.frame.set_euler_angles(theta=-45 * DEGREES, phi=65 * DEGREES)
        
        # 创建场景
        self.setup_axes()
        self.setup_fields()
        
        # 标题
        title = Text("Lorentz Force Dance", font_size=36, color=WHITE)
        title.to_edge(UP)
        title.fix_in_frame()
        self.add(title)
        
        # 等待一下
        self.wait(0.5)
        
        # 动画序列
        self.animate_intro()
        self.animate_single_particle()
        self.animate_multiple_particles()
        self.animate_camera_rotation()
        self.animate_outro()
    
    def setup_axes(self):
        """设置3D坐标系"""
        self.axes = ThreeDAxes(
            x_range=(-6, 6, 1),
            y_range=(-4, 4, 1),
            z_range=(-4, 4, 1),
            height=8,
            width=12,
            depth=8,
        )
        self.axes.set_stroke(GREY, opacity=0.3)
        self.add(self.axes)
        
        # 添加轴标签
        self.axes.add_axis_labels(x_tex="x", y_tex="y", z_tex="z")
        
        # 添加网格平面
        self.grid = NumberPlane(
            x_range=(-6, 6, 1),
            y_range=(-4, 4, 1),
            height=8,
            width=12,
        )
        self.grid.set_stroke(GREY, opacity=0.1)
        self.grid.rotate(90 * DEGREES, RIGHT)
        self.grid.move_to(ORIGIN)
        self.add(self.grid)
    
    def setup_fields(self):
        """设置电磁场可视化"""
        cfg = PhysicsConfig()
        
        # 磁场指示 (沿y轴)
        B_magnitude = np.linalg.norm(cfg.B_FIELD)
        B_color = BLUE_D
        
        # 在几个位置放置磁场箭头
        B_arrows = VGroup()
        for x in [-3, 0, 3]:
            for z in [-2, 0, 2]:
                arrow = Arrow(
                    start=np.array([x, -2, z]),
                    end=np.array([x, 2, z]),
                    color=B_color,
                    thickness=0.02,
                )
                B_arrows.add(arrow)
        
        B_label = TexText(r"$\vec{B}$ (Magnetic)", font_size=24, color=B_color)
        B_label.move_to(np.array([4, 2, 2]))
        
        self.B_field_group = VGroup(B_arrows, B_label)
        self.B_field_group.set_opacity(0.4)
        
        # 电场指示 (沿z轴)
        E_color = RED_D
        E_arrows = VGroup()
        for x in [-3, 0, 3]:
            for y in [-2, 0, 2]:
                arrow = Arrow(
                    start=np.array([x, y, -2]),
                    end=np.array([x, y, 2]),
                    color=E_color,
                    thickness=0.02,
                )
                E_arrows.add(arrow)
        
        E_label = TexText(r"$\vec{E}$ (Electric)", font_size=24, color=E_color)
        E_label.move_to(np.array([4, -2, 2]))
        
        self.E_field_group = VGroup(E_arrows, E_label)
        self.E_field_group.set_opacity(0.4)
        
        # 添加到场景但不显示
        self.add(self.B_field_group, self.E_field_group)
    
    def animate_intro(self):
        """开场动画 - 显示场"""
        # 淡入场矢量
        self.play(
            self.B_field_group.animate.set_opacity(0.6),
            self.E_field_group.animate.set_opacity(0.6),
            run_time=2,
        )
        
        # 显示漂移速度公式
        drift_formula = TexText(r"$\vec{v}_d = \frac{\vec{E} \times \vec{B}}{B^2}$", font_size=36)
        drift_formula.to_corner(UR)
        drift_formula.fix_in_frame()
        drift_formula.set_color(YELLOW)
        
        self.play(Write(drift_formula), run_time=1.5)
        self.wait(1)
        
        self.drift_formula = drift_formula
    
    def animate_single_particle(self):
        """单个粒子动画 - 展示基础螺旋运动"""
        cfg = PhysicsConfig()
        
        # 计算轨迹
        points, times = get_analytical_trajectory(
            q=cfg.Q_POSITIVE,
            m=cfg.MASS,
            v0=cfg.V0_BASE,
            r0=np.array([-4, 0, 0]),
            E=cfg.E_FIELD,
            B=cfg.B_FIELD,
            t_max=cfg.T_MAX,
            dt=cfg.DT
        )
        
        # 创建粒子
        particle = ChargedParticle(
            charge=cfg.Q_POSITIVE,
            mass=cfg.MASS,
            color=YELLOW,
            radius=cfg.PARTICLE_RADIUS
        )
        particle.move_to(points[0])
        
        # 创建轨迹曲线
        trajectory_curve = VMobject()
        trajectory_curve.set_points_as_corners(points)
        trajectory_curve.set_stroke(YELLOW, width=2, opacity=0.6)
        
        # 创建尾迹
        trail = TracedPath(
            particle.get_center,
            stroke_color=YELLOW,
            stroke_width=2,
            time_traced=cfg.TRAIL_LENGTH,
        )
        
        # 添加粒子标签
        label = TexText(r"$q > 0$", font_size=24, color=YELLOW)
        label.next_to(particle, UP, buff=0.3)
        label.add_updater(lambda m: m.next_to(particle, UP, buff=0.3))
        
        self.add(trail, particle, label)
        
        # 动画沿路径移动
        self.play(
            MoveAlongPath(particle, trajectory_curve, rate_func=linear),
            run_time=8,
            rate_func=linear,
        )
        
        # 保留轨迹但不保留粒子
        self.remove(label)
        final_path = trail.copy()
        final_path.clear_updaters()
        self.add(final_path)
        self.remove(particle, trail)
        
        self.first_particle_path = final_path
    
    def animate_multiple_particles(self):
        """多粒子动画 - 展示不同电荷和初始条件"""
        cfg = PhysicsConfig()
        
        # 定义多组粒子参数
        particle_configs = [
            # (电荷, 质量, 颜色, 初始位置, 初始速度)
            (1.0, 1.0, RED, [-4, 0.5, 0], [0.8, 0, 0.3]),
            (-1.0, 1.0, BLUE, [-4, -0.5, 0], [1.2, 0, 0.5]),
            (1.0, 2.0, GREEN, [-4, 0, 0.5], [1.0, 0, -0.2]),
            (-0.5, 1.0, PURPLE, [-4, 0, -0.5], [0.9, 0, 0.4]),
        ]
        
        particles = []
        trails = []
        paths = []
        
        for q, m, color, r0, v0 in particle_configs:
            # 计算轨迹
            points, _ = get_analytical_trajectory(
                q=q, m=m, v0=np.array(v0), r0=np.array(r0),
                E=cfg.E_FIELD, B=cfg.B_FIELD,
                t_max=cfg.T_MAX, dt=cfg.DT
            )
            
            # 创建粒子
            particle = ChargedParticle(
                charge=q, mass=m, color=color,
                radius=cfg.PARTICLE_RADIUS * (1 + 0.2 * abs(q))
            )
            particle.move_to(points[0])
            
            # 创建尾迹
            trail = TracedPath(
                particle.get_center,
                stroke_color=color,
                stroke_width=2,
                time_traced=cfg.TRAIL_LENGTH,
            )
            
            # 创建路径曲线
            path = VMobject()
            path.set_points_as_corners(points)
            path.set_stroke(color, width=2, opacity=0.4)
            
            particles.append(particle)
            trails.append(trail)
            paths.append(path)
        
        # 同时播放所有粒子
        particle_group = Group(*particles)
        trail_group = VGroup(*trails)
        
        self.add(trail_group, particle_group)
        
        # 创建移动动画
        animations = [
            MoveAlongPath(p, path, rate_func=linear)
            for p, path in zip(particles, paths)
        ]
        
        self.play(
            LaggedStart(*animations, lag_ratio=0.1),
            run_time=10,
        )
        
        # 保存最终轨迹
        self.multi_particle_paths = Group(*[
            t.copy().clear_updaters() for t in trails
        ])
        self.add(self.multi_particle_paths)
        self.remove(particle_group, trail_group)
    
    def animate_camera_rotation(self):
        """摄像机旋转 - 展示3D结构"""
        # 保存当前帧状态
        self.frame.save_state()
        
        # 旋转摄像机展示3D结构
        self.play(
            self.frame.animate.rotate(30 * DEGREES, UP),
            run_time=3,
        )
        
        self.play(
            self.frame.animate.rotate(-60 * DEGREES, UP),
            run_time=4,
        )
        
        self.play(
            self.frame.animate.rotate(30 * DEGREES, UP),
            run_time=3,
        )
        
        # 缓慢旋转展示
        self.play(
            self.frame.animate.increment_theta(PI),
            run_time=8,
            rate_func=linear,
        )
    
    def animate_outro(self):
        """结束动画"""
        # 淡出所有元素
        all_mobjects = VGroup(
            self.axes,
            self.grid,
            self.B_field_group,
            self.E_field_group,
            self.first_particle_path,
            self.multi_particle_paths,
        )
        
        if hasattr(self, 'drift_formula'):
            all_mobjects.add(self.drift_formula)
        
        self.play(
            FadeOut(all_mobjects),
            run_time=2,
        )
        
        # 结束语
        outro = Text(
            "Charged particles dance to the rhythm of fields",
            font_size=32,
            gradient=(BLUE, PURPLE, RED)
        )
        outro.fix_in_frame()
        
        self.play(Write(outro), run_time=2)
        self.wait(2)
        self.play(FadeOut(outro), run_time=1)


# =============================================================================
# 简化版本（用于快速测试）
# =============================================================================

class SimpleLorentz(ThreeDScene):
    """简化版洛伦兹力动画，适合快速测试"""
    
    def construct(self):
        # 设置背景
        from manimlib.utils.color import color_to_rgba
        self.camera.background_rgba = list(color_to_rgba("#0a0a15", 1.0))
        
        self.frame.set_euler_angles(theta=-45 * DEGREES, phi=60 * DEGREES)
        
        # 坐标系
        axes = ThreeDAxes(
            x_range=(-5, 5, 1),
            y_range=(-3, 3, 1),
            z_range=(-3, 3, 1),
        )
        axes.set_stroke(GREY, opacity=0.3)
        self.add(axes)
        
        # 参数
        E = np.array([0, 0, 2])
        B = np.array([0, 2, 0])
        q, m = 1.0, 1.0
        v0 = np.array([1, 0, 0.5])
        r0 = np.array([-3, 0, 0])
        
        # 计算轨迹
        points, _ = get_analytical_trajectory(q, m, v0, r0, E, B, t_max=8, dt=0.05)
        
        # 创建粒子
        particle = Sphere(radius=0.1, color=YELLOW)
        particle.set_gloss(0.8)
        
        # 轨迹曲线
        curve = VMobject()
        curve.set_points_as_corners(points)
        curve.set_stroke(YELLOW, width=2, opacity=0.6)
        
        # 尾迹
        trail = TracedPath(
            particle.get_center,
            stroke_color=YELLOW,
            stroke_width=2,
            time_traced=1.5,
        )
        
        particle.move_to(points[0])
        self.add(trail, particle)
        
        # 动画
        self.play(
            MoveAlongPath(particle, curve, rate_func=linear),
            run_time=6,
        )
        
        self.wait(1)


# =============================================================================
# 高级版本 - 带相空间图
# =============================================================================

class LorentzWithPhaseSpace(ThreeDScene):
    """
    带相空间子图的洛伦兹力动画
    主视图显示3D轨迹，角落显示相空间图
    """
    
    def construct(self):
        # 设置背景
        from manimlib.utils.color import color_to_rgba
        self.camera.background_rgba = list(color_to_rgba("#0a0a15", 1.0))
        
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)
        
        # 主3D场景
        self.setup_main_scene()
        
        # 相空间图 (固定在屏幕角落)
        self.setup_phase_space_plot()
        
        # 运行动画
        self.animate_simulation()
    
    def setup_main_scene(self):
        """设置主3D场景"""
        axes = ThreeDAxes(
            x_range=(-6, 6, 1),
            y_range=(-4, 4, 1),
            z_range=(-4, 4, 1),
        )
        axes.set_stroke(GREY, opacity=0.3)
        self.add(axes)
        self.main_axes = axes
        
        # 磁场指示
        B_arrows = VGroup(*[
            Arrow(
                start=np.array([x, -2, z]),
                end=np.array([x, 2, z]),
                color=BLUE_D,
                thickness=0.02,
            )
            for x in [-2, 0, 2] for z in [-1, 0, 1]
        ])
        B_arrows.set_opacity(0.3)
        self.add(B_arrows)
    
    def setup_phase_space_plot(self):
        """设置相空间图 (x vs vx)"""
        phase_axes = Axes(
            x_range=(-6, 6, 2),
            y_range=(-3, 3, 1),
            width=4,
            height=2.5,
        )
        phase_axes.to_corner(DR)
        phase_axes.set_stroke(GREY, opacity=0.5)
        phase_axes.fix_in_frame()
        
        # 标签
        x_label = TexText("$x$", font_size=20)
        x_label.next_to(phase_axes.x_axis, RIGHT, buff=0.1)
        x_label.fix_in_frame()
        
        vx_label = TexText("$v_x$", font_size=20)
        vx_label.next_to(phase_axes.y_axis, UP, buff=0.1)
        vx_label.fix_in_frame()
        
        self.phase_axes = phase_axes
        self.phase_labels = VGroup(x_label, vx_label)
        
        self.add(phase_axes, self.phase_labels)
        
        # 相空间轨迹
        self.phase_trajectory = VMobject()
        self.phase_trajectory.set_stroke(RED, width=2)
        self.phase_trajectory.fix_in_frame()
        self.add(self.phase_trajectory)
    
    def animate_simulation(self):
        """运行动画"""
        cfg = PhysicsConfig()
        
        # 计算轨迹
        points, velocities, times = compute_trajectory(
            q=cfg.Q_POSITIVE,
            m=cfg.MASS,
            v0=cfg.V0_BASE,
            r0=np.array([-4, 0, 0]),
            E=cfg.E_FIELD,
            B=cfg.B_FIELD,
            t_max=cfg.T_MAX,
            dt=cfg.DT
        )
        
        # 3D粒子
        particle3d = Sphere(radius=0.1, color=YELLOW)
        particle3d.set_gloss(0.8)
        particle3d.move_to(points[0])
        
        # 3D轨迹
        curve3d = VMobject()
        curve3d.set_points_as_corners(points)
        curve3d.set_stroke(YELLOW, width=2, opacity=0.5)
        
        # 3D尾迹
        trail3d = TracedPath(
            particle3d.get_center,
            stroke_color=YELLOW,
            stroke_width=2,
            time_traced=2,
        )
        
        # 相空间粒子
        phase_dot = Dot(color=RED, radius=0.08)
        phase_dot.fix_in_frame()
        phase_dot.move_to(self.phase_axes.c2p(points[0][0], velocities[0][0]))
        
        self.add(trail3d, particle3d, phase_dot)
        
        # 动画更新器
        current_index = [0]
        
        def update_phase_trajectory(mob):
            idx = min(current_index[0], len(points) - 1)
            phase_points = [
                self.phase_axes.c2p(p[0], v[0])
                for p, v in zip(points[:idx+1], velocities[:idx+1])
            ]
            if len(phase_points) > 1:
                mob.set_points_as_corners(phase_points)
        
        self.phase_trajectory.add_updater(update_phase_trajectory)
        
        # 播放动画
        n_frames = len(times)
        
        for i in range(n_frames):
            current_index[0] = i
            particle3d.move_to(points[i])
            phase_dot.move_to(self.phase_axes.c2p(points[i][0], velocities[i][0]))
            self.wait(cfg.DT)
        
        self.wait(1)


# 导出类列表
__all__ = [
    'LorentzDance',           # 完整版主场景
    'SimpleLorentz',          # 简化版
    'LorentzWithPhaseSpace',  # 带相空间图版
    'ChargedParticle',        # 粒子类
]
