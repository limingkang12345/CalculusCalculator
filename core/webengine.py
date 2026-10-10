"""QWebEngine 惰性预初始化。

整个程序中只有积木编辑器（ui/blockly.py）与可视化公式输入
（math_input/math_input.py）使用 QWebEngineView。浏览器内核进程的拉起
开销较大，本模块提供"每进程至多一次"的就绪等待，供上述两处首次创建
视图前调用，把内核启动成本从程序启动阶段移到真正需要 WebEngine 的时刻。

前提：QApplication 创建前已设置 AA_ShareOpenGLContexts（run.py 负责），
否则 QWebEngineView 在部分环境下会闪退——这也是本等待逻辑最初存在的原因。
"""

from PySide6.QtCore import QCoreApplication, QEventLoop, QTimer, QUrl

# 内核是否已就绪（每进程至多完整等待一次）
_ready = False


def is_ready():
    """返回内核是否已确认就绪。"""
    return _ready


def ensure_webengine_ready(timeout_ms=15000):
    """确保 QtWebEngine 内核进程已拉起（每进程至多执行一次实际等待）。

    创建一个不显示的 QWebEngineView 加载 about:blank，用 QEventLoop +
    单发定时器等待 loadFinished（等待期间线程挂起、不占 CPU，不与正在
    启动的浏览器进程争抢资源）。

    返回 True 表示内核已就绪；重复调用直接返回 True；
    导入失败或超时返回 False，由调用方决定降级行为（页面仍可继续加载，
    只是首次加载耗时较长）。
    """
    global _ready
    if _ready:
        return True
    try:
        from PySide6.QtWebEngineWidgets import QWebEngineView

        # 视图不会显示，无需 resize：尺寸对进程拉起与 loadFinished 无影响。
        view = QWebEngineView()
        state = {"done": False}
        loop = QEventLoop()
        timer = QTimer()
        timer.setSingleShot(True)

        def _on_loaded(*_args):
            del _args
            state["done"] = True
            loop.quit()

        view.loadFinished.connect(_on_loaded)
        timer.timeout.connect(loop.quit)
        timer.start(timeout_ms)
        view.load(QUrl("about:blank"))
        loop.exec()
        timer.stop()
        try:
            view.loadFinished.disconnect(_on_loaded)
        except Exception:
            pass
        view.close()
        view.deleteLater()
        QCoreApplication.processEvents()
        _ready = state["done"]
        return _ready
    except Exception:
        return False
