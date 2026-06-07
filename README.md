# CalculusCalculator 微积分计算器

**CalculusCalculator** 是一个基于 SymPy 和 PySide6 的图形化微积分计算工具，支持求导、积分、函数性质分析、表达式变形、方程（组）与不等式（组）求解、微分方程求解、符号计算、向量运算、解三角形、函数绘图等功能，并提供了存档/读档及 Web 版本。

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-6.9.1-green)](https://pypi.org/project/PySide6/)
[![SymPy](https://img.shields.io/badge/SymPy-1.14.0-orange)](https://www.sympy.org/)

---

## 基本信息

- **项目地址**：[GitHub - limingkang12345/CalculusCalculator](https://github.com/limingkang12345/CalculusCalculator)
- **网页版**：[https://limingkang.pythonanywhere.com](https://limingkang.pythonanywhere.com)
- **最新版本**：v1.5.0
- **开发语言**：Python 3.8+
- **核心库**：SymPy（符号计算）、PySide6（GUI 框架）
- **功能概览**：
  - 显函数 / 隐函数求导（支持代入求值）
  - 不定积分 / 定积分
  - 函数值域、单调区间、奇偶性、周期、最值
  - 表达式化简、展开、因式分解、通分、部分分式、三角恒等变换、对数变换、换元等 13 种方法
  - 方程、不等式、方程组、不等式组的求解
  - 常微分方程求解
  - 符号计算：三种计算引擎（Python 内置 / Mpmath 高精度 / SymPy 符号），支持 LaTeX 渲染与源码复制
  - 自定义函数列表（`fs` 字典），支持函数调用传参 `f(3)` 及嵌套调用 `f(g(2))`
  - 分母有理化：求导、积分、方程求解等结果自动执行有理化
  - **向量运算**（v1.5.0）：定义二维向量，支持加法、减法、点积、夹角计算及向量属性显示
  - **解三角形**（v1.5.0）：支持 ASA、AAS、SAS、SSA、SSS 等多种三角形条件求解
  - **函数绘图**（v1.5.0）：基于 Matplotlib 绘制函数图像，支持自定义定义域
  - 工程存档/读档（JSON 格式），支持保存方程组与不等式组

---

## v1.5.0 更新内容

1. 新增**向量**功能，支持定义二维向量并执行简单的向量运算（加法、减法、点积、夹角、模、方向角、单位向量）
2. 新增**解三角形**功能，支持 ASA、AAS、SAS、SSA、SSS 等多种三角形条件求解
3. 新增**绘图**功能，支持绘制单个函数的图像
4. 更改菜单栏布局，"新建"更名为"功能"，并对功能进行归类
5. 修复函数名被错误识别的问题（定义函数 t 后会将 sqrt 的 t 误替换为函数 t）

---

## 亮点分析

1. **功能全面**  
   覆盖了微积分、代数、方程求解中的常见需求，从基础的化简求导到隐函数、微分方程一应俱全。

2. **可视化界面**  
   基于 PySide6 构建多标签页界面，每个功能独立窗口，支持公式的 LaTeX 实时渲染（`QWebEngineView` + MathJax）。

3. **自定义函数**  
   用户可以定义 `f(x)`、`g(t)` 等函数，并在后续计算中通过 `f(3)`、`f(g(2))` 等形式直接调用，极大提升了灵活性和复用性。

4. **分母有理化**  
   计算结果如含根号分母，自动执行有理化（如 `1/sqrt(2)` → `sqrt(2)/2`），使表达式更符合数学规范。

5. **多引擎计算**  
   新增的"计算"选项卡提供三种引擎：Python 内置适用于简单数值计算，Mpmath 适用于高精度计算，SymPy 适用于符号运算与 LaTeX 生成。

6. **存档与恢复**  
   可以将当前所有标签页的输入、自定义函数列表、标签页序号等保存为 JSON 文件，下次打开时自动恢复现场。

7. **跨平台打包**  
   提供了 `cx_Freeze` 的打包配置（`setup.py`），可以生成 Windows 可执行文件，便于分发。

8. **向量运算**（v1.5.0 新增）  
   支持定义二维向量，查看向量的模、方向角、单位向量等属性，并可进行向量加法、减法、点积、夹角计算。

9. **解三角形**（v1.5.0 新增）  
   输入三角形的已知角度和边长条件，系统自动识别 ASA、AAS、SAS、SSA、SSS 等情形并求解，支持多解情况。

10. **函数绘图**（v1.5.0 新增）  
    基于 Matplotlib 绘制单个函数的图像，支持自定义定义域，自动处理间断点断线。

11. **Web 版补充**  
    除了桌面客户端，还提供了在线网页版（基于 PythonAnywhere），方便快速体验。

---

## 部署使用

### 环境准备

- Python 3.8 或更高版本
- 推荐使用虚拟环境

### 安装依赖

```bash
pip install -r requirements.txt
```

`requirements.txt` 内容：

- PySide6==6.9.1
- sympy==1.14.0

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
├── main.py              # 主窗口逻辑
├── run.py               # 程序入口
├── sympify.py                # 表达式安全转换、函数调用预处理、分母有理化
├── derivative.py             # 显/隐函数求导
├── integral.py               # 积分计算
├── functions.py              # 函数性质分析
├── simplification.py         # 表达式变形（13种方法）
├── solvers.py                # 方程/不等式/微分方程/解三角形求解
├── vectors.py                # 向量数据结构（预留）
├── layouts_tool.py           # 自适应布局管理器
├── saves.py                  # JSON 存档/读档
├── help.html                 # 内置帮助文档
├── setup.py                  # cx_Freeze 打包脚本
├── requirements.txt          # Python 依赖列表
├── update.txt                # 版本更新日志
├── ui/
│   ├── __init__.py           # 各选项卡逻辑实现
│   ├── ui_main.py            # 主窗口布局
│   ├── ui_dingyi.py          # 定义页布局
│   ├── ui_qiudao.py          # 求导页布局
│   ├── ui_jifen.py           # 积分页布局
│   ├── ui_bianxing.py        # 变形页布局
│   ├── ui_fangcheng.py       # 方程页布局
│   ├── ui_fangchengzu.py     # 方程组页布局
│   ├── ui_budengshi.py       # 不等式页布局
│   ├── ui_budengshizu.py     # 不等式组页布局
│   ├── ui_jisuan.py          # 计算页布局
│   ├── ui_shouye.py          # 首页布局
│   ├── ui_help.py            # 帮助页布局
│   ├── ui_dingyixiangliang.py # 定义向量页布局
│   ├── ui_huitu_hanshu.py    # 绘制函数页布局
│   └── ui_jiesanjiaoxing.py  # 解三角形页布局
└── resources.qrc        # 资源文件（MathJax等）
```

---

## 许可证

本项目采用 MIT 许可证。

## 作者

LiMingkang

- GitHub: [limingkang12345](https://github.com/limingkang12345)
- 网页版: [https://limingkang.pythonanywhere.com](https://limingkang.pythonanywhere.com)
- PYPI: [https://pypi.org/project/CalculusCalculator/](https://pypi.org/project/CalculusCalculator/)

欢迎 Star、Issue 和 Pull Request！
