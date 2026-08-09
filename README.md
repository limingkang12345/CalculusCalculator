# CalculusCalculator 微积分计算器

**CalculusCalculator** 是一个基于 SymPy 和 PySide6 的图形化微积分计算工具，支持求导、积分、函数性质分析、表达式变形、方程（组）与不等式（组）求解、微分方程求解、符号计算、向量运算、解三角形、函数绘图、**平面/立体几何定义、计算与绘图**、**积木化可视化编程**等功能，并提供了**表达式缓存**、**可视化公式输入**、**启动画面**、**初始化引导教学**、存档/读档（`.cca`）及 Web 版本。

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-6.11.1-green)](https://pypi.org/project/PySide6/)
[![SymPy](https://img.shields.io/badge/SymPy-1.14.0-orange)](https://www.sympy.org/)

---

## 基本信息

- **项目地址**：[GitHub - limingkang12345/CalculusCalculator](https://github.com/limingkang12345/CalculusCalculator)
- **项目文档**: [CalculusCalculator帮助文档](https://limingkang12345.github.io/CalculusCalculator/)
- **网页版**：[https://limingkang.pythonanywhere.com](https://limingkang.pythonanywhere.com)
- **最新版本**：v2.0.0
- **开发语言**：Python 3.10+
- **核心库**：SymPy（符号计算）、PySide6（GUI 框架）、Matplotlib（几何绘图）、Blockly（可视化编程）
- **功能概览**：
  - **积木化可视化编程**（v2.0.0）：通过拼接积木实现计算流程的可视化，无需编写代码
  - 显函数 / 隐函数求导（支持代入求值）
  - 不定积分 / 定积分
  - 函数值域、单调区间、奇偶性、周期、最值
  - 表达式化简、展开、因式分解、通分、部分分式、三角恒等变换、对数变换、换元等 13 种方法
  - 方程、不等式、方程组、不等式组的求解
  - 常微分方程求解
  - 符号计算：四种计算引擎（Python 内置 / Mpmath 高精度 / SymPy 符号 / LaTeX 代码生成），支持 LaTeX 渲染与源码复制
  - 自定义函数列表（`fs` 字典），支持函数调用传参 `f(3)` 及嵌套调用 `f(g(2))`
  - 分母有理化：求导、积分、方程求解等结果自动执行有理化
  - **向量运算**：定义二维向量，支持加法、减法、点积、夹角计算及向量属性显示
  - **解三角形**：支持 ASA、AAS、SAS、SSA、SSS 等多种三角形条件求解
  - **函数绘图**：基于 Matplotlib 绘制函数图像，支持自定义定义域、放缩、拖动与保存
  - **平面几何**：定义点/直线/线段/圆/三角形/多边形，支持位置关系构造（中垂线、角平分线、中线、高线、内切圆、旁切圆等），复选框筛选绘图
  - **立体几何**：定义三维点/直线/线段/平面，支持平行/垂直构造、垂足计算、斜二测画法，复选框筛选 3D 绘图
  - **几何计算**：平面几何 32 种运算（两点距离、中点、共线判断、直线/圆/三角形/多边形属性、向量计算、变换等）、立体几何 22 种运算（三维点/线/面关系、四面体体积、斜二测投影/面积变换等）
  - **回车快捷键**：各页面主要文本输入框支持回车键触发对应按钮功能
  - **表达式缓存**：通过缓存区管理常用表达式，支持对话框选择和标签页浏览
  - **可视化公式输入**（v2.0.0）：后端换用 MathLive 公式编辑器，以图形化方式插入数学公式
  - **存档设置**：设置页新增存档选项，可精细控制存档时保存哪些类型的数据
  - **工程存档/读档**（v2.0.0）：项目文件后缀改为 `.cca`（内容仍为 JSON），安装后可双击直接打开
  - **LaTeX 代码直接输入**：在表达式前添加 `$` 标识，可直接输入 LaTeX 代码，系统自动解析为 SymPy 表达式
  - **启动画面**（v2.0.0）：程序启动时显示进度画面，优化启动速度
  - **初始化引导教学**（v2.0.0）：首次启动时提供分步向导，在"表达式输入"一步含"动手试试"互动练习，帮助新用户快速上手

---

## v2.0.0 更新内容

#### 此版本为 CalculusCalculator 重大版本重构，带来全新功能

1. **积木化功能（Blockly）**：新增基于 Blockly 的可视化编程编辑器，通过拼接积木实现计算流程的可视化，无需编写代码，目前支持：
   - SymPy / LaTeX 表达式输入
   - 编辑器内直接执行流程，实时显示中间结果
   - 输出公式自动以 LaTeX 渲染
   - 定义函数 / 函数性质分析
   - 求导 / 积分
   - 解方程（组）/ 不等式（组）/ 解三角形
   - 工程存档 / 读档，受"设置 → 存档设置"项控制
   - 启动界面（首次打开积木编辑器时预初始化 WebEngine，避免闪退）

2. **公式编辑器全面升级**：后端换用 MathLive，显著提升可视化公式输入的使用体验

3. **启动画面**：新增启动画面（Splash Screen），显示启动进度，优化启动速度

4. **帮助文档双语支持**：帮助文档 Docs 新增英文支持，并为积木模式和启动页面提供英文支持

5. **初始化引导教学**：新增新手引导（Guide），满足以下任意一种情况时触发：
   - 设置文件未初始化
   - 设置中 `hasInitialized` 为否
   - 用户点击菜单「关于 → 引导」

6. **清除设置文件**：支持一键清除持久化的设置文件（settings.json）

7. **界面样式优化**：优化界面样式，增加主窗口初始大小

8. **首页丰富**：丰富首页内容，美化首页样式

9. **图像操作**：新增对绘制的函数 / 几何图像的放缩、拖动与保存支持

10. **项目文件格式**：更改工程文件后缀为 `.cca`（存档格式仍为 JSON），安装软件后可直接双击打开 `.cca` 文件

11. **修复问题**：
    - 修复公式渲染背景色与窗口背景色存在色差的问题
    - 修复解三角形公式无法渲染问题
    - 修复解三角方程 / 不等式时答案未化到最简问题
    - 修复调整颜色后绘图区背景颜色没有改变的问题

---

## 亮点分析

1. **功能全面**  
   覆盖了微积分、代数、方程求解、几何计算中的常见需求，从基础的化简求导到隐函数、微分方程、平面立体几何一应俱全。

2. **积木化可视化编程（v2.0.0 新增）**  
   基于 Blockly 提供拖拽式积木编辑器，无需编写代码即可搭建计算流程。输入表达式、执行流程、查看 LaTeX 渲染结果，定义函数、求导、积分、解方程/不等式/三角形等一应俱全，是零代码体验微积分计算的理想方式。

3. **可视化界面**  
   基于 PySide6 构建多标签页界面，每个功能独立窗口，计算结果以 LaTeX 形式在 `QGraphicsView`（SVG）中实时渲染，帮助文档使用 `QTextBrowser` 显示。

4. **自定义函数**  
   用户可以定义 `f(x)`、`g(t)` 等函数，并在后续计算中通过 `f(3)`、`f(g(2))` 等形式直接调用，极大提升了灵活性和复用性。

5. **分母有理化**  
   计算结果如含根号分母，自动执行有理化（如 `1/sqrt(2)` → `sqrt(2)/2`），使表达式更符合数学规范。

6. **多引擎计算**  
   "计算"选项卡提供四种引擎：Python 内置适用于简单数值计算，Mpmath 适用于高精度计算，SymPy 适用于符号运算与 LaTeX 生成，LaTeX 代码生成引擎可生成 LaTeX 代码。

7. **存档与恢复**  
   可以将当前所有标签页的输入、自定义函数列表、标签页序号、几何对象、积木编辑器状态等保存为 `.cca` 文件（JSON 格式），下次打开时自动恢复现场。安装后可双击 `.cca` 文件直接打开。

8. **跨平台打包**  
   提供了 `cx_Freeze` 的打包配置（`setup.py`），可以生成 Windows 和 Linux 可执行文件，便于分发。

9. **向量运算**  
   支持定义二维向量，查看向量的模、方向角、单位向量等属性，并可进行向量加法、减法、点积、夹角计算。

10. **解三角形**  
   输入三角形的已知角度和边长条件，系统自动识别 ASA、AAS、SAS、SSA、SSS 等情形并求解，支持多解情况。

11. **函数绘图**  
   基于 Matplotlib 绘制单个函数的图像，支持自定义定义域，自动处理间断点断线，并支持图像的放缩、拖动与保存。

12. **平面/立体几何**  
   支持平面几何 19 种构造和立体几何 12 种构造，并通过复选框筛选绘图，基于 Matplotlib 渲染 2D/3D 图像。

13. **几何计算**  
   在已定义几何对象的基础上，提供平面几何 32 种和立体几何 22 种运算，涵盖距离、中点、投影、面积、体积、向量、斜二测画法面积变换等。

14. **回车快捷键**  
   各页面主要输入框支持回车触发对应按钮，无需鼠标点击，提升操作效率。

15. **启动画面与引导教学**（v2.0.0 新增）
   启动时显示进度画面，提供初始化引导教学（Guide），带领新用户快速了解各功能区。
   引导在"表达式输入"一步提供"动手试试"互动练习（可即时验证 SymPy 表达式是否合法）；底部带进度条，支持左右方向键快捷切换。

16. **Web 版补充**  
   除了桌面客户端，还提供了在线网页版（基于 PythonAnywhere），方便快速体验。

17. **LaTeX 代码直接输入**  
   在表达式前添加 `$` 标识即可直接输入 LaTeX 代码（如 `$\frac{x}{2}`），系统自动将 LaTeX 解析为 SymPy 表达式进行计算。

18. **表达式缓存与可视化输入**（v2.0.0 新增）  
   缓存区可暂存常用表达式，支持弹窗选择与标签页管理；可视化公式输入后端换用 MathLive，无需记忆 LaTeX 即可插入数学符号。

19. **存档精细控制**  
   设置页可按类别选择性存档，避免不必要的数据写入项目文件。

20. **清除设置文件**（v2.0.0 新增）  
   一键清除持久化的设置文件，重置语言、主题与初始化状态。

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
│   └── render.py        # 公式渲染（SVG / QGraphicsView）
├── blockly/             # 积木化可视化编程（Google Blockly）
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
│   ├── __init__.py      # 各选项卡逻辑实现汇总
│   ├── main.py          # 主窗口逻辑
│   ├── blockly.py       # 积木编辑器（QWebChannel 桥接）
│   ├── guide.py         # 初始化引导教学
│   ├── <功能>.py         # 各功能页逻辑，如 dingyi / qiudao / jifen / bianxing /
│   │                    #   fangcheng / fangchengzu / budengshi / budengshizu / jisuan /
│   │                    #   shouye / dingyixiangliang / huitu_hanshu / jiesanjiaoxing /
│   │                    #   dingyi_pj / huitu_pj / dingyi_lj / huitu_lj / pjjisuan /
│   │                    #   ljjisuan / help / shezhi / huancun / blockly 等
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
