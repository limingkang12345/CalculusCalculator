from ui.ui_shezhi import *
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from core.settings import current_language, current_theme


class Shezhi(QWidget, Ui_shezhi):
    def __init__(self, parent, fs):
        super(Shezhi, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        # 根据当前语言预选单选按钮，避免每次打开都回到默认
        if current_language() == "en_US":
            self.shezhi_yingwen.setChecked(True)
        else:
            self.shezhi_zhongwen.setChecked(True)
        # 根据当前主题预选单选按钮（默认浅色）
        if current_theme() == "dark":
            self.shezhi_shense.setChecked(True)
        else:
            self.shezhi_qianse.setChecked(True)
        # 恢复上次存档过滤设置（首次使用时所有项全勾选）
        saved = getattr(self.parent, 'save_filters', None)
        if saved is not None:
            self._apply_saved_filters(saved)
        self.shezhi_yingyong.clicked.connect(self.on_apply)

    def _apply_saved_filters(self, saved):
        """将已保存的过滤设置还原到 QListWidget 的勾选状态。"""
        mapping = [
            (0, "fs"), (1, "eqs"), (2, "rels"),
            (3, "vs"), (4, "cache"), (5, "pjs"),
            (6, "ljs"), (7, "texts"), (8, "combos"),
            (9, "views"), (10, "save_settings"),
        ]
        # 先全部取消，再按要求勾选
        for i in range(self.shezhi_cundang.count()):
            self.shezhi_cundang.item(i).setCheckState(Qt.Unchecked)
        for idx, key in mapping:
            if saved.get(key, True):
                self.shezhi_cundang.item(idx).setCheckState(Qt.Checked)

    def on_apply(self):
        # 语言切换
        lang = "en_US" if self.shezhi_yingwen.isChecked() else "zh_CN"
        # 主题切换
        theme = "dark" if self.shezhi_shense.isChecked() else "light"
        if self.parent is not None:
            if hasattr(self.parent, "change_language"):
                self.parent.change_language(lang)
            if theme == "dark":
                self.parent.dark()
            else:
                self.parent.light()
        from core.settings import save_theme
        save_theme(theme)

        # 存档设置：将勾选状态写入 MainWindow.save_filters，
        # 供 saves.py 存档/读档时决定哪些数据类别生效
        def _checked(idx):
            it = self.shezhi_cundang.item(idx)
            return it is not None and it.checkState() == Qt.Checked

        self.parent.save_filters = {
            "fs":            _checked(0),   # 函数列表
            "eqs":           _checked(1),   # 方程列表（方程组）
            "rels":          _checked(2),   # 不等式列表（不等式组）
            "vs":            _checked(3),   # 向量列表
            "cache":         _checked(4),   # 所有缓存区内容
            "pjs":           _checked(5),   # 平面几何对象列表
            "ljs":           _checked(6),   # 立体几何对象列表
            "texts":         _checked(7),   # 所有文本框文本
            "combos":        _checked(8),   # 所有选择框选项
            "views":         _checked(9),   # 所有表达式显示框内容
            "save_settings": _checked(10),  # 所有设置选项
        }
