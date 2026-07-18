from PySide6.QtWidgets import QMainWindow, QMessageBox, QGraphicsView, QLineEdit, QStyle
from PySide6.QtCore import QTimer, QCoreApplication
from PySide6.QtGui import QColor, QIcon, QAction
from qdarktheme import setup_theme

from ui.ui_main import Ui_MainWindow
from functions.saves import savefile, openfile
from core.render import refreshGraphicsView
from core.settings import apply_language, save_language, save_theme
from ui.math_input import open_formula_dialog
from ui.huancun import open_cache

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
        self.cache = []

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
        self.ui.actiongithub.triggered.connect(lambda:webbrowser.open("https://github.com/limingkang12345/CalculusCalculator"))
        self.ui.actionwebsite.triggered.connect(lambda:webbrowser.open("https://limingkang.pythonanywhere.com"))
        self.ui.actionshezhi.triggered.connect(lambda:self.create_tab(20))
        self.ui.actionhuancun.triggered.connect(lambda:self.create_tab(21))
        
        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)

        self.create_tab(0)

        # 按保存的主题应用（默认浅色）；语言已在 run.py 启动时装入
        from core.settings import load_saved_theme
        if load_saved_theme() == "dark":
            self.dark()
        else:
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
        # 设置页强制更新设置选项
        for i in range(self.ui.tabWidget.count()):
            widget = self.ui.tabWidget.widget(i)
            if hasattr(widget, "on_apply"):
                widget.shezhi_qianse.setChecked(True)
                widget.shezhi_shense.setChecked(False)
        save_theme(self.theme)

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
        # 设置页强制更新设置选项
        for i in range(self.ui.tabWidget.count()):
            widget = self.ui.tabWidget.widget(i)
            if hasattr(widget, "on_apply"):
                widget.shezhi_shense.setChecked(True)
                widget.shezhi_qianse.setChecked(False)
        save_theme(self.theme)

    def change_language(self, lang):
        # 切换界面语言并即时刷新所有已打开窗口/标签页文本
        apply_language(lang)
        save_language(lang)
        # 主窗口自身（菜单、工具栏等由 Ui_MainWindow 管理）
        self.ui.retranslateUi(self)
        # 所有已打开的标签页
        for i in range(self.ui.tabWidget.count()):
            widget = self.ui.tabWidget.widget(i)
            if widget is None:
                continue
            # 主窗口用独立 self.ui；标签页多为多重继承，retranslateUi 直接在实例上
            ui_obj = widget if hasattr(widget, "retranslateUi") else getattr(widget, "ui", None)
            if ui_obj is not None and hasattr(ui_obj, "retranslateUi"):
                try:
                    ui_obj.retranslateUi(widget)
                except Exception:
                    pass
            # 同步刷新标签页标题
            base = getattr(widget, "_tab_base", None)
            suffix = getattr(widget, "_tab_suffix", "")
            if base is not None:
                self.ui.tabWidget.setTabText(i, QCoreApplication.translate("MainWindow", base) + suffix)
            # 设置页强制更新设置选项
            if hasattr(widget, "on_apply"):
                widget.shezhi_zhongwen.setChecked(True if lang == "zh_CN" else False)
                widget.shezhi_yingwen.setChecked(True if lang == "en_US" else False)
        # 更新所有文本框的快捷按钮文本（可视化输入/打开缓存区/存入缓存区）
        for tab_widget in self.tabs.values():
            for le in tab_widget.findChildren(QLineEdit):
                for attr, key in [("input_action", "可视化输入"),
                                  ("cache_action", "打开缓存区"),
                                  ("insert_action", "存入缓存区")]:
                    action = getattr(le, attr, None)
                    if action is not None:
                        action.setText(QCoreApplication.translate("MainWindow", key))

    def _on_insert_cache(self, lineedit):
        """存入缓存区：保存文本后，图标短暂变为对勾再恢复。"""
        text = lineedit.text().strip()
        if not text:
            return
        # 将文本存入缓存列表
        if text in self.cache:
            self.cache.remove(text)
        self.cache.insert(0, text)

        action = getattr(lineedit, 'insert_action', None)
        if action is None:
            return
        # 保存原图标，切换为对勾
        original_icon = action.icon()
        action.setIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton))
        # 延时恢复原图标
        QTimer.singleShot(800, lambda a=action, o=original_icon: a.setIcon(o))

    def close_tab(self, index, auto_create = True):
        # 关闭标签页
        # index(int):要关闭的标签页的索引
        # auto_create(bool):标签页数为0时是否自动创建首页
        tab_to_close = self.ui.tabWidget.widget(index)
        # 使用创建时记录的内部键，而非可能被翻译过的标签文本
        tab_name = getattr(tab_to_close, "_tab_key", None) or self.ui.tabWidget.tabText(index)
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
        base_key = list(ui.tabs_dict.keys())[index]
        suffix = str(n if n else self.tabs_n[index])
        new_tab_name = base_key + suffix
        # 记录内部键（用于 self.tabs 字典与保存/打开，保持中文不变）及翻译所需信息
        new_tab._tab_key = new_tab_name
        new_tab._tab_base = base_key
        new_tab._tab_suffix = suffix
        self.tabs_n[index] += (0 if n else 1)
        # 标签页标题使用翻译后的文本（内部键仍为中文，避免破坏字典查找）
        title = QCoreApplication.translate("MainWindow", base_key) + suffix
        self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.addTab(new_tab, title))
        self.tabs[new_tab_name] = self.ui.tabWidget.currentWidget()
        # 为所有文本输入框添加快捷输入和缓存区按钮
        def get_lambda(lineedit, i):  return lambda: [open_formula_dialog, open_cache, self._on_insert_cache][i](lineedit)
        for i in new_tab.findChildren(QLineEdit):
            i.input_action = QAction(QIcon.fromTheme("input-keyboard"), QCoreApplication.translate("MainWindow", "可视化输入"), i)
            i.input_action.triggered.connect(get_lambda(i, 0))
            i.addAction(i.input_action, QLineEdit.TrailingPosition)
            i.cache_action = QAction(QIcon.fromTheme("document-open"), QCoreApplication.translate("MainWindow", "打开缓存区"), i)
            i.cache_action.triggered.connect(get_lambda(i, 1))
            i.addAction(i.cache_action, QLineEdit.TrailingPosition)
            i.insert_action = QAction(QIcon.fromTheme("list-add"), QCoreApplication.translate("MainWindow", "存入缓存区"), i)
            i.insert_action.triggered.connect(get_lambda(i, 2))
            i.addAction(i.insert_action, QLineEdit.TrailingPosition)
