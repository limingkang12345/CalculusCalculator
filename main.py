import layouts_tool
from PySide6.QtCore import QTimer

from ui import *
from saves import savefile, openfile

import webbrowser, sys


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        try:
            self.setWindowIcon(QIcon("./favicon.ico"))
        except:
            pass
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.ui.tabWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.ui.tabWidget)
        self.setCentralWidget(central)

        self.fs, self.tabs, self.eqs, self.rels = {}, {}, {}, {}
        self.tabs_n = [1] * 11
        self._preinit_view = None

        self.layout_manager = layouts_tool.LayoutManager()

        self.setup()

    def setup(self):
        self.ui.actionsaveas.triggered.connect(lambda: savefile(self))
        self.ui.actionopen.triggered.connect(lambda: openfile(self))
        self.ui.actionexit.triggered.connect(lambda: sys.exit())
        self.ui.actionshouye.triggered.connect(lambda: self.create_tab(0))
        self.ui.actiondingyi.triggered.connect(lambda: self.create_tab(1))
        self.ui.actionqiudao.triggered.connect(lambda: self.create_tab(2))
        self.ui.actionjifen.triggered.connect(lambda: self.create_tab(3))
        self.ui.actionbianxing.triggered.connect(lambda: self.create_tab(4))
        self.ui.actionfangcheng.triggered.connect(lambda: self.create_tab(5))
        self.ui.actionfangchengzu.triggered.connect(lambda: self.create_tab(6))
        self.ui.actionbudengshi.triggered.connect(lambda: self.create_tab(7))
        self.ui.actionbudengshizu.triggered.connect(lambda: self.create_tab(8))
        self.ui.actionjisuan.triggered.connect(lambda: self.create_tab(9))
        self.ui.actionhelp.triggered.connect(lambda: self.create_tab(10))
        self.ui.actiongithub.triggered.connect(
            lambda: webbrowser.open("https://github.com/limingkang12345/CalculusCalculator"))
        self.ui.actionwebsite.triggered.connect(lambda: webbrowser.open("https://limingkang.pythonanywhere.com"))

        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)
        
        self.ui.actionopen.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.FolderOpen)))
        self.ui.actionsaveas.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSaveAs)))
        self.ui.actionexit.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.SystemLogOut)))
        self.ui.actionexit.setShortcut("Alt+F4")

        self.ui.actionshouye.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoHome))) # homepage
        self.ui.actionhelp.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.HelpFaq)))

        self.ui.actionwebsite.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.InsertLink)))

        self.create_tab(0)

        QTimer.singleShot(0, self._preinit_webengine)

    def _preinit_webengine(self):
        self._preinit_view = QWebEngineView()
        self._preinit_view.setUrl(QUrl("about:blank"))
        self._preinit_view.hide()

    def close_tab(self, index, auto_create=True):
        tab_to_close = self.ui.tabWidget.widget(index)
        tab_name = self.ui.tabWidget.tabText(index)
        self.ui.tabWidget.removeTab(index)
        tab_to_close.deleteLater()
        del self.tabs[tab_name]
        if self.ui.tabWidget.count() == 0 and auto_create:
            self.create_tab(0)

    def create_tab(self, index, n=0):
        # 新建标签页
        # index(int):标签页功能类型，与ui/__init__.py中的tabs_list对应
        # n(int):标签页序号，默认为0，有传入则使用传入值，否则使用默认值
        # 不传父对象（None），由 addTab 自动设置正确的父对象为 tabWidget 的堆叠窗口
        # 避免标签页先被设为 MainWindow 的子对象后又重新父化，导致原生窗口句柄重建引发闪退
        new_tab = tabs_list[index](self, self.fs)
        tab_type = list(tabs_dict.keys())[index]
        new_tab_name = tab_type + str(n if n else self.tabs_n[index])
        self.tabs_n[index] += (0 if n else 1)

        self.layout_manager.setup_tab(new_tab, tab_type)

        self.ui.tabWidget.addTab(new_tab, new_tab_name)
        self.ui.tabWidget.setCurrentWidget(new_tab)
        self.tabs[new_tab_name] = new_tab