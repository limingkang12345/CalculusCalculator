from ui.ui_shezhi import *
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Qt
from core.settings import current_language, current_theme, clear_settings_file


class Shezhi(QWidget, Ui_shezhi):
    def __init__(self, parent, fs):
        super(Shezhi, self).__init__(parent)
        del fs  # 设置页不直接使用共享 fs
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
        self.shezhi_qingchu.clicked.connect(self.on_clear_settings)

    def _apply_saved_filters(self, saved):
        """将已保存的过滤设置还原到 QListWidget 的勾选状态。"""
        mapping = [
            (0, "fs"), (1, "eqs"), (2, "rels"),
            (3, "vs"), (4, "cache"), (5, "pjs"),
            (6, "ljs"), (7, "blockly"), (8, "texts"),
            (9, "combos"), (10, "views"), (11, "save_settings"),
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
            "blockly":       _checked(7),   # 积木编辑区工程
            "texts":         _checked(8),   # 所有文本框文本
            "combos":        _checked(9),   # 所有选择框选项
            "views":         _checked(10),  # 所有表达式显示框内容
            "save_settings": _checked(11),  # 所有设置选项
        }

    def on_clear_settings(self):
        """清除设置文件：先警告，再二次确认；确认后删除文件并恢复默认界面。"""
        _t = lambda zh, en: en if (current_language() or "").startswith("en") else zh

        # 第一次：破坏性操作警告
        first = QMessageBox.warning(
            self,
            _t("清除设置文件", "Clear Settings File"),
            _t("此操作将删除设置文件（语言、主题、存档过滤等所有偏好），且无法撤销。\n确定要继续吗？",
               "This deletes the settings file (language, theme, save filters and all "
               "preferences). This cannot be undone.\nDo you want to continue?"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if first != QMessageBox.StandardButton.Yes:
            return

        # 第二次：二次确认
        second = QMessageBox.question(
            self,
            _t("二次确认", "Confirm Again"),
            _t("再次确认：真的要清除所有设置并恢复默认吗？",
               "Confirm again: really clear all settings and restore defaults?"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if second != QMessageBox.StandardButton.Yes:
            return

        # 先应用默认界面（语言 + 主题），这会因保存而重新写入设置文件
        if self.parent is not None and hasattr(self.parent, "change_language"):
            self.parent.change_language("zh_CN")
            self.parent.light()
        # 删除刚写入的设置文件，达到“清除”效果
        clear_settings_file()

        # 同步本页单选按钮到默认（中文 / 浅色）
        self.shezhi_zhongwen.setChecked(True)
        self.shezhi_yingwen.setChecked(False)
        self.shezhi_shense.setChecked(False)
        self.shezhi_qianse.setChecked(True)

        QMessageBox.information(
            self,
            _t("完成", "Done"),
            _t("设置文件已清除，已恢复默认（重新启动程序以完全生效）。",
               "Settings cleared; defaults restored (restart the app to take full effect)."),
        )
