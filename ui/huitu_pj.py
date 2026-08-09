from ui.ui_huitu_pj import *
from core.render import setGraphicsView, setGraphicsViewTheme
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QListWidgetItem
from PySide6.QtCore import Qt

class Huitu_pj(QWidget, Ui_huitu_pj):
    def __init__(self, parent, fs):
        super(Huitu_pj, self).__init__(parent)
        self.setupUi(self)
        setGraphicsViewTheme(self, parent)

        self.fs = fs
        self.parent = parent

        self.canvas = None
        self._pjs_hash = None  # 跟踪 pjs 变化，避免重复刷新列表
        self.draw_layout = QVBoxLayout(self.huitu_pingji)
        self.draw_layout.setContentsMargins(0, 0, 0, 0)

        self.huitu_pj_button.clicked.connect(self._draw)

    def showEvent(self, event):
        """切换至本页时自动刷新对象列表（仅在 pjs 内容变化时重建）"""
        super().showEvent(event)
        if hasattr(self.parent, 'pjs'):
            new_hash = len(self.parent.pjs)
            if new_hash != self._pjs_hash:
                self._refresh_object_list()
                self._pjs_hash = new_hash
        elif self._pjs_hash is not None:
            self._refresh_object_list()
            self._pjs_hash = None

    def set_theme(self, theme):
        # 主题切换后按新配色重绘上次的图表（无绘图时为空操作）
        if getattr(self, '_redraw', None) is not None:
            try:
                self._redraw()
            except Exception:
                pass

    def _refresh_object_list(self):
        """根据 pjs 刷新对象列表（全选 + 复选框），Qt 自动处理点击切换"""
        self.huitu_pj_list.clear()
        if not hasattr(self.parent, 'pjs') or not self.parent.pjs:
            return
        for name, val in self.parent.pjs.items():
            cat = val[0]
            display = f"[{cat}] {name}"
            item = QListWidgetItem(display)
            item.setData(Qt.ItemDataRole.UserRole, name)  # 存储原始名称
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked)  # 默认选中
            self.huitu_pj_list.addItem(item)

    def _draw(self):
        """仅绘制列表中选中的对象"""
        # 销毁之前画的canvas与导航工具栏
        if self.canvas is not None:
            self.draw_layout.removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None
        if getattr(self, 'toolbar', None) is not None:
            self.draw_layout.removeWidget(self.toolbar)
            self.toolbar.deleteLater()
            self.toolbar = None

        # 获取已定义的对象
        if not hasattr(self.parent, 'pjs') or not self.parent.pjs:
            return

        # 收集选中对象名称
        checked_names = set()
        for i in range(self.huitu_pj_list.count()):
            item = self.huitu_pj_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                checked_names.add(item.data(Qt.ItemDataRole.UserRole))

        if not checked_names:
            return

        from functions.paint2D import draw2d
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

        # 构建 (obj, style) 列表：仅选中的对象
        objects = []
        for name in checked_names:
            if name in self.parent.pjs:
                obj = self.parent.pjs[name][1]
                objects.append((obj, {'label': name}))

        if not objects:
            return

        try:
            fig = draw2d(objects, figsize=(6.0, 5.1), dpi=100,
                         theme=getattr(self.parent, 'theme', 'light'))
            self.fig = fig
            self.canvas = FigureCanvas(self.fig)
            # 原生 matplotlib 导航工具栏（Home/平移/缩放/保存）+ 滚轮缩放
            from core.render import attach_plot_toolbar
            self.toolbar = attach_plot_toolbar(self.draw_layout, self.canvas, self, wheel_zoom=True)
            self.draw_layout.addWidget(self.canvas)
            self._redraw = self._draw
        except Exception as e:
            QMessageBox.warning(self, "绘制失败", f"绘制时出错：\n{e}")
