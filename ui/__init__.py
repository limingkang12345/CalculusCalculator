from ui.ui_main import *
from ui.ui_shouye import *
from ui.ui_dingyi import *
from ui.ui_qiudao import *
from ui.ui_jifen import *
from ui.ui_bianxing import *
from ui.ui_fangcheng import *
from ui.ui_fangchengzu import *
from ui.ui_budengshi import *
from ui.ui_budengshizu import *
from ui.ui_jisuan import *
from ui.ui_help import *

import resources_rc
from derivative import derivative, yinhanshu_derivative
from integral import integral
from simplification import simplifies
from solvers import solve_fangcheng, solve_weifenfangcheng, solve_fangchengzu, solve_budengshi, solve_budengshizu
from functions import get_function_attr

from sympy import latex, Eq, Rel, symbols, Symbol, radsimp, radsimp
from sympify import sympify

from PySide6.QtWidgets import QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

def setWebEngineView(n, l, w):
        # 显示表达式
        # n:函数名
        # l:要显示的Latex表达式
        # w:要设置的WebEngineView
        
        html = r'<html><head><script src="qrc:///MathJax/es5/tex-svg.js"></script></head><body><div><p style="font-size:34px">\({}{}\)</p></div></body></html>'.format(n, l)
        w.setHtml(html)

class Shouye(QWidget, Ui_shouye):
    def __init__(self, parent, fs):
        super(Shouye, self).__init__(parent)
        self.setupUi(self)

class Dingyi(QWidget, Ui_dingyi):
    def __init__(self, parent, fs):
        super(Dingyi, self).__init__(parent)
        self.setupUi(self)
        
        self.dingyi_hanshuliebiao.itemClicked.connect(self.read_function)
        self.dingyi_baocun.clicked.connect(self.save_function)
        self.dingyi_shanchu.clicked.connect(self.delete_function)
        self.dingyi_hanshushuxing_cbx.addItems(["表达式&定义域", "值域", "单调递增区间", "单调递减区间", "奇偶性", "周期", "最大值", "最小值"])
        self.dingyi_hanshushuxing_cbx.setCurrentIndex(0)
        self.dingyi_hanshushuxing_cbx.currentIndexChanged.connect(self.update_function_attr)
        self.dingyi_zibianliangzhi.textChanged.connect(self.function_value)

        self.fs = fs
        self.parent = parent
        self.dingyi_hanshuliebiao.insertItems(0, list("{}({})".format(self.fs[i][0], self.fs[i][3]) for i in self.fs.keys()))

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
        self.fs[self.dingyi_mingcheng.text()] = [self.dingyi_mingcheng.text(), self.dingyi_biaodashi.text(), self.dingyi_dingyiyu.text(), self.dingyi_zibianliang.text()]
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
            setWebEngineView('' if self.dingyi_hanshushuxing_cbx.currentIndex() != 0 else self.dingyi_hanshuliebiao.currentItem().text() + "=", \
                latex(function_attr) if self.dingyi_hanshushuxing_cbx.currentIndex() != 0 else latex(function_attr[0]) + '({}\\in {})'.format(self.dingyi_zibianliang.text(), latex(function_attr[1])), \
                self.dingyi_hanshushuxing)
        except:
            pass

    def function_value(self):
        # 根据给定自变量值求出函数值
        f_value = radsimp(sympify(self.dingyi_biaodashi.text(), self.fs).subs(symbols(self.dingyi_zibianliang.text()), sympify(self.dingyi_zibianliangzhi.text(), self.fs)))
        self.dingyi_qiuzhi_lineedit.setText(str(f_value))
        try:
            setWebEngineView("{}({})=".format(self.dingyi_mingcheng.text(), latex(sympify(self.dingyi_zibianliangzhi.text(), self.fs))), latex(f_value), self.dingyi_qiuzhi)
        except:
            pass

