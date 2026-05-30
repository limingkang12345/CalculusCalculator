# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'jisuanGBKGhS.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QWidget)

class Ui_jisuan(object):
    def setupUi(self, jisuan):
        if not jisuan.objectName():
            jisuan.setObjectName(u"jisuan")
        jisuan.resize(801, 551)
        self.groupBox_12 = QGroupBox(jisuan)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.groupBox_12.setGeometry(QRect(10, 320, 771, 181))
        self.jisuan_jisuanjieguo = QWebEngineView(self.groupBox_12)
        self.jisuan_jisuanjieguo.setObjectName(u"jisuan_jisuanjieguo")
        self.jisuan_jisuanjieguo.setGeometry(QRect(10, 20, 751, 121))
        self.jisuan_jisuanjieguo.setUrl(QUrl(u"about:blank"))
        self.jisuan_jisuanjieguo_lineedit = QLineEdit(self.groupBox_12)
        self.jisuan_jisuanjieguo_lineedit.setObjectName(u"jisuan_jisuanjieguo_lineedit")
        self.jisuan_jisuanjieguo_lineedit.setGeometry(QRect(10, 150, 751, 21))
        self.groupBox_10 = QGroupBox(jisuan)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.groupBox_10.setGeometry(QRect(10, 110, 771, 51))
        self.label = QLabel(self.groupBox_10)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 20, 151, 18))
        self.jisuan_jingdu = QLineEdit(self.groupBox_10)
        self.jisuan_jingdu.setObjectName(u"jisuan_jingdu")
        self.jisuan_jingdu.setEnabled(True)
        self.jisuan_jingdu.setGeometry(QRect(170, 20, 591, 21))
        self.jisuan_jingdu.setMaxLength(-1)
        self.jisuan_jingdu.setClearButtonEnabled(True)
        self.jisuan_jisuan_button = QPushButton(jisuan)
        self.jisuan_jisuan_button.setObjectName(u"jisuan_jisuan_button")
        self.jisuan_jisuan_button.setGeometry(QRect(10, 510, 771, 26))
        self.groupBox_2 = QGroupBox(jisuan)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 10, 771, 51))
        self.jisuan_input = QLineEdit(self.groupBox_2)
        self.jisuan_input.setObjectName(u"jisuan_input")
        self.jisuan_input.setGeometry(QRect(10, 20, 751, 21))
        self.jisuan_input.setClearButtonEnabled(True)
        self.groupBox_13 = QGroupBox(jisuan)
        self.groupBox_13.setObjectName(u"groupBox_13")
        self.groupBox_13.setGeometry(QRect(10, 60, 771, 51))
        self.jisuan_jisuanyinqing = QComboBox(self.groupBox_13)
        self.jisuan_jisuanyinqing.setObjectName(u"jisuan_jisuanyinqing")
        self.jisuan_jisuanyinqing.setGeometry(QRect(10, 20, 751, 21))
        self.jisuan_jisuanyinqing.setEditable(False)
        self.jisuan_jisuanyinqing.setMaxVisibleItems(13)
        self.groupBox_16 = QGroupBox(jisuan)
        self.groupBox_16.setObjectName(u"groupBox_16")
        self.groupBox_16.setGeometry(QRect(10, 160, 771, 151))
        self.jisuan_yuanshi = QWebEngineView(self.groupBox_16)
        self.jisuan_yuanshi.setObjectName(u"jisuan_yuanshi")
        self.jisuan_yuanshi.setGeometry(QRect(10, 20, 751, 121))
        self.jisuan_yuanshi.setUrl(QUrl(u"about:blank"))

        self.retranslateUi(jisuan)

        QMetaObject.connectSlotsByName(jisuan)
    # setupUi

    def retranslateUi(self, jisuan):
        jisuan.setWindowTitle(QCoreApplication.translate("jisuan", u"Form", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("jisuan", u"\u8ba1\u7b97\u7ed3\u679c", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("jisuan", u"\u9009\u9879", None))
        self.label.setText(QCoreApplication.translate("jisuan", u"\u7cbe\u5ea6\uff08\u5341\u8fdb\u5236\u4f4d\u6570\uff09\uff1a", None))
        self.jisuan_jingdu.setText(QCoreApplication.translate("jisuan", u"16", None))
        self.jisuan_jisuan_button.setText(QCoreApplication.translate("jisuan", u"\u8ba1\u7b97", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("jisuan", u"\u8f93\u5165\u8868\u8fbe\u5f0f", None))
        self.groupBox_13.setTitle(QCoreApplication.translate("jisuan", u"\u8ba1\u7b97\u5f15\u64ce", None))
        self.groupBox_16.setTitle(QCoreApplication.translate("jisuan", u"\u539f\u5f0f", None))
    # retranslateUi

