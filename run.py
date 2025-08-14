from ui import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow

if __name__ == "__main__":
    # 主程序
    import sys
    app = QApplication(sys.argv)
    Mainwindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(Mainwindow)
    Mainwindow.show()
    sys.exit(app.exec())
