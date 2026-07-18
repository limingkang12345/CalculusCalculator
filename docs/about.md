# 关于

## 项目信息

- **项目地址**：[GitHub - limingkang12345/CalculusCalculator](https://github.com/limingkang12345/CalculusCalculator)
- **网页版**：[https://limingkang.pythonanywhere.com](https://limingkang.pythonanywhere.com)
- **PYPI**：[https://pypi.org/project/CalculusCalculator/](https://pypi.org/project/CalculusCalculator/)
- **核心库**：SymPy（符号计算）、PySide6（GUI）、Matplotlib（绘图）、PyQtDarkTheme-fork（主题）、latex2sympy2（LaTeX 解析）、pyqt5-math-widget（可视化公式输入）

## 版本历史

### v1.6.4
- **表达式缓存**：新增"缓存区"功能（菜单"文件 → 缓存区"），支持标签页管理缓存表达式；输入框旁三个快捷按钮：可视化输入、打开缓存区弹窗、存入缓存区
- **可视化公式输入**：基于 pyqt5-math-widget（已内置于 `math_input/` 目录），支持结构化选择和编辑数学符号
- **存档设置**：设置页新增"存档设置（保存时）"列表，可勾选/取消函数列表、方程列表等，精细控制存档数据范围
- **菜单调整**："解三角形"移至"求解"菜单子项，"变形"移至"计算"菜单子项
- **项目结构优化**：`core/` 目录添加 `__init__.py`；`ui/i18n.py` 重构为 `core/settings.py`
- **代码清理**：移除浅色/深色样式切换的残留 QAction

### v1.6.3
- 新增"设置"选项卡，并将主题样式设置项移入设置选项卡
- 新增"语言"设置项，支持英语界面
- 新增内置"帮助文档"，提供用户文档与 API 文档
- 修复不能进行不定积分和定积分的问题
- 移除 `resources_rc.py` 中打包的 MathJax 库，缩小 ico 体积

### v1.6.2（GitHub 最新发布）
- 数学公式显示组件更换为 `QGraphicsView`，大幅减小打包体积
- 重构项目结构，增强规范性
- 使用 `lazy_loader` 加快启动速度
- 修复暗色主题下帮助文档内容样式错误

### v1.6
- 窗口部件随窗口大小自适应
- 使用 PyQtDarkTheme-fork 实现现代化扁平 UI
- 新增"界面主题"菜单项，支持浅色/深色切换
- 额外提供 Nuitka 编译版本

### v1.6.1
- LaTeX 代码直接输入：在表达式前加 `$` 即可输入 LaTeX
- 帮助页面由 `QWebEngineView` 改为 `QTextBrowser`，加载性能提升
- 更新帮助文档与 README

### v1.5.2
- 几何计算：平面 32 种、立体 22 种运算
- 回车快捷键：主要输入框支持回车触发按钮
- 菜单栏新增"计算"项

### v1.5.1
- 平面几何 / 立体几何定义与绘图

### v1.5.0
- 向量、解三角形、函数绘图

### v1.4.4
- 计算选项卡：高精度与符号运算、LaTeX 生成
- 函数以 `函数名(自变量值)` 调用，支持嵌套
- 大部分结果自动分母有理化；不等式解集以集合/区间返回
- 方程组与不等式组写入存档；修复多解报错

### v1.4.3
- 新增 JSON 存档/读档功能
- 修复初次新建选项卡卡顿；改用 WinRAR/7z 打包

### v1.4.2
- 修复代数式输入时被自动化简、求解时不自动化简的问题

### v1.4.1
- 重构 UI：标签页可像浏览器一样增减
- 新增菜单栏（"关于"含 GitHub/网页版链接）
- UI 代码移入 `ui` 目录；缩小打包体积

## 已知限制

- 极复杂的符号表达式下 SymPy 计算可能较慢或占用较多内存。
- 表达式解析依赖 SymPy 的 `sympify`，需基本符合 Python/SymPy 语法。
- cx_Freeze 打包体积较大（约 100+ MB）。
- 网页版受 PythonAnywhere 资源限制，难以处理超大计算任务。

## 许可证

本项目采用 [MIT 许可证](https://opensource.org/licenses/MIT)。

## 作者

LiMingkang — GitHub: [limingkang12345](https://github.com/limingkang12345)
