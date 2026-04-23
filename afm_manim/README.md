# 原子力显微镜微视频 - Manim 渲染脚本

## 项目概述

本项目包含原子力显微镜（AFM）微视频的五个Manim场景脚本，总时长40秒，用于解释AFM的量子力学原理。

## 文件结构

```
afm_manim/
├── afm_scenes.py      # 主要场景脚本（包含5个Scene类）
├── render_all.py      # 批量渲染脚本
└── README.md          # 本文件
```

## 五个镜头说明

| 镜头 | 类名 | 内容 | 时长 |
|------|------|------|------|
| 1 | `Scene1_WaveFunctionComplex` | 波函数的复数本质与概率诠释 | 7秒 |
| 2 | `Scene2_SlaterDeterminant` | 全同粒子与反对称化 | 13秒 |
| 3 | `Scene3_ExponentialPauliRepulsion` | 从量子原理到指数排斥势 | 8秒 |
| 4 | `Scene4_FrequencyShiftDetection` | 频移检测原理 | 7秒 |
| 5 | `Scene5_AFMForceCurve` | 力曲线与工作模式 | 5秒 |

**总计: 40秒**

## 技术规格

- **渲染引擎**: Manim Community Edition (v0.18.0+)
- **分辨率**: 1920×1080 (16:9)
- **帧率**: 30 fps
- **背景色**: 黑色（便于与Blender合成）
- **输出格式**: MP4 (H.264)

## 渲染方法

### 方法一：单独渲染每个镜头

```bash
# 镜头1
manim -qh -o 镜头1_波函数 afm_scenes.py Scene1_WaveFunctionComplex

# 镜头2
manim -qh -o 镜头2_全同粒子 afm_scenes.py Scene2_SlaterDeterminant

# 镜头3
manim -qh -o 镜头3_指数势 afm_scenes.py Scene3_ExponentialPauliRepulsion

# 镜头4
manim -qh -o 镜头4_频移检测 afm_scenes.py Scene4_FrequencyShiftDetection

# 镜头5
manim -qh -o 镜头5_力曲线 afm_scenes.py Scene5_AFMForceCurve
```

### 方法二：批量渲染（推荐）

```bash
# 高质量渲染（1080p）
python render_all.py h

# 中等质量渲染（720p，用于预览）
python render_all.py m

# 低质量渲染（480p，用于快速测试）
python render_all.py l
```

## 渲染质量选项

| 选项 | 分辨率 | 用途 |
|------|--------|------|
| `-ql` | 854×480 | 快速预览 |
| `-qm` | 1280×720 | 标准预览 |
| `-qh` | 1920×1080 | 最终输出 |
| `-qk` | 3840×2160 | 4K输出 |

## 输出位置

渲染完成后，视频文件将位于：

```
media/videos/afm_scenes/1080p60/
├── 镜头1_波函数.mp4
├── 镜头2_全同粒子.mp4
├── 镜头3_指数势.mp4
├── 镜头4_频移检测.mp4
└── 镜头5_力曲线.mp4
```

## 与Blender合成

1. 所有Manim场景使用**黑色背景**
2. 输出视频可直接与Blender渲染的原子级动画叠加
3. 建议在视频编辑软件中使用**屏幕**或**加法**混合模式
4. 转场点设计：
   - 0:30 - Blender探针模型淡出，Manim镜头1淡入
   - 1:10 - Manim镜头5淡出，Blender表面重建淡入

## 颜色编码规范

| 元素 | 颜色 | 十六进制 |
|------|------|----------|
| 概率密度曲线 | 黄/橙 | `#FFC107` |
| 高斯云团 | 半透明蓝 | `#1E88E5` |
| 节点线 | 白 | `#FFFFFF` |
| 泡利排斥力/势 | 红 | `#E53935` |
| 范德华力 | 蓝 | `#1E88E5` |
| 激光 | 红 | `#FF0000` |
| 探测器/信号 | 绿 | `#43A047` |
| 平衡点/高亮 | 黄 | `#FFEB3B` |

## 依赖项

```bash
pip install manim numpy
```

## 物理参数说明

### 镜头1 - 波函数
- 波包中心: x₀ = 0
- 波包宽度: σ = 0.5
- 波数: k = 4

### 镜头2 - 全同粒子
- 高斯云团初始位置: ±1.5
- 重叠时显示节点线

### 镜头3 - 指数势
- 衰减长度: λ = 0.3 nm
- 势函数: V(z) = A·e^(-2z/λ)

### 镜头4 - 频移检测
- 探针振动频率: 10 rad/s
- 振动幅度: 0.15 单位

### 镜头5 - 力曲线
- 范德华力: F ∝ -1/z⁷
- 泡利排斥力: F ∝ e^(-2z/0.3)
- 平衡点: z ≈ 0.85 nm
- 探针振动幅度: 0.05 nm

## 注意事项

1. **避免除零**: 范德华力计算中 z > 0.5 保护
2. **变量命名**: 使用 `decay_len` 而非 `lambda`
3. **LaTeX环境**: Slater行列式使用 `vmatrix` 环境
4. **动态更新**: 使用 `ValueTracker` + `always_redraw` 实现动画

## 故障排除

### LaTeX编译错误
确保安装了完整的LaTeX发行版：
```bash
# Ubuntu/Debian
sudo apt-get install texlive-full

# macOS
brew install --cask mactex
```

### 内存不足
降低渲染质量或使用预览模式：
```bash
manim -ql -p afm_scenes.py Scene1_WaveFunctionComplex
```

### 中文显示问题
确保系统安装了 `Noto Sans CJK SC` 字体。

## 作者

Manim脚本基于详细分镜脚本开发，用于原子力显微镜科普微视频制作。