class Qiudao(QWidget, Ui_qiudao):
    def __init__(self, parent, fs):
        super(Qiudao, self).__init__(parent)
        self.setupUi(self)
        
        self.qiudao_input.textChanged.connect(self.setqiudao_yuanhanshu)
        self.qiudao_qiudao_button.clicked.connect(self.qiudao_button_f)
        self.qiudao_yinhanshu.stateChanged.connect(self.qiudao_yinhanshu_f)
        self.qiudao_qiuchujutizhi.stateChanged.connect(self.qiudao_jutizhi_f)

        self.fs = fs
        self.parent = parent
        
    def setqiudao_yuanhanshu(self):
        # 加载原函数
        try:
            setWebEngineView('f(x)=', latex(sympify(self.qiudao_input.text(), self.fs)), self.qiudao_yuanhanshu)
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
                setWebEngineView("f'(x)=", latex(dif), self.qiudao_daohanshu)
                self.qiudao_daohanshu_lineedit.setText(str(dif))
                dif = yinhanshu_derivative(self.qiudao_input.text(), self.qiudao_zibianliang.text(), self.qiudao_yinbianliang.text(), self.qiudao_qiudaocishu.text(), self.qiudao_zibianliangzhi.text(), self.fs)
                setWebEngineView("f'({})=".format(self.qiudao_zibianliangzhi.text()), latex(dif), self.qiudao_daoshuzhi)
                self.qiudao_daoshuzhi_lineedit.setText(str(dif))
            else:
                dif = yinhanshu_derivative(self.qiudao_input.text(), self.qiudao_zibianliang.text(), self.qiudao_yinbianliang.text(), self.qiudao_qiudaocishu.text(), None, self.fs)
                setWebEngineView("f'(x)=", latex(dif), self.qiudao_daohanshu)
                self.qiudao_daohanshu_lineedit.setText(str(dif))
        else:
            if self.is_jutizhi:
                dif = derivative(self.qiudao_input.text(), self.qiudao_zibianliang.text(), self.qiudao_qiudaocishu.text(), None, self.fs)
                setWebEngineView("f'(x)=", latex(dif), self.qiudao_daohanshu)
                self.qiudao_daohanshu_lineedit.setText(str(dif))
                dif = derivative(self.qiudao_input.text(), self.qiudao_zibianliang.text(), self.qiudao_qiudaocishu.text(), self.qiudao_zibianliangzhi.text(), self.fs)
                setWebEngineView("f'({})=".format(self.qiudao_zibianliangzhi.text()), latex(dif), self.qiudao_daoshuzhi)
                self.qiudao_daoshuzhi_lineedit.setText(str(dif))
            else:
                dif = derivative(self.qiudao_input.text(), self.qiudao_zibianliang.text(), self.qiudao_qiudaocishu.text(), None, self.fs)
                setWebEngineView("f'(x)=", latex(dif), self.qiudao_daohanshu)
                self.qiudao_daohanshu_lineedit.setText(str(dif))

class Jifen(QWidget, Ui_jifen):
    def __init__(self, parent, fs):
        super(Jifen, self).__init__(parent)
        self.setupUi(self)

        self.jifen_input.textChanged.connect(self.setjifen_beijihanshu)
        self.jifen_jifen_button.clicked.connect(self.jifen_button_f)
        self.jifen_dingjifen.stateChanged.connect(self.jifen_dingjifen_f)

        self.fs = fs
        self.parent = parent

    def setjifen_beijihanshu(self):
        # 加载原函数
        try:
            setWebEngineView('f(x)=', latex(sympify(self.jifen_input.text(), self.fs)), self.jifen_beijihanshu)
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
            setWebEngineView('F(x)=', latex(F), self.jifen_yuanhanshu)
            self.jifen_yuanhanshu_lineedit.setText(str(F))
            F = integral(self.jifen_input.text(), self.jifen_jifenbianliang.text(), self.jifen_xiaxianzhi.text(), self.jifen_shangxianzhi.text(), self.fs)
            setWebEngineView('F(x)=', latex(F), self.jifen_dingjifenzhi)
            self.jifen_dingjifenzhi_lineedit.setText(str(F))
            
        else:
            self.jifen_dingjifenzhi.setHtml("")
            F = integral(self.jifen_input.text(), self.jifen_jifenbianliang.text(), self.fs)
            setWebEngineView('F(x)=', latex(F), self.jifen_yuanhanshu)
            self.jifen_yuanhanshu_lineedit.setText(str(F))

