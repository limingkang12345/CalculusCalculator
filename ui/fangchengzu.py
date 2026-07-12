from ui.ui_fangchengzu import *
from functions.solvers import solve_fangchengzu
from core.sympify import sympify
from core.render import setGraphicsView, setGraphicsViewTheme
from sympy import latex, Eq, Symbol
from PySide6.QtWidgets import QWidget

class Fangchengzu(QWidget, Ui_fangchengzu):
    def __init__(self, parent, fs):
        super(Fangchengzu, self).__init__(parent)
        self.setupUi(self)
        setGraphicsViewTheme(self, parent)

        self.fangchengzu_baocun.clicked.connect(self.save_fangcheng)
        self.fangchengzu_shanchu.clicked.connect(self.delete_fangcheng)
        self.fangchengzu_fangcheng.itemClicked.connect(self.read_fangcheng)
        self.fangchengzu_qiujie.clicked.connect(self.fangchengzu_button_f)
        self.fangchengzu_zuoshi.returnPressed.connect(self.fangchengzu_baocun.click)
        self.fangchengzu_youshi.returnPressed.connect(self.fangchengzu_baocun.click)

        self.fs = fs
        self.parent = parent

        for i in self.parent.eqs.keys():
            self.fangchengzu_fangcheng.addItem(i)
        
    def read_fangcheng(self, item):
        # 读取方程并显示
        setGraphicsView('', latex(self.parent.eqs[item.text()]), self.fangchengzu_yuanfangcheng)
        self.fangchengzu_zuoshi.setText(str(self.parent.eqs[item.text()].lhs))
        self.fangchengzu_youshi.setText(str(self.parent.eqs[item.text()].rhs))

    def setfangchengzu_yuanfangcheng(self):
        # 切换至当前选项卡时加载不等式
        if self.fangchengzu_fangcheng.count() != 0:
            self.read_fangcheng(self.fangchengzu_fangcheng.currentItem())

    def save_fangcheng(self):
        # 保存方程
        if Eq(sympify(self.fangchengzu_zuoshi.text(), self.fs), sympify(self.fangchengzu_youshi.text(), self.fs)) not in self.parent.eqs.values():
            self.parent.eqs[str(Eq(sympify(self.fangchengzu_zuoshi.text(), self.fs), sympify(self.fangchengzu_youshi.text(), self.fs)))] = Eq(sympify(self.fangchengzu_zuoshi.text(), self.fs), sympify(self.fangchengzu_youshi.text(), self.fs))
            self.fangchengzu_fangcheng.addItem(str(Eq(sympify(self.fangchengzu_zuoshi.text(), self.fs), sympify(self.fangchengzu_youshi.text(), self.fs))))
            self.fangchengzu_fangcheng.setCurrentRow(self.fangchengzu_fangcheng.count() - 1)
        else:
            self.parent.eqs[str(Eq(sympify(self.fangchengzu_zuoshi.text(), self.fs), sympify(self.fangchengzu_youshi.text(), self.fs)))] = Eq(sympify(self.fangchengzu_zuoshi.text(), self.fs), sympify(self.fangchengzu_youshi.text(), self.fs))
        self.read_fangcheng(self.fangchengzu_fangcheng.currentItem())

    def delete_fangcheng(self):
        # 删除方程
        fangcheng = self.fangchengzu_fangcheng.takeItem(self.fangchengzu_fangcheng.currentRow())
        del self.parent.eqs[fangcheng.text()]
        del fangcheng
        if self.parent.eqs != {}:
            self.read_fangcheng(self.fangchengzu_fangcheng.currentItem())

    def fangchengzu_button_f(self):
        # 求解方程组
        try:
            result = solve_fangchengzu(list(self.parent.eqs.values()), [Symbol(s) for s in self.fangchengzu_ziyoubianliang.text().split(',')], self.fs)
        except:
            result = "无解"
        setGraphicsView('', latex(result).replace(':', "="), self.fangchengzu_jieji)
        self.fangchengzu_jieji_lineedit.setText(str(result))