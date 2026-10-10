import json
import os
from PySide6.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QMessageBox
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, QEventLoop, QCoreApplication


class MathLiveDialog(QDialog):
    """使用 MathLive 的公式输入对话框（缩小尺寸，键盘始终显示）

    LaTeX 的花括号补全在页面脚本中完成（见 math_input.html 的 normalizeLatex）：
    MathLive 取值时会把单字符参数写成 \\sqrt3、\\frac12 这类省略花括号的形式，
    sympify 无法解析。页面显示与回填都使用补全后的结果。
    """
    def __init__(self, parent=None, title="", initial_text="",
                 toolbar_groups=None, show_output=True, zoom=1.0):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        # 缩小对话框尺寸，类似普通提示框
        self.resize(580, 480)   # 宽度适中，高度含键盘
        self._result_latex = ""

        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(8, 8, 8, 8)

        # 首次打开时确保 WebEngine 内核已就绪（每进程至多等待一次；
        # 已由积木编辑器预初始化过则立即返回，无额外开销）
        from core.webengine import ensure_webengine_ready
        ensure_webengine_ready()

        self.webview = QWebEngineView()
        # 按当前语言加载公式编辑器页面（zh_CN / en_US）
        try:
            from core.settings import current_language
            html_name = "math_input_en.html" if current_language() == "en_US" \
                else "math_input.html"
        except Exception:
            html_name = "math_input.html"
        html_path = os.path.join(os.path.dirname(__file__), html_name)
        self.webview.setUrl(QUrl.fromLocalFile(html_path))
        # 让 WebView 占据大部分空间，但保留按钮区域
        layout.addWidget(self.webview, stretch=1)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self._on_ok)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self._initial_text = initial_text
        self.webview.loadFinished.connect(self._on_load_finished)

    def _on_load_finished(self):
        """页面加载完成后设置初始公式"""
        if self._initial_text:
            # LaTeX 中的反斜杠必须转义，否则 \sqrt 在 JS 字符串里会被当作转义序列
            # 丢掉反斜杠，MathLive 就会把 \sqrt{3} 显示成 sqrt3
            js = 'document.getElementById("mf").value = %s;' % json.dumps(self._initial_text)
            self.webview.page().runJavaScript(js)

    def _on_ok(self):
        """点击确定时获取公式并关闭对话框"""
        loop = QEventLoop()
        result = [None]

        def callback(value):
            result[0] = value
            loop.quit()

        # mathInputValue() 返回补全花括号后的 LaTeX
        self.webview.page().runJavaScript(
            'window.mathInputValue ? window.mathInputValue() : "";',
            callback
        )
        loop.exec()
        self._result_latex = result[0] if result[0] is not None else ""
        self.accept()

    def result_latex(self):
        return self._result_latex


def open_formula_dialog(parent, is_return = False):
    """
    打开公式输入对话框，与原有接口完全兼容。
    获取的 LaTeX 会通过 sympify 转换为表达式再设置回去。
    """
    from sympy import latex
    from core.sympify import sympify

    initial = parent.text() if hasattr(parent, 'text') else ""
    try:
        initial_latex = latex(sympify(initial, {}))
    except Exception:
        initial_latex = ""

    dlg = MathLiveDialog(
        parent=parent,
        title=QCoreApplication.translate("MainWindow", "插入公式"),
        initial_text=initial_latex,
        toolbar_groups=["struct", "greek", "edit", "operators", "functions"],
        show_output=True,
        zoom=1.2
    )

    if is_return:
        if dlg.exec() == QDialog.Accepted:
            latex_str = dlg.result_latex()
            try:
                return str(sympify('$' + latex_str, {}))
            except Exception as e:
                QMessageBox(parent=parent, title=QCoreApplication.translate("math_input", f"Sympy 转换失败: {e}"), buttons=QMessageBox.StandardButton.Ok)
                return latex_str

    else:
        if dlg.exec() == QDialog.Accepted:
            latex_str = dlg.result_latex()
            try:
                expr = sympify('$' + latex_str, {})
                parent.setText(str(expr))
            except Exception as e:
                print(f"SymPy 转换失败: {e}")
                parent.setText(latex_str)