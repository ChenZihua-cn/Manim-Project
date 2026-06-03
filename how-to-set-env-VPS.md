# The ManimCE + ffmpeg + Texlive 

## update

```bash
sudo apt update
sudo apt upgrade -y
# 安装基础依赖工具
sudo apt install -y python3 python3-pip python3-venv build-essential libcairo2-dev libpango1.0-dev
```
## install

```bash
sudo apt install -y ffmpeg

# 安装基础版 TeX Live 和常用扩展
sudo apt install -y texlive texlive-latex-extra
```

## venv 

```bash
# 创建虚拟环境
python3 -m venv .venv
# 激活虚拟环境
source .venv/bin/activate
```
## Manim

```bash
pip install manim
```


