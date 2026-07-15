import sys
from PySide6.QtCore import QCoreApplication

# 必须在导入任何读取 settings.json 的模块（ui.i18n）之前设置组织/应用名，
# 否则 QStandardPaths 在没有应用名时会随 QApplication 是否存在解析出不同路径，
# 导致主题/语言的“保存”与“读取”指向不同文件，设置无法跨重启持久化。
QCoreApplication.setOrganizationName("CalculusCalculator")
QCoreApplication.setApplicationName("CalculusCalculator")

from PySide6.QtWidgets import QApplication
from ui.i18n import apply_language, load_saved_language
from ui.main import MainWindow


if __name__ == "__main__":
    # 主程序
    app = QApplication(sys.argv)
    # 启动时按上次保存（或默认）的语言安装翻译器，保证初始界面即正确
    apply_language(load_saved_language())
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
