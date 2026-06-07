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
from ui.ui_dingyixiangliang import *
from ui.ui_huitu_hanshu import *
from ui.ui_jiesanjiaoxing import *

import resources_rc
from derivative import derivative, yinhanshu_derivative
from integral import integral
from simplification import simplifies
from solvers import solve_fangcheng, solve_weifenfangcheng, solve_fangchengzu, solve_budengshi, solve_budengshizu, solve_sanjiaoxing
from functions import get_function_attr

from sympy import latex, Eq, Rel, symbols, Symbol, radsimp, radsimp, simplify
from sympify import sympify

from PySide6.QtWidgets import QWidget, QVBoxLayout
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

# 该类为AI生成
class Dingyixiangliang(QWidget, Ui_dingyixiangliang):
    def __init__(self, parent, fs):
        super(Dingyixiangliang, self).__init__(parent)
        self.setupUi(self)

        self.dingyixiangliang_xiangliangliebiao.itemClicked.connect(self.read_vector)
        self.dingyixiangliang_baocun.clicked.connect(self.save_vector)
        self.dingyixiangliang_shanchu.clicked.connect(self.delete_vector)
        self.dingyixiangliang_xiangliangshuxing_cbx.addItems(["表达式", "模", "方向角", "单位向量"])
        self.dingyixiangliang_xiangliangshuxing_cbx.setCurrentIndex(0)
        self.dingyixiangliang_xiangliangshuxing_cbx.currentIndexChanged.connect(self.update_vector_attr)
        self.dingyixiangliang_jisuanfangfa.addItems(["加法", "减法", "点积", "夹角"])
        self.dingyixiangliang_jisuanfangfa.setCurrentIndex(0)
        self.dingyixiangliang_jisuan_button.clicked.connect(self.compute_vector)

        self.fs = fs
        self.parent = parent

        if not hasattr(self.parent, 'vs'):
            self.parent.vs = {}
        self.vs = self.parent.vs

        self.update_vector_list()
        self.update_vector_combos()

    def update_vector_list(self):
        # 刷新向量列表
        self.dingyixiangliang_xiangliangliebiao.clear()
        self.dingyixiangliang_xiangliangliebiao.insertItems(0,
            list("{}=({}, {})".format(self.vs[n][0], self.vs[n][1], self.vs[n][2]) for n in self.vs.keys()))

    def update_vector_combos(self):
        # 刷新向量运算区的下拉框
        self.dingyixiangliang_xiangliang1.clear()
        self.dingyixiangliang_xiangliang2.clear()
        names = list(self.vs.keys())
        self.dingyixiangliang_xiangliang1.addItems(names)
        self.dingyixiangliang_xiangliang2.addItems(names)

    def read_vector(self, item):
        # 读取向量信息，显示在编辑区
        name = item.text().split('=')[0]
        if name in self.vs:
            self.dingyixiangliang_mingcheng.setText(self.vs[name][0])
            self.dingyixiangliang_x.setText(self.vs[name][1])
            self.dingyixiangliang_y.setText(self.vs[name][2])
        self.dingyixiangliang_xiangliangshuxing_cbx.setCurrentIndex(0)
        self.update_vector_attr(0)

    def save_vector(self):
        # 保存向量信息
        name = self.dingyixiangliang_mingcheng.text()
        x = self.dingyixiangliang_x.text()
        y = self.dingyixiangliang_y.text()
        if name not in self.vs:
            self.dingyixiangliang_xiangliangliebiao.insertItem(0, "{}=({}, {})".format(name, x, y))
            self.dingyixiangliang_xiangliangliebiao.setCurrentRow(0)
        self.vs[name] = [name, x, y]
        self.update_vector_combos()
        self.dingyixiangliang_xiangliangshuxing_cbx.setCurrentIndex(0)
        self.update_vector_attr(0)

    def delete_vector(self):
        # 删除向量
        row = self.dingyixiangliang_xiangliangliebiao.currentRow()
        if row < 0:
            return
        item = self.dingyixiangliang_xiangliangliebiao.takeItem(row)
        name = self.dingyixiangliang_mingcheng.text()
        if name in self.vs:
            del self.vs[name]
        del item
        self.update_vector_combos()
        if self.vs:
            self.read_vector(self.dingyixiangliang_xiangliangliebiao.currentItem())
        self.update_vector_attr(0)

    def update_vector_attr(self, attr):
        # 计算并显示向量属性
        x_str = self.dingyixiangliang_x.text()
        y_str = self.dingyixiangliang_y.text()
        name = self.dingyixiangliang_mingcheng.text()
        try:
            x = sympify(x_str, self.fs)
            y = sympify(y_str, self.fs)
        except:
            return

        from sympy import sqrt, atan2

        if attr == 0:  # 表达式
            result = "({}, {})".format(x, y)
            latex_str = "\\vec{{{}}}=({}, {})".format(name, latex(x), latex(y))
        elif attr == 1:  # 模
            result = simplify(sqrt(x**2 + y**2))
            latex_str = "|\\vec{{{}}}|=".format(name) + latex(result)
        elif attr == 2:  # 方向角
            result = simplify(atan2(y, x))
            latex_str = "\\theta_{{{}}}=".format(name) + latex(result)
        elif attr == 3:  # 单位向量
            mag = sqrt(x**2 + y**2)
            ux = simplify(x / mag)
            uy = simplify(y / mag)
            result = "({}, {})".format(ux, uy)
            latex_str = "\\hat{{\\vec{{{}}}}}=({}, {})".format(name, latex(ux), latex(uy))
        else:
            return

        self.dingyixiangliang_xiangliangshuxing_lineedit.setText(str(result))
        try:
            setWebEngineView('', latex_str, self.dingyixiangliang_xiangliangshuxing)
        except:
            pass

    def compute_vector(self):
        # 执行向量运算
        v1_name = self.dingyixiangliang_xiangliang1.currentText()
        v2_name = self.dingyixiangliang_xiangliang2.currentText()
        method = self.dingyixiangliang_jisuanfangfa.currentIndex()

        if not v1_name or not v2_name or v1_name not in self.vs or v2_name not in self.vs:
            return

        try:
            x1 = sympify(self.vs[v1_name][1], self.fs)
            y1 = sympify(self.vs[v1_name][2], self.fs)
            x2 = sympify(self.vs[v2_name][1], self.fs)
            y2 = sympify(self.vs[v2_name][2], self.fs)
        except:
            return

        from sympy import sqrt, acos

        if method == 0:  # 加法
            rx = simplify(x1 + x2)
            ry = simplify(y1 + y2)
            result = "({}, {})".format(rx, ry)
            latex_str = "\\vec{{{}}}+\\vec{{{}}}=({}, {})".format(v1_name, v2_name, latex(rx), latex(ry))
        elif method == 1:  # 减法
            rx = simplify(x1 - x2)
            ry = simplify(y1 - y2)
            result = "({}, {})".format(rx, ry)
            latex_str = "\\vec{{{}}}-\\vec{{{}}}=({}, {})".format(v1_name, v2_name, latex(rx), latex(ry))
        elif method == 2:  # 点积
            dot = simplify(x1 * x2 + y1 * y2)
            result = dot
            latex_str = "\\vec{{{}}}\\cdot\\vec{{{}}}=".format(v1_name, v2_name) + latex(dot)
        elif method == 3:  # 夹角
            dot = x1 * x2 + y1 * y2
            mag1 = sqrt(x1**2 + y1**2)
            mag2 = sqrt(x2**2 + y2**2)
            cos_theta = simplify(dot / (mag1 * mag2))
            angle = simplify(acos(cos_theta))
            result = angle
            latex_str = "\\angle(\\vec{{{}}},\\vec{{{}}})=".format(v1_name, v2_name) + latex(angle)
        else:
            return

        self.dingyixiangliang_jisuan_lineedit.setText(str(result))
        try:
            setWebEngineView('', latex_str, self.dingyixiangliang_jisuan)
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

