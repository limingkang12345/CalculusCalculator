from ui.ui_budengshizu import *
from functions.solvers import solve_budengshizu
from core.sympify import sympify
from core.render import setGraphicsView, setGraphicsViewTheme
from sympy import latex, Rel, Symbol
from PySide6.QtWidgets import QWidget

class Budengshizu(QWidget, Ui_budengshizu):
    def __init__(self, parent, fs):
        super(Budengshizu, self).__init__(parent)
        self.setupUi(self)
        setGraphicsViewTheme(self, parent)

        self.budengshizu_budenghao.addItems(["!=", ">", ">=", "<", "<="])
        self.budengshizu_baocun.clicked.connect(self.save_budengshi)
        self.budengshizu_shanchu.clicked.connect(self.delete_budengshi)
        self.budengshizu_budengshi.itemClicked.connect(self.read_budengshi)
        self.budengshizu_qiujie.clicked.connect(self.budengshizu_button_f)
        self.budengshizu_zuoshi.returnPressed.connect(self.budengshizu_baocun.click)
        self.budengshizu_youshi.returnPressed.connect(self.budengshizu_baocun.click)

        self.fs = fs
        self.parent = parent

        for i in self.parent.rels.keys():
            self.budengshizu_budengshi.addItem(i)

    def read_budengshi(self, item):
        # 读取不等式并显示
        setGraphicsView('', latex(self.parent.rels[item.text()]), self.budengshizu_yuanbudengshi)
        self.budengshizu_zuoshi.setText(str(self.parent.rels[item.text()].lhs))
        self.budengshizu_youshi.setText(str(self.parent.rels[item.text()].rhs))

    def setbudengshizu_yuanbudengshi(self):
        # 切换至当前选项卡时加载不等式
        if self.budengshizu_budengshi.count() != 0:
            self.read_budengshi(self.budengshizu_budengshi.currentItem())

    def save_budengshi(self):
        # 保存不等式
        if Rel(sympify(self.budengshizu_zuoshi.text(), self.fs), sympify(self.budengshizu_youshi.text(), self.fs), self.budengshizu_budenghao.currentText()) not in self.parent.rels.values():
            self.parent.rels[str(Rel(sympify(self.budengshizu_zuoshi.text(), self.fs), sympify(self.budengshizu_youshi.text(), self.fs), self.budengshizu_budenghao.currentText()))] = \
                Rel(sympify(self.budengshizu_zuoshi.text(), self.fs), sympify(self.budengshizu_youshi.text(), self.fs), self.budengshizu_budenghao.currentText())
            self.budengshizu_budengshi.addItem(str(Rel(sympify(self.budengshizu_zuoshi.text(), self.fs), sympify(self.budengshizu_youshi.text(), self.fs), self.budengshizu_budenghao.currentText())))
            self.budengshizu_budengshi.setCurrentRow(self.budengshizu_budengshi.count() - 1)
        else:
            self.parent.rels[str(Rel(sympify(self.budengshizu_zuoshi.text(), self.fs), sympify(self.budengshizu_youshi.text(), self.fs), self.budengshizu_budenghao.currentText()))] = \
                Rel(sympify(self.budengshizu_zuoshi.text(), self.fs), sympify(self.budengshizu_youshi.text(), self.fs), self.budengshizu_budenghao.currentText())
        self.read_budengshi(self.budengshizu_budengshi.currentItem())
    
    def delete_budengshi(self):
        # 删除不等式
        budengshi = self.budengshizu_budengshi.takeItem(self.budengshizu_budengshi.currentRow())
        del self.parent.rels[budengshi.text()]
        del budengshi
        if self.parent.rels != {}:
            self.read_budengshi(self.budengshizu_budengshi.currentItem())

    def budengshizu_button_f(self):
        # 求解不等式组
        try:
            result = solve_budengshizu(list(self.parent.rels.values()), Symbol(self.budengshizu_ziyoubianliang.text()), self.fs) \
                if solve_budengshizu(list(self.parent.rels.values()), Symbol(self.budengshizu_ziyoubianliang.text()), self.fs) else "无解"
        except:
            result = "无解"
        setGraphicsView('', latex(result), self.budengshizu_jieji)
        self.budengshizu_jieji_lineedit.setText(str(result))
        