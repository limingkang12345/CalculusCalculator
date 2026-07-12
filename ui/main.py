from PySide6.QtWidgets import QMainWindow, QMessageBox, QGraphicsView
from PySide6.QtCore import QTimer
from PySide6.QtGui import QColor, QIcon
from qdarktheme import setup_theme

from ui.ui_main import Ui_MainWindow
from functions.saves import savefile, openfile
from core.render import refreshGraphicsView

import webbrowser, sys
import ui  # 提供 tabs_list, tabs_dict 等延迟加载配置

# tabs_list 和 tabs_dict 由 ui/__init__.py 通过 lazy_loader 延迟加载提供
# 子模块仅在首次创建对应 tab 时才被导入

qss_light = """QWidget { color: black; }
QGroupBox { border: 1px solid gray;}
QLineEdit { border: 1px solid rgb(64, 64, 64);}
QListWidget { border: 1px solid rgb(0, 0, 255);}
QPushButton { border: 1px solid rgb(255, 0, 0);}
QComboBox { border: 1px solid rgb(0, 0, 255);}"""

qss_dark = """QWidget { color: white; }
QGroupBox { border: 1px solid gray;}"""

class MainWindow(QMainWindow):
    def __init__(self, parent=None):

        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.fs, self.tabs, self.eqs, self.rels, self.vs = {}, {}, {}, {}, {}
        self.tabs_n = [1] * len(ui.tabs_list)

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
        self.ui.actiondingyi_pj.triggered.connect(lambda:self.create_tab(14))
        self.ui.actionhuitu_pingmianjihe.triggered.connect(lambda:self.create_tab(15))
        self.ui.actiondingyi_lj.triggered.connect(lambda:self.create_tab(16))
        self.ui.actionhuitu_litijihe.triggered.connect(lambda:self.create_tab(17))
        self.ui.actionpjjisuan.triggered.connect(lambda:self.create_tab(18))
        self.ui.actionljjisuan.triggered.connect(lambda:self.create_tab(19))
        self.ui.actionlight.triggered.connect(self.light)
        self.ui.actiondark.triggered.connect(self.dark)
        self.ui.actiongithub.triggered.connect(lambda:webbrowser.open("https://github.com/limingkang12345/CalculusCalculator"))
        self.ui.actionwebsite.triggered.connect(lambda:webbrowser.open("https://limingkang.pythonanywhere.com"))
        
        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)

        self.create_tab(0)

        self.light()

    def light(self):
        # 切换浅色主题，并将除Help页面外所有视图改为白色底色
        self.theme = "light"
        setup_theme(theme="light", additional_qss=qss_light)
        for tab_name, tab in self.tabs.items():
            if tab_name.startswith("帮助"):
                # 帮助文档需按主题重渲染（明暗配色不同）
                if hasattr(tab, "load_help"):
                    tab.load_help()
                continue
            for view in tab.findChildren(QGraphicsView):
                if view.scene() is not None:
                    view.scene().setBackgroundBrush(QColor(255, 255, 255))
        refreshGraphicsView()

    def dark(self):
        # 切换深色主题，并将除Help页面外所有视图改为黑色底色
        self.theme = "dark"
        setup_theme(theme="dark", additional_qss=qss_dark)
        for tab_name, tab in self.tabs.items():
            if tab_name.startswith("帮助"):
                # 帮助文档需按主题重渲染（明暗配色不同）
                if hasattr(tab, "load_help"):
                    tab.load_help()
                continue
            for view in tab.findChildren(QGraphicsView):
                if view.scene() is not None:
                    view.scene().setBackgroundBrush(QColor(0, 0, 0))
        refreshGraphicsView()

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
        new_tab = ui.tabs_list[index](self, self.fs)
        new_tab_name = list(ui.tabs_dict.keys())[index] + str(n if n else self.tabs_n[index])
        self.tabs_n[index] += (0 if n else 1)
        self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.addTab(new_tab, new_tab_name))
        self.tabs[new_tab_name] = self.ui.tabWidget.currentWidget()