class Huitu_hanshu(QWidget, Ui_huitu_hanshu):
    def __init__(self, parent, fs):
        super(Huitu_hanshu, self).__init__(parent)
        self.setupUi(self)

        self.fs = fs
        self.parent = parent

        self.huitu_hanshu_biaodashi_radio.toggled.connect(self.toggle_input_mode)
        self.huitu_hanshu_hanshu_radio.toggled.connect(self.toggle_input_mode)
        self.huitu_hanshu_huizhi.clicked.connect(self.draw_function)

        self.canvas = None
        self.draw_layout = QVBoxLayout(self.huitu_hanshu_huitu)
        self.draw_layout.setContentsMargins(0, 0, 0, 0)

        self.update_function_list()

    def toggle_input_mode(self):
        # 切换输入模式：表达式 / 选择函数
        is_expression = self.huitu_hanshu_biaodashi_radio.isChecked()
        self.huitu_hanshu_biaodashi.setEnabled(is_expression)
        self.huitu_hanshu_hanshu.setEnabled(not is_expression)

    def update_function_list(self):
        # 刷新已定义函数的下拉列表
        self.huitu_hanshu_hanshu.clear()
        for name in self.fs.keys():
            self.huitu_hanshu_hanshu.addItem("{}({})".format(name, self.fs[name][3]))

    def draw_function(self):
        # 销毁之前画的函数图像对象
        if self.canvas is not None:
            self.draw_layout.removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None

        import numpy as np
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
        from matplotlib.figure import Figure
        from sympy import lambdify

        # 获取表达式
        if self.huitu_hanshu_biaodashi_radio.isChecked():
            expr_str = self.huitu_hanshu_biaodashi.text()
            if not expr_str:
                return
            try:
                expr = sympify(expr_str, self.fs)
            except Exception:
                return
            free_syms = list(expr.free_symbols)
            if free_syms:
                var = list(free_syms)[0]
            else:
                var = Symbol('x')
        else:
            func_name = self.huitu_hanshu_hanshu.currentText().split('(')[0]
            if func_name not in self.fs:
                return
            expr_str = self.fs[func_name][1]
            var_str = self.fs[func_name][3]
            try:
                expr = sympify(expr_str, self.fs)
            except Exception:
                return
            var = Symbol(var_str)

        # 定义域
        left_str = self.huitu_hanshu_dingyiyu_left.text() or '-10'
        right_str = self.huitu_hanshu_dingyiyu_right.text() or '10'
        try:
            left = float(sympify(left_str, self.fs))
            right = float(sympify(right_str, self.fs))
        except Exception:
            left, right = -10, 10
        if left >= right:
            left, right = -10, 10

        try:
            # 将 SymPy 表达式转为 numpy 可调函数
            f = lambdify(var, expr, modules=['numpy', {'conjugate': np.conj}])

            # 生成密集的 x 采样点
            num_points = 2000
            x_vals = np.linspace(float(left), float(right), num_points)

            # 排除无穷大和 NaN 的 y 值，避免曲线断裂处连线
            with np.errstate(invalid='ignore', divide='ignore'):
                y_vals = np.asarray(f(x_vals), dtype=np.float64)

            # 构建 matplotlib 图形
            fig = Figure(figsize=(7.7, 3.9), dpi=100)
            ax = fig.add_subplot(111)

            # 在 NaN/Inf 处断开曲线
            mask = np.isfinite(y_vals)
            segments = []
            start = 0
            while start < len(mask):
                if mask[start]:
                    end = start
                    while end < len(mask) and mask[end]:
                        end += 1
                    segments.append((start, end))
                    start = end
                else:
                    start += 1

            for seg_start, seg_end in segments:
                ax.plot(x_vals[seg_start:seg_end], y_vals[seg_start:seg_end],
                        color='#1f77b4', linewidth=1.5)

            # 坐标轴和网格
            ax.axhline(y=0, color='black', linewidth=0.5)
            ax.axvline(x=0, color='black', linewidth=0.5)
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.set_xlim(float(left), float(right))

            # 自动缩放 y 轴到可见范围
            if np.any(mask):
                y_min, y_max = np.min(y_vals[mask]), np.max(y_vals[mask])
                margin = max((y_max - y_min) * 0.1, 1.0)
                ax.set_ylim(y_min - margin, y_max + margin)

            fig.tight_layout()

            self.fig = fig
            self.canvas = FigureCanvas(self.fig)
            self.draw_layout.addWidget(self.canvas)
        except Exception:
            pass
    
