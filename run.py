import os
import sys
import time

from PySide6.QtCore import QCoreApplication, QEventLoop, QTimer, QUrl, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPixmap
from PySide6.QtWidgets import QApplication, QSplashScreen

QCoreApplication.setOrganizationName("CalculusCalculator")
QCoreApplication.setApplicationName("CalculusCalculator")

t0 = time.time()

# 启动画面的静态资源：尺寸/配色集中定义，位图按主题缓存（见 make_splash_pixmap）。
SPLASH_SIZE = (560, 300)
SPLASH_BG = {"dark": "#7a45c4", "light": "#2c5f8a"}
SPLASH_TEXT_COLOR = "#ffffff"
# 上一次写入启动画面的文本，用于跳过重复的重绘（见 boot_step）。
_BOOT_LAST = {"splash": None, "text": None}
# 已生成过的启动画面位图：{theme: QPixmap}
_SPLASH_PIXMAPS = {}


def make_splash_pixmap(theme='light'):
    """生成启动画面位图（品牌色背景 + 程序名）。

    同一主题的位图只绘制一次并缓存：首次绘制的主要开销是字体库初始化，
    之后重复调用（主题刷新、重启启动画面等）直接复用结果，仅返回共享数据的
    QPixmap 副本引用，省去重新排版与光栅化。
    """

    pm = _SPLASH_PIXMAPS.get(theme)
    if pm is not None and not pm.isNull():
        return pm

    bg = SPLASH_BG.get(theme, SPLASH_BG['light'])
    pm = QPixmap(*SPLASH_SIZE)
    pm.fill(QColor(bg))
    painter = QPainter(pm)
    painter.setRenderHint(QPainter.TextAntialiasing, True)
    painter.setPen(QColor(SPLASH_TEXT_COLOR))
    painter.setFont(QFont("Microsoft YaHei", 24, QFont.Bold))
    painter.drawText(pm.rect().adjusted(0, 30, 0, 0),
                     Qt.AlignHCenter | Qt.AlignVCenter,
                     "CalculusCalculator")
    painter.setFont(QFont("Microsoft YaHei", 13))
    painter.drawText(pm.rect().adjusted(0, -70, 0, 0),
                     Qt.AlignHCenter | Qt.AlignVCenter,
                     "微积分计算器")
    painter.end()
    _SPLASH_PIXMAPS[theme] = pm
    return pm


def preinit_webengine():
    """预初始化 QWebEngine 进程，避免首次打开积木编辑器时闪退。

    用 QEventLoop + 定时超时替代 while + processEvents() 的轮询等待：
    等待期间线程挂起、不占 CPU（旧写法会持续空转，与正在启动的浏览器进程
    争抢 CPU，反而拖慢进程拉起），并保留 15 秒的超时上限。

    返回 loadFinished 是否触发（True 表示内核已就绪）。
    """

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
        timer.start(15000)
        view.load(QUrl("about:blank"))
        loop.exec()
        timer.stop()
        view.loadFinished.disconnect(_on_loaded)
        view.close()
        view.deleteLater()
        QCoreApplication.processEvents()
        return state["done"]
    except Exception:
        return False


def boot_step(splash, text):
    """在启动画面上更新进度文本。

    - 文本与上次相同时直接返回，跳过 showMessage 触发的整幅重绘；
    - processEvents 限定 50ms 上限并排除用户输入事件，避免启动阶段被
      事件流拖住，或重入尚未初始化完成的界面。
    """

    if splash is None:
        return
    if _BOOT_LAST["splash"] is splash and _BOOT_LAST["text"] == text:
        return
    _BOOT_LAST["splash"] = splash
    _BOOT_LAST["text"] = text
    splash.showMessage(text, Qt.AlignHCenter | Qt.AlignBottom,
                       QColor(SPLASH_TEXT_COLOR))
    QCoreApplication.processEvents(QEventLoop.ExcludeUserInputEvents, 50)


def open_file_arg():
    """返回命令行参数中的存档文件路径（.cca / .json），无则返回 None。"""

    for arg in sys.argv[1:]:
        low = arg.lower()
        if low.endswith(".cca") or low.endswith(".json"):
            return arg
    return None


def main():

    # 1. 开启共享 OpenGL 上下文
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts, True)

    # 2. 创建 QApplication
    app = QApplication(sys.argv)
    print(time.time() - t0, "QApplication Created.")

    # 3. 提前并应用语言（在启动画面显示前安装翻译器）
    from core.settings import apply_language, load_saved_language
    apply_language(load_saved_language())
    print(time.time() - t0, "Language Applied.")

    # 4. 启动画面
    from core.settings import current_theme
    print(time.time() - t0, "Theme Imported.")
    splash_pixmap = make_splash_pixmap(current_theme())
    print(time.time() - t0, "Pixmap Created.")
    splash = QSplashScreen(splash_pixmap, Qt.WindowStaysOnTopHint)
    print(time.time() - t0, "Splash Window Created.")
    splash.show()
    print(time.time() - t0, "Splash Window Showed.")

    # 5. 应用界面主题
    boot_step(splash, QCoreApplication.translate("Boot", "正在应用界面主题…"))
    from core.settings import load_saved_theme
    print(time.time() - t0, "Theme Loader Imported.")
    load_saved_theme()
    print(time.time() - t0, "Theme Applied.")

    # 6. 预初始化 QWebEngine 进程
    boot_step(splash, QCoreApplication.translate("Boot", "正在初始化浏览器内核…"))
    preinit_webengine()
    print(time.time() - t0, "WebEngine Preinitialized.")

    # 7. 创建主窗口
    boot_step(splash, QCoreApplication.translate("Boot", "正在创建主窗口…"))
    from ui.main import MainWindow
    print(time.time() - t0, "Main Window Imported.")
    mainWindow = MainWindow(file_arg=open_file_arg())
    print(time.time() - t0, "Main Window Created.")

    # 8. 启动时通过命令行参数传入的存档文件（如文件管理器双击 .cca 文件）
    if open_file_arg() is not None:
        boot_step(splash, QCoreApplication.translate("Boot", "正在加载启动存档…"))
        from functions.saves import load_from_path
        try:
            load_from_path(mainWindow, open_file_arg())
        except Exception:
            pass
    else:
        boot_step(splash, QCoreApplication.translate("Boot", "正在完成启动…"))

    # 9. 启动完成：显示主窗口
    splash.finish(mainWindow)
    print(time.time() - t0, "Splash Window Closed.")
    mainWindow.show()
    print(time.time() - t0, "Main Window Showed.")
    mainWindow.setup()
    print(time.time() - t0, "Main Window Slot Function Bound.")
    print("Wait for Main Window Being Closed...")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
