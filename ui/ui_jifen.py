# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'jifenlUBfgi.ui'
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
    QLineEdit, QPushButton, QSizePolicy, QWidget)

class Ui_jifen(object):
    def setupUi(self, jifen):
        if not jifen.objectName():
            jifen.setObjectName(u"jifen")
        jifen.resize(801, 551)
        self.gridLayout = QGridLayout(jifen)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox1_2 = QGroupBox(jifen)
        self.groupBox1_2.setObjectName(u"groupBox1_2")
        self.gridLayout_2 = QGridLayout(self.groupBox1_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.jifen_input = QLineEdit(self.groupBox1_2)
        self.jifen_input.setObjectName(u"jifen_input")
        self.jifen_input.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.jifen_input, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox1_2, 0, 0, 1, 4)

        self.groupBox_7 = QGroupBox(jifen)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.gridLayout_3 = QGridLayout(self.groupBox_7)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.jifen_jifenbianliang = QLineEdit(self.groupBox_7)
        self.jifen_jifenbianliang.setObjectName(u"jifen_jifenbianliang")
        self.jifen_jifenbianliang.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.jifen_jifenbianliang, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_7, 1, 0, 1, 1)

        self.groupBox_9 = QGroupBox(jifen)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.gridLayout_4 = QGridLayout(self.groupBox_9)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.jifen_xiaxianzhi = QLineEdit(self.groupBox_9)
        self.jifen_xiaxianzhi.setObjectName(u"jifen_xiaxianzhi")
        self.jifen_xiaxianzhi.setEnabled(False)
        self.jifen_xiaxianzhi.setClearButtonEnabled(True)

        self.gridLayout_4.addWidget(self.jifen_xiaxianzhi, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_9, 1, 1, 1, 1)

        self.groupBox_8 = QGroupBox(jifen)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.gridLayout_5 = QGridLayout(self.groupBox_8)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.jifen_shangxianzhi = QLineEdit(self.groupBox_8)
        self.jifen_shangxianzhi.setObjectName(u"jifen_shangxianzhi")
        self.jifen_shangxianzhi.setEnabled(False)
        self.jifen_shangxianzhi.setClearButtonEnabled(True)

        self.gridLayout_5.addWidget(self.jifen_shangxianzhi, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_8, 1, 2, 1, 1)

        self.jifen_dingjifen = QCheckBox(jifen)
        self.jifen_dingjifen.setObjectName(u"jifen_dingjifen")

        self.gridLayout.addWidget(self.jifen_dingjifen, 1, 3, 1, 1)

        self.groupBox2_2 = QGroupBox(jifen)
        self.groupBox2_2.setObjectName(u"groupBox2_2")
        self.gridLayout_6 = QGridLayout(self.groupBox2_2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(-1, 9, -1, 9)
        self.jifen_beijihanshu = QWebEngineView(self.groupBox2_2)
        self.jifen_beijihanshu.setObjectName(u"jifen_beijihanshu")
        self.jifen_beijihanshu.setUrl(QUrl(u"about:blank"))

        self.gridLayout_6.addWidget(self.jifen_beijihanshu, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox2_2, 2, 0, 1, 4)

        self.groupBox3_2 = QGroupBox(jifen)
        self.groupBox3_2.setObjectName(u"groupBox3_2")
        self.gridLayout_7 = QGridLayout(self.groupBox3_2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(-1, 9, -1, 9)
        self.jifen_yuanhanshu = QWebEngineView(self.groupBox3_2)
        self.jifen_yuanhanshu.setObjectName(u"jifen_yuanhanshu")
        self.jifen_yuanhanshu.setUrl(QUrl(u"about:blank"))

        self.gridLayout_7.addWidget(self.jifen_yuanhanshu, 0, 0, 1, 1)

        self.jifen_yuanhanshu_lineedit = QLineEdit(self.groupBox3_2)
        self.jifen_yuanhanshu_lineedit.setObjectName(u"jifen_yuanhanshu_lineedit")

        self.gridLayout_7.addWidget(self.jifen_yuanhanshu_lineedit, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox3_2, 3, 0, 1, 4)

        self.groupBox_11 = QGroupBox(jifen)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.gridLayout_8 = QGridLayout(self.groupBox_11)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(-1, 9, -1, 9)
        self.jifen_dingjifenzhi = QWebEngineView(self.groupBox_11)
        self.jifen_dingjifenzhi.setObjectName(u"jifen_dingjifenzhi")
        self.jifen_dingjifenzhi.setUrl(QUrl(u"about:blank"))

        self.gridLayout_8.addWidget(self.jifen_dingjifenzhi, 0, 0, 1, 1)

        self.jifen_dingjifenzhi_lineedit = QLineEdit(self.groupBox_11)
        self.jifen_dingjifenzhi_lineedit.setObjectName(u"jifen_dingjifenzhi_lineedit")

        self.gridLayout_8.addWidget(self.jifen_dingjifenzhi_lineedit, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_11, 4, 0, 1, 4)

        self.jifen_jifen_button = QPushButton(jifen)
        self.jifen_jifen_button.setObjectName(u"jifen_jifen_button")

        self.gridLayout.addWidget(self.jifen_jifen_button, 5, 0, 1, 4)

        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(2, 4)
        self.gridLayout.setRowStretch(3, 5)
        self.gridLayout.setRowStretch(4, 5)

        self.retranslateUi(jifen)

        QMetaObject.connectSlotsByName(jifen)
    # setupUi

    def retranslateUi(self, jifen):
        jifen.setWindowTitle(QCoreApplication.translate("jifen", u"Form", None))
        self.groupBox1_2.setTitle(QCoreApplication.translate("jifen", u"\u8f93\u5165\u8868\u8fbe\u5f0f", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("jifen", u"\u79ef\u5206\u53d8\u91cf", None))
        self.jifen_jifenbianliang.setText(QCoreApplication.translate("jifen", u"x", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("jifen", u"\u4e0b\u9650\u503c", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("jifen", u"\u4e0a\u9650\u503c", None))
        self.jifen_dingjifen.setText(QCoreApplication.translate("jifen", u"\u5b9a\u79ef\u5206", None))
        self.groupBox2_2.setTitle(QCoreApplication.translate("jifen", u"\u88ab\u79ef\u51fd\u6570", None))
        self.groupBox3_2.setTitle(QCoreApplication.translate("jifen", u"\u539f\u51fd\u6570", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("jifen", u"\u5b9a\u79ef\u5206\u503c", None))
        self.jifen_jifen_button.setText(QCoreApplication.translate("jifen", u"\u79ef\u5206", None))
    # retranslateUi

