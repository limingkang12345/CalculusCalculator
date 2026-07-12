# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'fangchengzueYXhBv.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
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
from PySide6.QtWidgets import (QApplication, QGraphicsView, QGridLayout, QGroupBox,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QWidget)

class Ui_fangchengzu(object):
    def setupUi(self, fangchengzu):
        if not fangchengzu.objectName():
            fangchengzu.setObjectName(u"fangchengzu")
        fangchengzu.resize(801, 551)
        self.gridLayout = QGridLayout(fangchengzu)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_23 = QGroupBox(fangchengzu)
        self.groupBox_23.setObjectName(u"groupBox_23")
        self.gridLayout_2 = QGridLayout(self.groupBox_23)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.fangchengzu_fangcheng = QListWidget(self.groupBox_23)
        self.fangchengzu_fangcheng.setObjectName(u"fangchengzu_fangcheng")

        self.gridLayout_2.addWidget(self.fangchengzu_fangcheng, 0, 0, 4, 1)

        self.fangchengzu_zuoshi = QLineEdit(self.groupBox_23)
        self.fangchengzu_zuoshi.setObjectName(u"fangchengzu_zuoshi")
        self.fangchengzu_zuoshi.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.fangchengzu_zuoshi, 0, 1, 1, 5)

        self.label_10 = QLabel(self.groupBox_23)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_2.addWidget(self.label_10, 1, 1, 1, 1)

        self.fangchengzu_youshi = QLineEdit(self.groupBox_23)
        self.fangchengzu_youshi.setObjectName(u"fangchengzu_youshi")
        self.fangchengzu_youshi.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.fangchengzu_youshi, 1, 2, 1, 4)

        self.label_13 = QLabel(self.groupBox_23)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_2.addWidget(self.label_13, 2, 1, 1, 2)

        self.fangchengzu_ziyoubianliang = QLineEdit(self.groupBox_23)
        self.fangchengzu_ziyoubianliang.setObjectName(u"fangchengzu_ziyoubianliang")
        self.fangchengzu_ziyoubianliang.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.fangchengzu_ziyoubianliang, 2, 3, 1, 1)

        self.fangchengzu_baocun = QPushButton(self.groupBox_23)
        self.fangchengzu_baocun.setObjectName(u"fangchengzu_baocun")

        self.gridLayout_2.addWidget(self.fangchengzu_baocun, 2, 4, 1, 1)

        self.fangchengzu_shanchu = QPushButton(self.groupBox_23)
        self.fangchengzu_shanchu.setObjectName(u"fangchengzu_shanchu")

        self.gridLayout_2.addWidget(self.fangchengzu_shanchu, 2, 5, 1, 1)

        self.label_25 = QLabel(self.groupBox_23)
        self.label_25.setObjectName(u"label_25")

        self.gridLayout_2.addWidget(self.label_25, 3, 1, 1, 3)


        self.gridLayout.addWidget(self.groupBox_23, 0, 0, 1, 1)

        self.groupBox_24 = QGroupBox(fangchengzu)
        self.groupBox_24.setObjectName(u"groupBox_24")
        self.gridLayout_3 = QGridLayout(self.groupBox_24)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.fangchengzu_yuanfangcheng = QGraphicsView(self.groupBox_24)
        self.fangchengzu_yuanfangcheng.setObjectName(u"fangchengzu_yuanfangcheng")
        self.fangchengzu_yuanfangcheng.setProperty(u"url", QUrl(u"about:blank"))

        self.gridLayout_3.addWidget(self.fangchengzu_yuanfangcheng, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_24, 1, 0, 1, 1)

        self.groupBox_25 = QGroupBox(fangchengzu)
        self.groupBox_25.setObjectName(u"groupBox_25")
        self.gridLayout_4 = QGridLayout(self.groupBox_25)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.fangchengzu_jieji = QGraphicsView(self.groupBox_25)
        self.fangchengzu_jieji.setObjectName(u"fangchengzu_jieji")
        self.fangchengzu_jieji.setProperty(u"url", QUrl(u"about:blank"))

        self.gridLayout_4.addWidget(self.fangchengzu_jieji, 0, 0, 1, 1)

        self.fangchengzu_jieji_lineedit = QLineEdit(self.groupBox_25)
        self.fangchengzu_jieji_lineedit.setObjectName(u"fangchengzu_jieji_lineedit")

        self.gridLayout_4.addWidget(self.fangchengzu_jieji_lineedit, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_25, 2, 0, 1, 1)

        self.fangchengzu_qiujie = QPushButton(fangchengzu)
        self.fangchengzu_qiujie.setObjectName(u"fangchengzu_qiujie")

        self.gridLayout.addWidget(self.fangchengzu_qiujie, 3, 0, 1, 1)

        self.gridLayout.setRowStretch(0, 4)
        self.gridLayout.setRowStretch(1, 4)
        self.gridLayout.setRowStretch(2, 5)

        self.retranslateUi(fangchengzu)

        QMetaObject.connectSlotsByName(fangchengzu)
    # setupUi

    def retranslateUi(self, fangchengzu):
        fangchengzu.setWindowTitle(QCoreApplication.translate("fangchengzu", u"Form", None))
        self.groupBox_23.setTitle(QCoreApplication.translate("fangchengzu", u"\u65b9\u7a0b\u7f16\u8f91", None))
        self.label_10.setText(QCoreApplication.translate("fangchengzu", u"=", None))
        self.fangchengzu_youshi.setText(QCoreApplication.translate("fangchengzu", u"0", None))
        self.label_13.setText(QCoreApplication.translate("fangchengzu", u"<html><head/><body><p>\u6c42\u89e3\u53d8\u91cf\uff1a</p></body></html>", None))
        self.fangchengzu_ziyoubianliang.setInputMask("")
        self.fangchengzu_ziyoubianliang.setText(QCoreApplication.translate("fangchengzu", u"x,y", None))
        self.fangchengzu_ziyoubianliang.setPlaceholderText("")
        self.fangchengzu_baocun.setText(QCoreApplication.translate("fangchengzu", u"\u4fdd\u5b58", None))
        self.fangchengzu_shanchu.setText(QCoreApplication.translate("fangchengzu", u"\u5220\u9664", None))
        self.label_25.setText(QCoreApplication.translate("fangchengzu", u"<html><head/><body><p>(\u63d0\u793a\uff1a\u8bf7<span style=\" font-weight:700; text-decoration: underline;\">\u53ea\u7528\u9017\u53f7</span>\u5206\u9694\u53d8\u91cf\uff0c\u4f8b\u5982\uff1ax,y,z)</p><p>(\u5305\u62ec<span style=\" font-weight:700; text-decoration: underline;\">\u65b9\u7a0b\u7ec4</span>\u6240\u6709\u9700\u8981\u6c42\u89e3\u7684\u53d8\u91cf)</p></body></html>", None))
        self.groupBox_24.setTitle(QCoreApplication.translate("fangchengzu", u"\u539f\u65b9\u7a0b", None))
        self.groupBox_25.setTitle(QCoreApplication.translate("fangchengzu", u"\u89e3\u96c6", None))
        self.fangchengzu_qiujie.setText(QCoreApplication.translate("fangchengzu", u"\u6c42\u89e3", None))
    # retranslateUi

