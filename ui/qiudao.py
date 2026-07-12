from ui.ui_qiudao import *
from functions.derivative import derivative, yinhanshu_derivative
from core.sympify import sympify
from core.render import setGraphicsView, setGraphicsViewTheme
from sympy import latex
from PySide6.QtWidgets import QWidget

class Qiudao(QWidget, Ui_qiudao):
    def __init__(self, parent, fs):
        super(Qiudao, self).__init__(parent)
        self.setupUi(self)
        setGraphicsViewTheme(self, parent)
        
        self.qiudao_input.textChanged.connect(self.setqiudao_yuanhanshu)
        self.qiudao_input.returnPressed.connect(self.qiudao_qiudao_button.click)
        self.qiudao_qiudao_button.clicked.connect(self.qiudao_button_f)
        self.qiudao_yinhanshu.stateChanged.connect(self.qiudao_yinhanshu_f)
        self.qiudao_qiuchujutizhi.stateChanged.connect(self.qiudao_jutizhi_f)

        self.fs = fs
        self.parent = parent
        
    def setqiudao_yuanhanshu(self):
        # 加载原函数
        try:
            setGraphicsView('f(x)=', latex(sympify(self.qiudao_input.text(), self.fs)), self.qiudao_yuanhanshu)
        except:
            pass

    def qiudao_yinhanshu_f(self):
        # 更改求解模式:是否隐函数
        self.is_yinhanshu = self.qiudao_yinhanshu.isChecked()
        self.qiudao_yinbianliang.setEnabled(self.qiudao_yinhanshu.isChecked())

    def qiudao_jutizhi_f(self):
        # 更改求解模式:是否具体值
        self.is_jutizhi = self.qiudao_qiuchujutizhi.isChecked()
        self.qiudao_zibianliangzhi.setEnabled(self.qiudao_qiuchujutizhi.isChecked())

    def qiudao_button_f(self):
        # 求导
        self.is_yinhanshu = self.qiudao_yinhanshu.isChecked()
        self.is_jutizhi = self.qiudao_qiuchujutizhi.isChecked()
        if self.is_yinhanshu:
            if self.is_jutizhi:
                dif = yinhanshu_derivative(self.qiudao_input.text(), self.qiudao_zibianliang.text(), self.qiudao_yinbianliang.text(), self.qiudao_qiudaocishu.text(), None, self.fs)
                setGraphicsView("f'(x)=", latex(dif), self.qiudao_daohanshu)
                self.qiudao_daohanshu_lineedit.setText(str(dif))
                dif = yinhanshu_derivative(self.qiudao_input.text(), self.qiudao_zibianliang.text(), self.qiudao_yinbianliang.text(), self.qiudao_qiudaocishu.text(), self.qiudao_zibianliangzhi.text(), self.fs)
                setGraphicsView("f'({})=".format(self.qiudao_zibianliangzhi.text()), latex(dif), self.qiudao_daoshuzhi)
                self.qiudao_daoshuzhi_lineedit.setText(str(dif))
            else:
                dif = yinhanshu_derivative(self.qiudao_input.text(), self.qiudao_zibianliang.text(), self.qiudao_yinbianliang.text(), self.qiudao_qiudaocishu.text(), None, self.fs)
                setGraphicsView("f'(x)=", latex(dif), self.qiudao_daohanshu)
                self.qiudao_daohanshu_lineedit.setText(str(dif))
        else:
            if self.is_jutizhi:
                dif = derivative(self.qiudao_input.text(), self.qiudao_zibianliang.text(), self.qiudao_qiudaocishu.text(), None, self.fs)
                setGraphicsView("f'(x)=", latex(dif), self.qiudao_daohanshu)
                self.qiudao_daohanshu_lineedit.setText(str(dif))
                dif = derivative(self.qiudao_input.text(), self.qiudao_zibianliang.text(), self.qiudao_qiudaocishu.text(), self.qiudao_zibianliangzhi.text(), self.fs)
                setGraphicsView("f'({})=".format(self.qiudao_zibianliangzhi.text()), latex(dif), self.qiudao_daoshuzhi)
                self.qiudao_daoshuzhi_lineedit.setText(str(dif))
            else:
                dif = derivative(self.qiudao_input.text(), self.qiudao_zibianliang.text(), self.qiudao_qiudaocishu.text(), None, self.fs)
                setGraphicsView("f'(x)=", latex(dif), self.qiudao_daohanshu)
                self.qiudao_daohanshu_lineedit.setText(str(dif))
