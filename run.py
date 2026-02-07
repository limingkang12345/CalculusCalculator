import sys
from main import MainWindow
from PySide6.QtWidgets import QApplication


if __name__ == "__main__":
    # 主程序
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