class Bianxing(QWidget, Ui_bianxing):
    def __init__(self, parent, fs):
        super(Bianxing, self).__init__(parent)
        self.setupUi(self)

        self.bianxing_bianxingfangfa.addItems(["通用化简(simplify)", "展开(expand)", "因式分解(factor)", "主元(collect)", "通分(cancel)", "分离(apart)"])
        self.bianxing_bianxingfangfa.addItems(["三角变换(trigsimp)", "三角展开(expand_trig)", "指数合并(powsimp)", "指数展开(expand_power_exp)"])
        self.bianxing_bianxingfangfa.addItems(["对数展开(expand_log)", "对数合并(logcombine)", "换元"])
        self.bianxing_bianxingfangfa.currentIndexChanged.connect(self.bianxing_bianxingfangfa_f)
        self.bianxing_input.textChanged.connect(self.setbianxing_yuanshi)
        self.bianxing_bianxing_button.clicked.connect(self.bianxing_button_f)

        self.fs = fs
        self.parent = parent

    def setbianxing_yuanshi(self):
        # 加载原式
        try:
            setWebEngineView('', latex(sympify(self.bianxing_input.text(), self.fs)), self.bianxing_yuanshi)
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
        setWebEngineView('', latex(self.bianxingshi), self.bianxing_bianxingshi)
        self.bianxing_bianxingshi_lineedit.setText(str(self.bianxingshi))

