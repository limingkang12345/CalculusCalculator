# CalculusCalculator 微积分计算器

**CalculusCalculator** 是一个基于 SymPy 和 PySide6 的图形化微积分计算工具，支持求导、积分、函数性质分析、表达式变形、方程（组）与不等式（组）求解、微分方程求解、符号计算、向量运算、解三角形、函数绘图、**平面/立体几何定义、计算与绘图**、**解几计算器（表达式画布）**、**积木化可视化编程**等功能，并提供了**表达式缓存**、**可视化公式输入**、**启动画面**、**初始化引导教学**、存档/读档（`.cca`）及 Web 版本。

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-6.11.1-green)](https://pypi.org/project/PySide6/)
[![SymPy](https://img.shields.io/badge/SymPy-1.14.0-orange)](https://www.sympy.org/)

---

## 基本信息

- **项目地址**：[GitHub - limingkang12345/CalculusCalculator](https://github.com/limingkang12345/CalculusCalculator)
- **项目文档**: [CalculusCalculator帮助文档](https://limingkang12345.github.io/CalculusCalculator/)
- **网页版**：[https://limingkang.pythonanywhere.com](https://limingkang.pythonanywhere.com)
- **最新版本**：v2.2.0
- **开发语言**：Python 3.10+
- **核心库**：SymPy（符号计算）、PySide6（GUI 框架）、Matplotlib（几何绘图）、Blockly（可视化编程）
- **功能概览**：
  - **微积分**：显 / 隐函数求导、不定 / 定积分、函数性质（值域、单调、奇偶、周期、最值）、13 种表达式变形
  - **方程与不等式**：方程、方程组、不等式、不等式组、常微分方程
  - **解几计算器**（v2.2.0）：表达式画布，节点级选中 / 拖拽 / 变形，常用方程按条件反推，几何表达式一键生成
  - **几何**：平面 19 种构造 + 32 种计算，立体 12 种构造 + 22 种计算，2D / 3D 绘图与斜二测画法
  - **其他计算**：向量运算、解三角形、函数绘图，以及 Python / Mpmath / SymPy / LaTeX 四种引擎
  - **交互**：功能集成页三区布局、积木化编程、MathLive 可视化输入、表达式缓存、回车快捷键
  - **工程化**：`.cca` 存档 / 读档与存档设置、启动画面、初始化引导、中英文界面与明暗主题、Web 版

---

## v2.2.0 更新内容

新增**解几计算器**（`expr_calculator/`）：以表达式画布的形式完成解析几何计算
  - **分层着色画布**：SymPy 表达式转自定义表达式树，按树深度着色（红 → 绿 → 蓝 → 紫），保留输入顺序与括号
  - **节点级交互**：点击选中节点、`+ / −` 交换相邻项、点击括号展开；选中节点可拖拽为浮动节点，与另一张卡片重叠时弹出运算对话框（替换 / 加 / 减 / 乘 / 除 / 乘方，分式节点另支持上下同乘 / 同除）
  - **"变"对话框**：化简、展开、因式分解、约分、通分、拆分、三角化简、有理化，以及替换、追加、追乘、倒数、除以、平方、算术平方根、乘方、换元；可选择覆盖原表达式或保存为副本
  - **方程能力**：方程卡片可求解（按变量与 SymPy 求解范围）；两张方程卡片重叠可联立求解，或应用韦达定理生成 `x₁+x₂`、`x₁·x₂`、`|x₁−x₂|`、判别式卡片
  - **常用方程**：圆 / 直线 / 椭圆 / 双曲线 / 抛物线模板，可留空保留参数符号，也可按"通过点 / 离心率 / 轴长 / 焦距 / 准线 / 焦点"等条件联立反推参数，解出多组即生成多张卡片
  - **几何表达式**：点到直线距离、两直线交点、交点线段中点、三角形面积（三点 / 直线+曲线+点），结果自动成为可继续变形的卡片
  - **卡片管理**：拖拽移动（重叠自动回退）、复制 / 删除 / 折叠、双击设置标题、右侧属性区（标题 / 表达式 / 变量 / 取值范围）、整张画布撤销重做

---

## 亮点分析

1. **一处做完数学**：微积分、方程与不等式、向量、解三角形、函数绘图、平面 / 立体几何的"定义 → 计算 → 绘图"全部收进**功能集成页**，不必在多个标签页之间来回跳转。

2. **解几计算器（v2.2.0 新增）**：表达式画布把公式拆成可点选的节点，任意子结构都能交换、展开、变形、换元或求解；常用方程可按几何条件反推参数，几何表达式直接给出距离、交点、中点与面积。适合课堂演示"同解变形"与"一题多解"。

3. **看得见的过程**：结果以可交互的 LaTeX 公式呈现，而非纯文本；**积木编辑器**把计算流程拆成积木，零代码搭流程并实时渲染每一步的结果。

4. **符号计算扎实**：由 SymPy 驱动，支持自定义函数 `f(3)` / `f(g(2))`、分母有理化，并提供 Python / Mpmath / SymPy / LaTeX 四种计算引擎。

5. **几何一条龙**：平面 19 种 + 立体 12 种构造，平面 32 种 + 立体 22 种计算，含斜二测画法与 2D / 3D 渲染。

6. **输入友好**：`$` 前缀直接写 LaTeX、MathLive 可视化输入、表达式缓存、回车即算。

7. **存档即现场**：输入、函数、几何对象、积木状态统一存入 `.cca`，双击即可还原，且可按类别精细控制存档范围。

8. **跨平台与双语**：cx_Freeze 打包 Windows / Linux，内置中英文界面与明暗主题，另有 Web 版可直接体验。

---

## 部署使用

### 环境准备

- Python 3.10 或更高版本
- 推荐使用虚拟环境

### 安装依赖

```bash
pip install -r requirements.txt
```

`requirements.txt` 内容：

- PySide6>=6.8.0.2
- sympy>=1.10.0
- matplotlib>=3.10.0
- PyQtDarkTheme-fork>=2.3.2
- latex2sympy2_extended>=1.0.0
- lazy_loader>=0.4

### 运行桌面版

```bash
python run.py
```

### 使用网页版

直接访问 https://limingkang.pythonanywhere.com 即可在线使用，无需安装。

### 打包教程

项目使用 cx_Freeze 将 Python 脚本打包为独立的 Windows 可执行文件。

安装打包依赖：

```bash
pip install cx_Freeze
```

在根目录执行打包命令：

```bash
python setup.py build
```

打包完成后，可执行文件位于 build/exe.win-amd64-3.x/ 目录下（具体名称取决于系统和 Python 版本）。

---

## 缺点简述

- 性能限制：对于极其复杂的符号表达式，SymPy 计算可能会较慢或内存占用较高。
- 表达式解析宽容度：依赖 SymPy 的 sympify，用户输入需基本符合 Python/SymPy 语法，对不规范的表达式可能报错。
- 打包体积：cx_Freeze 打包后的程序体积较大（约 100+ MB），因为包含了整个 Python 环境和依赖库。
- Web 版功能：在线版本受限于 PythonAnywhere 的资源，可能无法处理过大的计算任务。

---

## 附：文件结构说明

```
CalculusCalculator/
├── run.py               # 程序入口（含启动画面与引导逻辑）
├── setup.py             # cx_Freeze 打包脚本
├── requirements.txt     # Python 依赖列表
├── update.md            # 版本更新日志
├── mkdocs.yml           # 文档站（MkDocs）配置
├── README.md            # 项目说明
├── CalculusCalculator.iss  # Inno Setup 安装脚本
├── core/                # 核心模块
│   ├── __init__.py
│   ├── settings.py      # 语言/主题/初始化设置读写与切换
│   ├── sympify.py       # 表达式安全转换、函数调用预处理、LaTeX 解析
│   ├── render.py        # 公式渲染（SVG / QGraphicsView）
│   └── webengine.py     # QWebEngine 惰性预初始化
├── blockly/             # 积木化可视化编程（Google Blockly）
├── expr_calculator/     # 解几计算器（表达式画布）
│   ├── expr_tree.py     # 表达式树、LaTeX 打印器与 SymPy 互转
│   └── expr_viewer.py   # 表达式画布窗口、页面与各操作对话框
├── math_input/          # 可视化公式输入（MathLive）
├── mathjax/             # MathJax 公式渲染库
├── functions/           # 各计算功能实现
│   ├── derivative.py    # 显/隐函数求导
│   ├── integral.py      # 积分计算
│   ├── functions.py     # 函数性质分析
│   ├── simplification.py # 表达式变形（13 种方法）
│   ├── solvers.py       # 方程/不等式/微分方程/解三角形求解
│   ├── planes.py        # 平面几何计算与构造 API
│   ├── solids.py        # 立体几何计算与构造 API（含斜二测画法）
│   ├── paint2D.py       # 平面几何绘图渲染
│   ├── paint3D.py       # 立体几何 3D 绘图渲染
│   └── saves.py         # .cca 存档/读档
├── ui/                  # 界面层（PySide6）
│   ├── __init__.py      # 选项卡登记表（懒加载）
│   ├── main.py          # 主窗口逻辑
│   ├── functions.py     # 功能集成页（定义区 / 计算区 / 绘图区）
│   ├── shouye.py        # 首页
│   ├── shezhi.py        # 设置页
│   ├── huancun.py       # 缓存区
│   ├── help.py          # 帮助页
│   ├── blockly.py       # 积木编辑器（QWebChannel 桥接）
│   ├── expr.py          # 解几计算器标签页（包装表达式画布）
│   ├── guide.py         # 初始化引导教学
│   └── ui_*.py          # 各功能页布局（自动生成）
├── i18n/                # 翻译源文件与编译结果
│   ├── zh_CN.ts / .qm   # 中文翻译
│   └── en_US.ts / .qm   # 英文翻译
├── docs/                # 文档源码（MkDocs 构建，双语 zh/en）
│   ├── index.md         # 首页
│   ├── about.md         # 关于 / 版本历史
│   ├── zh/              # 中文文档（guide / dev / api）
│   └── en/              # 英文文档（guide / dev / api）
├── web/                 # 网页版代码
├── help.html            # 内置帮助文档（中文）
├── help_en.html         # 内置帮助文档（英文）
└── favicon.ico          # 应用图标
```

## 许可证

本项目采用 GPLv3 许可证。

## 作者

LiMingkang

- GitHub: [limingkang12345](https://github.com/limingkang12345)
- 官方文档: [CalculusCalculator帮助文档](https://limingkang12345.github.io/CalculusCalculator/)
- 网页版: [https://limingkang.pythonanywhere.com](https://limingkang.pythonanywhere.com)
- PYPI: [https://pypi.org/project/CalculusCalculator/](https://pypi.org/project/CalculusCalculator/)

欢迎 Star、Issue 和 Pull Request！
