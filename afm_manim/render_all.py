"""
原子力显微镜微视频 - 批量渲染脚本
用于连续渲染所有五个镜头
"""

"""
# 使用默认最高质量 (4K)
python afm_manim\render_all.py

# 显式指定质量
python afm_manim\render_all.py k   # 4K 最高质量
python afm_manim\render_all.py e   # 1080p 高质量
python afm_manim\render_all.py m   # 720p 中质量
python afm_manim\render_all.py l   # 480p 低质量（快速预览）
"""

import subprocess
import sys
import os

# 场景配置
SCENES = [
    ("Scene1_WaveFunctionComplex", "镜头1_波函数复数本质"),
    ("Scene2_SlaterDeterminant", "镜头2_全同粒子反对称化"),
    ("Scene3_ExponentialPauliRepulsion", "镜头3_指数排斥势"),
    ("Scene4_FrequencyShiftDetection", "镜头4_频移检测原理"),
    ("Scene5_AFMForceCurve", "镜头5_力曲线工作模式"),
]

def render_scene(class_name, output_name, quality="k"):
    """
    渲染单个场景
    
    参数:
        class_name: 场景类名
        output_name: 输出文件名前缀
        quality: 渲染质量 (l=低, m=中, h=高, k=4K)
    """
    cmd = [
        "manim",
        "-q", quality,
        "-o", output_name,
        "afm_scenes.py",
        class_name
    ]
    
    print(f"\n{'='*60}")
    print(f"正在渲染: {output_name}")
    print(f"命令: {' '.join(cmd)}")
    print(f"{'='*60}\n")
    
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0

def render_all(quality="k"):
    """批量渲染所有场景"""
    print("="*60)
    print("原子力显微镜微视频 - 批量渲染")
    print(f"渲染质量: {quality}")
    print(f"输出目录: ./media/videos/")
    print("="*60)
    
    success_count = 0
    for class_name, output_name in SCENES:
        if render_scene(class_name, output_name, quality):
            success_count += 1
            print(f"✓ {output_name} 渲染成功")
        else:
            print(f"✗ {output_name} 渲染失败")
    
    print(f"\n{'='*60}")
    print(f"渲染完成: {success_count}/{len(SCENES)} 个场景成功")
    print("="*60)

if __name__ == "__main__":
    # 获取命令行参数，默认使用 k (4K) 最高质量
    quality = sys.argv[1] if len(sys.argv) > 1 else "k"
    render_all(quality)
