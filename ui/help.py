from ui.ui_help import *
import resources_rc
import re
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import QUrl, QFile, QIODevice, QTextStream
from PySide6.QtGui import QPalette

# 暗色主题样式。
# 注意：Qt 富文本引擎对 <style> 中的“类型选择器”（如 th / code）支持不稳定，
# 但对“类选择器”可靠。因此这里统一使用类选择器（.hc_*），
# 并在 load_help 中通过正则给原始 HTML 的 th/td/code/.note 注入对应 class。
_DARK_STYLE = """
<style id="help-theme-style">
body { color: #e6e6e6; background-color: #202020; }
h2 { border-left: 4px solid #4aa3ff; }
.hc_th, .hc_td { border: 1px solid #5a5a5a; }
.hc_th { background-color: #3a3a3a; color: #e6e6e6; }
.hc_td { color: #e6e6e6; }
.hc_code { background-color: #3a3a3a; color: #e6e6e6; }
.note.hc_note { background-color: #4a4030; border-left: 4px solid #ffc107; color: #e6e6e6; }
a { color: #4aa3ff; }
</style>
"""

# 浅色主题样式：显式指定深色文字与白色背景，保证可读
_LIGHT_STYLE = """
<style id="help-theme-style">
body { color: #1a1a1a; background-color: #ffffff; }
</style>
"""

# 给原始 HTML 中的 th/td/code 增加主题 class（仅匹配无 class 的元素，避免重复注入）
_RE_TH = re.compile(r"<th(?=[\s>])")
_RE_TD = re.compile(r"<td(?=[\s>])")
_RE_CODE = re.compile(r"<code(?=[\s>])")
_RE_NOTE = re.compile(r'<div class="note"(?=[\s>])')


class Help(QWidget, Ui_help):
    def __init__(self, parent, fs):
        super(Help, self).__init__(parent)
        self.setupUi(self)

        self.load_help()

    def _is_dark(self):
        # 优先读取主窗口记录的当前主题；否则依据调色板推断
        mw = self.window()
        if hasattr(mw, "theme"):
            return mw.theme == "dark"
        app = QApplication.instance()
        if app is not None:
            return app.palette().color(QPalette.WindowText).lightness() > 128
        return False

    def load_help(self):
        """读取 qrc 中的 help.html，注入主题 class 与适配样式后显示。"""
        file = QFile(u":/help.html")
        if not file.open(QIODevice.ReadOnly | QIODevice.Text):
            # 资源读取失败时回退到原始 setSource 行为
            self.textBrowser.setSource(QUrl(u"qrc:/help.html"))
            return
        html = QTextStream(file).readAll()
        file.close()

        dark = self._is_dark()

        # 为原始元素注入主题 class，使类选择器样式生效
        html = _RE_TH.sub('<th class="hc_th"', html)
        html = _RE_TD.sub('<td class="hc_td"', html)
        html = _RE_CODE.sub('<code class="hc_code"', html)
        html = _RE_NOTE.sub('<div class="note hc_note"', html)

        style = _DARK_STYLE if dark else _LIGHT_STYLE
        if "</head>" in html:
            html = html.replace("</head>", style + "</head>", 1)
        else:
            html = html + style

        # 同时设置视口背景，确保页面留白区域（body 外边距）也随主题变色
        if dark:
            self.textBrowser.setStyleSheet(
                "QTextBrowser { background-color: #202020; color: #e6e6e6; border: none; }"
            )
        else:
            self.textBrowser.setStyleSheet(
                "QTextBrowser { background-color: #ffffff; color: #1a1a1a; border: none; }"
            )

        self.textBrowser.setHtml(html)
