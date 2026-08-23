import os
import sys
import time

from PySide6.QtCore import QCoreApplication, QUrl, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPixmap
from PySide6.QtWidgets import QApplication, QSplashScreen

QCoreApplication.setOrganizationName("CalculusCalculator")
QCoreApplication.setApplicationName("CalculusCalculator")

def make_splash_pixmap(theme='light'):
    """生成启动画面位图（品牌色背景 + 程序名）。"""

    bg = "#7a45c4" if theme == 'dark' else "#2c5f8a"
    pm = QPixmap(560, 300)
    pm.fill(QColor(bg))
    painter = QPainter(pm)
    painter.setRenderHint(QPainter.TextAntialiasing, True)
    painter.setPen(QColor("#ffffff"))
    font = QFont("Microsoft YaHei", 24, QFont.Bold)
    painter.setFont(font)
    painter.drawText(pm.rect().adjusted(0, 30, 0, 0),
                     Qt.AlignHCenter | Qt.AlignVCenter,
                     "CalculusCalculator")
    font2 = QFont("Microsoft YaHei", 13)
    painter.setFont(font2)
    painter.drawText(pm.rect().adjusted(0, -70, 0, 0),
                     Qt.AlignHCenter | Qt.AlignVCenter,
                     "微积分计算器")
    painter.end()
    return pm


def preinit_webengine():
    """预初始化 QWebEngine 进程，避免首次打开积木编辑器时闪退。"""

    try:
        from PySide6.QtWebEngineWidgets import QWebEngineView

        view = QWebEngineView()
        view.resize(320, 240)
        state = {"done": False}

        def _on_loaded(*_args):
            del _args
            state["done"] = True

        view.loadFinished.connect(_on_loaded)
        view.load(QUrl("about:blank"))
        deadline = time.monotonic() + 15
        while not state["done"] and time.monotonic() < deadline:
            QCoreApplication.processEvents()
            QCoreApplication.processEvents()
        view.close()
        view.deleteLater()
        QCoreApplication.processEvents()
        return True
    except Exception:
        return False


def boot_step(splash, text):
    """在启动画面上更新进度文本。"""

    if splash is not None:
        splash.showMessage(text, Qt.AlignHCenter | Qt.AlignBottom,
                           QColor("#ffffff"))
        QCoreApplication.processEvents()


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

    # 3. 提前并应用语言（在启动画面显示前安装翻译器）
    from core.settings import apply_language, load_saved_language
    apply_language(load_saved_language())

    # 4. 启动画面
    from core.settings import current_theme
    splash = QSplashScreen(make_splash_pixmap(current_theme()), Qt.WindowStaysOnTopHint)
    splash.show()

    # 5. 应用界面主题
    boot_step(splash, QCoreApplication.translate("Boot", "正在应用界面主题…"))
    from core.settings import load_saved_theme
    load_saved_theme()

    # 6. 预初始化 QWebEngine 进程
    boot_step(splash, QCoreApplication.translate("Boot", "正在初始化浏览器内核…"))
    preinit_webengine()

    # 7. 创建主窗口
    boot_step(splash, QCoreApplication.translate("Boot", "正在创建主窗口…"))
    from ui.main import MainWindow
    mainWindow = MainWindow(file_arg=open_file_arg())

    # 8. 启动时通过命令行参数传入的存档文件（如文件管理器双击 .cca 文件）
    if open_file_arg() is not None:
        boot_step(splash, QCoreApplication.translate("Boot", "正在加载启动存档…"))
        from functions.saves import load_from_path
        try:
            load_from_path(mainWindow, startup_file)
        except Exception:
            pass
    else:
        boot_step(splash, QCoreApplication.translate("Boot", "正在完成启动…"))

    # 9. 启动完成：显示主窗口
    splash.finish(mainWindow)
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
