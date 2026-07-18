from ui.ui_budengshi import *
from functions.solvers import solve_budengshi
from core.sympify import sympify
from core.render import setGraphicsView, setGraphicsViewTheme
from sympy import latex, Rel
from PySide6.QtWidgets import QWidget

class Budengshi(QWidget, Ui_budengshi):
    def __init__(self, parent, fs):
        super(Budengshi, self).__init__(parent)
        self.setupUi(self)
        setGraphicsViewTheme(self, parent)

        self.budengshi_budenghao.addItems(["!=", ">", ">=", "<", "<="])
        self.budengshi_budenghao.currentIndexChanged.connect(self.setbudengshi_yuanshi)
        self.budengshi_zuoshi.textChanged.connect(self.setbudengshi_yuanshi)
        self.budengshi_youshi.textChanged.connect(self.setbudengshi_yuanshi)
        self.budengshi_quzhifanwei.textChanged.connect(self.setbudengshi_yuanshi)
        self.budengshi_zuoshi.returnPressed.connect(self.budengshi_qiujie.click)
        self.budengshi_youshi.returnPressed.connect(self.budengshi_qiujie.click)
        self.budengshi_quzhifanwei.returnPressed.connect(self.budengshi_qiujie.click)
        self.budengshi_qiujie.clicked.connect(self.budengshi_button_f)

        self.fs = fs
        self.parent = parent

    def setbudengshi_yuanshi(self):
        # 加载原不等式
        try:
            self.rel_budengshi = Rel(sympify(self.budengshi_zuoshi.text(), self.fs), sympify(self.budengshi_youshi.text(), self.fs), self.budengshi_budenghao.currentText())
            setGraphicsView('', '{}\\quad (x\\in {})'.format(latex(self.rel_budengshi), latex(sympify(self.budengshi_quzhifanwei.text(), self.fs))), self.budengshi_yuanshi)
        except:
            pass

    def budengshi_button_f(self):
        # 求解不等式
        self.jieji_budengshi = solve_budengshi(self.rel_budengshi, self.budengshi_zhuyuanfuhao.text(), self.budengshi_quzhifanwei.text(), self.fs)
        setGraphicsView('', latex(self.jieji_budengshi), self.budengshi_jieji)
        self.budengshi_jieji_lineedit.setText(str(self.jieji_budengshi))
