# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'budengshizuOyRXwR.ui'
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
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QWidget)

class Ui_budengshizu(object):
    def setupUi(self, budengshizu):
        if not budengshizu.objectName():
            budengshizu.setObjectName(u"budengshizu")
        budengshizu.resize(801, 551)
        self.groupBox_59 = QGroupBox(budengshizu)
        self.groupBox_59.setObjectName(u"groupBox_59")
        self.groupBox_59.setGeometry(QRect(10, 340, 771, 161))
        self.budengshizu_jieji = QWebEngineView(self.groupBox_59)
        self.budengshizu_jieji.setObjectName(u"budengshizu_jieji")
        self.budengshizu_jieji.setGeometry(QRect(10, 20, 751, 101))
        self.budengshizu_jieji.setUrl(QUrl(u"about:blank"))
        self.budengshizu_jieji_lineedit = QLineEdit(self.groupBox_59)
        self.budengshizu_jieji_lineedit.setObjectName(u"budengshizu_jieji_lineedit")
        self.budengshizu_jieji_lineedit.setGeometry(QRect(10, 130, 751, 21))
        self.groupBox_61 = QGroupBox(budengshizu)
        self.groupBox_61.setObjectName(u"groupBox_61")
        self.groupBox_61.setGeometry(QRect(10, 10, 771, 201))
        self.budengshizu_zuoshi = QLineEdit(self.groupBox_61)
        self.budengshizu_zuoshi.setObjectName(u"budengshizu_zuoshi")
        self.budengshizu_zuoshi.setGeometry(QRect(270, 20, 491, 21))
        self.budengshizu_zuoshi.setClearButtonEnabled(True)
        self.budengshizu_youshi = QLineEdit(self.groupBox_61)
        self.budengshizu_youshi.setObjectName(u"budengshizu_youshi")
        self.budengshizu_youshi.setGeometry(QRect(350, 50, 411, 21))
        self.budengshizu_youshi.setClearButtonEnabled(True)
        self.budengshizu_shanchu = QPushButton(self.groupBox_61)
        self.budengshizu_shanchu.setObjectName(u"budengshizu_shanchu")
        self.budengshizu_shanchu.setGeometry(QRect(670, 80, 87, 26))
        self.budengshizu_baocun = QPushButton(self.groupBox_61)
        self.budengshizu_baocun.setObjectName(u"budengshizu_baocun")
        self.budengshizu_baocun.setGeometry(QRect(570, 80, 87, 26))
        self.budengshizu_budengshi = QListWidget(self.groupBox_61)
        self.budengshizu_budengshi.setObjectName(u"budengshizu_budengshi")
        self.budengshizu_budengshi.setGeometry(QRect(10, 20, 251, 171))
        self.label_33 = QLabel(self.groupBox_61)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setGeometry(QRect(270, 80, 151, 18))
        self.budengshizu_ziyoubianliang = QLineEdit(self.groupBox_61)
        self.budengshizu_ziyoubianliang.setObjectName(u"budengshizu_ziyoubianliang")
        self.budengshizu_ziyoubianliang.setGeometry(QRect(430, 80, 121, 21))
        self.budengshizu_ziyoubianliang.setClearButtonEnabled(True)
        self.budengshizu_budenghao = QComboBox(self.groupBox_61)
        self.budengshizu_budenghao.setObjectName(u"budengshizu_budenghao")
        self.budengshizu_budenghao.setGeometry(QRect(270, 50, 71, 21))
        self.budengshizu_qiujie = QPushButton(budengshizu)
        self.budengshizu_qiujie.setObjectName(u"budengshizu_qiujie")
        self.budengshizu_qiujie.setGeometry(QRect(10, 510, 771, 26))
        self.groupBox_60 = QGroupBox(budengshizu)
        self.groupBox_60.setObjectName(u"groupBox_60")
        self.groupBox_60.setGeometry(QRect(10, 210, 771, 131))
        self.budengshizu_yuanbudengshi = QWebEngineView(self.groupBox_60)
        self.budengshizu_yuanbudengshi.setObjectName(u"budengshizu_yuanbudengshi")
        self.budengshizu_yuanbudengshi.setGeometry(QRect(10, 20, 751, 101))
        self.budengshizu_yuanbudengshi.setUrl(QUrl(u"about:blank"))

        self.retranslateUi(budengshizu)

        self.budengshizu_budenghao.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(budengshizu)
    # setupUi

    def retranslateUi(self, budengshizu):
        budengshizu.setWindowTitle(QCoreApplication.translate("budengshizu", u"Form", None))
        self.groupBox_59.setTitle(QCoreApplication.translate("budengshizu", u"\u89e3\u96c6", None))
        self.groupBox_61.setTitle(QCoreApplication.translate("budengshizu", u"\u4e0d\u7b49\u5f0f\u7f16\u8f91", None))
        self.budengshizu_youshi.setText(QCoreApplication.translate("budengshizu", u"0", None))
        self.budengshizu_shanchu.setText(QCoreApplication.translate("budengshizu", u"\u5220\u9664", None))
        self.budengshizu_baocun.setText(QCoreApplication.translate("budengshizu", u"\u4fdd\u5b58", None))
        self.label_33.setText(QCoreApplication.translate("budengshizu", u"<html><head/><body><p>\u6c42\u89e3\u53d8\u91cf(<span style=\" font-weight:700; text-decoration: underline;\">\u4ec5\u5141\u8bb8\u4e00\u5143</span>)\uff1a</p></body></html>", None))
        self.budengshizu_ziyoubianliang.setInputMask("")
        self.budengshizu_ziyoubianliang.setText(QCoreApplication.translate("budengshizu", u"x", None))
        self.budengshizu_ziyoubianliang.setPlaceholderText("")
        self.budengshizu_qiujie.setText(QCoreApplication.translate("budengshizu", u"\u6c42\u89e3", None))
        self.groupBox_60.setTitle(QCoreApplication.translate("budengshizu", u"\u539f\u4e0d\u7b49\u5f0f", None))
    # retranslateUi