class Jiesanjiaoxing(QWidget, Ui_jiesanjiaoxing):
    def __init__(self, parent, fs):
        super(Jiesanjiaoxing, self).__init__(parent)
        self.setupUi(self)

        self.fs = fs
        self.parent = parent

        self.jiesanjiaoxing_qiujie.clicked.connect(self.solve_triangle)

    def _parse_conditions(self):
        """解析三个条件，返回 (angles_dict, sides_dict, error_msg)"""
        combos = [
            (self.jiesanjiaoxing_tiaojian1_cbx, self.jiesanjiaoxing_tiaojian1),
            (self.jiesanjiaoxing_tiaojian2_cbx, self.jiesanjiaoxing_tiaojian2),
            (self.jiesanjiaoxing_tiaojian3_cbx, self.jiesanjiaoxing_tiaojian3),
        ]

        angles = {}
        sides = {}
        angle_names = {1: 'A', 2: 'B', 3: 'C'}
        side_names = {4: 'a', 5: 'b', 6: 'c'}
        for cbx, line_edit in combos:
            idx = cbx.currentIndex()
            val_text = line_edit.text().strip()
            if idx == 0 or not val_text:
                continue

            try:
                val = sympify(val_text, self.fs)
            except Exception:
                return None, None, "条件值格式错误"

            if idx in angle_names:
                angles[angle_names[idx]] = val
            elif idx in side_names:
                sides[side_names[idx]] = val

        total = len(angles) + len(sides)
        if total != 3:
            return None, None, "请填入恰好3个有效且不重复的条件"

        return angles, sides, None

    def solve_triangle(self):
        """求解三角形"""
        # 清空上次结果
        self.jiesanjiaoxing_yuantiaojian.setHtml("")
        self.jiesanjiaoxing_jieguo.setHtml("")
        self.jiesanjiaoxing_jieguo_lineedit.setText("")

        angles, sides, error = self._parse_conditions()
        if error:
            self.jiesanjiaoxing_jieguo_lineedit.setText(error)
            return

        angle_display = {k: latex(v) for k, v in angles.items()}
        side_display = {k: latex(v) for k, v in sides.items()}
        known_parts = []
        for k, v in {**angle_display, **side_display}.items():
            known_parts.append(f"{k} = {v}")
        condition_latex = r"\triangle ABC \quad " + r",\ ".join(known_parts)
        try:
            setWebEngineView('', condition_latex, self.jiesanjiaoxing_yuantiaojian)
        except Exception:
            pass

        result = solve_sanjiaoxing(angles, sides, self.fs)

        if not result:
            self.jiesanjiaoxing_jieguo_lineedit.setText("无解")
            return
        if isinstance(result, str):
            self.jiesanjiaoxing_jieguo_lineedit.setText(str(result))
            return

        lines = []
        for i, (res_angles, res_sides) in enumerate(result):
            parts = []
            for k, v in res_angles.items():
                parts.append(f"{k} = {latex(v)}")
            for k, v in res_sides.items():
                parts.append(f"{k} = {latex(v)}")
            if len(result) > 1:
                lines.append(r"\text{解}" + str(i + 1) + r":\ " + r",\ ".join(parts))
            else:
                lines.append(r",\ ".join(parts))

        result_latex = r" \\ ".join(lines) if len(lines) > 1 else lines[0]

        flat = []
        for i, (res_angles, res_sides) in enumerate(result):
            seg = []
            for k, v in res_angles.items():
                seg.append(f"{k} = {v}")
            for k, v in res_sides.items():
                seg.append(f"{k} = {v}")
            flat.append(" | ".join(seg))
        self.jiesanjiaoxing_jieguo_lineedit.setText("  ||  ".join(flat))

        try:
            setWebEngineView('', result_latex, self.jiesanjiaoxing_jieguo)
        except Exception:
            pass

#tabs_name = ["首页", "定义", "求导", "积分", "变形", "方程", "方程组", "不等式", "不等式组", "帮助"]
tabs_list = [Shouye, Dingyi, Qiudao, Jifen, Bianxing, Fangcheng, Fangchengzu, Budengshi, Budengshizu, Jisuan, Help, Dingyixiangliang, Huitu_hanshu, Jiesanjiaoxing]
tabs_dict = {"首页":0, "定义":1, "求导":2, "积分":3, "变形":4, "方程":5, "方程组":6, "不等式":7, "不等式组":8, "计算":9, "帮助":10, "定义向量":11, "绘制函数":12, "解三角形":13}
