# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'budengshiXtHTMl.ui'
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

class Ui_budengshi(object):
    def setupUi(self, budengshi):
        if not budengshi.objectName():
            budengshi.setObjectName(u"budengshi")
        budengshi.resize(801, 551)
        self.groupBox_40 = QGroupBox(budengshi)
        self.groupBox_40.setObjectName(u"groupBox_40")
        self.groupBox_40.setGeometry(QRect(10, 310, 771, 191))
        self.budengshi_jieji = QWebEngineView(self.groupBox_40)
        self.budengshi_jieji.setObjectName(u"budengshi_jieji")
        self.budengshi_jieji.setGeometry(QRect(10, 20, 751, 131))
        self.budengshi_jieji.setUrl(QUrl(u"about:blank"))
        self.budengshi_jieji_lineedit = QLineEdit(self.groupBox_40)
        self.budengshi_jieji_lineedit.setObjectName(u"budengshi_jieji_lineedit")
        self.budengshi_jieji_lineedit.setGeometry(QRect(10, 160, 751, 21))
        self.groupBox_38 = QGroupBox(budengshi)
        self.groupBox_38.setObjectName(u"groupBox_38")
        self.groupBox_38.setGeometry(QRect(10, 10, 771, 80))
        self.budengshi_zuoshi = QLineEdit(self.groupBox_38)
        self.budengshi_zuoshi.setObjectName(u"budengshi_zuoshi")
        self.budengshi_zuoshi.setGeometry(QRect(10, 20, 751, 21))
        self.budengshi_youshi = QLineEdit(self.groupBox_38)
        self.budengshi_youshi.setObjectName(u"budengshi_youshi")
        self.budengshi_youshi.setGeometry(QRect(90, 50, 671, 21))
        self.budengshi_budenghao = QComboBox(self.groupBox_38)
        self.budengshi_budenghao.setObjectName(u"budengshi_budenghao")
        self.budengshi_budenghao.setGeometry(QRect(10, 50, 71, 21))
        self.groupBox_39 = QGroupBox(budengshi)
        self.groupBox_39.setObjectName(u"groupBox_39")
        self.groupBox_39.setGeometry(QRect(10, 90, 771, 51))
        self.label_14 = QLabel(self.groupBox_39)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(10, 20, 81, 18))
        self.budengshi_zhuyuanfuhao = QLineEdit(self.groupBox_39)
        self.budengshi_zhuyuanfuhao.setObjectName(u"budengshi_zhuyuanfuhao")
        self.budengshi_zhuyuanfuhao.setGeometry(QRect(100, 20, 51, 21))
        self.label_15 = QLabel(self.groupBox_39)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(170, 20, 111, 18))
        self.budengshi_quzhifanwei = QLineEdit(self.groupBox_39)
        self.budengshi_quzhifanwei.setObjectName(u"budengshi_quzhifanwei")
        self.budengshi_quzhifanwei.setGeometry(QRect(290, 20, 471, 21))
        self.groupBox_37 = QGroupBox(budengshi)
        self.groupBox_37.setObjectName(u"groupBox_37")
        self.groupBox_37.setGeometry(QRect(10, 150, 771, 161))
        self.budengshi_yuanshi = QWebEngineView(self.groupBox_37)
        self.budengshi_yuanshi.setObjectName(u"budengshi_yuanshi")
        self.budengshi_yuanshi.setGeometry(QRect(10, 20, 751, 131))
        self.budengshi_yuanshi.setUrl(QUrl(u"about:blank"))
        self.budengshi_qiujie = QPushButton(budengshi)
        self.budengshi_qiujie.setObjectName(u"budengshi_qiujie")
        self.budengshi_qiujie.setGeometry(QRect(10, 510, 771, 26))

        self.retranslateUi(budengshi)

        QMetaObject.connectSlotsByName(budengshi)
    # setupUi

    def retranslateUi(self, budengshi):
        budengshi.setWindowTitle(QCoreApplication.translate("budengshi", u"Form", None))
        self.groupBox_40.setTitle(QCoreApplication.translate("budengshi", u"\u89e3\u96c6", None))
        self.groupBox_38.setTitle(QCoreApplication.translate("budengshi", u"\u8f93\u5165\u4e0d\u7b49\u5f0f", None))
        self.budengshi_youshi.setText(QCoreApplication.translate("budengshi", u"0", None))
        self.groupBox_39.setTitle(QCoreApplication.translate("budengshi", u"\u9009\u9879", None))
        self.label_14.setText(QCoreApplication.translate("budengshi", u"\u4e3b\u5143\u7b26\u53f7\uff1a", None))
        self.budengshi_zhuyuanfuhao.setText(QCoreApplication.translate("budengshi", u"x", None))
        self.label_15.setText(QCoreApplication.translate("budengshi", u"\u4e3b\u5143\u53d6\u503c\u8303\u56f4\uff1a", None))
        self.budengshi_quzhifanwei.setText(QCoreApplication.translate("budengshi", u"Reals", None))
        self.groupBox_37.setTitle(QCoreApplication.translate("budengshi", u"\u539f\u4e0d\u7b49\u5f0f", None))
        self.budengshi_qiujie.setText(QCoreApplication.translate("budengshi", u"\u6c42\u89e3", None))
    # retranslateUi

