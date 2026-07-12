from ui.ui_fangcheng import *
from functions.solvers import solve_fangcheng, solve_weifenfangcheng
from core.sympify import sympify
from core.render import setGraphicsView, setGraphicsViewTheme
from sympy import latex, Eq
from PySide6.QtWidgets import QWidget

class Fangcheng(QWidget, Ui_fangcheng):
    def __init__(self, parent, fs):
        super(Fangcheng, self).__init__(parent)
        self.setupUi(self)
        setGraphicsViewTheme(self, parent)

        self.fangcheng_zuoshi.textChanged.connect(self.setfangcheng_yuanfangcheng)
        self.fangcheng_youshi.textChanged.connect(self.setfangcheng_yuanfangcheng)
        self.fangcheng_quzhifanwei.textChanged.connect(self.setfangcheng_yuanfangcheng)
        self.fangcheng_zuoshi.returnPressed.connect(self.fangcheng_qiujie.click)
        self.fangcheng_youshi.returnPressed.connect(self.fangcheng_qiujie.click)
        self.fangcheng_quzhifanwei.returnPressed.connect(self.fangcheng_qiujie.click)
        self.fangcheng_weifenfangcheng.stateChanged.connect(self.fangcheng_weifenfangcheng_f)
        self.fangcheng_qiujie.clicked.connect(self.fangcheng_button_f)

        self.fs = fs
        self.parent = parent

    def setfangcheng_yuanfangcheng(self):
        # 加载原方程
        try:
            self.eq_fangcheng = Eq(sympify(self.fangcheng_zuoshi.text(), self.fs if not self.fangcheng_weifenfangcheng.isChecked() else {}), \
                                   sympify(self.fangcheng_youshi.text(), self.fs if not self.fangcheng_weifenfangcheng.isChecked() else {}))
            setGraphicsView('','{} (x\\in {})'.format(latex(self.eq_fangcheng), latex(sympify(self.fangcheng_quzhifanwei.text(), self.fs))) if not self.fangcheng_weifenfangcheng.isChecked() \
                                  else latex(self.eq_fangcheng), self.fangcheng_yuanfangcheng)
        except:
            pass

    def fangcheng_weifenfangcheng_f(self):
        # 更改求解模式:是否微分方程
        self.fangcheng_zhuyuanfuhao.setText("f(x)" if self.fangcheng_weifenfangcheng.isChecked() else "x")
        self.fangcheng_zhuyuanfuhao.setEnabled(not self.fangcheng_weifenfangcheng.isChecked())
        self.fangcheng_quzhifanwei.setText("" if self.fangcheng_weifenfangcheng.isChecked() else "Reals")
        self.fangcheng_quzhifanwei.setEnabled(not self.fangcheng_weifenfangcheng.isChecked())

    def fangcheng_button_f(self):
        # 求解方程
        if self.fangcheng_weifenfangcheng.isChecked():
            self.jieji_fangcheng = solve_weifenfangcheng(self.eq_fangcheng, self.fangcheng_zhuyuanfuhao.text(), self.fs)
            setGraphicsView('', latex(self.jieji_fangcheng), self.fangcheng_jieji)
            self.fangcheng_jieji_lineedit.setText(str(self.jieji_fangcheng))
        else:
            self.jieji_fangcheng = solve_fangcheng(self.eq_fangcheng, self.fangcheng_zhuyuanfuhao.text(), self.fangcheng_quzhifanwei.text(), self.fs)
            setGraphicsView('', latex(self.jieji_fangcheng), self.fangcheng_jieji)
            self.fangcheng_jieji_lineedit.setText(str(self.jieji_fangcheng))
