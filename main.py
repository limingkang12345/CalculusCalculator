from PySide6.QtWidgets import QMainWindow

from ui import *

import webbrowser

class MainWindow(QMainWindow):
    def __init__(self, parent=None):

        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.fs, self.tabs = {}, {}
        self.tabs_n = [1] * 10

        self.setup()

    def setup(self):

        self.ui.actionshouye.triggered.connect(lambda:self.create_tab(0))
        self.ui.actiondingyi.triggered.connect(lambda:self.create_tab(1))
        self.ui.actionqiudao.triggered.connect(lambda:self.create_tab(2))
        self.ui.actionjifen.triggered.connect(lambda:self.create_tab(3))
        self.ui.actionbianxing.triggered.connect(lambda:self.create_tab(4))
        self.ui.actionfangcheng.triggered.connect(lambda:self.create_tab(5))
        self.ui.actionfangchengzu.triggered.connect(lambda:self.create_tab(6))
        self.ui.actionbudengshi.triggered.connect(lambda:self.create_tab(7))
        self.ui.actionbudengshizu.triggered.connect(lambda:self.create_tab(8))
        self.ui.actionhelp.triggered.connect(lambda:self.create_tab(9))
        self.ui.actiongithub.triggered.connect(lambda:webbrowser.open("https://github.com/limingkang12345/CalculusCalculator"))
        self.ui.actionwebsite.triggered.connect(lambda:webbrowser.open("https://limingkang.pythonanywhere.com"))
        
        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)

        self.create_tab(0)

    def close_tab(self, index):
        # 关闭标签页
        tab_to_close = self.ui.tabWidget.widget(index)
        tab_name = self.ui.tabWidget.tabText(index)
        self.ui.tabWidget.removeTab(index)
        tab_to_close.deleteLater()
        del self.tabs[tab_name]
        if self.ui.tabWidget.count() == 0:
            self.create_tab(0)
        
    def create_tab(self, index):
        # 新建标签页
        # index(int):标签页功能类型，与ui/__init__.py中的tabs_list对应
        new_tab = tabs_list[index](self, self.fs)
        new_tab_name = tabs_name[index] + str(self.tabs_n[index])
        self.tabs_n[index] += 1
        self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.addTab(new_tab, new_tab_name))
        self.tabs[new_tab_name] = self.ui.tabWidget.currentWidget()
