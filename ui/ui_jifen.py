# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'jifenWUoWFQ.ui'
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

class Ui_jifen(object):
    def setupUi(self, jifen):
        if not jifen.objectName():
            jifen.setObjectName(u"jifen")
        jifen.resize(801, 551)
        self.groupBox1_2 = QGroupBox(jifen)
        self.groupBox1_2.setObjectName(u"groupBox1_2")
        self.groupBox1_2.setGeometry(QRect(10, 10, 771, 51))
        self.jifen_input = QLineEdit(self.groupBox1_2)
        self.jifen_input.setObjectName(u"jifen_input")
        self.jifen_input.setGeometry(QRect(10, 20, 751, 21))
        self.jifen_input.setClearButtonEnabled(True)
        self.groupBox_7 = QGroupBox(jifen)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setGeometry(QRect(10, 60, 251, 51))
        self.jifen_jifenbianliang = QLineEdit(self.groupBox_7)
        self.jifen_jifenbianliang.setObjectName(u"jifen_jifenbianliang")
        self.jifen_jifenbianliang.setGeometry(QRect(10, 20, 231, 24))
        self.jifen_jifenbianliang.setClearButtonEnabled(True)
        self.groupBox3_2 = QGroupBox(jifen)
        self.groupBox3_2.setObjectName(u"groupBox3_2")
        self.groupBox3_2.setGeometry(QRect(10, 240, 771, 131))
        self.jifen_yuanhanshu = QWebEngineView(self.groupBox3_2)
        self.jifen_yuanhanshu.setObjectName(u"jifen_yuanhanshu")
        self.jifen_yuanhanshu.setGeometry(QRect(10, 19, 751, 71))
        self.jifen_yuanhanshu.setUrl(QUrl(u"about:blank"))
        self.jifen_yuanhanshu_lineedit = QLineEdit(self.groupBox3_2)
        self.jifen_yuanhanshu_lineedit.setObjectName(u"jifen_yuanhanshu_lineedit")
        self.jifen_yuanhanshu_lineedit.setGeometry(QRect(10, 100, 751, 21))
        self.groupBox_11 = QGroupBox(jifen)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.groupBox_11.setGeometry(QRect(10, 370, 771, 131))
        self.jifen_dingjifenzhi = QWebEngineView(self.groupBox_11)
        self.jifen_dingjifenzhi.setObjectName(u"jifen_dingjifenzhi")
        self.jifen_dingjifenzhi.setGeometry(QRect(10, 20, 751, 71))
        self.jifen_dingjifenzhi.setUrl(QUrl(u"about:blank"))
        self.jifen_dingjifenzhi_lineedit = QLineEdit(self.groupBox_11)
        self.jifen_dingjifenzhi_lineedit.setObjectName(u"jifen_dingjifenzhi_lineedit")
        self.jifen_dingjifenzhi_lineedit.setGeometry(QRect(10, 100, 751, 21))
        self.jifen_dingjifen = QCheckBox(jifen)
        self.jifen_dingjifen.setObjectName(u"jifen_dingjifen")
        self.jifen_dingjifen.setGeometry(QRect(530, 80, 89, 22))
        self.groupBox_8 = QGroupBox(jifen)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setGeometry(QRect(400, 60, 121, 51))
        self.jifen_shangxianzhi = QLineEdit(self.groupBox_8)
        self.jifen_shangxianzhi.setObjectName(u"jifen_shangxianzhi")
        self.jifen_shangxianzhi.setEnabled(False)
        self.jifen_shangxianzhi.setGeometry(QRect(10, 20, 101, 24))
        self.jifen_shangxianzhi.setClearButtonEnabled(True)
        self.jifen_jifen_button = QPushButton(jifen)
        self.jifen_jifen_button.setObjectName(u"jifen_jifen_button")
        self.jifen_jifen_button.setGeometry(QRect(10, 510, 771, 26))
        self.groupBox_9 = QGroupBox(jifen)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.groupBox_9.setGeometry(QRect(270, 60, 121, 51))
        self.jifen_xiaxianzhi = QLineEdit(self.groupBox_9)
        self.jifen_xiaxianzhi.setObjectName(u"jifen_xiaxianzhi")
        self.jifen_xiaxianzhi.setEnabled(False)
        self.jifen_xiaxianzhi.setGeometry(QRect(10, 20, 101, 24))
        self.jifen_xiaxianzhi.setClearButtonEnabled(True)
        self.groupBox2_2 = QGroupBox(jifen)
        self.groupBox2_2.setObjectName(u"groupBox2_2")
        self.groupBox2_2.setGeometry(QRect(10, 110, 771, 131))
        self.jifen_beijihanshu = QWebEngineView(self.groupBox2_2)
        self.jifen_beijihanshu.setObjectName(u"jifen_beijihanshu")
        self.jifen_beijihanshu.setGeometry(QRect(10, 20, 751, 101))
        self.jifen_beijihanshu.setUrl(QUrl(u"about:blank"))

        self.retranslateUi(jifen)

        QMetaObject.connectSlotsByName(jifen)
    # setupUi

    def retranslateUi(self, jifen):
        jifen.setWindowTitle(QCoreApplication.translate("jifen", u"Form", None))
        self.groupBox1_2.setTitle(QCoreApplication.translate("jifen", u"\u8f93\u5165\u8868\u8fbe\u5f0f", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("jifen", u"\u79ef\u5206\u53d8\u91cf", None))
        self.jifen_jifenbianliang.setText(QCoreApplication.translate("jifen", u"x", None))
        self.groupBox3_2.setTitle(QCoreApplication.translate("jifen", u"\u539f\u51fd\u6570", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("jifen", u"\u5b9a\u79ef\u5206\u503c", None))
        self.jifen_dingjifen.setText(QCoreApplication.translate("jifen", u"\u5b9a\u79ef\u5206", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("jifen", u"\u4e0a\u9650\u503c", None))
        self.jifen_jifen_button.setText(QCoreApplication.translate("jifen", u"\u79ef\u5206", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("jifen", u"\u4e0b\u9650\u503c", None))
        self.groupBox2_2.setTitle(QCoreApplication.translate("jifen", u"\u88ab\u79ef\u51fd\u6570", None))
    # retranslateUi

