from ui.ui_huitu_lj import *
from core.render import setGraphicsView, setGraphicsViewTheme
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QListWidgetItem
from PySide6.QtCore import Qt

class Huitu_lj(QWidget, Ui_huitu_lj):
    """立体几何绘图页面"""
    def __init__(self, parent, fs):
        super(Huitu_lj, self).__init__(parent)
        self.setupUi(self)
        setGraphicsViewTheme(self, parent)

        self.fs = fs
        self.parent = parent

        self.canvas = None
        self._ljs_hash = None
        self.draw_layout = QVBoxLayout(self.huitu_pingji)
        self.draw_layout.setContentsMargins(0, 0, 0, 0)

        self.huitu_lj_button.clicked.connect(self._draw)

    def showEvent(self, event):
        super().showEvent(event)
        if hasattr(self.parent, 'ljs'):
            new_hash = len(self.parent.ljs)
            if new_hash != self._ljs_hash:
                self._refresh_object_list()
                self._ljs_hash = new_hash
        elif self._ljs_hash is not None:
            self._refresh_object_list()
            self._ljs_hash = None

    def set_theme(self, theme):
        # 主题切换后按新配色重绘上次的图表（无绘图时为空操作）
        if getattr(self, '_redraw', None) is not None:
            try:
                self._redraw()
            except Exception:
                pass

    def _refresh_object_list(self):
        self.huitu_lj_list.clear()
        if not hasattr(self.parent, 'ljs') or not self.parent.ljs:
            return
        for name, val in self.parent.ljs.items():
            cat = val[0]
            display = f"[{cat}] {name}"
            item = QListWidgetItem(display)
            item.setData(Qt.ItemDataRole.UserRole, name)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked)
            self.huitu_lj_list.addItem(item)

    def _draw(self):
        if self.canvas is not None:
            self.draw_layout.removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None
        if getattr(self, 'toolbar', None) is not None:
            self.draw_layout.removeWidget(self.toolbar)
            self.toolbar.deleteLater()
            self.toolbar = None

        if not hasattr(self.parent, 'ljs') or not self.parent.ljs:
            return

        checked_names = set()
        for i in range(self.huitu_lj_list.count()):
            item = self.huitu_lj_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                checked_names.add(item.data(Qt.ItemDataRole.UserRole))

        if not checked_names: return

        from functions.paint3D import draw3d
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

        objects = []
        for name in checked_names:
            if name in self.parent.ljs:
                objects.append((self.parent.ljs[name][1], {'label': name}))

        if not objects: return

        try:
            fig = draw3d(objects, figsize=(6.0, 5.1), dpi=100,
                         theme=getattr(self.parent, 'theme', 'light'))
            self.fig = fig
            self.canvas = FigureCanvas(self.fig)
            # 原生 matplotlib 导航工具栏；3D 轴自身支持鼠标拖拽旋转视图
            from core.render import attach_plot_toolbar
            self.toolbar = attach_plot_toolbar(self.draw_layout, self.canvas, self, wheel_zoom=False)
            self.draw_layout.addWidget(self.canvas)
            self._redraw = self._draw
        except Exception as e:
            QMessageBox.warning(self, "绘制失败", f"绘制时出错：\n{e}")
