from ui.ui_jisuan import *
from core.sympify import sympify
from core.render import setGraphicsView, setGraphicsViewTheme
from sympy import latex, radsimp
from PySide6.QtWidgets import QWidget

class Jisuan(QWidget, Ui_jisuan):
    def __init__(self, parent, fs):
        super(Jisuan, self).__init__(parent)
        self.setupUi(self)
        setGraphicsViewTheme(self, parent)

        self.jisuan_jisuanyinqing.addItems(["Python内置引擎", "Mpmath高精度引擎", "Sympy符号引擎", "Latex代码生成引擎"])
        self.jisuan_jisuanyinqing.currentIndexChanged.connect(self.jisuan_jisuanyinqing_f)
        self.jisuan_jisuan_button.clicked.connect(self.jisuan_button_f)
        self.jisuan_input.textChanged.connect(self.setjisuan_yuanshi)
        self.jisuan_input.returnPressed.connect(self.jisuan_jisuan_button.click)

        self.fs = fs
        self.parent = parent

        self.jisuan_jisuanyinqing_f()
    
    def setjisuan_yuanshi(self):
        # 加载原式
        try:
            setGraphicsView("", self.jisuan_input.text(), self.jisuan_yuanshi)
        except:
            pass
    
    def jisuan_jisuanyinqing_f(self):
        # 识别计算引擎并更改文本框状态
        if self.jisuan_jisuanyinqing.currentIndex() == 1:
            self.jisuan_jingdu.setEnabled(True)
        else:
            self.jisuan_jingdu.setEnabled(False)

    def jisuan_button_f(self):
        # 计算结果
        import sys
        sys.set_int_max_str_digits(0)
        def show(result, view_is_latex = False, lineedit_is_latex = False):
            setGraphicsView("", latex(result), self.jisuan_jisuanjieguo)
            self.jisuan_jisuanjieguo_lineedit.setMaxLength(len(str(latex(result) if lineedit_is_latex else result)) + 1)
            self.jisuan_jisuanjieguo_lineedit.setText(str(latex(result) if lineedit_is_latex else result))
        if self.jisuan_jisuanyinqing.currentIndex() == 0:
            result = eval(self.jisuan_input.text())
            show(result)
        elif self.jisuan_jisuanyinqing.currentIndex() == 1:
            import mpmath as mp
            from mpmath import sin, cos, tan, cot, sec, csc, sinh, cosh, tanh, coth, sech, csch, exp, log, ln, sqrt, root, pi, e, phi
            with mp.workdps(int(self.jisuan_jingdu.text())):
                result = eval(self.jisuan_input.text())
                show(result)
        elif self.jisuan_jisuanyinqing.currentIndex() == 2:
            result = radsimp(sympify(self.jisuan_input.text(), self.fs, is_simplify = True))
            show(result, True)
        elif self.jisuan_jisuanyinqing.currentIndex() == 3:
            show(sympify(self.jisuan_input.text(), fs = {}), True, True)
