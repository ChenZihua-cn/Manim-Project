# ManimGL 环境配置与使用手册

> 本项目使用 **3b1b 原版 ManimGL v1.7.2**（即 `manimgl`），不是 Manim Community 版本。
> 源码位于 `D:\30856\Manim\manim\`，虚拟环境位于 `D:\30856\Manim\.venv\`。

---

## 一、快速启动（环境正常时）

每次使用前，先激活虚拟环境：

```bash
# Git Bash / 终端
cd D:/30856/Manim
source .venv/Scripts/activate

# PowerShell
cd D:\30856\Manim
.venv\Scripts\Activate.ps1

# CMD
cd D:\30856\Manim
.venv\Scripts\activate.bat
```

验证环境是否正常：

```bash
manimgl --version
# 应输出：ManimGL v1.7.2
```

---

## 二、依赖说明

manimgl 的依赖分为两类：

### Python 包（`pip install -e .` 自动处理，无需手动安装）

| 包 | 用途 |
|----|------|
| moderngl / PyOpenGL | OpenGL Python 绑定，渲染核心 |
| manimpango | 文本排版（基于 Pango/Cairo） |
| numpy / scipy / sympy | 数学计算 |
| Pillow / skia-pathops | 图像处理 |
| pyglet / moderngl_window | 窗口管理 |
| 其他 | 详见 `manim/requirements.txt` |

### 系统级工具（需手动安装，重装系统后必须重新安装）

> **OpenGL 驱动不需要单独安装**，它由显卡驱动提供。你的 NVIDIA RTX 4060 驱动已提供 OpenGL 3.3，完全满足需求。只要保持显卡驱动正常就行。

| 工具 | 用途 | 当前版本 | 下载地址 |
|------|------|----------|----------|
| **ffmpeg** | 导出 MP4/GIF 视频必须 | 2025-12-04 | https://www.gyan.dev/ffmpeg/builds/ （下载 full build） |
| **MiKTeX** | 渲染 `Tex` / `MathTex` 数学公式必须 | 26.2 | https://miktex.org/download |

安装后需确认两个工具都在系统 PATH 中（用 `ffmpeg -version` 和 `pdflatex --version` 验证）。

---

## 三、使用 uv 进行安装（推荐 - 无需预装 Python）

> **优势**：如果电脑上没有 Python，但已安装 uv，uv 会自动下载并管理 Python 版本，省去手动安装 Python 的麻烦。

### 前提条件

- 已安装 **uv**（下载地址：https://docs.astral.sh/uv/getting-started/installation/）
- 已安装 **ffmpeg**（路径已在系统 PATH 中，位于 `C:\ffmpeg-*\bin`）
- 已安装 **MiKTeX**（路径：`C:\Users\30856\AppData\Local\Programs\MiKTeX`）
- 显卡驱动正常（OpenGL 由驱动提供，不需要额外操作）
- `manim\` 源码目录完整（从 https://github.com/3b1b/manim 下载）

### 安装步骤

#### 步骤 1：确认依赖可用

```bash
# 检查 uv 是否可用
uv --version

# 检查 ffmpeg 和 MiKTeX
ffmpeg -version
pdflatex --version
```

#### 步骤 2：使用 uv 创建虚拟环境

```bash
cd D:/30856/Manim
# uv 会自动下载 Python 3.10 并创建虚拟环境
uv venv .venv --python 3.10
```

#### 步骤 3：激活虚拟环境

```bash
# Git Bash / 终端
source .venv/Scripts/activate

# PowerShell
.venv\Scripts\Activate.ps1

