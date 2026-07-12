from ui.ui_jifen import *
from functions.integral import integral
from core.sympify import sympify
from core.render import setGraphicsView, setGraphicsViewTheme
from sympy import latex
from PySide6.QtWidgets import QWidget

class Jifen(QWidget, Ui_jifen):
    def __init__(self, parent, fs):
        super(Jifen, self).__init__(parent)
        self.setupUi(self)
        setGraphicsViewTheme(self, parent)

        self.jifen_input.textChanged.connect(self.setjifen_beijihanshu)
        self.jifen_input.returnPressed.connect(self.jifen_jifen_button.click)
        self.jifen_jifen_button.clicked.connect(self.jifen_button_f)
        self.jifen_dingjifen.stateChanged.connect(self.jifen_dingjifen_f)

        self.fs = fs
        self.parent = parent

    def setjifen_beijihanshu(self):
        # 加载原函数
        try:
            setGraphicsView('f(x)=', latex(sympify(self.jifen_input.text(), self.fs)), self.jifen_beijihanshu)
        except:
            pass

    def jifen_dingjifen_f(self):
        # 更改求解模式:是否定积分
        self.is_dingjifen = self.jifen_dingjifen.isChecked()
        self.jifen_shangxianzhi.setEnabled(self.jifen_dingjifen.isChecked())
        self.jifen_xiaxianzhi.setEnabled(self.jifen_dingjifen.isChecked())

    def jifen_button_f(self):
        # 积分
        self.is_dingjifen = self.jifen_dingjifen.isChecked()
        if self.is_dingjifen:
            F = integral(self.jifen_input.text(), self.jifen_jifenbianliang.text(), self.fs)
            setGraphicsView('F(x)=', latex(F), self.jifen_yuanhanshu)
            self.jifen_yuanhanshu_lineedit.setText(str(F))
            F = integral(self.jifen_input.text(), self.jifen_jifenbianliang.text(), self.jifen_xiaxianzhi.text(), self.jifen_shangxianzhi.text(), self.fs)
            setGraphicsView('F(x)=', latex(F), self.jifen_dingjifenzhi)
            self.jifen_dingjifenzhi_lineedit.setText(str(F))
            
        else:
            self.jifen_dingjifenzhi.setHtml("")
            F = integral(self.jifen_input.text(), self.jifen_jifenbianliang.text(), self.fs)
            setGraphicsView('F(x)=', latex(F), self.jifen_yuanhanshu)
            self.jifen_yuanhanshu_lineedit.setText(str(F))
