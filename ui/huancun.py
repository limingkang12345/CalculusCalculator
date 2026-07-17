from ui.ui_huancun import *
from PySide6.QtWidgets import QWidget, QDialog, QVBoxLayout, QDialogButtonBox, QApplication
from PySide6.QtGui import QAction, QIcon


def _find_main_window(widget):
    """向上遍历父级链，查找拥有 cache 和 fs 属性的 MainWindow 实例。"""
    w = widget
    while w is not None:
        if hasattr(w, 'cache') and hasattr(w, 'fs'):
            return w
        w = w.parentWidget()
    return None


def open_cache(parent):
    """打开缓存区对话框，从 MainWindow.cache 加载所有缓存项。

    用户双击某一缓存项后，其文本将被填入触发此操作的 QLineEdit，
    对话框自动关闭。也可点击"确定"不选任何项关闭。

    Args:
        parent: 触发此操作的 QLineEdit 实例，作为对话框父窗口。
    """
    main = _find_main_window(parent)
    cache_items = main.cache if main else []

    dialog = QDialog(parent)
    dialog.setWindowTitle("缓存区（双击选择）")
    dialog.resize(500, 400)

    layout = QVBoxLayout(dialog)

    # 复用 Huancun 控件，其内部已包含 QListWidget（huancunqu）及布局
    cache_widget = Huancun(dialog, main.fs if main else {})
    # 禁用 groupBox 标题避免在对话框中重复显示"缓存区（双击选择）"
    cache_widget.groupBox.setTitle("")
    layout.addWidget(cache_widget)

    # 加载缓存项到列表
    cache_widget.huancunqu.clear()
    if cache_items:
        cache_widget.huancunqu.addItems(cache_items)
    cache_widget.huancunqu.setCurrentRow(0)

    # 双击任意缓存项 → 填入输入框并关闭对话框
    def on_double_click(item):
        try:  parent.setText(item.text())
        except:  pass
        dialog.accept()
    cache_widget.huancunqu.itemDoubleClicked.connect(on_double_click)

    # 确定 / 取消 按钮
    buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    buttons.accepted.connect(lambda: on_double_click(cache_widget.huancunqu.currentItem()))
    buttons.rejected.connect(dialog.reject)
    layout.addWidget(buttons)

    dialog.exec()


class Huancun(QWidget, Ui_huancun):
    def __init__(self, parent, fs):
        super(Huancun, self).__init__(parent)
        self.setupUi(self)
        
        self.refresh_cache_list()
        self.huancunqu.itemDoubleClicked.connect(self._on_item_double_clicked)

    def refresh_cache_list(self):
        """刷新缓存区列表。从 MainWindow.cache 同步最新数据。"""
        self.huancunqu.clear()
        main = _find_main_window(self)
        if main and main.cache:
            self.huancunqu.addItems(main.cache)
        else:
            self.huancunqu.addItem("[暂无缓存项]")

    def _on_item_double_clicked(self, item):
        """双击缓存项回调：将文本复制到剪贴板（标签页模式）。"""
        text = item.text()
        if text and text != "[暂无缓存项]":
            QApplication.clipboard().setText(text)