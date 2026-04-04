# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'fangchengwakGeg.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGroupBox, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QWidget)

class Ui_fangcheng(object):
    def setupUi(self, fangcheng):
        if not fangcheng.objectName():
            fangcheng.setObjectName(u"fangcheng")
        fangcheng.resize(801, 551)
        self.groupBox_15 = QGroupBox(fangcheng)
        self.groupBox_15.setObjectName(u"groupBox_15")
        self.groupBox_15.setGeometry(QRect(10, 90, 771, 51))
        self.label_5 = QLabel(self.groupBox_15)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 20, 81, 18))
        self.fangcheng_zhuyuanfuhao = QLineEdit(self.groupBox_15)
        self.fangcheng_zhuyuanfuhao.setObjectName(u"fangcheng_zhuyuanfuhao")
        self.fangcheng_zhuyuanfuhao.setGeometry(QRect(100, 20, 51, 21))
        self.label_6 = QLabel(self.groupBox_15)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(170, 20, 111, 18))
        self.fangcheng_quzhifanwei = QLineEdit(self.groupBox_15)
        self.fangcheng_quzhifanwei.setObjectName(u"fangcheng_quzhifanwei")
        self.fangcheng_quzhifanwei.setGeometry(QRect(290, 20, 361, 21))
        self.fangcheng_weifenfangcheng = QCheckBox(self.groupBox_15)
        self.fangcheng_weifenfangcheng.setObjectName(u"fangcheng_weifenfangcheng")
        self.fangcheng_weifenfangcheng.setGeometry(QRect(670, 20, 89, 22))
        self.groupBox_14 = QGroupBox(fangcheng)
        self.groupBox_14.setObjectName(u"groupBox_14")
        self.groupBox_14.setGeometry(QRect(10, 10, 771, 80))
        self.fangcheng_zuoshi = QLineEdit(self.groupBox_14)
        self.fangcheng_zuoshi.setObjectName(u"fangcheng_zuoshi")
        self.fangcheng_zuoshi.setGeometry(QRect(10, 20, 751, 21))
        self.label_4 = QLabel(self.groupBox_14)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 50, 16, 18))
        self.fangcheng_youshi = QLineEdit(self.groupBox_14)
        self.fangcheng_youshi.setObjectName(u"fangcheng_youshi")
        self.fangcheng_youshi.setGeometry(QRect(30, 50, 731, 21))
        self.groupBox_17 = QGroupBox(fangcheng)
        self.groupBox_17.setObjectName(u"groupBox_17")
        self.groupBox_17.setGeometry(QRect(10, 310, 771, 191))
        self.fangcheng_jieji = QWebEngineView(self.groupBox_17)
        self.fangcheng_jieji.setObjectName(u"fangcheng_jieji")
        self.fangcheng_jieji.setGeometry(QRect(10, 20, 751, 131))
        self.fangcheng_jieji.setUrl(QUrl(u"about:blank"))
        self.fangcheng_jieji_lineedit = QLineEdit(self.groupBox_17)
        self.fangcheng_jieji_lineedit.setObjectName(u"fangcheng_jieji_lineedit")
        self.fangcheng_jieji_lineedit.setGeometry(QRect(10, 160, 751, 21))
        self.fangcheng_qiujie = QPushButton(fangcheng)
        self.fangcheng_qiujie.setObjectName(u"fangcheng_qiujie")
        self.fangcheng_qiujie.setGeometry(QRect(10, 510, 771, 26))
        self.groupBox_18 = QGroupBox(fangcheng)
        self.groupBox_18.setObjectName(u"groupBox_18")
        self.groupBox_18.setGeometry(QRect(10, 150, 771, 161))
        self.fangcheng_yuanfangcheng = QWebEngineView(self.groupBox_18)
        self.fangcheng_yuanfangcheng.setObjectName(u"fangcheng_yuanfangcheng")
        self.fangcheng_yuanfangcheng.setGeometry(QRect(10, 20, 751, 131))
        self.fangcheng_yuanfangcheng.setUrl(QUrl(u"about:blank"))

        self.retranslateUi(fangcheng)

        QMetaObject.connectSlotsByName(fangcheng)
    # setupUi

    def retranslateUi(self, fangcheng):
        fangcheng.setWindowTitle(QCoreApplication.translate("fangcheng", u"Form", None))
        self.groupBox_15.setTitle(QCoreApplication.translate("fangcheng", u"\u9009\u9879", None))
        self.label_5.setText(QCoreApplication.translate("fangcheng", u"\u4e3b\u5143\u7b26\u53f7\uff1a", None))
        self.fangcheng_zhuyuanfuhao.setText(QCoreApplication.translate("fangcheng", u"x", None))
        self.label_6.setText(QCoreApplication.translate("fangcheng", u"\u4e3b\u5143\u53d6\u503c\u8303\u56f4\uff1a", None))
        self.fangcheng_quzhifanwei.setText(QCoreApplication.translate("fangcheng", u"Reals", None))
        self.fangcheng_weifenfangcheng.setText(QCoreApplication.translate("fangcheng", u"\u5fae\u5206\u65b9\u7a0b", None))
        self.groupBox_14.setTitle(QCoreApplication.translate("fangcheng", u"\u8f93\u5165\u65b9\u7a0b", None))
        self.label_4.setText(QCoreApplication.translate("fangcheng", u"=", None))
        self.fangcheng_youshi.setText(QCoreApplication.translate("fangcheng", u"0", None))
        self.groupBox_17.setTitle(QCoreApplication.translate("fangcheng", u"\u89e3\u96c6", None))
        self.fangcheng_qiujie.setText(QCoreApplication.translate("fangcheng", u"\u6c42\u89e3", None))
        self.groupBox_18.setTitle(QCoreApplication.translate("fangcheng", u"\u539f\u65b9\u7a0b", None))
    # retranslateUi

