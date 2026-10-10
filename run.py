import os
import sys
import time
import unicodedata
from contextlib import contextmanager

from PySide6.QtCore import QCoreApplication, QEventLoop, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPixmap
from PySide6.QtWidgets import QApplication, QWidget

QCoreApplication.setOrganizationName("CalculusCalculator")
QCoreApplication.setApplicationName("CalculusCalculator")

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


class BootSplash(QWidget):
    """轻量启动画面，提供 QSplashScreen 兼容的 showMessage()/finish() 子集。

    实测（Windows）：QSplashScreen.show() 约 1.4s，而普通 QWidget 加
    Qt.SplashScreen 窗口标志仅约 0.5s——差距来自 QSplashScreen 内部
    额外的窗口系统初始化，与位图绘制无关。故用带相同窗口标志的
    QWidget 自绘实现，视觉与原版一致（背景位图 + 底部进度文本）。
    """

    def __init__(self, pixmap):
        super().__init__(None, Qt.SplashScreen | Qt.WindowStaysOnTopHint)
        self._pixmap = pixmap
        self._message = ""
        self.setFixedSize(pixmap.size())

    def showMessage(self, text, alignment=Qt.AlignHCenter | Qt.AlignBottom,
                    color=QColor(SPLASH_TEXT_COLOR)):
        """更新底部进度文本；对齐/颜色参数仅为兼容 QSplashScreen 签名。"""
        del alignment
        if text == self._message:
            return
        self._message = text
        self._message_color = color
        self.update()

    def clearMessage(self):
        self.showMessage("")

    def paintEvent(self, event):
        del event
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self._pixmap)
        if self._message:
            painter.setPen(QColor(getattr(self, "_message_color",
                                           SPLASH_TEXT_COLOR)))
            # 底部留出少量边距，与原 QSplashScreen 的视觉位置一致
            painter.drawText(self.rect().adjusted(0, 0, 0, -16),
                             Qt.AlignHCenter | Qt.AlignBottom, self._message)

    def finish(self, widget):
        """关闭启动画面并激活主窗口（对齐 QSplashScreen.finish 行为）。"""
        self.close()
        if widget is not None:
            widget.activateWindow()
            widget.raise_()


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


class BootProfiler:
    """启动性能分析：分阶段计时，结束时输出规范化报告。

    - 基于 time.perf_counter() 高精度单调时钟；
    - stage() 上下文管理器记录每个阶段的起点与耗时；
    - report() 输出对齐表格（阶段 / 耗时 / 占比 / 累计），未计入任何
      阶段的间隙单独汇总为"其他"，便于定位开销来源；
    - 设置环境变量 CALC_BOOT_PROFILE=0 可关闭报告输出。
    """

    def __init__(self, title="启动性能分析"):
        self.title = title
        self._t0 = time.perf_counter()
        # [(名称, 起点相对偏移, 结束相对偏移)]
        self.stages = []
        self._reported = False

    @contextmanager
    def stage(self, name):
        start = time.perf_counter()
        try:
            yield
        finally:
            self.stages.append((name, start - self._t0, time.perf_counter() - self._t0))

    @staticmethod
    def _pad(name, width):
        """按显示宽度补齐（中日韩全角字符按 2 列计），保证表格对齐。"""
        gap = width - sum(2 if unicodedata.east_asian_width(c) in "WF" else 1
                          for c in name)
        return name + " " * max(gap, 2)

    def report(self):
        """输出启动耗时报告；重复调用或被环境变量关闭时静默返回。"""
        if self._reported:
            return
        self._reported = True
        if os.environ.get("CALC_BOOT_PROFILE", "1").strip().lower() in ("0", "false", "off"):
            return

        total = time.perf_counter() - self._t0
        spent = [end - start for _n, start, end in self.stages]
        gap = total - sum(spent)  # 各阶段之间的间隙（boot_step 刷新等）

        line = "=" * 62
        print(line)
        print("{}   总耗时 {:.3f} s   （CALC_BOOT_PROFILE=0 关闭本报告）".format(
            self.title, total))
        print(line)
        print(self._pad("阶段", 22) + "{:>10}{:>9}{:>11}".format("耗时", "占比", "累计"))
        printed = 0.0
        for (name, _start, _end), dur in zip(self.stages, spent):
            printed += dur
            print(self._pad(name, 22)
                  + "{:>8.3f} s{:>8.1%}{:>10.3f} s".format(
                      dur, dur / total if total else 0.0, printed))
        if gap > 0.0005:
            print(self._pad("其他（事件处理等间隙）", 22)
                  + "{:>8.3f} s{:>8.1%}{:>10.3f} s".format(
                      gap, gap / total if total else 0.0, total))
        print(line)


def main():

    prof = BootProfiler()

    # 1. 开启共享 OpenGL 上下文（WebEngine 必需，必须先于 QApplication 设置）
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts, True)

    # 2. 创建 QApplication
    with prof.stage("创建 QApplication"):
        app = QApplication(sys.argv)

    # 3. 提前并应用语言（在启动画面显示前安装翻译器）
    with prof.stage("应用语言设置"):
        from core.settings import apply_language, load_saved_language
        apply_language(load_saved_language())

    # 4. 启动画面
    with prof.stage("显示启动画面"):
        from core.settings import current_theme
        splash = BootSplash(make_splash_pixmap(current_theme()))
        splash.show()

    # 5. 创建主窗口
    file_arg = open_file_arg()
    boot_step(splash, QCoreApplication.translate("Boot", "正在创建主窗口…"))
    with prof.stage("导入主窗口模块"):
        from ui.main import MainWindow
    with prof.stage("创建主窗口"):
        mainWindow = MainWindow(file_arg=file_arg)

    # 6. 启动时通过命令行参数传入的存档文件（如文件管理器双击 .cca 文件）
    if file_arg is not None:
        boot_step(splash, QCoreApplication.translate("Boot", "正在加载启动存档…"))
        with prof.stage("加载启动存档"):
            from functions.saves import load_from_path
            try:
                load_from_path(mainWindow, file_arg)
            except Exception:
                pass
    else:
        boot_step(splash, QCoreApplication.translate("Boot", "正在完成启动…"))

    # 7. 启动完成：显示主窗口，再绑定菜单/应用主题（重活后置，先让窗口出现）
    with prof.stage("显示主窗口"):
        splash.finish(mainWindow)
        mainWindow.show()

    with prof.stage("初始化设置与菜单绑定"):
        mainWindow.setup()

    # 8. 输出启动性能报告后进入事件循环
    prof.report()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
