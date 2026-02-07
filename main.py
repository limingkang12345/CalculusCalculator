from ui import Ui_MainWindow
import mathjax_rc

from derivative import derivative, yinhanshu_derivative
from integral import integral
from simplification import simplifies
from sympy import sympify, latex

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QSplitter, QWidget
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setup()

    def setup(self):
        self.ui.qiudao_input.textChanged.connect(self.setqiudao_yuanhanshu)
        self.ui.qiudao_qiudao_button.clicked.connect(self.qiudao_button_f)
        self.ui.qiudao_yinhanshu.stateChanged.connect(self.qiudao_yinhanshu_f)
        self.ui.qiudao_qiuchujutizhi.stateChanged.connect(self.qiudao_jutizhi_f)
        self.ui.jifen_input.textChanged.connect(self.setjifen_beijihanshu)
        self.ui.jifen_jifen_button.clicked.connect(self.jifen_button_f)
        self.ui.jifen_dingjifen.stateChanged.connect(self.jifen_dingjifen_f)
        self.ui.bianxing_bianxingfangfa.addItems(["通用变形(simplify)", "展开(expand)", "因式分解(factor)", "主元(collect)", "通分(cancel)", "分离(apart)"])
        self.ui.bianxing_bianxingfangfa.addItems(["三角变换(trigsimp)", "三角展开(expand_trig)", "指数合并(powsimp)", "指数展开(expand_power_exp)"])
        self.ui.bianxing_bianxingfangfa.addItems(["对数展开(expand_log)", "对数合并(logcombine)"])
        self.ui.bianxing_input.textChanged.connect(self.setbianxing_yuanshi)
        self.ui.bianxing_bianxing_button.clicked.connect(self.bianxing_button_f)

        layout = QVBoxLayout(self.ui.centralwidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui.tabWidget)

        homepage = QVBoxLayout(self.ui.shouye)
        homepage.setContentsMargins(0, 0, 0, 0)
        homepage.addWidget(self.ui.shouye_welcome)

    def setWebEngineView(self, l, w):
        # 显示表达式
        # l:要显示的Latex表达式
        # w:要设置的WebEngineView
        """这个是在线的
        w.setHtml("<html><head><script type=\"text/javascript\" \
                   src=\"https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/latest.js?config=TeX-MML-AM_CHTML\">\
                   </script></head><body><p style=\"font-size:40px\">\\(f(x)={}\\)</p></body></html>".format(l))
        """
        # 这个是离线的
        w.setHtml("<html><head>" +
                  "<script src=\"qrc:///MathJax-4.0.0/tex-svg.js\"></script>" +
                  "</head><body><p style=\"font-size:40px\">\\(f(x)={}\\)</p></body></html>".format(l))

    def setqiudao_yuanhanshu(self):
        # 加载原函数
        try:
            self.setWebEngineView(latex(sympify(self.ui.qiudao_input.text())), self.ui.qiudao_yuanhanshu)
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
                self.setWebEngineView(yinhanshu_derivative(self.ui.qiudao_input.text(), self.ui.qiudao_zibianliang.text(),
                                                           self.ui.qiudao_yinbianliang.text(), self.ui.qiudao_qiudaocishu.text(), None), self.ui.qiudao_daohanshu)
                self.setWebEngineView(yinhanshu_derivative(self.ui.qiudao_input.text(), self.ui.qiudao_zibianliang.text(),
                                                           self.ui.qiudao_yinbianliang.text(), self.ui.qiudao_qiudaocishu.text(), self.ui.qiudao_zibianliangzhi.text()), self.ui.qiudao_daoshuzhi)
            else:
                self.setWebEngineView(yinhanshu_derivative(self.ui.qiudao_input.text(), self.ui.qiudao_zibianliang.text(),
                                                           self.ui.qiudao_yinbianliang.text(), self.ui.qiudao_qiudaocishu.text(), None), self.ui.qiudao_daohanshu)
        else:
            if self.is_jutizhi:
                self.setWebEngineView \
                    (derivative(self.ui.qiudao_input.text(), self.ui.qiudao_zibianliang.text(), self.ui.qiudao_qiudaocishu.text(), None), self.ui.qiudao_daohanshu)
                self.setWebEngineView \
                    (derivative(self.ui.qiudao_input.text(), self.ui.qiudao_zibianliang.text(), self.ui.qiudao_qiudaocishu.text(), self.ui.
                                qiudao_zibianliangzhi.text()), self.ui.qiudao_daoshuzhi)
            else:
                self.ui.qiudao_daoshuzhi.setHtml("")
                self.setWebEngineView \
                    (derivative(self.ui.qiudao_input.text(), self.ui.qiudao_zibianliang.text(), self.ui.qiudao_qiudaocishu.text(), None), self.ui.qiudao_daohanshu)

    def setjifen_beijihanshu(self):
        # 加载原函数
        self.setWebEngineView(latex(sympify(self.ui.jifen_input.text())), self.ui.jifen_beijihanshu)

    def jifen_dingjifen_f(self):
        # 更改求解模式:是否定积分
        self.is_dingjifen = self.ui.jifen_dingjifen.isChecked()
        self.ui.jifen_shangxianzhi.setEnabled(self.ui.jifen_dingjifen.isChecked())
        self.ui.jifen_xiaxianzhi.setEnabled(self.ui.jifen_dingjifen.isChecked())

    def jifen_button_f(self):
        # 积分
        self.is_dingjifen = self.ui.jifen_dingjifen.isChecked()
        if self.is_dingjifen:
            self.setWebEngineView(integral(self.ui.jifen_input.text(), self.ui.jifen_jifenbianliang.text()), self.ui.jifen_yuanhanshu)
            self.setWebEngineView(integral(self.ui.jifen_input.text(), self.ui.jifen_jifenbianliang.text(),
                                           self.ui.jifen_xiaxianzhi.text(), self.ui.jifen_shangxianzhi.text()), self.ui.jifen_dingjifenzhi)
        else:
            self.ui.jifen_dingjifenzhi.setHtml("")
            self.setWebEngineView(integral(self.ui.jifen_input.text(), self.ui.jifen_jifenbianliang.text()), self.ui.jifen_yuanhanshu)

    def setbianxing_yuanshi(self):
        # 加载原式
        self.setWebEngineView(latex(sympify(self.ui.bianxing_input.text())), self.ui.bianxing_yuanshi)

    def bianxing_button_f(self):
        # 变形
        self.bianxingfangfa = self.ui.bianxing_bianxingfangfa.currentIndex()
        self.bianxingshi = simplifies(self.ui.bianxing_input.text(), self.bianxingfangfa)
        self.setWebEngineView(latex(self.bianxingshi), self.ui.bianxing_bianxingshi)
        self.ui.bianxing_bianxingshi_lineedit.setText(str(self.bianxingshi))

