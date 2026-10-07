import re

from ui.ui_shouye import *
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QFont, QFontMetrics

# 标题基准文本（用于按实际可用宽度缩放，避免单行过长把窗口撑宽）
_TITLE_TEXT = "CalculusCalculator"
_TITLE_SIZE_RE = re.compile(r"(font-size:)(\d+)(pt)")

# 首页背景渐变（对角线，左上→右下），与 v2 首页一致：
# 浅色模式蓝→白；深色模式深紫→黑。
_HOME_GRADIENT = {
    'light': 'background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 120, 240, 255), stop:1 rgba(255, 255, 255, 255));',
    'dark': 'background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(140, 82, 220, 255), stop:1 rgba(0, 0, 0, 255));',
}

# 深色模式下的文字配色替换（键为 .ui 中使用的浅色值）
_DARK_COLORS = {
    '#000000': '#ffffff',
}


def _swap_colors(html, dark):
    """把富文本中的浅色配色替换为深色配色。"""

    if not dark:
        return html
    for light, dark_color in _DARK_COLORS.items():
        html = html.replace(light, dark_color)
    return html


class Shouye(QWidget, Ui_shouye):
    """首页：标题横幅。

    界面为单个 QLabel，富文本只用 Qt 富文本引擎支持的基本标签，不依赖
    QWebEngineView；深色主题下背景渐变与文字颜色随之切换。
    """

    def __init__(self, parent, fs):
        super(Shouye, self).__init__(parent)
        self.setupUi(self)
        # 记录当前主题：语言切换时据此重新上色（self.parent 是 QWidget 的方法）
        self._theme = getattr(parent, 'theme', 'light')
        # .ui 中保存的是浅色配色原文，按当前主题生成实际使用的富文本
        self._base_html = self.shouye_welcome.text()
        # 允许标签比其内容更窄，避免 minimumSizeHint 把窗口撑宽
        self.shouye_welcome.setMinimumSize(0, 0)
        self._apply_theme(self._theme)

    def retranslateUi(self, widget):
        """语言切换后重新取 .ui 文案并按当前主题重新上色。"""

        super().retranslateUi(widget)
        if not hasattr(self, '_base_html'):
            return
        self._base_html = self.shouye_welcome.text()
        self._apply_theme(self._theme)

    def set_theme(self, theme):
        """按主题切换首页背景渐变与文字颜色。"""

        self._theme = theme
        self._apply_theme(theme)

    def _apply_theme(self, theme):
        """套用主题：背景渐变 + 文字配色。"""

        dark = theme == 'dark'
        self.shouye_welcome.setStyleSheet(_HOME_GRADIENT['dark' if dark else 'light'])
        self._title_html = _swap_colors(self._base_html, dark)
        self._fit_title()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._fit_title()

    def _fit_title(self):
        """按窗口实际可用宽度缩放标题字号，使其完整显示且不强制窗口变宽。"""

        label = self.shouye_welcome
        # 使用窗口宽度（而非标签当前宽度）作为基准，避免被已撑大的尺寸正反馈
        win = self.window()
        target = win.width() if win is not None else 800
        avail = max(200, min(target, 800) - 30)
        try:
            fm = QFontMetrics(QFont("Times New Roman", 75))
            text_w = fm.horizontalAdvance(_TITLE_TEXT)
        except Exception:
            text_w = 0
        if text_w <= 0:
            return
        pt = max(14, min(75, int(75 * avail / text_w)))

        def resize_title(match):
            return match.group(1) + str(pt) + match.group(3)

        new_html = _TITLE_SIZE_RE.sub(resize_title, self._title_html, count=1)
        if new_html != label.text():
            label.setText(new_html)