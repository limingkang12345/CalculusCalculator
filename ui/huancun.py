from ui.ui_huancun import Ui_huancun
from PySide6.QtWidgets import QWidget, QDialog, QVBoxLayout, QDialogButtonBox, QApplication
from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtGui import QAction, QIcon


_PLACEHOLDER = lambda: QCoreApplication.translate("huancun", "[暂无缓存项]")
_CACHE_TITLE = lambda: QCoreApplication.translate("huancun", "缓存区（双击选择）")


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
    dialog.setWindowTitle(_CACHE_TITLE())
    dialog.resize(500, 400)

    layout = QVBoxLayout(dialog)

    # 复用 Huancun 控件，其内部已包含 QListWidget（huancunqu）及布局
    cache_widget = Huancun(dialog, main.fs if main else {})
    # 禁用 groupBox 标题避免在对话框中重复显示缓存区标题
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
            self.huancunqu.addItem(_PLACEHOLDER())

    def retranslateUi(self, *args):
        """语言切换时刷新：先调用基类翻译（groupBox 标题等），
        再实时更新代码中生成的“暂无缓存项”占位项文本。"""
        Ui_huancun.retranslateUi(self, self)
        # 占位项文本在代码中生成，retranslateUi 不会自动刷新；
        # 缓存为空时列表仅含该占位项，按旧译文找到后替换为新译文。
        old = _PLACEHOLDER()
        items = self.huancunqu.findItems(old, Qt.MatchExactly)
        if items:
            for it in items:
                it.setText(_PLACEHOLDER())
        elif self.huancunqu.count() == 0:
            # 兜底：未找到旧占位项（如初始即为空）时整体重建
            self.refresh_cache_list()

    def _on_item_double_clicked(self, item):
        """双击缓存项回调：将文本复制到剪贴板（标签页模式）。"""
        text = item.text()
        if text and text != _PLACEHOLDER():
            QApplication.clipboard().setText(text)