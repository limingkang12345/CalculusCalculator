from ui.ui_dingyixiangliang import *
from core.sympify import sympify
from core.render import setGraphicsView, setGraphicsViewTheme
from sympy import latex, simplify
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QCoreApplication

class Dingyixiangliang(QWidget, Ui_dingyixiangliang):
    def __init__(self, parent, fs):
        super(Dingyixiangliang, self).__init__(parent)
        self.setupUi(self)
        setGraphicsViewTheme(self, parent)

        self.dingyixiangliang_xiangliangliebiao.itemClicked.connect(self.read_vector)
        self.dingyixiangliang_baocun.clicked.connect(self.save_vector)
        self.dingyixiangliang_shanchu.clicked.connect(self.delete_vector)
        self.dingyixiangliang_mingcheng.returnPressed.connect(self.dingyixiangliang_baocun.click)
        self.dingyixiangliang_x.returnPressed.connect(self.dingyixiangliang_baocun.click)
        self.dingyixiangliang_y.returnPressed.connect(self.dingyixiangliang_baocun.click)
        self._populate_vector_combos()
        self.dingyixiangliang_xiangliangshuxing_cbx.setCurrentIndex(0)
        self.dingyixiangliang_xiangliangshuxing_cbx.currentIndexChanged.connect(self.update_vector_attr)
        self.dingyixiangliang_jisuanfangfa.setCurrentIndex(0)
        self.dingyixiangliang_jisuan_button.clicked.connect(self.compute_vector)

        self.fs = fs
        self.parent = parent
        if not hasattr(self.parent, 'vs'):
            self.parent.vs = {}
        self.vs = self.parent.vs
        self.update_vector_list()
        self.update_vector_combos()

    def retranslateUi(self, widget):
        super().retranslateUi(widget)
        self._populate_vector_combos()

    def _populate_vector_combos(self):
        tr = QCoreApplication.translate
        # 向量属性（保持当前选中索引）
        idx_attr = self.dingyixiangliang_xiangliangshuxing_cbx.currentIndex()
        self.dingyixiangliang_xiangliangshuxing_cbx.clear()
        self.dingyixiangliang_xiangliangshuxing_cbx.addItems([
            tr("dingyixiangliang", "表达式"),
            tr("dingyixiangliang", "模"),
            tr("dingyixiangliang", "方向角"),
            tr("dingyixiangliang", "单位向量"),
        ])
        if 0 <= idx_attr < self.dingyixiangliang_xiangliangshuxing_cbx.count():
            self.dingyixiangliang_xiangliangshuxing_cbx.setCurrentIndex(idx_attr)
        # 计算方法
        idx_func = self.dingyixiangliang_jisuanfangfa.currentIndex()
        self.dingyixiangliang_jisuanfangfa.clear()
        self.dingyixiangliang_jisuanfangfa.addItems([
            tr("dingyixiangliang", "加法"),
            tr("dingyixiangliang", "减法"),
            tr("dingyixiangliang", "点积"),
            tr("dingyixiangliang", "夹角"),
        ])
        if 0 <= idx_func < self.dingyixiangliang_jisuanfangfa.count():
            self.dingyixiangliang_jisuanfangfa.setCurrentIndex(idx_func)

    def update_vector_list(self):
        # 刷新向量列表
        self.dingyixiangliang_xiangliangliebiao.clear()
        self.dingyixiangliang_xiangliangliebiao.insertItems(0,
            list("{}=({}, {})".format(self.vs[n][0], self.vs[n][1], self.vs[n][2]) for n in self.vs.keys()))

    def update_vector_combos(self):
        # 刷新向量运算区的下拉框
        self.dingyixiangliang_xiangliang1.clear()
        self.dingyixiangliang_xiangliang2.clear()
        names = list(self.vs.keys())
        self.dingyixiangliang_xiangliang1.addItems(names)
        self.dingyixiangliang_xiangliang2.addItems(names)

    def read_vector(self, item):
        # 读取向量信息，显示在编辑区
        name = item.text().split('=')[0]
        if name in self.vs:
            self.dingyixiangliang_mingcheng.setText(self.vs[name][0])
            self.dingyixiangliang_x.setText(self.vs[name][1])
            self.dingyixiangliang_y.setText(self.vs[name][2])
        self.dingyixiangliang_xiangliangshuxing_cbx.setCurrentIndex(0)
        self.update_vector_attr(0)

    def save_vector(self):
        # 保存向量信息
        name = self.dingyixiangliang_mingcheng.text()
        x = self.dingyixiangliang_x.text()
        y = self.dingyixiangliang_y.text()
        if name not in self.vs:
            self.dingyixiangliang_xiangliangliebiao.insertItem(0, "{}=({}, {})".format(name, x, y))
            self.dingyixiangliang_xiangliangliebiao.setCurrentRow(0)
        self.vs[name] = [name, x, y]
        self.update_vector_combos()
        self.dingyixiangliang_xiangliangshuxing_cbx.setCurrentIndex(0)
        self.update_vector_attr(0)

    def delete_vector(self):
        # 删除向量
        row = self.dingyixiangliang_xiangliangliebiao.currentRow()
        if row < 0:
            return
        item = self.dingyixiangliang_xiangliangliebiao.takeItem(row)
        name = self.dingyixiangliang_mingcheng.text()
        if name in self.vs:
            del self.vs[name]
        del item
        self.update_vector_combos()
        if self.vs:
            self.read_vector(self.dingyixiangliang_xiangliangliebiao.currentItem())
        self.update_vector_attr(0)

    def update_vector_attr(self, attr):
        # 计算并显示向量属性
        x_str = self.dingyixiangliang_x.text()
        y_str = self.dingyixiangliang_y.text()
        name = self.dingyixiangliang_mingcheng.text()
        try:
            x = sympify(x_str, self.fs)
            y = sympify(y_str, self.fs)
        except:
            return

        from sympy import sqrt, atan2

        if attr == 0:  # 表达式
            result = "({}, {})".format(x, y)
            latex_str = "\\vec{{{}}}=({}, {})".format(name, latex(x), latex(y))
        elif attr == 1:  # 模
            result = simplify(sqrt(x**2 + y**2))
            latex_str = "|\\vec{{{}}}|=".format(name) + latex(result)
        elif attr == 2:  # 方向角
            result = simplify(atan2(y, x))
            latex_str = "\\theta_{{{}}}=".format(name) + latex(result)
        elif attr == 3:  # 单位向量
            mag = sqrt(x**2 + y**2)
            ux = simplify(x / mag)
            uy = simplify(y / mag)
            result = "({}, {})".format(ux, uy)
            latex_str = "\\hat{{\\vec{{{}}}}}=({}, {})".format(name, latex(ux), latex(uy))
        else:
            return

        self.dingyixiangliang_xiangliangshuxing_lineedit.setText(str(result))
        try:
            setGraphicsView('', latex_str, self.dingyixiangliang_xiangliangshuxing)
        except:
            pass

    def compute_vector(self):
        # 执行向量运算
        v1_name = self.dingyixiangliang_xiangliang1.currentText()
        v2_name = self.dingyixiangliang_xiangliang2.currentText()
        method = self.dingyixiangliang_jisuanfangfa.currentIndex()

        if not v1_name or not v2_name or v1_name not in self.vs or v2_name not in self.vs:
            return

        try:
            x1 = sympify(self.vs[v1_name][1], self.fs)
            y1 = sympify(self.vs[v1_name][2], self.fs)
            x2 = sympify(self.vs[v2_name][1], self.fs)
            y2 = sympify(self.vs[v2_name][2], self.fs)
        except:
            return

        from sympy import sqrt, acos

        if method == 0:  # 加法
            rx = simplify(x1 + x2)
            ry = simplify(y1 + y2)
            result = "({}, {})".format(rx, ry)
            latex_str = "\\vec{{{}}}+\\vec{{{}}}=({}, {})".format(v1_name, v2_name, latex(rx), latex(ry))
        elif method == 1:  # 减法
            rx = simplify(x1 - x2)
            ry = simplify(y1 - y2)
            result = "({}, {})".format(rx, ry)
            latex_str = "\\vec{{{}}}-\\vec{{{}}}=({}, {})".format(v1_name, v2_name, latex(rx), latex(ry))
        elif method == 2:  # 点积
            dot = simplify(x1 * x2 + y1 * y2)
            result = dot
            latex_str = "\\vec{{{}}}\\cdot\\vec{{{}}}=".format(v1_name, v2_name) + latex(dot)
        elif method == 3:  # 夹角
            dot = x1 * x2 + y1 * y2
            mag1 = sqrt(x1**2 + y1**2)
            mag2 = sqrt(x2**2 + y2**2)
            cos_theta = simplify(dot / (mag1 * mag2))
            angle = simplify(acos(cos_theta))
            result = angle
            latex_str = "\\angle(\\vec{{{}}},\\vec{{{}}})=".format(v1_name, v2_name) + latex(angle)
        else:
            return

        self.dingyixiangliang_jisuan_lineedit.setText(str(result))
        try:
            setGraphicsView('', latex_str, self.dingyixiangliang_jisuan)
        except:
            pass
        