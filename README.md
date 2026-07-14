# Manim-Project

一个存放 manim 动画脚本的仓库，包含三个主题：

1. **AFM（原子力显微镜）** — 5 个场景解释 AFM 工作原理，总时长约 40 秒
2. **TEM（透射电子显微镜 / 电磁波）** — 三维演示电磁波传播
3. **测试脚本** — Manim 基础功能验证

## 仓库文件

```
Project_1/
├── .gitignore                    # Git 忽略规则
├── .venv/                        # Python 虚拟环境（uv 管理）
│   └── Scripts/                  # 激活脚本：Activate.ps1 / activate
├── afm_manim/                    # AFM 微视频渲染脚本
│   ├── README.md                 # AFM 项目说明文档
│   ├── render_all.py             # 批量渲染所有 5 个镜头（支持 k/e/m/l 质量参数）
│   ├── afm_scenes.py             # 主要场景：波函数复数本质与概率诠释等 5 个 Scene
│   ├── afm_adjust.py             # AFM 位置调整动画（左半屏 16:9）
│   ├── afm_system.py             # AFM 幅度调制系统反馈控制示意图
│   ├── afm_scenes_ai.py          # AI 辅助版本：完整 5 镜头脚本（40s, 1920×1080, 30fps）
│   └── afm-adjust-ai.py          # AI 辅助版本：AFM 位置调整动画
├── TEM/                          # 透射电子显微镜 / 电磁波模拟
│   ├── Electromagnetic_CE.py     # Manim Community Edition 版电磁波脚本
│   └── Electromagnetic.py        # 原版电磁波脚本
├── custom_config.yml             # Manim 自定义配置（输出目录、默认参数等）
├── manim.cfg                     # Manim 全局配置文件
├── requirements.txt              # Python 依赖包列表
├── test.py                       # 测试脚本：3D 场景 + MarkupText 渲染验证
├── how-to-set-env.md             # Windows 本地环境搭建指南
├── how-to-set-env-VPS.md        # VPS / Linux 服务器环境搭建指南
└── how-to-load-docker.txt        # Docker 容器快速启动命令
```

## AFM 微视频（afm_manim/）

| 文件 | 说明 |
|------|------|
| `render_all.py` | 批量渲染入口，支持 `k`(4K) / `e`(1080p) / `m`(720p) / `l`(480p) 参数 |
| `afm_scenes.py` | 5 个核心场景：波函数复数本质、概率诠释等，总时长约 40s |
| `afm_adjust.py` | AFM 探针位置调整动画（左半屏 16:9） |
| `afm_system.py` | AFM 幅度调制系统反馈控制信号流向示意图 |
| `afm_scenes_ai.py` | AI 辅助重写版：完整 5 镜头脚本，分辨率 1920×1080，30fps |
| `afm-adjust-ai.py` | AI 辅助重写版：AFM 位置调整动画 |

## TEM / 电磁波（TEM/）

| 文件 | 说明 |
|------|------|
| `Electromagnetic_CE.py` | Manim Community Edition 版电磁波三维演示 |
| `Electromagnetic.py` | 原版电磁波脚本 |

## 环境配置

- **Windows 本地**：见 [`how-to-set-env.md`](./how-to-set-env.md)
- **VPS / Linux**：见 [`how-to-set-env-VPS.md`](./how-to-set-env-VPS.md)
- **Docker**：`docker run -d --name Physics -v "D:/30856/Manim/Project:/manim" manimcommunity/manim:stable tail -f /dev/null`

## 快速开始

```bash
# 1. 激活虚拟环境
cd D:\30856\Manim\Project_1
.venv\Scripts\Activate.ps1   # PowerShell
# source .venv/Scripts/activate   # Git Bash

# 2. 渲染 AFM 全部场景
manim afm_manim/render_all.py k

# 3. 运行测试脚本
manim test.py SimpleScene
```

