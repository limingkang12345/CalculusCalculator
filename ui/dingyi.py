from ui.ui_dingyi import *
from functions.functions import get_function_attr
from core.sympify import sympify
from core.render import setGraphicsView, setGraphicsViewTheme
from sympy import latex, symbols, radsimp
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QCoreApplication

class Dingyi(QWidget, Ui_dingyi):
    def __init__(self, parent, fs):
        super(Dingyi, self).__init__(parent)
        self.setupUi(self)
        setGraphicsViewTheme(self, parent)
        
        self.dingyi_hanshuliebiao.itemClicked.connect(self.read_function)
        self.dingyi_baocun.clicked.connect(self.save_function)
        self.dingyi_shanchu.clicked.connect(self.delete_function)
        self.dingyi_mingcheng.returnPressed.connect(self.dingyi_baocun.click)
        self.dingyi_biaodashi.returnPressed.connect(self.dingyi_baocun.click)
        self.dingyi_dingyiyu.returnPressed.connect(self.dingyi_baocun.click)
        self.dingyi_zibianliang.returnPressed.connect(self.dingyi_baocun.click)
        self._populate_attr_combo()
        self.dingyi_hanshushuxing_cbx.setCurrentIndex(0)
        self.dingyi_hanshushuxing_cbx.currentIndexChanged.connect(self.update_function_attr)
        self.dingyi_zibianliangzhi.textChanged.connect(self.function_value)

        self.fs = fs
        self.parent = parent
        self.dingyi_hanshuliebiao.insertItems(0, list("{}({})".format(self.fs[i][0], self.fs[i][3]) for i in self.fs.keys()))

    def retranslateUi(self, widget):
        super().retranslateUi(widget)
        self._populate_attr_combo()

    def _populate_attr_combo(self):
        self.dingyi_hanshushuxing_cbx.clear()
        self.dingyi_hanshushuxing_cbx.addItems([
            QCoreApplication.translate("dingyi", "表达式&定义域"),
            QCoreApplication.translate("dingyi", "值域"),
            QCoreApplication.translate("dingyi", "单调递增区间"),
            QCoreApplication.translate("dingyi", "单调递减区间"),
            QCoreApplication.translate("dingyi", "奇偶性"),
            QCoreApplication.translate("dingyi", "周期"),
            QCoreApplication.translate("dingyi", "最大值"),
            QCoreApplication.translate("dingyi", "最小值"),
        ])
    
    def read_function(self, item):
        # 读取函数信息，显示在文本框中
        fn = item.text().split('(')[0]
        if fn != '':
            self.dingyi_mingcheng.setText(self.fs[fn][0])
            self.dingyi_biaodashi.setText(self.fs[fn][1])
            self.dingyi_dingyiyu.setText(self.fs[fn][2])
            self.dingyi_zibianliang.setText(self.fs[fn][3])
        self.dingyi_hanshushuxing_cbx.setCurrentIndex(0)
        self.update_function_attr(0)
        self.function_value()

    def setdingyi_hanshushuxing_view(self):
        # 切换至定义页面渲染公式
        self.read_function(self.dingyi_hanshuliebiao.currentItem())

    def save_function(self):
        # 保存函数信息，显示在列表中
        if self.dingyi_mingcheng.text() not in self.fs.keys():
            self.dingyi_hanshuliebiao.insertItem(0, "{}({})".format(self.dingyi_mingcheng.text(), self.dingyi_zibianliang.text()))
            self.dingyi_hanshuliebiao.setCurrentRow(0)
        self.fs[self.dingyi_mingcheng.text()] = [self.dingyi_mingcheng.text(), str(sympify(self.dingyi_biaodashi.text(), self.fs)), self.dingyi_dingyiyu.text(), self.dingyi_zibianliang.text()]
        self.dingyi_hanshushuxing_cbx.setCurrentIndex(0)
        self.update_function_attr(0)
        self.function_value()

    def delete_function(self):
        # 删除相应的函数
        f = self.dingyi_hanshuliebiao.takeItem(self.dingyi_hanshuliebiao.currentRow())
        del f
        del self.fs[self.dingyi_mingcheng.text()]
        if self.fs != {}:
            self.read_function(self.dingyi_hanshuliebiao.currentItem())
        self.update_function_attr(0)
        self.function_value()

    def update_function_attr(self, attr):
        # 获取函数属性并显示
        function_attr = get_function_attr(self.dingyi_biaodashi.text(), self.dingyi_zibianliang.text(), self.dingyi_dingyiyu.text(), attr, self.fs)
        self.dingyi_hanshushuxing_lineedit.setText(str(function_attr))
        try:
            setGraphicsView('' if self.dingyi_hanshushuxing_cbx.currentIndex() != 0 else self.dingyi_hanshuliebiao.currentItem().text() + "=", \
                latex(function_attr) if self.dingyi_hanshushuxing_cbx.currentIndex() != 0 else latex(function_attr[0]) + '({}\\in {})'.format(self.dingyi_zibianliang.text(), latex(function_attr[1])), \
                self.dingyi_hanshushuxing)
        except:
            pass

    def function_value(self):
        # 根据给定自变量值求出函数值
        f_value = radsimp(sympify(self.dingyi_biaodashi.text(), self.fs).subs(symbols(self.dingyi_zibianliang.text()), sympify(self.dingyi_zibianliangzhi.text(), self.fs)))
        self.dingyi_qiuzhi_lineedit.setText(str(f_value))
        try:
            setGraphicsView("{}({})=".format(self.dingyi_mingcheng.text(), latex(sympify(self.dingyi_zibianliangzhi.text(), self.fs))), latex(f_value), self.dingyi_qiuzhi)
        except:
            pass