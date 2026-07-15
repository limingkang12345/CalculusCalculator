# 公式渲染

CalculusCalculator 在多处将表达式以数学公式形式呈现，主要依赖 LaTeX。

## 结果公式渲染

求导、积分、函数性质、变形、方程求解等模块的计算结果，会通过 `core/render.py` 将 LaTeX
转换为 SVG，并在 `QGraphicsView` 中渲染显示，支持浅色 / 深色背景。

- 浅色主题：视图背景为白色
- 深色主题：视图背景为黑色
- 切换主题后，已显示的公式会自动按新配色刷新

## 计算选项卡的 LaTeX 输出

"计算"选项卡（见 [计算选项卡](../modules/calculation.md)）提供三种计算引擎，其中：

- **SymPy 符号引擎**：基于 SymPy 进行符号运算，结果**同时以 LaTeX 代码和纯文本两种形式**显示。
- **LaTeX 代码生成引擎**：根据输入的 Python 表达式直接生成对应的 LaTeX 代码，便于复制到论文、笔记中。

## 帮助文档渲染

内置"帮助"页面使用 `QTextBrowser` 显示静态文档（v1.6.1 起由 `QWebEngineView` 改为 `QTextBrowser`），
显著提升加载性能，并随主窗口缩放自适应调整大小。

## 输入即 LaTeX

在任意表达式输入框中，以 `$` 开头的 LaTeX 代码会被自动解析为 SymPy 表达式后再渲染，
详见 [字符串解析](sympify.md#一latex-代码直接输入v161-新增)。
