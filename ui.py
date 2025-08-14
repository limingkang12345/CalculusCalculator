# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Tools.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QTabWidget, QWidget)
from derivative import derivative, yinhanshu_derivative
from integral import integral
from sympy import sympify, latex

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 801, 601))
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.North)
        self.tabWidget.setTabShape(QTabWidget.TabShape.Rounded)
        self.shouye = QWidget()
        self.shouye.setObjectName(u"shouye")
        self.gridLayoutWidget = QWidget(self.shouye)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(9, 9, 781, 551))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.shouye_welcome = QLabel(self.gridLayoutWidget)
        self.shouye_welcome.setObjectName(u"shouye_welcome")
        self.shouye_welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.shouye_welcome, 0, 0, 1, 1)

        self.tabWidget.addTab(self.shouye, "")
        self.qiudao = QWidget()
        self.qiudao.setObjectName(u"qiudao")
        self.groupBox1 = QGroupBox(self.qiudao)
        self.groupBox1.setObjectName(u"groupBox1")
        self.groupBox1.setGeometry(QRect(10, 10, 771, 51))
        self.qiudao_input = QLineEdit(self.groupBox1)
        self.qiudao_input.setObjectName(u"qiudao_input")
        self.qiudao_input.setGeometry(QRect(10, 20, 751, 21))
        self.qiudao_input.textChanged.connect(self.setqiudao_yuanhanshu)
        self.groupBox2 = QGroupBox(self.qiudao)
        self.groupBox2.setObjectName(u"groupBox2")
        self.groupBox2.setGeometry(QRect(10, 110, 771, 131))
        self.qiudao_yuanhanshu = QWebEngineView(self.groupBox2)
        self.qiudao_yuanhanshu.setObjectName(u"qiudao_yuanhanshu")
        self.qiudao_yuanhanshu.setGeometry(QRect(10, 20, 751, 101))
        self.qiudao_yuanhanshu.setUrl(QUrl(u"about:blank"))
        self.groupBox3 = QGroupBox(self.qiudao)
        self.groupBox3.setObjectName(u"groupBox3")
        self.groupBox3.setGeometry(QRect(10, 250, 771, 131))
        self.qiudao_daohanshu = QWebEngineView(self.groupBox3)
        self.qiudao_daohanshu.setObjectName(u"qiudao_daohanshu")
        self.qiudao_daohanshu.setGeometry(QRect(10, 19, 751, 101))
        self.qiudao_daohanshu.setUrl(QUrl(u"about:blank"))
        self.qiudao_qiudao_button = QPushButton(self.qiudao)
        self.qiudao_qiudao_button.setObjectName(u"qiudao_qiudao_button")
        self.qiudao_qiudao_button.setGeometry(QRect(10, 530, 771, 26))
        self.qiudao_qiudao_button.clicked.connect(self.qiudao_button)
        self.groupBox = QGroupBox(self.qiudao)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 60, 121, 51))
        self.qiudao_zibianliang = QLineEdit(self.groupBox)
        self.qiudao_zibianliang.setObjectName(u"qiudao_zibianliang")
        self.qiudao_zibianliang.setGeometry(QRect(10, 20, 101, 24))
        self.qiudao_zibianliang.setText("x")
        self.qiudao_yinhanshu = QCheckBox(self.qiudao)
        self.qiudao_yinhanshu.setObjectName(u"qiudao_yinhanshu")
        self.qiudao_yinhanshu.setGeometry(QRect(530, 80, 89, 22))
        self.qiudao_yinhanshu.stateChanged.connect(self.qiudao_yinhanshu_f)
        self.groupBox_3 = QGroupBox(self.qiudao)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(270, 60, 121, 51))
        self.qiudao_qiudaocishu = QLineEdit(self.groupBox_3)
        self.qiudao_qiudaocishu.setObjectName(u"qiudao_qiudaocishu")
        self.qiudao_qiudaocishu.setGeometry(QRect(10, 20, 101, 24))
        self.qiudao_qiudaocishu.setText("1")
        self.groupBox_4 = QGroupBox(self.qiudao)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(140, 60, 121, 51))
        self.qiudao_yinbianliang = QLineEdit(self.groupBox_4)
        self.qiudao_yinbianliang.setObjectName(u"qiudao_yinbianliang")
        self.qiudao_yinbianliang.setGeometry(QRect(10, 20, 101, 24))
        self.qiudao_yinbianliang.setEnabled(False)
        self.groupBox_5 = QGroupBox(self.qiudao)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setGeometry(QRect(10, 390, 771, 131))
        self.qiudao_daoshuzhi = QWebEngineView(self.groupBox_5)
        self.qiudao_daoshuzhi.setObjectName(u"qiudao_daoshuzhi")
        self.qiudao_daoshuzhi.setGeometry(QRect(10, 20, 751, 101))
        self.qiudao_daoshuzhi.setUrl(QUrl(u"about:blank"))
        self.groupBox_6 = QGroupBox(self.qiudao)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setGeometry(QRect(400, 60, 121, 51))
        self.qiudao_zibianliangzhi = QLineEdit(self.groupBox_6)
        self.qiudao_zibianliangzhi.setObjectName(u"qiudao_zibianliangzhi")
        self.qiudao_zibianliangzhi.setGeometry(QRect(10, 20, 101, 24))
        self.qiudao_zibianliangzhi.setEnabled(False)
        self.qiudao_qiuchujutizhi = QCheckBox(self.qiudao)
        self.qiudao_qiuchujutizhi.setObjectName(u"qiudao_qiuchujutizhi")
        self.qiudao_qiuchujutizhi.setGeometry(QRect(600, 80, 89, 22))
        self.qiudao_qiuchujutizhi.stateChanged.connect(self.qiudao_jutizhi_f)
        self.tabWidget.addTab(self.qiudao, "")
        self.jifen = QWidget()
        self.jifen.setObjectName(u"jifen")
        self.groupBox_7 = QGroupBox(self.jifen)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setGeometry(QRect(10, 60, 251, 51))
        self.jifen_jifenbianliang = QLineEdit(self.groupBox_7)
        self.jifen_jifenbianliang.setObjectName(u"jifen_jifenbianliang")
        self.jifen_jifenbianliang.setGeometry(QRect(10, 20, 231, 24))
        self.jifen_jifenbianliang.setText("x")
        self.groupBox_8 = QGroupBox(self.jifen)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setGeometry(QRect(400, 60, 121, 51))
        self.jifen_shangxianzhi = QLineEdit(self.groupBox_8)
        self.jifen_shangxianzhi.setObjectName(u"jifen_shangxianzhi")
        self.jifen_shangxianzhi.setGeometry(QRect(10, 20, 101, 24))
        self.jifen_shangxianzhi.setEnabled(False)
        self.groupBox3_2 = QGroupBox(self.jifen)
        self.groupBox3_2.setObjectName(u"groupBox3_2")
        self.groupBox3_2.setGeometry(QRect(10, 250, 771, 131))
        self.jifen_yuanhanshu = QWebEngineView(self.groupBox3_2)
        self.jifen_yuanhanshu.setObjectName(u"jifen__yuanhanshu")
        self.jifen_yuanhanshu.setGeometry(QRect(10, 19, 751, 101))
        self.jifen_yuanhanshu.setUrl(QUrl(u"about:blank"))
        self.groupBox2_2 = QGroupBox(self.jifen)
        self.groupBox2_2.setObjectName(u"groupBox2_2")
        self.groupBox2_2.setGeometry(QRect(10, 110, 771, 131))
        self.jifen_beijihanshu = QWebEngineView(self.groupBox2_2)
        self.jifen_beijihanshu.setObjectName(u"jifen_beijihanshu")
        self.jifen_beijihanshu.setGeometry(QRect(10, 20, 751, 101))
        self.jifen_beijihanshu.setUrl(QUrl(u"about:blank"))
        self.groupBox_11 = QGroupBox(self.jifen)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.groupBox_11.setGeometry(QRect(10, 390, 771, 131))
        self.jifen_dingjifenzhi = QWebEngineView(self.groupBox_11)
        self.jifen_dingjifenzhi.setObjectName(u"jifen_dingjifenzhi")
        self.jifen_dingjifenzhi.setGeometry(QRect(10, 20, 751, 101))
        self.jifen_dingjifenzhi.setUrl(QUrl(u"about:blank"))
        self.groupBox1_2 = QGroupBox(self.jifen)
        self.groupBox1_2.setObjectName(u"groupBox1_2")
        self.groupBox1_2.setGeometry(QRect(10, 10, 771, 51))
        self.jifen_input = QLineEdit(self.groupBox1_2)
        self.jifen_input.setObjectName(u"jifen_input")
        self.jifen_input.setGeometry(QRect(10, 20, 751, 21))
        self.jifen_input.textChanged.connect(self.setjifen_beijihanshu)
        self.jifen_jifen_button = QPushButton(self.jifen)
        self.jifen_jifen_button.setObjectName(u"jifen_jifen_button")
        self.jifen_jifen_button.setGeometry(QRect(10, 530, 771, 26))
        self.jifen_jifen_button.clicked.connect(self.jifen_button_f)
        self.groupBox_9 = QGroupBox(self.jifen)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.groupBox_9.setGeometry(QRect(270, 60, 121, 51))
        self.jifen_xiaxianzhi = QLineEdit(self.groupBox_9)
        self.jifen_xiaxianzhi.setObjectName(u"jifen_xiaxianzhi")
        self.jifen_xiaxianzhi.setGeometry(QRect(10, 20, 101, 24))
        self.jifen_xiaxianzhi.setEnabled(False)
        self.jifen_dingjifen = QCheckBox(self.jifen)
        self.jifen_dingjifen.setObjectName(u"jifen_dingjifen")
        self.jifen_dingjifen.setGeometry(QRect(530, 80, 89, 22))
        self.jifen_dingjifen.stateChanged.connect(self.jifen_dingjifen_f)
        self.tabWidget.addTab(self.jifen, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u5fae\u79ef\u5206\u8ba1\u7b97\u5668v1.0", None))
        self.shouye_welcome.setText(QCoreApplication.translate("MainWindow", u"\u6b22\u8fce\u4f7f\u7528\u5fae\u79ef\u5206\u8ba1\u7b97\u5668v1.0\uff01", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.shouye), QCoreApplication.translate("MainWindow", u"\u9996\u9875", None))
        self.groupBox1.setTitle(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u8868\u8fbe\u5f0f", None))
        self.groupBox2.setTitle(QCoreApplication.translate("MainWindow", u"\u539f\u51fd\u6570", None))
        self.groupBox3.setTitle(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fd\u6570", None))
        self.qiudao_qiudao_button.setText(QCoreApplication.translate("MainWindow", u"\u6c42\u5bfc", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u81ea\u53d8\u91cf", None))
        self.qiudao_yinhanshu.setText(QCoreApplication.translate("MainWindow", u"\u9690\u51fd\u6570", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\u6c42\u5bfc\u6b21\u6570", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"\u56e0\u53d8\u91cf(\u4ec5\u9690\u51fd\u6570)", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"\u5bfc\u6570\u503c", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"\u81ea\u53d8\u91cf\u503c", None))
        self.qiudao_qiuchujutizhi.setText(QCoreApplication.translate("MainWindow", u"\u6c42\u51fa\u5177\u4f53\u503c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.qiudao), QCoreApplication.translate("MainWindow", u"\u6c42\u5bfc", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"\u79ef\u5206\u53d8\u91cf", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"\u4e0a\u9650\u503c", None))
        self.groupBox3_2.setTitle(QCoreApplication.translate("MainWindow", u"\u539f\u51fd\u6570", None))
        self.groupBox2_2.setTitle(QCoreApplication.translate("MainWindow", u"\u88ab\u79ef\u51fd\u6570", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("MainWindow", u"\u5b9a\u79ef\u5206\u503c", None))
        self.groupBox1_2.setTitle(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u8868\u8fbe\u5f0f", None))
        self.jifen_jifen_button.setText(QCoreApplication.translate("MainWindow", u"\u79ef\u5206", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"\u4e0b\u9650\u503c", None))
        self.jifen_dingjifen.setText(QCoreApplication.translate("MainWindow", u"\u5b9a\u79ef\u5206", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.jifen), QCoreApplication.translate("MainWindow", u"\u79ef\u5206", None))
    # retranslateUi

    def setWebEngineView(self, l, w):
        # 显示表达式
        # l:要显示的Latex表达式
        # w:要设置的WebEngineView
        w.setHtml("<html><head><script type=\"text/javascript\" \
                        src=\"https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/latest.js?config=TeX-MML-AM_CHTML\">\
                        </script></head><body><p style=\"font-size:40px\">\\(f(x)={}\\)</p></body></html>".format(l))

    def setqiudao_yuanhanshu(self):
        # 加载原函数
        self.setWebEngineView(latex(sympify(self.qiudao_input.text())), self.qiudao_yuanhanshu)

    def qiudao_yinhanshu_f(self):
        # 更改求解模式:是否隐函数
        self.is_yinhanshu = self.qiudao_yinhanshu.isChecked()
        self.qiudao_yinbianliang.setEnabled(self.qiudao_yinhanshu.isChecked())

    def qiudao_jutizhi_f(self):
        # 更改求解模式:是否具体值
        self.is_jutizhi = self.qiudao_qiuchujutizhi.isChecked()
        self.qiudao_zibianliangzhi.setEnabled(self.qiudao_qiuchujutizhi.isChecked())

    def qiudao_button(self):
        # 求导
        self.is_yinhanshu = self.qiudao_yinhanshu.isChecked()
        self.is_jutizhi = self.qiudao_qiuchujutizhi.isChecked()
        if self.is_yinhanshu:
            if self.is_jutizhi:
                self.setWebEngineView(yinhanshu_derivative(self.qiudao_input.text(), self.qiudao_zibianliang.text(), self.qiudao_yinbianliang.text(), self.qiudao_qiudaocishu.text(), None), self.qiudao_daohanshu)
                self.setWebEngineView(yinhanshu_derivative(self.qiudao_input.text(), self.qiudao_zibianliang.text(), self.qiudao_yinbianliang.text(), self.qiudao_qiudaocishu.text(), self.qiudao_zibianliangzhi.text()), self.qiudao_daoshuzhi)
            else:
                self.setWebEngineView(yinhanshu_derivative(self.qiudao_input.text(), self.qiudao_zibianliang.text(), self.qiudao_yinbianliang.text(), self.qiudao_qiudaocishu.text(), None), self.qiudao_daohanshu)
        else:
            if self.is_jutizhi:
                self.setWebEngineView(derivative(self.qiudao_input.text(), self.qiudao_zibianliang.text(), self.qiudao_qiudaocishu.text(), None), self.qiudao_daohanshu)
                self.setWebEngineView(derivative(self.qiudao_input.text(), self.qiudao_zibianliang.text(), self.qiudao_qiudaocishu.text(), self.qiudao_zibianliangzhi.text()), self.qiudao_daoshuzhi)
            else:
                self.setWebEngineView(derivative(self.qiudao_input.text(), self.qiudao_zibianliang.text(), self.qiudao_qiudaocishu.text(), None), self.qiudao_daohanshu)

    def setjifen_beijihanshu(self):
        # 加载原函数
        self.setWebEngineView(latex(sympify(self.jifen_input.text())), self.jifen_beijihanshu)

    def jifen_dingjifen_f(self):
        # 更改求解模式:是否定积分
        self.is_dingjifen = self.jifen_dingjifen.isChecked()
        self.jifen_shangxianzhi.setEnabled(self.jifen_dingjifen.isChecked()) 
        self.jifen_xiaxianzhi.setEnabled(self.jifen_dingjifen.isChecked())

    def jifen_button_f(self):
        # 积分
        self.is_dingjifen = self.jifen_dingjifen.isChecked()
        if self.is_dingjifen:
            self.setWebEngineView(integral(self.jifen_input.text(), self.jifen_jifenbianliang.text()), self.jifen_yuanhanshu)
            self.setWebEngineView(integral(self.jifen_input.text(), self.jifen_jifenbianliang.text(), self.jifen_xiaxianzhi.text(), self.jifen_shangxianzhi.text()), self.jifen_dingjifenzhi)
        else:
            self.setWebEngineView(integral(self.jifen_input.text(), self.jifen_jifenbianliang.text()), self.jifen_yuanhanshu)
