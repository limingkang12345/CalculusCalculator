from ui.ui_huitu_hanshu import *
from core.sympify import sympify
from core.render import setGraphicsView, setGraphicsViewTheme, applyPlotTheme
from sympy import Symbol
from PySide6.QtWidgets import QWidget, QVBoxLayout

class Huitu_hanshu(QWidget, Ui_huitu_hanshu):
    def __init__(self, parent, fs):
        super(Huitu_hanshu, self).__init__(parent)
        self.setupUi(self)
        setGraphicsViewTheme(self, parent)

        self.fs = fs
        self.parent = parent

        self.huitu_hanshu_biaodashi_radio.toggled.connect(self.toggle_input_mode)
        self.huitu_hanshu_hanshu_radio.toggled.connect(self.toggle_input_mode)
        self.huitu_hanshu_huizhi.clicked.connect(self.draw_function)
        self.huitu_hanshu_biaodashi.returnPressed.connect(self.huitu_hanshu_huizhi.click)

        self.canvas = None
        self.draw_layout = QVBoxLayout(self.huitu_hanshu_huitu)
        self.draw_layout.setContentsMargins(0, 0, 0, 0)

        self.update_function_list()

    def set_theme(self, theme):
        # 主题切换后按新配色重绘上次的图表（无绘图时为空操作）
        if getattr(self, '_redraw', None) is not None:
            try:
                self._redraw()
            except Exception:
                pass

    def toggle_input_mode(self):
        # 切换输入模式：表达式 / 选择函数
        is_expression = self.huitu_hanshu_biaodashi_radio.isChecked()
        self.huitu_hanshu_biaodashi.setEnabled(is_expression)
        self.huitu_hanshu_hanshu.setEnabled(not is_expression)

    def update_function_list(self):
        # 刷新已定义函数的下拉列表
        self.huitu_hanshu_hanshu.clear()
        for name in self.fs.keys():
            self.huitu_hanshu_hanshu.addItem("{}({})".format(name, self.fs[name][3]))

    def draw_function(self):
        # 销毁之前画的函数图像对象与导航工具栏
        if self.canvas is not None:
            self.draw_layout.removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None
        if getattr(self, 'toolbar', None) is not None:
            self.draw_layout.removeWidget(self.toolbar)
            self.toolbar.deleteLater()
            self.toolbar = None

        import numpy as np
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
        from matplotlib.figure import Figure
        from sympy import lambdify

        # 获取表达式
        if self.huitu_hanshu_biaodashi_radio.isChecked():
            expr_str = self.huitu_hanshu_biaodashi.text()
            if not expr_str:
                return
            try:
                expr = sympify(expr_str, self.fs)
            except Exception:
                return
            free_syms = list(expr.free_symbols)
            if free_syms:
                var = list(free_syms)[0]
            else:
                var = Symbol('x')
        else:
            func_name = self.huitu_hanshu_hanshu.currentText().split('(')[0]
            if func_name not in self.fs:
                return
            expr_str = self.fs[func_name][1]
            var_str = self.fs[func_name][3]
            try:
                expr = sympify(expr_str, self.fs)
            except Exception:
                return
            var = Symbol(var_str)

        # 定义域
        left_str = self.huitu_hanshu_dingyiyu_left.text() or '-10'
        right_str = self.huitu_hanshu_dingyiyu_right.text() or '10'
        try:
            left = float(sympify(left_str, self.fs))
            right = float(sympify(right_str, self.fs))
        except Exception:
            left, right = -10, 10
        if left >= right:
            left, right = -10, 10

        try:
            # 将 SymPy 表达式转为 numpy 可调函数
            f = lambdify(var, expr, modules=['numpy', {'conjugate': np.conj}])

            # 生成密集的 x 采样点
            num_points = 2000
            x_vals = np.linspace(float(left), float(right), num_points)

            # 排除无穷大和 NaN 的 y 值，避免曲线断裂处连线
            with np.errstate(invalid='ignore', divide='ignore'):
                y_vals = np.asarray(f(x_vals), dtype=np.float64)

            # 构建 matplotlib 图形
            fig = Figure(figsize=(7.7, 3.9), dpi=100)
            ax = fig.add_subplot(111)
            _bg, _fg, grid_c, axis_c = applyPlotTheme(
                fig, ax, getattr(self.parent, 'theme', 'light'))

            # 在 NaN/Inf 处断开曲线
            mask = np.isfinite(y_vals)
            segments = []
            start = 0
            while start < len(mask):
                if mask[start]:
                    end = start
                    while end < len(mask) and mask[end]:
                        end += 1
                    segments.append((start, end))
                    start = end
                else:
                    start += 1

            for seg_start, seg_end in segments:
                ax.plot(x_vals[seg_start:seg_end], y_vals[seg_start:seg_end],
                        color='#1f77b4', linewidth=1.5)

            # 坐标轴和网格
            ax.axhline(y=0, color=axis_c, linewidth=0.5)
            ax.axvline(x=0, color=axis_c, linewidth=0.5)
            ax.grid(True, linestyle='--', alpha=0.6, color=grid_c)
            ax.set_xlim(float(left), float(right))

            # 自动缩放 y 轴到可见范围
            if np.any(mask):
                y_min, y_max = np.min(y_vals[mask]), np.max(y_vals[mask])
                margin = max((y_max - y_min) * 0.1, 1.0)
                ax.set_ylim(y_min - margin, y_max + margin)

            fig.tight_layout()

            self.fig = fig
            self.canvas = FigureCanvas(self.fig)
            # 原生 matplotlib 导航工具栏（Home/平移/缩放/保存）+ 滚轮缩放
            from core.render import attach_plot_toolbar
            self.toolbar = attach_plot_toolbar(self.draw_layout, self.canvas, self, wheel_zoom=True)
            self.draw_layout.addWidget(self.canvas)
            self._redraw = self.draw_function
        except Exception:
            pass
