import io
import json
import os
import sys

from PySide6.QtCore import QCoreApplication, QObject, QUrl, Signal, Slot
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWidgets import (QApplication, QDialog, QDialogButtonBox,
                               QListWidget, QVBoxLayout, QWidget)

from ui.ui_blockly import Ui_blockly


class PythonBridge(QObject):
    """在 Python 与页面 JavaScript 之间桥接代码执行、输入读取与结果回传。"""

    pythonResult = Signal(str)
    # 对话框结果回传（避免带返回值的 slot 在 WebChannel 中的兼容性问题）
    cachePicked = Signal(str)
    formulaResult = Signal(str)

    def __init__(self, fs):
        super().__init__()
        self.fs = fs
        self.page = None
        self.inputs = {}
        # 主窗体引用（用于共享缓存区 main.cache）
        self.main = None
        # 积木编辑器工作区状态（JS 端实时同步，供存档 JSON 写入）
        self.state = ''

    def setPage(self, page):
        self.page = page

    def _dialog_parent(self):
        """返回可作为模态对话框父窗口的 QWidget（优先顶层主窗体）。"""
        if self.main is not None:
            return self.main
        if self.page is not None:
            try:
                return self.page.view()
            except Exception:
                pass
        return None

    @Slot(str)
    def copyText(self, text):
        """将文本写入系统剪贴板。

        供积木编辑器"复制代码"按钮使用：QtWebEngine 中浏览器的
        Clipboard API / execCommand('copy') 常因权限或用户手势限制而失效，
        直接通过 QClipboard 写入系统剪贴板最可靠。
        """
        QApplication.clipboard().setText(text or '')

    # ------------------------------------------------------------------ #
    # 缓存区与公式编辑器（与原生文本框共用 main.cache）
    # ------------------------------------------------------------------ #
    @Slot(result=list)
    def getCache(self):
        """返回缓存区列表（与原生文本框共用 main.cache）。"""
        return list(self.main.cache) if self.main is not None else []

    @Slot(str)
    def saveToCache(self, text):
        """将文本存入缓存区头部（与原生文本框共用 main.cache）。"""
        if self.main is None or not text:
            return
        if text in self.main.cache:
            self.main.cache.remove(text)
        self.main.cache.insert(0, text)

    @Slot()
    def openCacheDialog(self):
        """打开缓存区对话框；选中结果通过 cachePicked 信号回传 JS。
        延迟到 WebChannel 调用栈之外再 exec，避免嵌套事件循环影响渲染。"""
        from PySide6.QtCore import QTimer
        QTimer.singleShot(0, self._open_cache_dialog_impl)

    def _open_cache_dialog_impl(self):
        items = self.getCache()
        dlg = QDialog(self._dialog_parent())
        dlg.setWindowTitle(QCoreApplication.translate(
            'blockly', '缓存区（双击选择）'))
        dlg.resize(500, 400)
        layout = QVBoxLayout(dlg)
        list_widget = QListWidget()
        if items:
            list_widget.addItems(items)
        else:
            list_widget.addItem(QCoreApplication.translate(
                'blockly', '[暂无缓存项]'))
        list_widget.setCurrentRow(0)
        layout.addWidget(list_widget)

        result = ['']

        def on_pick(item):
            if item is not None:
                result[0] = item.text()
            dlg.accept()

        list_widget.itemDoubleClicked.connect(on_pick)
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: on_pick(list_widget.currentItem()))
        buttons.rejected.connect(dlg.reject)
        layout.addWidget(buttons)
        dlg.exec()
        self.cachePicked.emit(result[0])

    @Slot(str)
    def openFormulaDialog(self, initial=''):
        """打开 MathLive 公式编辑器对话框；结果通过 formulaResult 信号回传 JS。
        延迟到 WebChannel 调用栈之外再 exec，避免嵌套 WebEngine 渲染空白。"""
        from PySide6.QtCore import QTimer
        QTimer.singleShot(0, lambda: self._open_formula_dialog_impl(initial))

    def _open_formula_dialog_impl(self, initial=''):
        from math_input.math_input import MathLiveDialog
        from core.sympify import sympify
        from sympy import latex
        try:
            initial_latex = latex(sympify(initial, {}))
        except Exception:
            initial_latex = ''
        dlg = MathLiveDialog(
            parent=self._dialog_parent(),
            title=QCoreApplication.translate('blockly', '插入公式'),
            initial_text=initial_latex,
            toolbar_groups=['struct', 'greek', 'edit', 'operators', 'functions'],
            show_output=True,
            zoom=1.2
        )
        picked = initial
        if dlg.exec() == QDialog.Accepted:
            latex_str = dlg.result_latex()
            try:
                picked = str(sympify('$' + latex_str, {}))
            except Exception:
                picked = latex_str
        self.formulaResult.emit(picked)

    def _runJavaScript(self, script):
        if self.page is not None:
            try:
                self.page.runJavaScript(script)
                return True
            except Exception:
                pass
        return False

    @Slot(str)
    def setInputs(self, jsonText):
        try:
            self.inputs = json.loads(jsonText)
        except Exception:
            self.inputs = {}

    @Slot(result=list)
    def getFunctions(self):
        """返回已定义函数的名称列表（供积木编辑器动态下拉使用）。"""
        return list(self.fs.keys())

    @Slot(str)
    def setState(self, jsonText):
        """JS 端将工作区序列化结果同步到 Python，供存档 JSON 写入。"""
        self.state = jsonText

    @Slot(str)
    def setFunctionNames(self, jsonNames):
        """同步"定义函数"积木中的函数名（仅名字）到积木编辑器的独立 fs。

        已存在（含已运行定义的完整函数体）的项保留原样，
        新名字添加占位，不再出现的名字移除。
        """
        try:
            names = json.loads(jsonNames)
        except Exception:
            return
        new_fs = {}
        for name in names:
            if name in self.fs:
                new_fs[name] = self.fs[name]  # 保留已有（可能含完整定义）
            else:
                new_fs[name] = [name, '', '', '']  # 占位：仅名字
        self.fs = new_fs

    def get_input(self, name):
        return self.inputs.get(name, '')

    def py_output(self, name, value):
        # 将输出以结构化参数回传页面，由页面的 addOutput(name, value) 渲染。
        # 携带 {text, latex} 标记：text 为显示文本，latex 表示该文本是否为
        # 可靠的 LaTeX 公式（由 _format_value 判定），避免 JS 端启发式误判
        # （例如把含 "^" 的普通文本误当作 LaTeX 渲染）。
        text, is_latex = self._format_value(value)
        payload = json.dumps({'text': text, 'latex': is_latex})
        if not self._runJavaScript(
            'window.addOutput({}, {});'.format(json.dumps(name), payload)
        ):
            # 页面不可用时的回退：以纯文本形式展示。
            self._runJavaScript(
                'displayPythonResult({});'.format(json.dumps('输出 {}: {}'.format(name, text)))
            )
        return value

    @staticmethod
    def _format_value(value):
        """将任意值转为 (显示文本, 是否为 LaTeX) 的二元组。

        - sympy 对象 / 可解析为数学表达式的字符串 → (latex_str, True)
        - 纯文本 / 无法解析的字符串 → (原样文本, False)
        - 容器（dict/list/tuple/set）→ 递归拼接，任一成员为 LaTeX 则整体标记为 LaTeX
        """
        if value is None:
            return ('', False)
        try:
            from sympy import latex as _latex, sympify as _sympify
        except Exception:
            _latex = None
            _sympify = None
        # 递归处理容器（方程组/三角形解等）。
        if isinstance(value, dict):
            items = [(k, PythonBridge._format_value(v)) for k, v in value.items()]
            parts = ['{}={}'.format(k, t) for k, (t, _) in items]
            return (r',\ '.join(parts), any(f for _, f in items))
        if isinstance(value, (list, tuple, set)):
            items = [PythonBridge._format_value(v) for v in value]
            parts = [t for t, _ in items]
            return (r'\ \ \ '.join(parts), any(f for _, f in items))
        # 字符串：尝试 sympify+latex 转为 LaTeX；纯文本/非数学字符串原样返回（非 LaTeX）。
        if isinstance(value, str):
            if _sympify is not None and _latex is not None and value.strip():
                try:
                    return (_latex(_sympify(value)), True)
                except Exception:
                    pass
            return (value, False)
        # int/float/sympy 等其他数学对象 → LaTeX。
        if _latex is not None:
            try:
                return (_latex(value), True)
            except Exception:
                pass
        return (str(value), False)

    # ------------------------------------------------------------------ #
    # 供 Blockly 积木调用的辅助函数（写入 eval/exec 环境）。
    # ------------------------------------------------------------------ #
    def _define_func(self, name, expr, domain, var):
        """定义函数：fs[name] = [名称, 表达式, 定义域, 变量]"""
        from core.sympify import sympify
        if not name or not expr:
            return '错误：函数名称和表达式不能为空'
        try:
            body = str(sympify(expr, self.fs))
        except Exception as err:
            return '错误：函数表达式无效 - {}'.format(err)
        self.fs[name] = [name, body, domain or 'Reals', var or 'x']
        return '已定义函数 {}({}) = {}'.format(name, var or 'x', body)

    def _py_simplifies(self, expr, method, zhuyuan='', huanyuan='', huanyuanshi=''):
        from functions.simplification import simplifies
        return simplifies(expr, int(method), zhuyuan or None,
                          huanyuan or None, huanyuanshi or None, self.fs)

    def _py_solve_fangchengzu(self, eqs, vars_text):
        from functions.solvers import solve_fangchengzu
        from core.sympify import sympify
        from sympy import Eq, Symbol
        eq_list = [Eq(sympify(e, self.fs), 0) for e in eqs]
        var_list = [Symbol(s.strip()) for s in vars_text.split(',') if s.strip()]
        return solve_fangchengzu(eq_list, var_list, self.fs)

    def _py_solve_budengshi(self, lhs, op, rhs, var, domain='Reals'):
        from functions.solvers import solve_budengshi
        from core.sympify import sympify
        from sympy import Rel
        rel = Rel(sympify(lhs, self.fs), sympify(rhs, self.fs), op)
        return solve_budengshi(rel, var, domain or 'Reals', self.fs)

    def _py_solve_budengshizu(self, items, var):
        from functions.solvers import solve_budengshizu
        from core.sympify import sympify
        from sympy import Rel, Symbol
        rels = [Rel(sympify(l, self.fs), sympify(r, self.fs), o)
                for (l, o, r) in items]
        return solve_budengshizu(rels, Symbol(var), self.fs)

    def _py_solve_triangle(self, *conds):
        from functions.solvers import solve_sanjiaoxing
        from core.sympify import sympify
        angles = {}
        sides = {}
        mapping = {'A': ('A', angles), 'B': ('B', angles), 'C': ('C', angles),
                   'a': ('a', sides), 'b': ('b', sides), 'c': ('c', sides)}
        for kind, val in conds:
            key = (kind or '').strip()
            if not key or key not in mapping or not val:
                continue
            target_key, target = mapping[key]
            target[target_key] = sympify(val, self.fs)
        return solve_sanjiaoxing(angles, sides, self.fs)

    def _py_calc(self, expr):
        from core.sympify import sympify
        from sympy import radsimp
        return radsimp(sympify(expr, self.fs, is_simplify=True))

    def _py_func_value(self, name, arg=''):
        """计算已定义函数的值；arg 为空时返回函数表达式本身。"""
        from core.sympify import sympify
        from sympy import symbols
        if not name or name not in self.fs:
            return '未定义函数: {}'.format(name or '?')
        body = self.fs[name][1]
        var = self.fs[name][3]
        expr = sympify(body, self.fs)
        if not arg:
            return expr
        return expr.subs(symbols(var), sympify(arg, self.fs))

    @Slot(str)
    def executePython(self, code):
        env = {
            'fs': self.fs,
            'get_input': self.get_input,
            'py_output': self.py_output,
            'define_func': self._define_func,
            'py_simplifies': self._py_simplifies,
            'py_solve_fangchengzu': self._py_solve_fangchengzu,
            'py_solve_budengshi': self._py_solve_budengshi,
            'py_solve_budengshizu': self._py_solve_budengshizu,
            'py_solve_triangle': self._py_solve_triangle,
            'py_calc': self._py_calc,
            'py_func_value': self._py_func_value,
        }
        error_text = None

        try:
            # 优先按单表达式执行（生成器大多产出表达式）。
            eval(compile(code, '<blockly>', 'eval'), env)
        except SyntaxError:
            # 多语句代码：捕获标准输出，并捕获运行异常。
            out_buffer = io.StringIO()
            old_stdout = sys.stdout
            try:
                sys.stdout = out_buffer
                exec(code, env)
            except Exception as err:
                error_text = '执行错误: {}'.format(err)
            finally:
                sys.stdout = old_stdout
        except Exception as err:
            error_text = '执行错误: {}'.format(err)

        # 仅在出错时在 resultMessage 显示提示；成功时结果已在右侧输出表格中。
        if error_text:
            if not self._runJavaScript('displayPythonResult({});'.format(json.dumps(error_text))):
                self.pythonResult.emit(error_text)