class Fangcheng(QWidget, Ui_fangcheng):
    def __init__(self, parent, fs):
        super(Fangcheng, self).__init__(parent)
        self.setupUi(self)

        self.fangcheng_zuoshi.textChanged.connect(self.setfangcheng_yuanfangcheng)
        self.fangcheng_youshi.textChanged.connect(self.setfangcheng_yuanfangcheng)
        self.fangcheng_quzhifanwei.textChanged.connect(self.setfangcheng_yuanfangcheng)
        self.fangcheng_weifenfangcheng.stateChanged.connect(self.fangcheng_weifenfangcheng_f)
        self.fangcheng_qiujie.clicked.connect(self.fangcheng_button_f)

        self.fs = fs
        self.parent = parent

    def setfangcheng_yuanfangcheng(self):
        # 加载原方程
        try:
            self.eq_fangcheng = Eq(sympify(self.fangcheng_zuoshi.text(), self.fs if not self.fangcheng_weifenfangcheng.isChecked() else {}), \
                                   sympify(self.fangcheng_youshi.text(), self.fs if not self.fangcheng_weifenfangcheng.isChecked() else {}))
            setWebEngineView('','{} (x\\in {})'.format(latex(self.eq_fangcheng), latex(sympify(self.fangcheng_quzhifanwei.text(), self.fs))) if not self.fangcheng_weifenfangcheng.isChecked() \
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
            setWebEngineView('', latex(self.jieji_fangcheng), self.fangcheng_jieji)
            self.fangcheng_jieji_lineedit.setText(str(self.jieji_fangcheng))
        else:
            self.jieji_fangcheng = solve_fangcheng(self.eq_fangcheng, self.fangcheng_zhuyuanfuhao.text(), self.fangcheng_quzhifanwei.text(), self.fs)
            setWebEngineView('', latex(self.jieji_fangcheng), self.fangcheng_jieji)
            self.fangcheng_jieji_lineedit.setText(str(self.jieji_fangcheng))

class Fangchengzu(QWidget, Ui_fangchengzu):
    def __init__(self, parent, fs):
        super(Fangchengzu, self).__init__(parent)
        self.setupUi(self)

        self.fangchengzu_baocun.clicked.connect(self.save_fangcheng)
        self.fangchengzu_shanchu.clicked.connect(self.delete_fangcheng)
        self.fangchengzu_fangcheng.itemClicked.connect(self.read_fangcheng)
        self.fangchengzu_qiujie.clicked.connect(self.fangchengzu_button_f)

        self.fs = fs
        self.parent = parent

        for i in self.parent.eqs.keys():
            self.fangchengzu_fangcheng.addItem(i)
        
    def read_fangcheng(self, item):
        # 读取方程并显示
        setWebEngineView('', latex(self.parent.eqs[item.text()]), self.fangchengzu_yuanfangcheng)
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
        setWebEngineView('', latex(result).replace(':', "="), self.fangchengzu_jieji)
        self.fangchengzu_jieji_lineedit.setText(str(result))

class Budengshi(QWidget, Ui_budengshi):
    def __init__(self, parent, fs):
        super(Budengshi, self).__init__(parent)
        self.setupUi(self)

        self.budengshi_budenghao.addItems(["!=", ">", ">=", "<", "<="])
        self.budengshi_budenghao.currentIndexChanged.connect(self.setbudengshi_yuanshi)
        self.budengshi_zuoshi.textChanged.connect(self.setbudengshi_yuanshi)
        self.budengshi_youshi.textChanged.connect(self.setbudengshi_yuanshi)
        self.budengshi_quzhifanwei.textChanged.connect(self.setbudengshi_yuanshi)
        self.budengshi_qiujie.clicked.connect(self.budengshi_button_f)

        self.fs = fs
        self.parent = parent

    def setbudengshi_yuanshi(self):
        # 加载原不等式
        try:
            self.rel_budengshi = Rel(sympify(self.budengshi_zuoshi.text(), self.fs), sympify(self.budengshi_youshi.text(), self.fs), self.budengshi_budenghao.currentText())
            setWebEngineView('', '{}\\quad (x\\in {})'.format(latex(self.rel_budengshi), latex(sympify(self.budengshi_quzhifanwei.text(), self.fs))), self.budengshi_yuanshi)
        except:
            pass

    def budengshi_button_f(self):
        # 求解不等式
        self.jieji_budengshi = solve_budengshi(self.rel_budengshi, self.budengshi_zhuyuanfuhao.text(), self.budengshi_quzhifanwei.text(), self.fs)
        setWebEngineView('', latex(self.jieji_budengshi), self.budengshi_jieji)
        self.budengshi_jieji_lineedit.setText(str(self.jieji_budengshi))

class Budengshizu(QWidget, Ui_budengshizu):
    def __init__(self, parent, fs):
        super(Budengshizu, self).__init__(parent)
        self.setupUi(self)

        self.budengshizu_budenghao.addItems(["!=", ">", ">=", "<", "<="])
        self.budengshizu_baocun.clicked.connect(self.save_budengshi)
        self.budengshizu_shanchu.clicked.connect(self.delete_budengshi)
        self.budengshizu_budengshi.itemClicked.connect(self.read_budengshi)
        self.budengshizu_qiujie.clicked.connect(self.budengshizu_button_f)

        self.fs = fs
        self.parent = parent

        for i in self.parent.rels.keys():
            self.budengshizu_budengshi.addItem(i)

    def read_budengshi(self, item):
        # 读取不等式并显示
        setWebEngineView('', latex(self.parent.rels[item.text()]), self.budengshizu_yuanbudengshi)
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
        setWebEngineView('', latex(result), self.budengshizu_jieji)
        self.budengshizu_jieji_lineedit.setText(str(result))

class Jisuan(QWidget, Ui_jisuan):
    def __init__(self, parent, fs):
        super(Jisuan, self).__init__(parent)
        self.setupUi(self)

        self.jisuan_jisuanyinqing.addItems(["Python内置引擎", "Mpmath高精度引擎", "Sympy符号引擎", "Latex代码生成引擎"])
        self.jisuan_jisuanyinqing.currentIndexChanged.connect(self.jisuan_jisuanyinqing_f)
        self.jisuan_jisuan_button.clicked.connect(self.jisuan_button_f)
        self.jisuan_input.textChanged.connect(self.setjisuan_yuanshi)

        self.fs = fs
        self.parent = parent

        self.jisuan_jisuanyinqing_f()
    
    def setjisuan_yuanshi(self):
        # 加载原式
        try:
            setWebEngineView("", self.jisuan_input.text(), self.jisuan_yuanshi)
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
            setWebEngineView("", latex(result) if view_is_latex else result, self.jisuan_jisuanjieguo)
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

class Help(QWidget, Ui_help):
    def __init__(self, parent, fs):
        super(Help, self).__init__(parent)
        self.setupUi(self)

        self.help_path = QUrl("qrc:///help.html")
        self.webEngineView.setUrl(self.help_path)

#tabs_name = ["首页", "定义", "求导", "积分", "变形", "方程", "方程组", "不等式", "不等式组", "帮助"]
tabs_list = [Shouye, Dingyi, Qiudao, Jifen, Bianxing, Fangcheng, Fangchengzu, Budengshi, Budengshizu, Jisuan, Help]
tabs_dict = {"首页":0, "定义":1, "求导":2, "积分":3, "变形":4, "方程":5, "方程组":6, "不等式":7, "不等式组":8, "计算":9, "帮助":10}
