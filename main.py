from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, QTimer

from ui import *
from saves import savefile, openfile

import webbrowser, sys

class MainWindow(QMainWindow):
    def __init__(self, parent=None):

        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.fs, self.tabs, self.eqs, self.rels, self.vs = {}, {}, {}, {}, {}
        self.tabs_n = [1] * len(tabs_list)
        self._preinit_view = None

        self.setup()

    def setup(self):

        self.ui.actionsaveas.triggered.connect(lambda:savefile(self))
        self.ui.actionopen.triggered.connect(lambda:openfile(self))
        self.ui.actionexit.triggered.connect(lambda:sys.exit())
        self.ui.actionshouye.triggered.connect(lambda:self.create_tab(0))
        self.ui.actiondingyi.triggered.connect(lambda:self.create_tab(1))
        self.ui.actionqiudao.triggered.connect(lambda:self.create_tab(2))
        self.ui.actionjifen.triggered.connect(lambda:self.create_tab(3))
        self.ui.actionbianxing.triggered.connect(lambda:self.create_tab(4))
        self.ui.actionfangcheng.triggered.connect(lambda:self.create_tab(5))
        self.ui.actionfangchengzu.triggered.connect(lambda:self.create_tab(6))
        self.ui.actionbudengshi.triggered.connect(lambda:self.create_tab(7))
        self.ui.actionbudengshizu.triggered.connect(lambda:self.create_tab(8))
        self.ui.actionjisuan.triggered.connect(lambda:self.create_tab(9))
        self.ui.actionhelp.triggered.connect(lambda:self.create_tab(10))
        self.ui.actiondingyixiangliang.triggered.connect(lambda:self.create_tab(11))
        self.ui.actionhuitu_hanshu.triggered.connect(lambda:self.create_tab(12))
        self.ui.actionjiesanjiaoxing.triggered.connect(lambda:self.create_tab(13))
        self.ui.actionhuitu_pingmianjihe.triggered.connect(lambda:QMessageBox.information(self, "功能未完善", "抱歉！该功能目前尚未完善\n请关注本项目后续进展！", buttons=QMessageBox.StandardButton.Ok))
        self.ui.actionhuitu_litijihe.triggered.connect(lambda:QMessageBox.information(self, "功能未完善", "抱歉！该功能目前尚未完善\n请关注本项目后续进展！", buttons=QMessageBox.StandardButton.Ok))
        self.ui.actiongithub.triggered.connect(lambda:webbrowser.open("https://github.com/limingkang12345/CalculusCalculator"))
        self.ui.actionwebsite.triggered.connect(lambda:webbrowser.open("https://limingkang.pythonanywhere.com"))
        
        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)

        self.create_tab(0)

        # 预初始化 QWebEngineView，让 WebEngine 子进程提前启动，
        # 避免用户首次创建带 QWebEngineView 标签页时窗口闪退
        QTimer.singleShot(0, self._preinit_webengine)

    def _preinit_webengine(self):
        # 预初始化 WebEngine 子进程，消除首次创建 WebEngine 标签页时的闪退问题
        self._preinit_view = QWebEngineView()
        self._preinit_view.setUrl(QUrl("about:blank"))
        self._preinit_view.hide()

    def close_tab(self, index, auto_create = True):
        # 关闭标签页
        # index(int):要关闭的标签页的索引
        # auto_create(bool):标签页数为0时是否自动创建首页
        tab_to_close = self.ui.tabWidget.widget(index)
        tab_name = self.ui.tabWidget.tabText(index)
        self.ui.tabWidget.removeTab(index)
        tab_to_close.deleteLater()
        del self.tabs[tab_name]
        if self.ui.tabWidget.count() == 0 and auto_create:
            self.create_tab(0)
        
    def create_tab(self, index, n = 0):
        # 新建标签页
        # index(int):标签页功能类型，与ui/__init__.py中的tabs_list对应
        # n(int):标签页序号，默认为0，有传入则使用传入值，否则使用默认值
        # 不传父对象（None），由 addTab 自动设置正确的父对象为 tabWidget 的堆叠窗口
        # 避免标签页先被设为 MainWindow 的子对象后又重新父化，导致原生窗口句柄重建引发闪退
        new_tab = tabs_list[index](self, self.fs)
        new_tab_name = list(tabs_dict.keys())[index] + str(n if n else self.tabs_n[index])
        self.tabs_n[index] += (0 if n else 1)
        self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.addTab(new_tab, new_tab_name))
        self.tabs[new_tab_name] = self.ui.tabWidget.currentWidget()
