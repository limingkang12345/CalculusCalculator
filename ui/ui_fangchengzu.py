# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'fangchengzuiXmwHO.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QWidget)

class Ui_fangchengzu(object):
    def setupUi(self, fangchengzu):
        if not fangchengzu.objectName():
            fangchengzu.setObjectName(u"fangchengzu")
        fangchengzu.resize(801, 551)
        self.groupBox_24 = QGroupBox(fangchengzu)
        self.groupBox_24.setObjectName(u"groupBox_24")
        self.groupBox_24.setGeometry(QRect(10, 210, 771, 131))
        self.fangchengzu_yuanfangcheng = QWebEngineView(self.groupBox_24)
        self.fangchengzu_yuanfangcheng.setObjectName(u"fangchengzu_yuanfangcheng")
        self.fangchengzu_yuanfangcheng.setGeometry(QRect(10, 20, 751, 101))
        self.fangchengzu_yuanfangcheng.setUrl(QUrl(u"about:blank"))
        self.fangchengzu_qiujie = QPushButton(fangchengzu)
        self.fangchengzu_qiujie.setObjectName(u"fangchengzu_qiujie")
        self.fangchengzu_qiujie.setGeometry(QRect(10, 510, 771, 26))
        self.groupBox_25 = QGroupBox(fangchengzu)
        self.groupBox_25.setObjectName(u"groupBox_25")
        self.groupBox_25.setGeometry(QRect(10, 340, 771, 161))
        self.fangchengzu_jieji = QWebEngineView(self.groupBox_25)
        self.fangchengzu_jieji.setObjectName(u"fangchengzu_jieji")
        self.fangchengzu_jieji.setGeometry(QRect(10, 20, 751, 101))
        self.fangchengzu_jieji.setUrl(QUrl(u"about:blank"))
        self.fangchengzu_jieji_lineedit = QLineEdit(self.groupBox_25)
        self.fangchengzu_jieji_lineedit.setObjectName(u"fangchengzu_jieji_lineedit")
        self.fangchengzu_jieji_lineedit.setGeometry(QRect(10, 130, 751, 21))
        self.groupBox_23 = QGroupBox(fangchengzu)
        self.groupBox_23.setObjectName(u"groupBox_23")
        self.groupBox_23.setGeometry(QRect(10, 10, 771, 201))
        self.fangchengzu_zuoshi = QLineEdit(self.groupBox_23)
        self.fangchengzu_zuoshi.setObjectName(u"fangchengzu_zuoshi")
        self.fangchengzu_zuoshi.setGeometry(QRect(270, 20, 491, 21))
        self.label_10 = QLabel(self.groupBox_23)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(270, 50, 16, 18))
        self.fangchengzu_youshi = QLineEdit(self.groupBox_23)
        self.fangchengzu_youshi.setObjectName(u"fangchengzu_youshi")
        self.fangchengzu_youshi.setGeometry(QRect(290, 50, 471, 21))
        self.fangchengzu_shanchu = QPushButton(self.groupBox_23)
        self.fangchengzu_shanchu.setObjectName(u"fangchengzu_shanchu")
        self.fangchengzu_shanchu.setGeometry(QRect(670, 80, 87, 26))
        self.fangchengzu_baocun = QPushButton(self.groupBox_23)
        self.fangchengzu_baocun.setObjectName(u"fangchengzu_baocun")
        self.fangchengzu_baocun.setGeometry(QRect(570, 80, 87, 26))
        self.fangchengzu_fangcheng = QListWidget(self.groupBox_23)
        self.fangchengzu_fangcheng.setObjectName(u"fangchengzu_fangcheng")
        self.fangchengzu_fangcheng.setGeometry(QRect(10, 20, 251, 171))
        self.label_13 = QLabel(self.groupBox_23)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(270, 80, 71, 18))
        self.fangchengzu_ziyoubianliang = QLineEdit(self.groupBox_23)
        self.fangchengzu_ziyoubianliang.setObjectName(u"fangchengzu_ziyoubianliang")
        self.fangchengzu_ziyoubianliang.setGeometry(QRect(340, 80, 211, 21))
        self.label_25 = QLabel(self.groupBox_23)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setGeometry(QRect(270, 110, 281, 51))

        self.retranslateUi(fangchengzu)

        QMetaObject.connectSlotsByName(fangchengzu)
    # setupUi

    def retranslateUi(self, fangchengzu):
        fangchengzu.setWindowTitle(QCoreApplication.translate("fangchengzu", u"Form", None))
        self.groupBox_24.setTitle(QCoreApplication.translate("fangchengzu", u"\u539f\u65b9\u7a0b", None))
        self.fangchengzu_qiujie.setText(QCoreApplication.translate("fangchengzu", u"\u6c42\u89e3", None))
        self.groupBox_25.setTitle(QCoreApplication.translate("fangchengzu", u"\u89e3\u96c6", None))
        self.groupBox_23.setTitle(QCoreApplication.translate("fangchengzu", u"\u65b9\u7a0b\u7f16\u8f91", None))
        self.label_10.setText(QCoreApplication.translate("fangchengzu", u"=", None))
        self.fangchengzu_youshi.setText(QCoreApplication.translate("fangchengzu", u"0", None))
        self.fangchengzu_shanchu.setText(QCoreApplication.translate("fangchengzu", u"\u5220\u9664", None))
        self.fangchengzu_baocun.setText(QCoreApplication.translate("fangchengzu", u"\u4fdd\u5b58", None))
        self.label_13.setText(QCoreApplication.translate("fangchengzu", u"<html><head/><body><p>\u6c42\u89e3\u53d8\u91cf\uff1a</p></body></html>", None))
        self.fangchengzu_ziyoubianliang.setInputMask("")
        self.fangchengzu_ziyoubianliang.setText(QCoreApplication.translate("fangchengzu", u"x,y", None))
        self.fangchengzu_ziyoubianliang.setPlaceholderText("")
        self.label_25.setText(QCoreApplication.translate("fangchengzu", u"<html><head/><body><p>(\u63d0\u793a\uff1a\u8bf7<span style=\" font-weight:700; text-decoration: underline;\">\u53ea\u7528\u9017\u53f7</span>\u5206\u9694\u53d8\u91cf\uff0c\u4f8b\u5982\uff1ax,y,z)</p><p>(\u5305\u62ec<span style=\" font-weight:700; text-decoration: underline;\">\u65b9\u7a0b\u7ec4</span>\u6240\u6709\u9700\u8981\u6c42\u89e3\u7684\u53d8\u91cf)</p></body></html>", None))
    # retranslateUi

