from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy, QWidget, QGroupBox, QLineEdit
from PySide6.QtWebEngineWidgets import QWebEngineView


class LayoutManager:

    def setup_tab(self, tab, tab_type):
        """为标签页设置自适应布局"""
        if tab_type == '首页':
            return

        if tab_type == '帮助':
            if tab.layout():
                old = tab.layout()
                while old.count():
                    old.takeAt(0)
                del old
            layout = QVBoxLayout(tab)
            layout.setContentsMargins(0, 0, 0, 0)
            tab.webEngineView.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            layout.addWidget(tab.webEngineView)
            return

        if tab.layout():
            old = tab.layout()
            while old.count():
                old.takeAt(0)
            del old

        # TODO: 改成switch case?
        if tab_type == '求导':
            self._setup_qiudao(tab)
        elif tab_type == '积分':
            self._setup_jifen(tab)
        elif tab_type == '定义':
            self._setup_dingyi(tab)
        elif tab_type == '变形':
            self._setup_bianxing(tab)
        elif tab_type == '方程':
            self._setup_fangcheng(tab)
        elif tab_type == '方程组':
            self._setup_fangchengzu(tab)
        elif tab_type == '不等式':
            self._setup_budengshi(tab)
        elif tab_type == '不等式组':
            self._setup_budengshizu(tab)
        elif tab_type == '计算':
            self._setup_jisuan(tab)
        else:
            return

        for gb in tab.findChildren(QGroupBox):
            if tab_type == '不等式组' and gb is tab.groupBox_61:
                continue
            gb.setSizePolicy(QSizePolicy.Policy.Expanding, gb.sizePolicy().verticalPolicy())
            self._arrange_groupbox_children(gb)

    def _setup_qiudao(self, tab):
        """求导页"""
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        layout.addWidget(tab.groupBox1)
        row = QWidget()
        h = QHBoxLayout(row)
        h.setContentsMargins(0, 0, 0, 0)
        h.addWidget(tab.groupBox)
        h.addWidget(tab.groupBox_4)
        h.addWidget(tab.groupBox_3)
        h.addWidget(tab.groupBox_6)
        h.addWidget(tab.qiudao_yinhanshu)
        h.addWidget(tab.qiudao_qiuchujutizhi)
        h.addStretch()
        layout.addWidget(row)
        tab.groupBox2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(tab.groupBox2, 2)
        tab.groupBox3.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(tab.groupBox3, 2)
        tab.groupBox_5.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(tab.groupBox_5, 1)
        layout.addWidget(tab.qiudao_qiudao_button)

    def _setup_jifen(self, tab):
        """积分页"""
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        layout.addWidget(tab.groupBox1_2)
        row = QWidget()
        h = QHBoxLayout(row)
        h.setContentsMargins(0, 0, 0, 0)
        h.addWidget(tab.groupBox_7)
        h.addWidget(tab.groupBox_9)
        h.addWidget(tab.groupBox_8)
        h.addWidget(tab.jifen_dingjifen)
        h.addStretch()
        layout.addWidget(row)
        tab.groupBox2_2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(tab.groupBox2_2, 2)
        tab.groupBox3_2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(tab.groupBox3_2, 2)
        tab.groupBox_11.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(tab.groupBox_11, 1)
        layout.addWidget(tab.jifen_jifen_button)

    def _setup_dingyi(self, tab):
        """定义页"""
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        top = QWidget()
        top_layout = QHBoxLayout(top)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.addWidget(tab.groupBox_19, 1)
        right = QWidget()
        right_v = QVBoxLayout(right)
        right_v.setContentsMargins(0, 0, 0, 0)
        right_v.addWidget(tab.groupBox_20)
        right_v.addWidget(tab.groupBox_21)
        top_layout.addWidget(right, 2)
        layout.addWidget(top, 1)
        tab.groupBox_22.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(tab.groupBox_22, 1)

    def _setup_bianxing(self, tab):
        """变形页"""
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        layout.addWidget(tab.groupBox_2)
        layout.addWidget(tab.groupBox_13)
        layout.addWidget(tab.groupBox_10)
        tab.groupBox_16.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(tab.groupBox_16, 2)
        tab.groupBox_12.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(tab.groupBox_12, 2)
        layout.addWidget(tab.bianxing_bianxing_button)

    def _setup_fangcheng(self, tab):
        """方程页"""
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        layout.addWidget(tab.groupBox_14)
        layout.addWidget(tab.groupBox_15)
        tab.groupBox_18.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(tab.groupBox_18, 1)
        tab.groupBox_17.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(tab.groupBox_17, 1)
        layout.addWidget(tab.fangcheng_qiujie)

    def _setup_fangchengzu(self, tab):
        """方程组页"""
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        layout.addWidget(tab.groupBox_23)
        tab.groupBox_24.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(tab.groupBox_24, 1)
        tab.groupBox_25.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(tab.groupBox_25, 1)
        layout.addWidget(tab.fangchengzu_qiujie)

    def _setup_budengshi(self, tab):
        """不等式页"""
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        layout.addWidget(tab.groupBox_38)
        layout.addWidget(tab.groupBox_39)
        tab.groupBox_37.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(tab.groupBox_37, 1)
        tab.groupBox_40.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(tab.groupBox_40, 1)
        layout.addWidget(tab.budengshi_qiujie)

    def _setup_budengshizu(self, tab):
        """不等式组页"""
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(0)

        self._arrange_budengshizu_edit(tab)
        tab.groupBox_61.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(tab.groupBox_61)

        tab.groupBox_60.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(tab.groupBox_60, 1)
        tab.groupBox_59.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(tab.groupBox_59, 1)

        layout.addWidget(tab.budengshizu_qiujie)

    def _setup_jisuan(self, tab):
        """计算页"""
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        layout.addWidget(tab.groupBox_2)
        layout.addWidget(tab.groupBox_13)
        layout.addWidget(tab.groupBox_10)
        tab.groupBox_16.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(tab.groupBox_16, 1)
        tab.groupBox_12.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(tab.groupBox_12, 1)
        layout.addWidget(tab.jisuan_jisuan_button)

    def _setup_generic(self, tab):
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        children = [c for c in tab.children() if isinstance(c, QWidget) and c.parent() == tab]
        children.sort(key=lambda w: w.geometry().y())
        for child in children:
            layout.addWidget(child)

    def _arrange_budengshizu_edit(self, tab):
        """不等式组编辑区"""
        groupbox = tab.groupBox_61
        if groupbox.layout():
            return

        layout = QHBoxLayout(groupbox)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        layout.addWidget(tab.budengshizu_budengshi, 1)

        right = QWidget()
        right_v = QVBoxLayout(right)
        right_v.setContentsMargins(0, 0, 0, 0)
        right_v.setSpacing(5)

        row1 = QWidget()
        row1_layout = QHBoxLayout(row1)
        row1_layout.setContentsMargins(0, 0, 0, 0)
        tab.budengshizu_zuoshi.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        row1_layout.addWidget(tab.budengshizu_zuoshi, 1)
        right_v.addWidget(row1)

        row2 = QWidget()
        row2_layout = QHBoxLayout(row2)
        row2_layout.setContentsMargins(0, 0, 0, 0)
        row2_layout.addWidget(tab.budengshizu_budenghao)
        tab.budengshizu_youshi.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        row2_layout.addWidget(tab.budengshizu_youshi, 1)
        right_v.addWidget(row2)

        row3 = QWidget()
        row3_layout = QHBoxLayout(row3)
        row3_layout.setContentsMargins(0, 0, 0, 0)
        row3_layout.addWidget(tab.label_33)
        tab.budengshizu_ziyoubianliang.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        row3_layout.addWidget(tab.budengshizu_ziyoubianliang, 1)
        row3_layout.addWidget(tab.budengshizu_baocun)
        row3_layout.addWidget(tab.budengshizu_shanchu)
        right_v.addWidget(row3)

        right.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(right, 2)

        right_v.addStretch()
        right.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(right, 2)

    def _arrange_groupbox_children(self, groupbox):
        """自动为GroupBox内部绝对定位控件创建布局：单行水平/多行垂直，QLineEdit水平拉伸，QWebEngineView垂直拉伸"""
        if groupbox.layout():
            return

        children = [c for c in groupbox.children() if isinstance(c, QWidget) and c.parent() == groupbox and not c.isWindowType()]
        if not children:
            return

        webviews = [c for c in children if isinstance(c, QWebEngineView)]
        if len(webviews) == 1 and len(children) == 1:
            layout = QVBoxLayout(groupbox)
            layout.setContentsMargins(5, 5, 5, 5)
            webviews[0].setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            layout.addWidget(webviews[0], 1)
            return

        rows = {}
        for child in children:
            y = child.geometry().y() // 10
            rows.setdefault(y, []).append(child)

        if len(rows) == 1:
            layout = QHBoxLayout(groupbox)
            widgets = sorted(rows[list(rows.keys())[0]], key=lambda c: c.geometry().x())
            for child in widgets:
                if isinstance(child, QLineEdit):
                    child.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                    layout.addWidget(child, 1)
                else:
                    layout.addWidget(child)
            layout.addStretch()
        else:
            layout = QVBoxLayout(groupbox)
            for y in sorted(rows.keys()):
                row_widgets = rows[y]
                if len(row_widgets) == 1:
                    child = row_widgets[0]
                    if isinstance(child, QWebEngineView):
                        child.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                        layout.addWidget(child, 1)
                    elif isinstance(child, QLineEdit):
                        child.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                        layout.addWidget(child)
                    else:
                        layout.addWidget(child)
                else:
                    h_layout = QHBoxLayout()
                    for child in sorted(row_widgets, key=lambda c: c.geometry().x()):
                        if isinstance(child, QLineEdit):
                            child.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                            h_layout.addWidget(child, 1)
                        else:
                            h_layout.addWidget(child)
                    h_layout.addStretch()
                    container = QWidget()
                    container.setLayout(h_layout)
                    layout.addWidget(container)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
