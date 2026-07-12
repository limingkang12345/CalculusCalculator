# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'jisuanAsYCGW.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGraphicsView, QGridLayout,
    QGroupBox, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QWidget)

class Ui_jisuan(object):
    def setupUi(self, jisuan):
        if not jisuan.objectName():
            jisuan.setObjectName(u"jisuan")
        jisuan.resize(801, 551)
        self.gridLayout = QGridLayout(jisuan)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_2 = QGroupBox(jisuan)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.jisuan_input = QLineEdit(self.groupBox_2)
        self.jisuan_input.setObjectName(u"jisuan_input")
        self.jisuan_input.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.jisuan_input, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_2, 0, 0, 1, 1)

        self.groupBox_13 = QGroupBox(jisuan)
        self.groupBox_13.setObjectName(u"groupBox_13")
        self.gridLayout_3 = QGridLayout(self.groupBox_13)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.jisuan_jisuanyinqing = QComboBox(self.groupBox_13)
        self.jisuan_jisuanyinqing.setObjectName(u"jisuan_jisuanyinqing")
        self.jisuan_jisuanyinqing.setEditable(False)
        self.jisuan_jisuanyinqing.setMaxVisibleItems(13)

        self.gridLayout_3.addWidget(self.jisuan_jisuanyinqing, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_13, 1, 0, 1, 1)

        self.groupBox_10 = QGroupBox(jisuan)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.gridLayout_4 = QGridLayout(self.groupBox_10)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label = QLabel(self.groupBox_10)
        self.label.setObjectName(u"label")

        self.gridLayout_4.addWidget(self.label, 0, 0, 1, 1)

        self.jisuan_jingdu = QLineEdit(self.groupBox_10)
        self.jisuan_jingdu.setObjectName(u"jisuan_jingdu")
        self.jisuan_jingdu.setEnabled(True)
        self.jisuan_jingdu.setMaxLength(-1)
        self.jisuan_jingdu.setClearButtonEnabled(True)

        self.gridLayout_4.addWidget(self.jisuan_jingdu, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.groupBox_10, 2, 0, 1, 1)

        self.groupBox_16 = QGroupBox(jisuan)
        self.groupBox_16.setObjectName(u"groupBox_16")
        self.gridLayout_5 = QGridLayout(self.groupBox_16)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.jisuan_yuanshi = QGraphicsView(self.groupBox_16)
        self.jisuan_yuanshi.setObjectName(u"jisuan_yuanshi")
        self.jisuan_yuanshi.setProperty(u"url", QUrl(u"about:blank"))

        self.gridLayout_5.addWidget(self.jisuan_yuanshi, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_16, 3, 0, 1, 1)

        self.groupBox_12 = QGroupBox(jisuan)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.gridLayout_6 = QGridLayout(self.groupBox_12)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.jisuan_jisuanjieguo = QGraphicsView(self.groupBox_12)
        self.jisuan_jisuanjieguo.setObjectName(u"jisuan_jisuanjieguo")
        self.jisuan_jisuanjieguo.setProperty(u"url", QUrl(u"about:blank"))

        self.gridLayout_6.addWidget(self.jisuan_jisuanjieguo, 0, 0, 1, 1)

        self.jisuan_jisuanjieguo_lineedit = QLineEdit(self.groupBox_12)
        self.jisuan_jisuanjieguo_lineedit.setObjectName(u"jisuan_jisuanjieguo_lineedit")

        self.gridLayout_6.addWidget(self.jisuan_jisuanjieguo_lineedit, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_12, 4, 0, 1, 1)

        self.jisuan_jisuan_button = QPushButton(jisuan)
        self.jisuan_jisuan_button.setObjectName(u"jisuan_jisuan_button")

        self.gridLayout.addWidget(self.jisuan_jisuan_button, 5, 0, 1, 1)

        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(2, 1)
        self.gridLayout.setRowStretch(3, 4)
        self.gridLayout.setRowStretch(4, 5)

        self.retranslateUi(jisuan)

        QMetaObject.connectSlotsByName(jisuan)
    # setupUi

    def retranslateUi(self, jisuan):
        jisuan.setWindowTitle(QCoreApplication.translate("jisuan", u"Form", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("jisuan", u"\u8f93\u5165\u8868\u8fbe\u5f0f", None))
        self.groupBox_13.setTitle(QCoreApplication.translate("jisuan", u"\u8ba1\u7b97\u5f15\u64ce", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("jisuan", u"\u9009\u9879", None))
        self.label.setText(QCoreApplication.translate("jisuan", u"\u7cbe\u5ea6\uff08\u5341\u8fdb\u5236\u4f4d\u6570\uff09\uff1a", None))
        self.jisuan_jingdu.setText(QCoreApplication.translate("jisuan", u"16", None))
        self.groupBox_16.setTitle(QCoreApplication.translate("jisuan", u"\u539f\u5f0f", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("jisuan", u"\u8ba1\u7b97\u7ed3\u679c", None))
        self.jisuan_jisuan_button.setText(QCoreApplication.translate("jisuan", u"\u8ba1\u7b97", None))
    # retranslateUi

