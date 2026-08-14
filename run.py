import os
import sys
import time

# 在导入 QtWebEngine 相关模块前设置 Chromium 启动参数：
# CalculateNativeWinOcclusion 为 Windows 原生窗口遮挡计算，禁用它可减少
# 无谓的遮挡事件与重绘，加快窗口显示与整体启动。
os.environ.setdefault(
    'QTWEBENGINE_CHROMIUM_FLAGS',
    '--disable-features=CalculateNativeWinOcclusion'
)
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --disable-dev-shm-usage --no-sandbox"
os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = ""

from PySide6.QtCore import QCoreApplication, QUrl, Qt

# 禁用不必要的 WebEngine 功能（如拼写检查、翻译等）
QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_UseSoftwareOpenGL)

# 必须在导入任何读取 settings.json 的模块（core.settings）之前设置组织/应用名，
# 否则 QStandardPaths 在没有应用名时会随 QApplication 是否存在解析出不同路径，
# 导致主题/语言的“保存”与“读取”指向不同文件，设置无法跨重启持久化。
QCoreApplication.setOrganizationName("CalculusCalculator")
QCoreApplication.setApplicationName("CalculusCalculator")

from PySide6.QtGui import QColor, QFont, QPainter, QPixmap
from PySide6.QtWidgets import QApplication, QSplashScreen


def make_splash_pixmap(theme='light'):
    """生成启动画面位图（品牌色背景 + 程序名）。

    浅色模式：蓝底；深色模式：紫底（与首页深紫→黑背景一致）。
    """
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
    """预初始化 QWebEngine 进程，避免首次打开积木编辑器时闪退。

    创建一个隐藏的 QWebEngineView 并加载 about:blank，等待加载完成，
    提前完成 WebEngine 库加载与渲染进程启动，随后销毁该视图。
    """
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
    """返回命令行参数中的存档文件路径（.cca / .json），无则返回 None。

    用于在文件管理器中双击 .cca 存档（已与程序关联）时，直接加载该存档。
    """
    for arg in sys.argv[1:]:
        low = arg.lower()
        if low.endswith(".cca") or low.endswith(".json"):
            return arg
    return None


def main():
    # WebEngine 要求在 QApplication 创建前开启共享 OpenGL 上下文
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts, True)

    app = QApplication(sys.argv)

    # 提前加载并应用语言（在启动画面显示前安装翻译器），
    # 保证启动画面上展示的各进度文案都能按用户所选语言正确翻译。
    from core.settings import apply_language, load_saved_language
    apply_language(load_saved_language())

    # 启动画面（显示启动进度）
    from core.settings import current_theme
    splash = QSplashScreen(make_splash_pixmap(current_theme()), Qt.WindowStaysOnTopHint)
    splash.show()

    # 1. 写入版本信息（版本号未变化时跳过写盘，避免拖慢启动）
    boot_step(splash, QCoreApplication.translate("Boot", "正在写入版本信息…"))
    from core.settings import save_version, APP_VERSION
    save_version(APP_VERSION)

    # 2. 应用界面主题
    boot_step(splash, QCoreApplication.translate("Boot", "正在应用界面主题…"))
    from core.settings import load_saved_theme
    load_saved_theme()

    # 3. 预初始化 QWebEngine 进程
    boot_step(splash, QCoreApplication.translate("Boot", "正在初始化浏览器内核…"))
    preinit_webengine()

    # 4. 导入计算功能模块
    boot_step(splash, QCoreApplication.translate("Boot", "正在导入计算功能模块…"))
    from functions import (  # noqa: F401  触发核心功能模块加载
        derivative, integral, solvers, simplification,
        planes, solids, saves,
    )

    # 5. 创建主窗口
    boot_step(splash, QCoreApplication.translate("Boot", "正在创建主窗口…"))
    from ui.main import MainWindow
    mainWindow = MainWindow()

    # 启动时通过命令行参数传入的存档文件（如文件管理器双击 .cca 文件）
    startup_file = open_file_arg()

    # 7. 首次启动引导：无设置文件或“是否已初始化”为否时显示引导教学。
    #    若本次启动直接打开了存档，则跳过引导，直接加载存档。
    from core.settings import load_initialized
    if not load_initialized() and startup_file is None:
        # 先收起启动画面，再以模态显示引导，避免遮挡
        splash.finish(mainWindow)
        mainWindow.show_guide()
    else:
        splash.finish(mainWindow)

    # 直接加载命令行传入的存档（.cca / .json 均可）
    if startup_file is not None:
        boot_step(splash, QCoreApplication.translate("Boot", "正在加载启动存档…"))
        from functions.saves import load_from_path
        try:
            load_from_path(mainWindow, startup_file)
        except Exception:
            pass
    else:
        boot_step(splash, QCoreApplication.translate("Boot", "正在完成启动…"))

    # 启动完成：显示主窗口
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
