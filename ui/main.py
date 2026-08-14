from PySide6.QtWidgets import QMainWindow, QGraphicsView, QLineEdit, QStyle
from PySide6.QtCore import QTimer, QCoreApplication
from PySide6.QtGui import QColor, QIcon, QAction
from qdarktheme import setup_theme

from ui.ui_main import Ui_MainWindow
from core.settings import apply_language, save_language, save_theme

import webbrowser, sys
import ui  # 提供 tabs_list, tabs_dict 等延迟加载配置

# 注意：functions.saves / core.render（matplotlib+sympy）、math_input、
# ui.huancun 等重量级模块一律延迟到实际使用时再导入，以加快启动速度。

# tabs_list 和 tabs_dict 由 ui/__init__.py 通过 lazy_loader 延迟加载提供
# 子模块仅在首次创建对应 tab 时才被导入

qss_light = """QWidget { color: #1f2329; }

/* 输入框：白底 + 清晰边框 + 聚焦蓝色高亮 */
QLineEdit, QComboBox, QSpinBox, QTextEdit, QPlainTextEdit {
    border: 1px solid #7a8089;
    border-radius: 4px;
    padding: 3px 6px;
    background-color: #ffffff;
    selection-background-color: #b9d8f5;
    selection-color: #1f2329;
}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus,
QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #0078d4;
}
QLineEdit:disabled, QComboBox:disabled, QSpinBox:disabled {
    color: #8a9099;
    background-color: #f2f3f5;
    border: 1px solid #c6cad0;
}

/* 下拉框下拉列表 */
QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #7a8089;
    selection-background-color: #0078d4;
    selection-color: #ffffff;
    outline: none;
}

/* 列表与表格 */
QListWidget, QTreeWidget, QTableWidget {
    border: 1px solid #8a9099;
    border-radius: 4px;
    background-color: #ffffff;
    alternate-background-color: #f2f5fa;
}
QListWidget::item:hover, QTreeWidget::item:hover, QTableWidget::item:hover,
QListView::item:hover, QTableView::item:hover {
    background-color: #e3effb;
}
QListWidget::item:selected, QTreeWidget::item:selected, QTableWidget::item:selected,
QListView::item:selected, QTableView::item:selected,
QComboBox QAbstractItemView::item:selected {
    background-color: #0078d4;
    color: #ffffff;
}
/* 下拉框：弹出列表与主显示区选中项统一为不透明深蓝底 + 白字，
   避免 qdarktheme 的半透明浅蓝背景与白色文字叠加导致难以分辨 */
QComboBox::item:selected {
    background-color: #0078d4;
    color: #ffffff;
}

/* 分组框：浅灰卡片 + 蓝色标题 */
QGroupBox {
    border: 1px solid #b4bac2;
    border-radius: 6px;
    margin-top: 12px;
    padding: 8px;
    background-color: #fbfcfe;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
    color: #005a9e;
    font-weight: bold;
}

/* 按钮：主按钮品牌蓝填充，普通按钮白底 */
QPushButton {
    border: 1px solid #7a8089;
    border-radius: 4px;
    padding: 5px 12px;
    background-color: #ffffff;
    color: #1f2329;
}
QPushButton:hover { background-color: #e3effb; border: 1px solid #0078d4; }
QPushButton:pressed { background-color: #cfe3f7; }
QPushButton:disabled { color: #8a9099; background-color: #f2f3f5; border: 1px solid #c6cad0; }
QPushButton:default {
    background-color: #0078d4;
    border: 1px solid #0078d4;
    color: #ffffff;
}
QPushButton:default:hover { background-color: #006cbd; }
QPushButton:default:pressed { background-color: #005a9e; }

/* 菜单 */
QMenu { background-color: #ffffff; border: 1px solid #8a9099; }
QMenu::item { padding: 4px 20px 4px 12px; }
QMenu::item:selected { background-color: #0078d4; color: #ffffff; }
QMenu::separator { height: 1px; background: #d0d4dc; margin: 4px 8px; }

/* 滚动条 */
QScrollBar:vertical { background: #eef0f2; width: 10px; border-radius: 5px; }
QScrollBar::handle:vertical { background: #9aa0aa; border-radius: 5px; min-height: 20px; }
QScrollBar::handle:vertical:hover { background: #6c727c; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QScrollBar:horizontal { background: #eef0f2; height: 10px; border-radius: 5px; }
QScrollBar::handle:horizontal { background: #9aa0aa; border-radius: 5px; min-width: 20px; }
QScrollBar::handle:horizontal:hover { background: #6c727c; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0px; }

/* 复选框 / 单选 */
QCheckBox, QRadioButton { spacing: 5px; color: #1f2329; }
QCheckBox:hover, QRadioButton:hover { color: #0078d4; }
QCheckBox:disabled, QRadioButton:disabled { color: #9aa0aa; }

/* 表头 */
QHeaderView::section {
    background-color: #e7ebf0;
    border: 1px solid #b4bac2;
    padding: 4px 6px;
    color: #1f2329;
    font-weight: bold;
}
QHeaderView::section:hover { background-color: #dde4ee; }

/* 工具提示 */
QToolTip {
    background-color: #ffffff;
    color: #1f2329;
    border: 1px solid #7a8089;
    padding: 4px 6px;
}

/* 进度条 */
QProgressBar {
    border: 1px solid #8a9099;
    border-radius: 4px;
    text-align: center;
    background-color: #ffffff;
}
QProgressBar::chunk {
    background-color: #0078d4;
    border-radius: 3px;
}"""

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

        self.ui.actionsaveas.triggered.connect(lambda:self._save_file())
        self.ui.actionopen.triggered.connect(lambda:self._open_file())
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
        self.ui.actionyindao.triggered.connect(self.show_guide)
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
        self.ui.actionblockly.triggered.connect(lambda:self.create_tab(22))
        
        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)

        self.create_tab(0)

        # 按保存的主题应用（默认浅色）；语言已在 run.py 启动时装入
        from core.settings import load_saved_theme
        if load_saved_theme() == "dark":
            self.dark()
        else:
            self.light()

    def _save_file(self):
        from functions.saves import savefile
        savefile(self)

    def _open_file(self):
        from functions.saves import openfile
        openfile(self)

    def show_guide(self):
        """显示初始化引导（新手教学）。可在“关于 → 引导”重复打开。"""
        from ui.guide import GuideDialog
        dlg = GuideDialog(
            self,
            open_help_callback=lambda: self.create_tab(10),
            apply_language_callback=self.change_language,
            apply_theme_callback=lambda t: (self.dark() if t == "dark" else self.light()),
        )
        dlg.exec()

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
            # 积木编辑器页面跟随主题切换
            if hasattr(tab, "set_theme"):
                tab.set_theme("light")
            for view in tab.findChildren(QGraphicsView):
                if view.scene() is not None:
                    view.scene().setBackgroundBrush(QColor(255, 255, 255))
        # 延迟导入 matplotlib（重量级），仅切换主题时加载
        from core.render import refreshGraphicsView
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
            # 积木编辑器页面跟随主题切换
            if hasattr(tab, "set_theme"):
                tab.set_theme("dark")
            for view in tab.findChildren(QGraphicsView):
                if view.scene() is not None:
                    view.scene().setBackgroundBrush(QColor(0, 0, 0))
        # 延迟导入 matplotlib（重量级），仅切换主题时加载
        from core.render import refreshGraphicsView
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
            # 积木编辑器（Web 页面）：重新加载页面以完整切换语言
            if hasattr(widget, "set_language"):
                try:
                    widget.set_language(lang)
                except Exception:
                    pass
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

    '''def _enable_tab_resizable(self, tab):
        """将标签页顶层 QGridLayout 中占满整行的单控件行重排为垂直 QSplitter，
        使各区域可自由拖拽调整高度；无法安全转换的页面保持原布局。
        """
        from PySide6.QtWidgets import QGridLayout, QSplitter, QVBoxLayout, QWidget
        from PySide6.QtCore import Qt
        try:
            layout = tab.layout()
            if layout is None or not isinstance(layout, QGridLayout):
                return
            gl = layout
            cols = gl.columnCount()
            if cols <= 0 or gl.rowCount() < 2:
                return

            # 按行收集控件，识别"单个控件且占满整行"的区域。
            from collections import defaultdict
            rows_map = defaultdict(list)   # row -> [(colSpan, widget)]
            for i in range(gl.count()):
                item = gl.itemAt(i)
                w = item.widget() if item is not None else None
                if w is None:
                    continue
                row, _col, _rspan, cspan = gl.getItemPosition(i)
                rows_map[row].append((cspan, w))

            segments = []          # (kind, widgets, stretch)
            single_full_count = 0
            for r in range(gl.rowCount()):
                entries = rows_map.get(r)
                if not entries:
                    continue
                stretch = gl.rowStretch(r)
                if len(entries) == 1 and entries[0][0] == cols:
                    segments.append(('single', [entries[0][1]], stretch))
                    single_full_count += 1
                else:
                    segments.append(('multi', [e[1] for e in entries], stretch))
            if single_full_count < 2:
                return  # 没有可拖拽的多段区域

            splitter = QSplitter(Qt.Vertical)
            splitter.setChildrenCollapsible(False)
            # 明显的拖拽把手，方便用户调整各区域高度
            splitter.setHandleWidth(8)
            splitter.setStyleSheet(
                'QSplitter::handle { background: #cfd8dc; }'
                'QSplitter::handle:hover { background: #5c81a6; }')
            for kind, widgets, _stretch in segments:
                if kind == 'single':
                    splitter.addWidget(widgets[0])
                else:
                    holder = QWidget()
                    vbox = QVBoxLayout(holder)
                    vbox.setContentsMargins(0, 0, 0, 0)
                    for w in widgets:
                        vbox.addWidget(w)
                    splitter.addWidget(holder)
            # 按各行原始拉伸比例分配初始高度，避免某段过大/过小
            total_stretch = sum(max(s, 1) for (_k, _w, s) in segments)
            base = 520
            sizes = []
            for (_k, _w, s) in segments:
                sizes.append(max(90, int(base * max(s, 1) / total_stretch)))
            splitter.setSizes(sizes)
            # 应用各行原始拉伸比例（窗口缩放时的增长比例）
            for i, (_k, _w, stretch) in enumerate(segments):
                if stretch > 0:
                    splitter.setStretchFactor(i, stretch)

            # 清空原 grid 的布局项（控件已被 splitter 重新父化），
            # 然后把 splitter 加回原 grid，避免 setLayout 被 Qt 拒绝。
            while gl.count():
                gl.takeAt(0)
            gl.addWidget(splitter, 0, 0, 1, 1)
        except Exception:
            pass'''

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
        # 启用标签页内容区域自由拖拽拉伸（QGridLayout → QSplitter）
        #self._enable_tab_resizable(new_tab)
        # 为所有文本输入框添加快捷输入和缓存区按钮
        # 公式编辑器 / 缓存区模块延迟到点击时导入（QWebEngineWidgets 等为重量级）。
        # 注意：QAction.triggered 会额外传入 checked 参数，必须用 *_args 吸收，
        # 否则 i 会被 checked 覆盖，导致所有按钮误触公式编辑器。
        def get_lambda(lineedit, i):
            def run(*_args):
                del _args
                if i == 0:
                    from math_input.math_input import open_formula_dialog
                    open_formula_dialog(lineedit)
                elif i == 1:
                    from ui.huancun import open_cache
                    open_cache(lineedit)
                else:
                    self._on_insert_cache(lineedit)
            return run
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