# CMD
.venv\Scripts\activate.bat
```

#### 步骤 4：使用 uv 安装依赖

```bash
cd manim
# uv sync 会自动读取 pyproject.toml 或 requirements.txt 安装所有依赖
uv sync
cd ..
```

或者用传统方法：

```bash
cd manim
uv pip install -e .
cd ..
```

#### 步骤 5：验证安装

```bash
python -c "import manimlib; print('OK')"
manimgl --version
```

---

## 四、从零重建环境（环境完全失效时）

### 前提条件

- 已安装 **Python 3.10**（路径：`C:\Program Files\Python310\python.exe`）
- 已安装 **ffmpeg**（路径已在系统 PATH 中，位于 `C:\ffmpeg-*\bin`）
- 已安装 **MiKTeX**（路径：`C:\Users\30856\AppData\Local\Programs\MiKTeX`）
- 显卡驱动正常（OpenGL 由驱动提供，不需要额外操作）
- `manim\` 源码目录完整（从 https://github.com/3b1b/manim 下载）

### 步骤 1：确认系统依赖可用

```bash
ffmpeg -version       # 应输出 ffmpeg 版本信息
pdflatex --version    # 应输出 MiKTeX-pdfTeX 版本信息
```

若任一命令失败，先安装对应工具（见上方依赖说明）再继续。

### 步骤 2：删除旧虚拟环境

```bash
cd D:/30856/Manim
rm -rf .venv
```

### 步骤 3：用 Python 3.10 创建新虚拟环境

```bash
"C:/Program Files/Python310/python.exe" -m venv .venv
```

### 步骤 4：激活虚拟环境

```bash
source .venv/Scripts/activate
```

### 步骤 5：安装 manimgl（从本地源码，开发模式）

```bash
cd manim
pip install -e .
cd ..
```

> `-e` 表示 editable 模式，对源码的修改会直接生效，无需重新安装。

### 步骤 6：验证安装

```bash
python -c "import manimlib; print('OK')"
manimgl --version
```

两条命令均正常输出即表示环境配置成功。

### 步骤 7：测试运行示例场景

```bash
manimgl manim/example_scenes.py OpeningManimExample
```

---

## 五、常用命令行操作

### 基本语法

```
manimgl <文件路径> <场景类名> [选项]
```

### 预览模式（最常用，实时窗口）

```bash
# 打开交互窗口预览场景
manimgl my_scene.py MyScene
```

窗口快捷键：
- `Space` —— 暂停 / 继续
- `→` / `←` —— 下一个 / 上一个动画（Presenter 模式下）
- `q` —— 退出

### 导出视频

```bash
# 导出为视频文件（保存到 videos/ 目录）
manimgl my_scene.py MyScene -w

# 导出并自动打开
manimgl my_scene.py MyScene -w -o

# 导出为 GIF
manimgl my_scene.py MyScene -w -i
```

### 分辨率控制

```bash
manimgl my_scene.py MyScene -w -l        # 480p（低画质，速度快）
manimgl my_scene.py MyScene -w -m        # 720p（中等画质）
manimgl my_scene.py MyScene -w --hd      # 1080p
manimgl my_scene.py MyScene -w --uhd     # 4K

# 自定义分辨率
manimgl my_scene.py MyScene -w -r 1280x720
```

### 只保存最后一帧（截图）

```bash
manimgl my_scene.py MyScene -s
```

### 从指定动画编号开始渲染

```bash
# 从第 3 个动画开始
manimgl my_scene.py MyScene -n 3

# 只渲染第 3 到第 6 个动画
manimgl my_scene.py MyScene -n 3,6
```

### 设置背景颜色

```bash
manimgl my_scene.py MyScene -c BLACK
manimgl my_scene.py MyScene -c "#1a1a2e"
```

### 自定义帧率

```bash
manimgl my_scene.py MyScene -w --fps 60
```

### 演示模式（PPT 风格，按空格翻页）

```bash
manimgl my_scene.py MyScene -p
```

### 交互式调试（在指定行插入 iPython 断点）

```bash
manimgl my_scene.py MyScene -e 42    # 在第 42 行暂停进入 iPython
```

### 渲染文件内所有场景

```bash
manimgl my_scene.py -a -w
```

### 清除 Tex/Text 缓存

```bash
manimgl --clear-cache
```

---

## 四、目录结构说明

```
D:\30856\Manim\
├── .venv\              # 虚拟环境（不要手动修改）
├── manim\              # manimgl 源码（从 GitHub 克隆）
│   ├── manimlib\       # 核心库代码
│   ├── example_scenes.py
│   └── requirements.txt
├── Experimental\       # 自己的实验性场景文件
└── 环境配置与使用手册.md  # 本文件
```

---

## 五、常见问题

### `ModuleNotFoundError: No module named 'manimlib'`

原因：manimgl 没有安装到当前虚拟环境，或虚拟环境没有激活。

```bash
source .venv/Scripts/activate
cd manim && pip install -e . && cd ..
```

### `manimgl: command not found`

原因：虚拟环境未激活。执行 `source .venv/Scripts/activate` 后重试。

### LaTeX 渲染失败（`Tex` / `MathTex` 报错）

检查 MiKTeX 是否在 PATH 中：

```bash
pdflatex --version
```

若命令不存在，在系统环境变量 PATH 中添加：
`C:\Users\30856\AppData\Local\Programs\MiKTeX\miktex\bin\x64`

### ffmpeg 相关报错

检查 ffmpeg 是否可用：

```bash
ffmpeg -version
```

若不可用，确认 PATH 中包含 ffmpeg 的 `bin` 目录。
