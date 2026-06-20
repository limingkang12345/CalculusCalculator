# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bianxingzuKBjI.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QWidget)

class Ui_bianxing(object):
    def setupUi(self, bianxing):
        if not bianxing.objectName():
            bianxing.setObjectName(u"bianxing")
        bianxing.resize(801, 551)
        self.gridLayout = QGridLayout(bianxing)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_2 = QGroupBox(bianxing)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.bianxing_input = QLineEdit(self.groupBox_2)
        self.bianxing_input.setObjectName(u"bianxing_input")
        self.bianxing_input.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.bianxing_input, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_2, 0, 0, 1, 1)

        self.groupBox_13 = QGroupBox(bianxing)
        self.groupBox_13.setObjectName(u"groupBox_13")
        self.gridLayout_3 = QGridLayout(self.groupBox_13)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.bianxing_bianxingfangfa = QComboBox(self.groupBox_13)
        self.bianxing_bianxingfangfa.setObjectName(u"bianxing_bianxingfangfa")
        self.bianxing_bianxingfangfa.setEditable(False)
        self.bianxing_bianxingfangfa.setMaxVisibleItems(13)

        self.gridLayout_3.addWidget(self.bianxing_bianxingfangfa, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_13, 1, 0, 1, 1)

        self.groupBox_10 = QGroupBox(bianxing)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.gridLayout_4 = QGridLayout(self.groupBox_10)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label = QLabel(self.groupBox_10)
        self.label.setObjectName(u"label")

        self.gridLayout_4.addWidget(self.label, 0, 0, 1, 1)

        self.bianxing_zhuyuanfuhao = QLineEdit(self.groupBox_10)
        self.bianxing_zhuyuanfuhao.setObjectName(u"bianxing_zhuyuanfuhao")
        self.bianxing_zhuyuanfuhao.setEnabled(False)
        self.bianxing_zhuyuanfuhao.setClearButtonEnabled(True)

        self.gridLayout_4.addWidget(self.bianxing_zhuyuanfuhao, 0, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox_10)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_4.addWidget(self.label_2, 0, 2, 1, 1)

        self.bianxing_huanyuanfuhao = QLineEdit(self.groupBox_10)
        self.bianxing_huanyuanfuhao.setObjectName(u"bianxing_huanyuanfuhao")
        self.bianxing_huanyuanfuhao.setEnabled(False)
        self.bianxing_huanyuanfuhao.setClearButtonEnabled(True)

        self.gridLayout_4.addWidget(self.bianxing_huanyuanfuhao, 0, 3, 1, 1)

        self.label_3 = QLabel(self.groupBox_10)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_4.addWidget(self.label_3, 0, 4, 1, 1)

        self.bianxing_huanyuanshi = QLineEdit(self.groupBox_10)
        self.bianxing_huanyuanshi.setObjectName(u"bianxing_huanyuanshi")
        self.bianxing_huanyuanshi.setEnabled(False)
        self.bianxing_huanyuanshi.setClearButtonEnabled(True)

        self.gridLayout_4.addWidget(self.bianxing_huanyuanshi, 0, 5, 1, 1)


        self.gridLayout.addWidget(self.groupBox_10, 2, 0, 1, 1)

        self.groupBox_16 = QGroupBox(bianxing)
        self.groupBox_16.setObjectName(u"groupBox_16")
        self.gridLayout_5 = QGridLayout(self.groupBox_16)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.bianxing_yuanshi = QWebEngineView(self.groupBox_16)
        self.bianxing_yuanshi.setObjectName(u"bianxing_yuanshi")
        self.bianxing_yuanshi.setUrl(QUrl(u"about:blank"))

        self.gridLayout_5.addWidget(self.bianxing_yuanshi, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_16, 3, 0, 1, 1)

        self.groupBox_12 = QGroupBox(bianxing)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.gridLayout_6 = QGridLayout(self.groupBox_12)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.bianxing_bianxingshi = QWebEngineView(self.groupBox_12)
        self.bianxing_bianxingshi.setObjectName(u"bianxing_bianxingshi")
        self.bianxing_bianxingshi.setUrl(QUrl(u"about:blank"))

        self.gridLayout_6.addWidget(self.bianxing_bianxingshi, 0, 0, 1, 1)

        self.bianxing_bianxingshi_lineedit = QLineEdit(self.groupBox_12)
        self.bianxing_bianxingshi_lineedit.setObjectName(u"bianxing_bianxingshi_lineedit")

        self.gridLayout_6.addWidget(self.bianxing_bianxingshi_lineedit, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_12, 4, 0, 1, 1)

        self.bianxing_bianxing_button = QPushButton(bianxing)
        self.bianxing_bianxing_button.setObjectName(u"bianxing_bianxing_button")

        self.gridLayout.addWidget(self.bianxing_bianxing_button, 5, 0, 1, 1)

        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(2, 1)
        self.gridLayout.setRowStretch(3, 4)
        self.gridLayout.setRowStretch(4, 5)
        self.gridLayout.setRowStretch(5, 1)

        self.retranslateUi(bianxing)

        QMetaObject.connectSlotsByName(bianxing)
    # setupUi

    def retranslateUi(self, bianxing):
        bianxing.setWindowTitle(QCoreApplication.translate("bianxing", u"Form", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("bianxing", u"\u8f93\u5165\u8868\u8fbe\u5f0f", None))
        self.groupBox_13.setTitle(QCoreApplication.translate("bianxing", u"\u53d8\u5f62\u65b9\u6cd5", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("bianxing", u"\u9009\u9879", None))
        self.label.setText(QCoreApplication.translate("bianxing", u"\u4e3b\u5143\u7b26\u53f7\uff1a", None))
        self.bianxing_zhuyuanfuhao.setText(QCoreApplication.translate("bianxing", u"x", None))
        self.label_2.setText(QCoreApplication.translate("bianxing", u"\u6362\u5143\u7b26\u53f7\uff1a", None))
        self.bianxing_huanyuanfuhao.setText(QCoreApplication.translate("bianxing", u"t", None))
        self.label_3.setText(QCoreApplication.translate("bianxing", u"=", None))
        self.bianxing_huanyuanshi.setText(QCoreApplication.translate("bianxing", u"x+1", None))
        self.groupBox_16.setTitle(QCoreApplication.translate("bianxing", u"\u539f\u5f0f", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("bianxing", u"\u53d8\u5f62\u5f0f", None))
        self.bianxing_bianxing_button.setText(QCoreApplication.translate("bianxing", u"\u53d8\u5f62", None))
    # retranslateUi

