from ui.ui_bianxing import *
from functions.simplification import simplifies
from core.sympify import sympify
from core.render import setGraphicsView, setGraphicsViewTheme
from sympy import latex
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QCoreApplication

class Bianxing(QWidget, Ui_bianxing):
    def __init__(self, parent, fs):
        super(Bianxing, self).__init__(parent)
        self.setupUi(self)
        setGraphicsViewTheme(self, parent)

        self._populate_transform_combo()
        self.bianxing_bianxingfangfa.currentIndexChanged.connect(self.bianxing_bianxingfangfa_f)

        self.fs = fs
        self.parent = parent

    def retranslateUi(self, widget):
        super().retranslateUi(widget)
        self._populate_transform_combo()

    def _populate_transform_combo(self):
        tr = QCoreApplication.translate
        self.bianxing_bianxingfangfa.clear()
        self.bianxing_bianxingfangfa.addItems([
            tr("bianxing", "通用化简(simplify)"),
            tr("bianxing", "展开(expand)"),
            tr("bianxing", "因式分解(factor)"),
            tr("bianxing", "主元(collect)"),
            tr("bianxing", "通分(cancel)"),
            tr("bianxing", "分离(apart)"),
            tr("bianxing", "三角变换(trigsimp)"),
            tr("bianxing", "三角展开(expand_trig)"),
            tr("bianxing", "指数合并(powsimp)"),
            tr("bianxing", "指数展开(expand_power_exp)"),
            tr("bianxing", "对数展开(expand_log)"),
            tr("bianxing", "对数合并(logcombine)"),
            tr("bianxing", "换元"),
        ])
        self.bianxing_bianxingfangfa.setCurrentIndex(0)
        self.bianxing_input.textChanged.connect(self.setbianxing_yuanshi)
        self.bianxing_input.returnPressed.connect(self.bianxing_bianxing_button.click)
        self.bianxing_bianxing_button.clicked.connect(self.bianxing_button_f)


    def setbianxing_yuanshi(self):
        # 加载原式
        try:
            setGraphicsView('', latex(sympify(self.bianxing_input.text(), self.fs)), self.bianxing_yuanshi)
        except:
            pass

    def bianxing_bianxingfangfa_f(self):
        # 识别变形方法并更改文本框状态
        if self.bianxing_bianxingfangfa.currentIndex() == 3:
            self.bianxing_zhuyuanfuhao.setEnabled(True)
            self.bianxing_huanyuanfuhao.setEnabled(False)
            self.bianxing_huanyuanshi.setEnabled(False)
        elif self.bianxing_bianxingfangfa.currentIndex() == 12:
            self.bianxing_zhuyuanfuhao.setEnabled(True)
            self.bianxing_huanyuanfuhao.setEnabled(True)
            self.bianxing_huanyuanshi.setEnabled(True)
        else:
            self.bianxing_zhuyuanfuhao.setEnabled(False)
            self.bianxing_huanyuanfuhao.setEnabled(False)
            self.bianxing_huanyuanshi.setEnabled(False)

    def bianxing_button_f(self):
        # 变形
        self.bianxingfangfa = self.bianxing_bianxingfangfa.currentIndex()
        self.bianxingshi = simplifies(self.bianxing_input.text(), self.bianxingfangfa, self.bianxing_zhuyuanfuhao.text() if self.bianxing_zhuyuanfuhao.isEnabled() else None, \
            self.bianxing_huanyuanfuhao.text() if self.bianxing_huanyuanfuhao.isEnabled() else None, self.bianxing_huanyuanshi.text() if self.bianxing_huanyuanshi.isEnabled() else None, self.fs)
        setGraphicsView('', latex(self.bianxingshi), self.bianxing_bianxingshi)
        self.bianxing_bianxingshi_lineedit.setText(str(self.bianxingshi))
