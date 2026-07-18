from ui.ui_shouye import *
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QFont, QFontMetrics

# 标题基准字号与基准文本（用于按实际可用宽度缩放，避免单行过长把窗口撑宽）
_TITLE_BASE_PT = 50
_TITLE_TEXT = "CalculusCalculator"


class Shouye(QWidget, Ui_shouye):
    def __init__(self, parent, fs):
        super(Shouye, self).__init__(parent)
        self.setupUi(self)
        # 保存原始 HTML，便于按窗口宽度重算字号
        self._title_html = self.shouye_welcome.text()
        self.shouye_welcome.setWordWrap(True)
        # 允许标签比其内容更窄，避免 minimumSizeHint 把窗口撑宽
        self.shouye_welcome.setMinimumSize(0, 0)
        self._fit_title()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._fit_title()

    def _fit_title(self):
        # 按窗口实际可用宽度缩放标题字号，使其完整显示且不强制窗口变宽
        label = self.shouye_welcome
        # 使用窗口宽度（而非标签当前宽度）作为基准，避免被已撑大的尺寸正反馈
        win = self.window()
        target = win.width() if win is not None else 800
        avail = max(200, min(target, 800) - 30)
        try:
            fm = QFontMetrics(QFont("Times New Roman", _TITLE_BASE_PT))
            text_w = fm.horizontalAdvance(_TITLE_TEXT)
        except Exception:
            text_w = 0
        if text_w <= 0:
            return
        pt = int(_TITLE_BASE_PT * avail / text_w)
        pt = max(14, min(_TITLE_BASE_PT, pt))
        new_html = self._title_html.replace("font-size:50pt", "font-size:{}pt".format(pt))
        if new_html != label.text():
            label.setText(new_html)
