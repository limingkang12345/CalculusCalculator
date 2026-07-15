# CalculusCalculator 微积分计算器

**CalculusCalculator** 是一个基于 SymPy 与 PySide6 的图形化微积分计算工具，覆盖求导、积分、函数性质分析、表达式变形、方程（组）与不等式（组）求解、微分方程、符号计算、向量运算、解三角形、函数绘图，以及平面 / 立体几何的定义、计算与绘图，并提供工程存档 / 读档、内置帮助文档、浅色 / 深色主题与中英文界面。

[在 GitHub 上查看](https://github.com/limingkang12345/CalculusCalculator) · [网页版](https://limingkang.pythonanywhere.com)

## 核心特性

- **功能全面**：微积分、代数、方程求解、几何计算一应俱全。
- **可视化界面**：基于 PySide6 的多标签页界面，公式以 LaTeX 实时渲染。
- **自定义函数**：可定义 `f(x)`、`g(t)`，并通过 `f(3)`、`f(g(2))` 形式调用。
- **分母有理化**：含根号分母的结果自动有理化（如 `1/sqrt(2) → sqrt(2)/2`）。
- **多引擎计算**：Python 内置 / Mpmath 高精度 / SymPy 符号三种引擎，支持 LaTeX 输出。
- **几何计算**：平面 32 种、立体 22 种运算，配合 Matplotlib 2D/3D 绘图。
- **存档与恢复**：所有标签页输入、自定义函数、几何对象保存为 JSON，下次自动恢复。
- **设置与多语言**：内置"设置"选项卡，支持中文 / 英文界面与浅色 / 深色主题。
- **内置帮助文档**：提供用户文档与 API 文档（本站点即其源码）。

## 快速导航

- 想马上用起来？看 [快速开始](guide/quickstart.md)。
- 需要安装 / 打包？看 [安装教程](guide/installation.md)。
- 调整语言、主题或存档？看 [配置选项](guide/configuration.md)。
- 不确定输入语法？看 [字符串解析](api/core/sympify.md)。
- 查阅各功能用法？看 [功能模块](api/modules/derivative.md)。

## 许可证

本项目采用 MIT 许可证。作者 LiMingkang。