class Blockly(QWidget, Ui_blockly):
    def __init__(self, parent, fs):
        super().__init__(parent)
        self.setupUi(self)
        # 积木编辑器使用独立于原生标签页的 fs（与主窗体共享 fs 互不影响）。
        # 函数名由"定义函数"积木放置/改名时通过 setFunctionNames 实时同步，
        # 完整定义在运行"定义函数"积木时写入。
        del fs  # 忽略传入的共享 fs
        self.fs = {}

        # 主窗体引用：缓存区与原生文本框共用 main.cache
        self.main = None
        w = self.parentWidget()
        while w is not None:
            if hasattr(w, 'cache') and hasattr(w, 'fs'):
                self.main = w
                break
            w = w.parentWidget()

        self.index_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'blockly', 'index.html')
        )

        self.bridge = PythonBridge(self.fs)
        self.bridge.main = self.main
        self.bridge.setPage(self.view.page())

        self.channel = QWebChannel(self.view.page())
        self.channel.registerObject('pyBridge', self.bridge)
        self.view.page().setWebChannel(self.channel)

        # 存档恢复：页面加载完成后再注入积木编辑器状态
        self._pending_state = None
        self._page_loaded = False
        self.view.loadFinished.connect(self._on_page_loaded)

        # 按当前语言与主题加载积木编辑器（zh_CN/en_US + light/dark）。
        # 注意：必须用 QUrl.setQuery 附加参数；直接拼接 "?lang=..." 会让
        # WebEngine 把 query 当作文件名的一部分而 ERR_FILE_NOT_FOUND。
        from core.settings import current_language, current_theme
        lang = current_language()
        theme = current_theme()
        self._current_lang = 'en_US' if lang == 'en_US' else 'zh_CN'
        page_url = QUrl.fromLocalFile(self.index_path)
        page_url.setQuery('lang={}&theme={}'.format(
            self._current_lang,
            'dark' if theme == 'dark' else 'light'))
        self.view.load(page_url)

    # ------------------------------------------------------------------ #
    # 存档支持：状态序列化结果随存档 JSON 保存/恢复
    # ------------------------------------------------------------------ #
    @property
    def state(self):
        """积木编辑器工作区序列化结果（JS 端实时同步到 bridge）。"""
        return self.bridge.state

    def restore_state(self, json_text):
        """从存档恢复积木编辑器内容；页面加载完成后执行。"""
        self._pending_state = json_text or ''
        self._flush_pending_state()

    def set_theme(self, theme):
        """按需切换积木编辑器页面主题（设置页"应用"时由主窗体调用）。"""
        t = 'dark' if theme == 'dark' else 'light'
        try:
            self.view.page().runJavaScript(
                'window.applyBlocklyTheme({});'.format(json.dumps(t)))
        except Exception:
            pass

    def set_language(self, lang):
        """按需切换积木编辑器页面语言（设置页"应用"时由主窗体调用）。

        通过带新语言参数重新加载页面来切换：前端在加载时依据 URL 的
        lang 参数加载对应的 Blockly 语言包与自定义积木译文，从而完整
        切换工具箱分类名、内置积木文本与界面文案。重载前先保存当前工作
        区状态，页面加载完成后再恢复，避免用户积木丢失。
        """
        lang_code = 'en_US' if lang == 'en_US' else 'zh_CN'
        if lang_code == getattr(self, '_current_lang', None):
            return
        self._current_lang = lang_code
        if getattr(self, 'bridge', None) is not None:
            self._pending_state = self.bridge.state
        self._page_loaded = False
        try:
            from core.settings import current_theme
            theme = 'dark' if current_theme() == 'dark' else 'light'
        except Exception:
            theme = 'light'
        page_url = QUrl.fromLocalFile(self.index_path)
        page_url.setQuery('lang={}&theme={}'.format(lang_code, theme))
        self.view.load(page_url)

    def _on_page_loaded(self, *_args):
        del _args
        self._page_loaded = True
        self._flush_pending_state()

    def _flush_pending_state(self):
        if not self._page_loaded or not self._pending_state:
            return
        try:
            self.view.page().runJavaScript(
                'window.loadBlocklyState({});'.format(json.dumps(self._pending_state)))
        except Exception:
            pass
        self._pending_state = None
