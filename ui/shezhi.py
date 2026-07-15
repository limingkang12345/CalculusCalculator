from ui.ui_shezhi import *
from PySide6.QtWidgets import QWidget
from ui.i18n import current_language, current_theme


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
        self.shezhi_yingyong.clicked.connect(self.on_apply)

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
        from ui.i18n import save_theme
        save_theme(theme)
