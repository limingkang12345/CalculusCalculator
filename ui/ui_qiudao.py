# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qiudaojFPHLe.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGroupBox, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_qiudao(object):
    def setupUi(self, qiudao):
        if not qiudao.objectName():
            qiudao.setObjectName(u"qiudao")
        qiudao.resize(801, 551)
        self.qiudao_qiuchujutizhi = QCheckBox(qiudao)
        self.qiudao_qiuchujutizhi.setObjectName(u"qiudao_qiuchujutizhi")
        self.qiudao_qiuchujutizhi.setGeometry(QRect(600, 80, 89, 22))
        self.groupBox_5 = QGroupBox(qiudao)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setGeometry(QRect(10, 370, 771, 131))
        self.qiudao_daoshuzhi = QWebEngineView(self.groupBox_5)
        self.qiudao_daoshuzhi.setObjectName(u"qiudao_daoshuzhi")
        self.qiudao_daoshuzhi.setGeometry(QRect(10, 20, 751, 71))
        self.qiudao_daoshuzhi.setUrl(QUrl(u"about:blank"))
        self.qiudao_daoshuzhi_lineedit = QLineEdit(self.groupBox_5)
        self.qiudao_daoshuzhi_lineedit.setObjectName(u"qiudao_daoshuzhi_lineedit")
        self.qiudao_daoshuzhi_lineedit.setGeometry(QRect(10, 100, 751, 21))
        self.qiudao_qiudao_button = QPushButton(qiudao)
        self.qiudao_qiudao_button.setObjectName(u"qiudao_qiudao_button")
        self.qiudao_qiudao_button.setGeometry(QRect(10, 510, 771, 26))
        self.groupBox1 = QGroupBox(qiudao)
        self.groupBox1.setObjectName(u"groupBox1")
        self.groupBox1.setGeometry(QRect(10, 10, 771, 51))
        self.qiudao_input = QLineEdit(self.groupBox1)
        self.qiudao_input.setObjectName(u"qiudao_input")
        self.qiudao_input.setGeometry(QRect(10, 20, 751, 21))
        self.groupBox2 = QGroupBox(qiudao)
        self.groupBox2.setObjectName(u"groupBox2")
        self.groupBox2.setGeometry(QRect(10, 110, 771, 131))
        self.qiudao_yuanhanshu = QWebEngineView(self.groupBox2)
        self.qiudao_yuanhanshu.setObjectName(u"qiudao_yuanhanshu")
        self.qiudao_yuanhanshu.setGeometry(QRect(10, 20, 751, 101))
        self.qiudao_yuanhanshu.setUrl(QUrl(u"about:blank"))
        self.groupBox_6 = QGroupBox(qiudao)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setGeometry(QRect(400, 60, 121, 51))
        self.qiudao_zibianliangzhi = QLineEdit(self.groupBox_6)
        self.qiudao_zibianliangzhi.setObjectName(u"qiudao_zibianliangzhi")
        self.qiudao_zibianliangzhi.setEnabled(False)
        self.qiudao_zibianliangzhi.setGeometry(QRect(10, 20, 101, 24))
        self.groupBox_4 = QGroupBox(qiudao)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(140, 60, 121, 51))
        self.qiudao_yinbianliang = QLineEdit(self.groupBox_4)
        self.qiudao_yinbianliang.setObjectName(u"qiudao_yinbianliang")
        self.qiudao_yinbianliang.setEnabled(False)
        self.qiudao_yinbianliang.setGeometry(QRect(10, 20, 101, 24))
        self.groupBox = QGroupBox(qiudao)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 60, 121, 51))
        self.qiudao_zibianliang = QLineEdit(self.groupBox)
        self.qiudao_zibianliang.setObjectName(u"qiudao_zibianliang")
        self.qiudao_zibianliang.setGeometry(QRect(10, 20, 101, 24))
        self.groupBox3 = QGroupBox(qiudao)
        self.groupBox3.setObjectName(u"groupBox3")
        self.groupBox3.setGeometry(QRect(10, 240, 771, 131))
        self.qiudao_daohanshu = QWebEngineView(self.groupBox3)
        self.qiudao_daohanshu.setObjectName(u"qiudao_daohanshu")
        self.qiudao_daohanshu.setGeometry(QRect(10, 20, 751, 71))
        self.qiudao_daohanshu.setUrl(QUrl(u"about:blank"))
        self.qiudao_daohanshu_lineedit = QLineEdit(self.groupBox3)
        self.qiudao_daohanshu_lineedit.setObjectName(u"qiudao_daohanshu_lineedit")
        self.qiudao_daohanshu_lineedit.setGeometry(QRect(10, 100, 751, 21))
        self.qiudao_yinhanshu = QCheckBox(qiudao)
        self.qiudao_yinhanshu.setObjectName(u"qiudao_yinhanshu")
        self.qiudao_yinhanshu.setGeometry(QRect(530, 80, 89, 22))
        self.groupBox_3 = QGroupBox(qiudao)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(270, 60, 121, 51))
        self.qiudao_qiudaocishu = QLineEdit(self.groupBox_3)
        self.qiudao_qiudaocishu.setObjectName(u"qiudao_qiudaocishu")
        self.qiudao_qiudaocishu.setGeometry(QRect(10, 20, 101, 24))

        self.retranslateUi(qiudao)

        QMetaObject.connectSlotsByName(qiudao)
    # setupUi

    def retranslateUi(self, qiudao):
        qiudao.setWindowTitle(QCoreApplication.translate("qiudao", u"Form", None))
        self.qiudao_qiuchujutizhi.setText(QCoreApplication.translate("qiudao", u"\u6c42\u51fa\u5177\u4f53\u503c", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("qiudao", u"\u5bfc\u6570\u503c", None))
        self.qiudao_qiudao_button.setText(QCoreApplication.translate("qiudao", u"\u6c42\u5bfc", None))
        self.groupBox1.setTitle(QCoreApplication.translate("qiudao", u"\u8f93\u5165\u8868\u8fbe\u5f0f", None))
        self.groupBox2.setTitle(QCoreApplication.translate("qiudao", u"\u539f\u51fd\u6570", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("qiudao", u"\u81ea\u53d8\u91cf\u503c", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("qiudao", u"\u56e0\u53d8\u91cf(\u4ec5\u9690\u51fd\u6570)", None))
        self.groupBox.setTitle(QCoreApplication.translate("qiudao", u"\u81ea\u53d8\u91cf", None))
        self.qiudao_zibianliang.setText(QCoreApplication.translate("qiudao", u"x", None))
        self.groupBox3.setTitle(QCoreApplication.translate("qiudao", u"\u5bfc\u51fd\u6570", None))
        self.qiudao_yinhanshu.setText(QCoreApplication.translate("qiudao", u"\u9690\u51fd\u6570", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("qiudao", u"\u6c42\u5bfc\u6b21\u6570", None))
        self.qiudao_qiudaocishu.setText(QCoreApplication.translate("qiudao", u"1", None))
    # retranslateUi

