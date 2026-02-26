from ui import Ui_MainWindow

import resources
from derivative import derivative, yinhanshu_derivative
from integral import integral
from simplification import simplifies
from solvers import solve_fangcheng, solve_weifenfangcheng, solve_fangchengzu, solve_budengshi, solve_budengshizu
from functions import get_function_attr

from sympy import latex, Eq, Rel, symbols, Symbol
from sympify import sympify
import os

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QSplitter, QWidget, QGroupBox, QStackedWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QRect, QUrl

class MainWindow(QMainWindow):
    def __init__(self, parent=None):

        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ps = [self.ui.tabWidget.widget(i).objectName() for i in range(self.ui.tabWidget.count())]
        self.ws = {p.objectName():[[w.parent().objectName(), w.objectName(), str(w.parent().geometry())[15::], str(w.geometry())[15::]] for w in self.ui.tabWidget.findChild(QWidget, p.objectName()).findChildren(QWebEngineView)] \
                   for p in self.ui.tabWidget.findChild(QStackedWidget).children()}
        self.fs, self.eqs, self.rels = {}, {}, {}

        self.setup()

    def setup(self):

        self.ui.tabWidget.currentChanged.connect(self.updateWebEngineView)
        
        self.ui.dingyi_hanshuliebiao.itemClicked.connect(self.read_function)
        self.ui.dingyi_baocun.clicked.connect(self.save_function)
        self.ui.dingyi_shanchu.clicked.connect(self.delete_function)
        self.ui.dingyi_hanshushuxing.addItems(["表达式&定义域", "值域", "单调递增区间", "单调递减区间", "奇偶性", "周期", "最大值", "最小值"])
        self.ui.dingyi_hanshushuxing.setCurrentIndex(0)
        self.ui.dingyi_hanshushuxing.currentIndexChanged.connect(self.update_function_attr)
        self.ui.dingyi_zibianliangzhi.textChanged.connect(self.function_value)

        self.ui.qiudao_input.textChanged.connect(self.setqiudao_yuanhanshu)
        self.ui.qiudao_qiudao_button.clicked.connect(self.qiudao_button_f)
        self.ui.qiudao_yinhanshu.stateChanged.connect(self.qiudao_yinhanshu_f)
        self.ui.qiudao_qiuchujutizhi.stateChanged.connect(self.qiudao_jutizhi_f)

        self.ui.jifen_input.textChanged.connect(self.setjifen_beijihanshu)
        self.ui.jifen_jifen_button.clicked.connect(self.jifen_button_f)
        self.ui.jifen_dingjifen.stateChanged.connect(self.jifen_dingjifen_f)

        self.ui.bianxing_bianxingfangfa.addItems(["通用化简(simplify)", "展开(expand)", "因式分解(factor)", "主元(collect)", "通分(cancel)", "分离(apart)"])
        self.ui.bianxing_bianxingfangfa.addItems(["三角变换(trigsimp)", "三角展开(expand_trig)", "指数合并(powsimp)", "指数展开(expand_power_exp)"])
        self.ui.bianxing_bianxingfangfa.addItems(["对数展开(expand_log)", "对数合并(logcombine)", "换元"])
        self.ui.bianxing_bianxingfangfa.currentIndexChanged.connect(self.bianxing_bianxingfangfa_f)
        self.ui.bianxing_input.textChanged.connect(self.setbianxing_yuanshi)
        self.ui.bianxing_bianxing_button.clicked.connect(self.bianxing_button_f)

        self.ui.fangcheng_zuoshi.textChanged.connect(self.setfangcheng_yuanfangcheng)
        self.ui.fangcheng_youshi.textChanged.connect(self.setfangcheng_yuanfangcheng)
        self.ui.fangcheng_quzhifanwei.textChanged.connect(self.setfangcheng_yuanfangcheng)
        self.ui.fangcheng_weifenfangcheng.stateChanged.connect(self.fangcheng_weifenfangcheng_f)
        self.ui.fangcheng_qiujie.clicked.connect(self.fangcheng_button_f)

        self.ui.fangchengzu_baocun.clicked.connect(self.save_fangcheng)
        self.ui.fangchengzu_shanchu.clicked.connect(self.delete_fangcheng)
        self.ui.fangchengzu_fangcheng.itemClicked.connect(self.read_fangcheng)
        self.ui.fangchengzu_qiujie.clicked.connect(self.fangchengzu_button_f)

        self.ui.budengshi_budenghao.addItems(["!=", ">", ">=", "<", "<="])
        self.ui.budengshi_budenghao.currentIndexChanged.connect(self.setbudengshi_yuanshi)
        self.ui.budengshi_zuoshi.textChanged.connect(self.setbudengshi_yuanshi)
        self.ui.budengshi_youshi.textChanged.connect(self.setbudengshi_yuanshi)
        self.ui.budengshi_quzhifanwei.textChanged.connect(self.setbudengshi_yuanshi)
        self.ui.budengshi_qiujie.clicked.connect(self.budengshi_button_f)

        self.ui.budengshizu_budenghao.addItems(["!=", ">", ">=", "<", "<="])
        self.ui.budengshizu_baocun.clicked.connect(self.save_budengshi)
        self.ui.budengshizu_shanchu.clicked.connect(self.delete_budengshi)
        self.ui.budengshizu_budengshi.itemClicked.connect(self.read_budengshi)
        self.ui.budengshizu_qiujie.clicked.connect(self.budengshizu_button_f)

        layout = QVBoxLayout(self.ui.centralwidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui.tabWidget)

        homepage = QVBoxLayout(self.ui.shouye)
        homepage.setContentsMargins(0, 0, 0, 0)
        homepage.addWidget(self.ui.shouye_welcome)

        self.help_path = QUrl("qrc:///help.html")
        self.ui.webEngineView.setUrl(self.help_path)
        
        self.updateWebEngineView("shouye")

    def setWebEngineView(self, n, l, w):
        # 显示表达式
        # n:函数名
        # l:要显示的Latex表达式
        # w:要设置的WebEngineView
        
        base_url = QUrl.fromLocalFile(os.path.dirname(__file__) + '/')
        html = r'<html><head><script src="qrc:///MathJax/es5/tex-svg.js"></script></head><body><div><p style="font-size:34px">\({}{}\)</p></div></body></html>'.format(n, l)
        w.setHtml(html, base_url)

    def updateWebEngineView(self, arg):
        # 切换页面时创建当前页面渲染框，销毁其他页面渲染框
        p = self.ui.tabWidget.currentWidget().objectName()
        for w in self.ws[p]:
            exec("self.ui.{} = QWebEngineView(self.ui.{})".format(w[1], w[0]))
            exec("self.ui.{}.setObjectName(u'{}')".format(w[1], w[1]))
            exec("self.ui.{}.setGeometry({})".format(w[1], w[3]))
            exec("self.ui.{}.show()".format(w[1]))
            try:
                exec("self.set{}()".format(w[1]))
            except:
                pass
            if w[1] == "webEngineView":
                exec("self.ui.webEngineView.setUrl(self.help_path)")
        for other_p in self.ps:
            if other_p != p:
                for w in self.ws[other_p]:
                    try:
                        self.ui.tabWidget.findChild(QStackedWidget).findChild(QWidget, other_p).findChild(QWebEngineView, w[1]).deleteLater()
                    except:
                        pass
    
    def read_function(self, item):
        # 读取函数信息，显示在文本框中
        fn = item.text().split('(')[0]
        if fn != '':
            self.ui.dingyi_mingcheng.setText(self.fs[fn][0])
            self.ui.dingyi_biaodashi.setText(self.fs[fn][1])
            self.ui.dingyi_dingyiyu.setText(self.fs[fn][2])
            self.ui.dingyi_zibianliang.setText(self.fs[fn][3])
        self.ui.dingyi_hanshushuxing.setCurrentIndex(0)
        self.update_function_attr(0)
        self.function_value()

    def setdingyi_hanshushuxing_view(self):
        # 切换至定义页面渲染公式
        self.read_function(self.ui.dingyi_hanshuliebiao.currentItem())

    def save_function(self):
        # 保存函数信息，显示在列表中
        if self.ui.dingyi_mingcheng.text() not in self.fs.keys():
            self.ui.dingyi_hanshuliebiao.insertItem(0, "{}({})".format(self.ui.dingyi_mingcheng.text(), self.ui.dingyi_zibianliang.text()))
            self.ui.dingyi_hanshuliebiao.setCurrentRow(0)
        self.fs[self.ui.dingyi_mingcheng.text()] = [self.ui.dingyi_mingcheng.text(), self.ui.dingyi_biaodashi.text(), self.ui.dingyi_dingyiyu.text(), self.ui.dingyi_zibianliang.text()]
        self.ui.dingyi_hanshushuxing.setCurrentIndex(0)
        self.update_function_attr(0)
        self.function_value()

    def delete_function(self):
        # 删除相应的函数
        f = self.ui.dingyi_hanshuliebiao.takeItem(self.ui.dingyi_hanshuliebiao.currentRow())
        del f
        del self.fs[self.ui.dingyi_mingcheng.text()]
        if self.fs != {}:
            self.read_function(self.ui.dingyi_hanshuliebiao.currentItem())
        self.update_function_attr(0)
        self.function_value()

    def update_function_attr(self, attr):
        # 获取函数属性并显示
        function_attr = get_function_attr(self.ui.dingyi_biaodashi.text(), self.ui.dingyi_zibianliang.text(), self.ui.dingyi_dingyiyu.text(), attr, self.fs)
        self.ui.dingyi_hanshushuxing_lineedit.setText(str(function_attr))
        try:
            self.setWebEngineView('' if self.ui.dingyi_hanshushuxing.currentIndex() != 0 else self.ui.dingyi_hanshuliebiao.currentItem().text() + "=", \
                latex(function_attr) if self.ui.dingyi_hanshushuxing.currentIndex() != 0 else latex(function_attr[0]) + '({}\\in {})'.format(self.ui.dingyi_zibianliang.text(), latex(function_attr[1])), \
                self.ui.dingyi_hanshushuxing_view)
        except:
            pass

    def function_value(self):
        # 根据给定自变量值求出函数值
        f_value = sympify(self.ui.dingyi_biaodashi.text(), self.fs).subs(symbols(self.ui.dingyi_zibianliang.text()), sympify(self.ui.dingyi_zibianliangzhi.text(), self.fs))
        self.ui.dingyi_qiuzhi_lineedit.setText(str(f_value))
        try:
            self.setWebEngineView("{}({})=".format(self.ui.dingyi_mingcheng.text(), latex(sympify(self.ui.dingyi_zibianliangzhi.text(), self.fs))), latex(f_value), self.ui.dingyi_qiuzhi)
        except:
            pass

    def setqiudao_yuanhanshu(self):
        # 加载原函数
        try:
            self.setWebEngineView('f(x)=', latex(sympify(self.ui.qiudao_input.text(), self.fs)), self.ui.qiudao_yuanhanshu)
        except:
            pass

    def qiudao_yinhanshu_f(self):
        # 更改求解模式:是否隐函数
        self.is_yinhanshu = self.ui.qiudao_yinhanshu.isChecked()
        self.ui.qiudao_yinbianliang.setEnabled(self.ui.qiudao_yinhanshu.isChecked())

    def qiudao_jutizhi_f(self):
        # 更改求解模式:是否具体值
        self.is_jutizhi = self.ui.qiudao_qiuchujutizhi.isChecked()
        self.ui.qiudao_zibianliangzhi.setEnabled(self.ui.qiudao_qiuchujutizhi.isChecked())

    def qiudao_button_f(self):
        # 求导
        self.is_yinhanshu = self.ui.qiudao_yinhanshu.isChecked()
        self.is_jutizhi = self.ui.qiudao_qiuchujutizhi.isChecked()
        if self.is_yinhanshu:
            if self.is_jutizhi:
                dif = yinhanshu_derivative(self.ui.qiudao_input.text(), self.ui.qiudao_zibianliang.text(), self.ui.qiudao_yinbianliang.text(), self.ui.qiudao_qiudaocishu.text(), None, self.fs)
                self.setWebEngineView("f'(x)=", latex(dif), self.ui.qiudao_daohanshu)
                self.ui.qiudao_daohanshu_lineedit.setText(str(dif))
                dif = yinhanshu_derivative(self.ui.qiudao_input.text(), self.ui.qiudao_zibianliang.text(), self.ui.qiudao_yinbianliang.text(), self.ui.qiudao_qiudaocishu.text(), self.ui.qiudao_zibianliangzhi.text(), self.fs)
                self.setWebEngineView("f'({})=".format(self.ui.qiudao_zibianliangzhi.text()), latex(dif), self.ui.qiudao_daoshuzhi)
                self.ui.qiudao_daoshuzhi_lineedit.setText(str(dif))
            else:
                dif = yinhanshu_derivative(self.ui.qiudao_input.text(), self.ui.qiudao_zibianliang.text(), self.ui.qiudao_yinbianliang.text(), self.ui.qiudao_qiudaocishu.text(), None, self.fs)
                self.setWebEngineView("f'(x)=", latex(dif), self.ui.qiudao_daohanshu)
                self.ui.qiudao_daohanshu_lineedit.setText(str(dif))
        else:
            if self.is_jutizhi:
                dif = derivative(self.ui.qiudao_input.text(), self.ui.qiudao_zibianliang.text(), self.ui.qiudao_qiudaocishu.text(), None, self.fs)
                self.setWebEngineView("f'(x)=", latex(dif), self.ui.qiudao_daohanshu)
                self.ui.qiudao_daohanshu_lineedit.setText(str(dif))
                dif = derivative(self.ui.qiudao_input.text(), self.ui.qiudao_zibianliang.text(), self.ui.qiudao_qiudaocishu.text(), self.ui.qiudao_zibianliangzhi.text(), self.fs)
                self.setWebEngineView("f'({})=".format(self.ui.qiudao_zibianliangzhi.text()), latex(dif), self.ui.qiudao_daoshuzhi)
                self.ui.qiudao_daoshuzhi_lineedit.setText(str(dif))
            else:
                dif = derivative(self.ui.qiudao_input.text(), self.ui.qiudao_zibianliang.text(), self.ui.qiudao_qiudaocishu.text(), None, self.fs)
                self.setWebEngineView("f'(x)=", latex(dif), self.ui.qiudao_daohanshu)
                self.ui.qiudao_daohanshu_lineedit.setText(str(dif))

    def setjifen_beijihanshu(self):
        # 加载原函数
        try:
            self.setWebEngineView('f(x)=', latex(sympify(self.ui.jifen_input.text(), self.fs)), self.ui.jifen_beijihanshu)
        except:
            pass

    def jifen_dingjifen_f(self):
        # 更改求解模式:是否定积分
        self.is_dingjifen = self.ui.jifen_dingjifen.isChecked()
        self.ui.jifen_shangxianzhi.setEnabled(self.ui.jifen_dingjifen.isChecked())
        self.ui.jifen_xiaxianzhi.setEnabled(self.ui.jifen_dingjifen.isChecked())

    def jifen_button_f(self):
        # 积分
        self.is_dingjifen = self.ui.jifen_dingjifen.isChecked()
        if self.is_dingjifen:
            F = integral(self.ui.jifen_input.text(), self.ui.jifen_jifenbianliang.text(), self.fs)
            self.setWebEngineView('F(x)=', latex(F), self.ui.jifen_yuanhanshu)
            self.ui.jifen_yuanhanshu_lineedit.setText(str(F))
            F = integral(self.ui.jifen_input.text(), self.ui.jifen_jifenbianliang.text(), self.ui.jifen_xiaxianzhi.text(), self.ui.jifen_shangxianzhi.text(), self.fs)
            self.setWebEngineView('F(x)=', latex(F), self.ui.jifen_dingjifenzhi)
            self.ui.jifen_dingjifenzhi_lineedit.setText(str(F))
            
        else:
            self.ui.jifen_dingjifenzhi.setHtml("")
            F = integral(self.ui.jifen_input.text(), self.ui.jifen_jifenbianliang.text(), self.fs)
            self.setWebEngineView('F(x)=', latex(F), self.ui.jifen_yuanhanshu)
            self.ui.jifen_yuanhanshu_lineedit.setText(str(F))

    def setbianxing_yuanshi(self):
        # 加载原式
        try:
            self.setWebEngineView('', latex(sympify(self.ui.bianxing_input.text(), self.fs)), self.ui.bianxing_yuanshi)
        except:
            pass

    def bianxing_bianxingfangfa_f(self):
        # 识别变形方法并更改文本框状态
        if self.ui.bianxing_bianxingfangfa.currentIndex() == 3:
            self.ui.bianxing_zhuyuanfuhao.setEnabled(True)
            self.ui.bianxing_huanyuanfuhao.setEnabled(False)
            self.ui.bianxing_huanyuanshi.setEnabled(False)
        elif self.ui.bianxing_bianxingfangfa.currentIndex() == 12:
            self.ui.bianxing_zhuyuanfuhao.setEnabled(True)
            self.ui.bianxing_huanyuanfuhao.setEnabled(True)
            self.ui.bianxing_huanyuanshi.setEnabled(True)
        else:
            self.ui.bianxing_zhuyuanfuhao.setEnabled(False)
            self.ui.bianxing_huanyuanfuhao.setEnabled(False)
            self.ui.bianxing_huanyuanshi.setEnabled(False)

    def bianxing_button_f(self):
        # 变形
        self.bianxingfangfa = self.ui.bianxing_bianxingfangfa.currentIndex()
        self.bianxingshi = simplifies(self.ui.bianxing_input.text(), self.bianxingfangfa, self.ui.bianxing_zhuyuanfuhao.text() if self.ui.bianxing_zhuyuanfuhao.isEnabled() else None, \
            self.ui.bianxing_huanyuanfuhao.text() if self.ui.bianxing_huanyuanfuhao.isEnabled() else None, self.ui.bianxing_huanyuanshi.text() if self.ui.bianxing_huanyuanshi.isEnabled() else None, self.fs)
        self.setWebEngineView('', latex(self.bianxingshi), self.ui.bianxing_bianxingshi)
        self.ui.bianxing_bianxingshi_lineedit.setText(str(self.bianxingshi))

    def setfangcheng_yuanfangcheng(self):
        # 加载原方程
            self.eq_fangcheng = Eq(sympify(self.ui.fangcheng_zuoshi.text(), self.fs if not self.ui.fangcheng_weifenfangcheng.isChecked() else {}), \
                                   sympify(self.ui.fangcheng_youshi.text(), self.fs if not self.ui.fangcheng_weifenfangcheng.isChecked() else {}))
            self.setWebEngineView('','{} (x\\in {})'.format(latex(self.eq_fangcheng), latex(sympify(self.ui.fangcheng_quzhifanwei.text(), self.fs))) if not self.ui.fangcheng_weifenfangcheng.isChecked() \
                                  else latex(self.eq_fangcheng), self.ui.fangcheng_yuanfangcheng)

    def fangcheng_weifenfangcheng_f(self):
        # 更改求解模式:是否微分方程
        self.ui.fangcheng_zhuyuanfuhao.setText("f(x)" if self.ui.fangcheng_weifenfangcheng.isChecked() else "x")
        self.ui.fangcheng_zhuyuanfuhao.setEnabled(not self.ui.fangcheng_weifenfangcheng.isChecked())
        self.ui.fangcheng_quzhifanwei.setText("" if self.ui.fangcheng_weifenfangcheng.isChecked() else "Reals")
        self.ui.fangcheng_quzhifanwei.setEnabled(not self.ui.fangcheng_weifenfangcheng.isChecked())

    def fangcheng_button_f(self):
        # 求解方程
        if self.ui.fangcheng_weifenfangcheng.isChecked():
            self.jieji_fangcheng = solve_weifenfangcheng(self.eq_fangcheng, self.ui.fangcheng_zhuyuanfuhao.text(), self.fs)
            self.setWebEngineView('', latex(self.jieji_fangcheng), self.ui.fangcheng_jieji)
            self.ui.fangcheng_jieji_lineedit.setText(str(self.jieji_fangcheng))
        else:
            self.jieji_fangcheng = solve_fangcheng(self.eq_fangcheng, self.ui.fangcheng_zhuyuanfuhao.text(), self.ui.fangcheng_quzhifanwei.text(), self.fs)
            self.setWebEngineView('', latex(self.jieji_fangcheng), self.ui.fangcheng_jieji)
            self.ui.fangcheng_jieji_lineedit.setText(str(self.jieji_fangcheng))
    
    def read_fangcheng(self, item):
        # 读取方程并显示
        self.setWebEngineView('', latex(self.eqs[item.text()]), self.ui.fangchengzu_yuanfangcheng)
        self.ui.fangchengzu_zuoshi.setText(str(self.eqs[item.text()].lhs))
        self.ui.fangchengzu_youshi.setText(str(self.eqs[item.text()].rhs))

    def setfangchengzu_yuanfangcheng(self):
        # 切换至当前选项卡时加载不等式
        if self.ui.fangchengzu_fangcheng.count() != 0:
            self.read_fangcheng(self.ui.fangchengzu_fangcheng.currentItem())

    def save_fangcheng(self):
        # 保存方程
        if Eq(sympify(self.ui.fangchengzu_zuoshi.text(), self.fs), sympify(self.ui.fangchengzu_youshi.text(), self.fs)) not in self.eqs.values():
            self.eqs[str(Eq(sympify(self.ui.fangchengzu_zuoshi.text(), self.fs), sympify(self.ui.fangchengzu_youshi.text(), self.fs)))] = Eq(sympify(self.ui.fangchengzu_zuoshi.text(), self.fs), sympify(self.ui.fangchengzu_youshi.text(), self.fs))
            self.ui.fangchengzu_fangcheng.addItem(str(Eq(sympify(self.ui.fangchengzu_zuoshi.text(), self.fs), sympify(self.ui.fangchengzu_youshi.text(), self.fs))))
            self.ui.fangchengzu_fangcheng.setCurrentRow(self.ui.fangchengzu_fangcheng.count() - 1)
        else:
            self.eqs[str(Eq(sympify(self.ui.fangchengzu_zuoshi.text(), self.fs), sympify(self.ui.fangchengzu_youshi.text(), self.fs)))] = Eq(sympify(self.ui.fangchengzu_zuoshi.text(), self.fs), sympify(self.ui.fangchengzu_youshi.text(), self.fs))
        self.read_fangcheng(self.ui.fangchengzu_fangcheng.currentItem())

    def delete_fangcheng(self):
        # 删除方程
        fangcheng = self.ui.fangchengzu_fangcheng.takeItem(self.ui.fangchengzu_fangcheng.currentRow())
        del self.eqs[fangcheng.text()]
        del fangcheng
        if self.eqs != {}:
            self.read_fangcheng(self.ui.fangchengzu_fangcheng.currentItem())

    def fangchengzu_button_f(self):
        # 求解方程组
        try:
            result = solve_fangchengzu(list(self.eqs.values()), [Symbol(s) for s in self.ui.fangchengzu_ziyoubianliang.text().split(',')], self.fs)
        except:
            result = "无解"
        self.setWebEngineView('', latex(result).replace(':', "="), self.ui.fangchengzu_jieji)
        self.ui.fangchengzu_jieji_lineedit.setText(result)

    def setbudengshi_yuanshi(self):
        # 加载原不等式
        try:
            self.rel_budengshi = Rel(sympify(self.ui.budengshi_zuoshi.text(), self.fs), sympify(self.ui.budengshi_youshi.text(), self.fs), self.ui.budengshi_budenghao.currentText())
            self.setWebEngineView('', '{}\\quad (x\\in {})'.format(latex(self.rel_budengshi), latex(sympify(self.ui.budengshi_quzhifanwei.text(), self.fs))), self.ui.budengshi_yuanshi)
        except:
            pass

    def budengshi_button_f(self):
        # 求解不等式
        self.jieji_budengshi = solve_budengshi(self.rel_budengshi, self.ui.budengshi_zhuyuanfuhao.text(), self.ui.budengshi_quzhifanwei.text(), self.fs)
        self.setWebEngineView('', latex(self.jieji_budengshi), self.ui.budengshi_jieji)
        self.ui.budengshi_jieji_lineedit.setText(str(self.jieji_budengshi))

    def read_budengshi(self, item):
        # 读取不等式并显示
        self.setWebEngineView('', latex(self.rels[item.text()]), self.ui.budengshizu_yuanbudengshi)
        self.ui.budengshizu_zuoshi.setText(str(self.rels[item.text()].lhs))
        self.ui.budengshizu_youshi.setText(str(self.rels[item.text()].rhs))

    def setbudengshizu_yuanbudengshi(self):
        # 切换至当前选项卡时加载不等式
        if self.ui.budengshizu_budengshi.count() != 0:
            self.read_budengshi(self.ui.budengshizu_budengshi.currentItem())

    def save_budengshi(self):
        # 保存不等式
        if Rel(sympify(self.ui.budengshizu_zuoshi.text(), self.fs), sympify(self.ui.budengshizu_youshi.text(), self.fs), self.ui.budengshizu_budenghao.currentText()) not in self.rels.values():
            self.rels[str(Rel(sympify(self.ui.budengshizu_zuoshi.text(), self.fs), sympify(self.ui.budengshizu_youshi.text(), self.fs), self.ui.budengshizu_budenghao.currentText()))] = \
                Rel(sympify(self.ui.budengshizu_zuoshi.text(), self.fs), sympify(self.ui.budengshizu_youshi.text(), self.fs), self.ui.budengshizu_budenghao.currentText())
            self.ui.budengshizu_budengshi.addItem(str(Rel(sympify(self.ui.budengshizu_zuoshi.text(), self.fs), sympify(self.ui.budengshizu_youshi.text(), self.fs), self.ui.budengshizu_budenghao.currentText())))
            self.ui.budengshizu_budengshi.setCurrentRow(self.ui.budengshizu_budengshi.count() - 1)
        else:
            self.rels[str(Rel(sympify(self.ui.budengshizu_zuoshi.text(), self.fs), sympify(self.ui.budengshizu_youshi.text(), self.fs), self.ui.budengshizu_budenghao.currentText()))] = \
                Rel(sympify(self.ui.budengshizu_zuoshi.text(), self.fs), sympify(self.ui.budengshizu_youshi.text(), self.fs), self.ui.budengshizu_budenghao.currentText())
        self.read_budengshi(self.ui.budengshizu_budengshi.currentItem())
    
    def delete_budengshi(self):
        # 删除不等式
        budengshi = self.ui.budengshizu_budengshi.takeItem(self.ui.budengshizu_budengshi.currentRow())
        del self.rels[budengshi.text()]
        del budengshi
        if self.rels != {}:
            self.read_budengshi(self.ui.budengshizu_budengshi.currentItem())

    def budengshizu_button_f(self):
        # 求解不等式组
        try:
            result = solve_budengshizu(list(self.rels.values()), Symbol(self.ui.budengshizu_ziyoubianliang.text()), self.fs) \
                if solve_budengshizu(list(self.rels.values()), Symbol(self.ui.budengshizu_ziyoubianliang.text()), self.fs) else "无解"
        except:
            result = "无解"
        self.setWebEngineView('', latex(result), self.ui.budengshizu_jieji)
        self.ui.budengshizu_jieji_lineedit.setText(str(result))