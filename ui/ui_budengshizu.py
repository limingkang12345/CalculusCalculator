# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'budengshizuUGlVoF.ui'
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
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QWidget)

class Ui_budengshizu(object):
    def setupUi(self, budengshizu):
        if not budengshizu.objectName():
            budengshizu.setObjectName(u"budengshizu")
        budengshizu.resize(801, 551)
        self.gridLayout = QGridLayout(budengshizu)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_61 = QGroupBox(budengshizu)
        self.groupBox_61.setObjectName(u"groupBox_61")
        self.gridLayout_2 = QGridLayout(self.groupBox_61)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.budengshizu_budengshi = QListWidget(self.groupBox_61)
        self.budengshizu_budengshi.setObjectName(u"budengshizu_budengshi")

        self.gridLayout_2.addWidget(self.budengshizu_budengshi, 0, 0, 3, 1)

        self.budengshizu_zuoshi = QLineEdit(self.groupBox_61)
        self.budengshizu_zuoshi.setObjectName(u"budengshizu_zuoshi")
        self.budengshizu_zuoshi.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.budengshizu_zuoshi, 0, 1, 1, 5)

        self.budengshizu_budenghao = QComboBox(self.groupBox_61)
        self.budengshizu_budenghao.setObjectName(u"budengshizu_budenghao")

        self.gridLayout_2.addWidget(self.budengshizu_budenghao, 1, 1, 1, 1)

        self.budengshizu_youshi = QLineEdit(self.groupBox_61)
        self.budengshizu_youshi.setObjectName(u"budengshizu_youshi")
        self.budengshizu_youshi.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.budengshizu_youshi, 1, 2, 1, 4)

        self.label_33 = QLabel(self.groupBox_61)
        self.label_33.setObjectName(u"label_33")

        self.gridLayout_2.addWidget(self.label_33, 2, 1, 1, 2)

        self.budengshizu_ziyoubianliang = QLineEdit(self.groupBox_61)
        self.budengshizu_ziyoubianliang.setObjectName(u"budengshizu_ziyoubianliang")
        self.budengshizu_ziyoubianliang.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.budengshizu_ziyoubianliang, 2, 3, 1, 1)

        self.budengshizu_baocun = QPushButton(self.groupBox_61)
        self.budengshizu_baocun.setObjectName(u"budengshizu_baocun")

        self.gridLayout_2.addWidget(self.budengshizu_baocun, 2, 4, 1, 1)

        self.budengshizu_shanchu = QPushButton(self.groupBox_61)
        self.budengshizu_shanchu.setObjectName(u"budengshizu_shanchu")

        self.gridLayout_2.addWidget(self.budengshizu_shanchu, 2, 5, 1, 1)


        self.gridLayout.addWidget(self.groupBox_61, 0, 0, 1, 1)

        self.groupBox_60 = QGroupBox(budengshizu)
        self.groupBox_60.setObjectName(u"groupBox_60")
        self.gridLayout_3 = QGridLayout(self.groupBox_60)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.budengshizu_yuanbudengshi = QWebEngineView(self.groupBox_60)
        self.budengshizu_yuanbudengshi.setObjectName(u"budengshizu_yuanbudengshi")
        self.budengshizu_yuanbudengshi.setUrl(QUrl(u"about:blank"))

        self.gridLayout_3.addWidget(self.budengshizu_yuanbudengshi, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_60, 1, 0, 1, 1)

        self.groupBox_59 = QGroupBox(budengshizu)
        self.groupBox_59.setObjectName(u"groupBox_59")
        self.gridLayout_4 = QGridLayout(self.groupBox_59)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.budengshizu_jieji = QWebEngineView(self.groupBox_59)
        self.budengshizu_jieji.setObjectName(u"budengshizu_jieji")
        self.budengshizu_jieji.setUrl(QUrl(u"about:blank"))

        self.gridLayout_4.addWidget(self.budengshizu_jieji, 0, 0, 1, 1)

        self.budengshizu_jieji_lineedit = QLineEdit(self.groupBox_59)
        self.budengshizu_jieji_lineedit.setObjectName(u"budengshizu_jieji_lineedit")

        self.gridLayout_4.addWidget(self.budengshizu_jieji_lineedit, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_59, 2, 0, 1, 1)

        self.budengshizu_qiujie = QPushButton(budengshizu)
        self.budengshizu_qiujie.setObjectName(u"budengshizu_qiujie")

        self.gridLayout.addWidget(self.budengshizu_qiujie, 3, 0, 1, 1)

        self.gridLayout.setRowStretch(0, 6)
        self.gridLayout.setRowStretch(1, 4)
        self.gridLayout.setRowStretch(2, 5)

        self.retranslateUi(budengshizu)

        self.budengshizu_budenghao.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(budengshizu)
    # setupUi

    def retranslateUi(self, budengshizu):
        budengshizu.setWindowTitle(QCoreApplication.translate("budengshizu", u"Form", None))
        self.groupBox_61.setTitle(QCoreApplication.translate("budengshizu", u"\u4e0d\u7b49\u5f0f\u7f16\u8f91", None))
        self.budengshizu_youshi.setText(QCoreApplication.translate("budengshizu", u"0", None))
        self.label_33.setText(QCoreApplication.translate("budengshizu", u"<html><head/><body><p>\u6c42\u89e3\u53d8\u91cf(<span style=\" font-weight:700; text-decoration: underline;\">\u4ec5\u5141\u8bb8\u4e00\u5143</span>)\uff1a</p></body></html>", None))
        self.budengshizu_ziyoubianliang.setInputMask("")
        self.budengshizu_ziyoubianliang.setText(QCoreApplication.translate("budengshizu", u"x", None))
        self.budengshizu_ziyoubianliang.setPlaceholderText("")
        self.budengshizu_baocun.setText(QCoreApplication.translate("budengshizu", u"\u4fdd\u5b58", None))
        self.budengshizu_shanchu.setText(QCoreApplication.translate("budengshizu", u"\u5220\u9664", None))
        self.groupBox_60.setTitle(QCoreApplication.translate("budengshizu", u"\u539f\u4e0d\u7b49\u5f0f", None))
        self.groupBox_59.setTitle(QCoreApplication.translate("budengshizu", u"\u89e3\u96c6", None))
        self.budengshizu_qiujie.setText(QCoreApplication.translate("budengshizu", u"\u6c42\u89e3", None))
    # retranslateUi

