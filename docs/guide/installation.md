# 安装教程

## 依赖说明

`requirements.txt` 内容如下：

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| PySide6 | >=6.9.1 | GUI 框架 |
| sympy | >=1.14.0 | 符号计算核心 |
| matplotlib | >=3.10.9 | 几何绘图 |
| PyQtDarkTheme-fork | >=2.3.6 | 浅色 / 深色主题 |
| latex2sympy2 | >=1.9.1 | LaTeX 解析 |
| lazy_loader | >=0.4 | 模块延迟加载 |

## 安装步骤

```bash
# 建议使用虚拟环境
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

## 打包为 Windows 可执行文件

项目使用 cx_Freeze 打包。先安装打包依赖：

```bash
pip install cx_Freeze
```

在仓库根目录执行：

```bash
python setup.py build
```

打包完成后，可执行文件位于 `build/exe.win-amd64-3.x/`（名称取决于系统与 Python 版本）。
打包会把 `i18n/` 翻译文件一并复制到可执行文件同级目录。

!!! note
    打包体积较大（约 100+ MB），因为包含了完整的 Python 环境与依赖库。
