# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'budengshiPPndBi.ui'
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
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_budengshi(object):
    def setupUi(self, budengshi):
        if not budengshi.objectName():
            budengshi.setObjectName(u"budengshi")
        budengshi.resize(801, 551)
        self.gridLayout = QGridLayout(budengshi)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_38 = QGroupBox(budengshi)
        self.groupBox_38.setObjectName(u"groupBox_38")
        self.gridLayout_2 = QGridLayout(self.groupBox_38)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.budengshi_zuoshi = QLineEdit(self.groupBox_38)
        self.budengshi_zuoshi.setObjectName(u"budengshi_zuoshi")
        self.budengshi_zuoshi.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.budengshi_zuoshi, 0, 0, 1, 2)

        self.budengshi_budenghao = QComboBox(self.groupBox_38)
        self.budengshi_budenghao.setObjectName(u"budengshi_budenghao")

        self.gridLayout_2.addWidget(self.budengshi_budenghao, 1, 0, 1, 1)

        self.budengshi_youshi = QLineEdit(self.groupBox_38)
        self.budengshi_youshi.setObjectName(u"budengshi_youshi")
        self.budengshi_youshi.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.budengshi_youshi, 1, 1, 1, 1)


        self.gridLayout.addWidget(self.groupBox_38, 0, 0, 1, 1)

        self.groupBox_39 = QGroupBox(budengshi)
        self.groupBox_39.setObjectName(u"groupBox_39")
        self.horizontalLayout = QHBoxLayout(self.groupBox_39)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_14 = QLabel(self.groupBox_39)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout.addWidget(self.label_14)

        self.budengshi_zhuyuanfuhao = QLineEdit(self.groupBox_39)
        self.budengshi_zhuyuanfuhao.setObjectName(u"budengshi_zhuyuanfuhao")
        self.budengshi_zhuyuanfuhao.setClearButtonEnabled(True)

        self.horizontalLayout.addWidget(self.budengshi_zhuyuanfuhao)

        self.label_15 = QLabel(self.groupBox_39)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout.addWidget(self.label_15)

        self.budengshi_quzhifanwei = QLineEdit(self.groupBox_39)
        self.budengshi_quzhifanwei.setObjectName(u"budengshi_quzhifanwei")
        self.budengshi_quzhifanwei.setClearButtonEnabled(True)

        self.horizontalLayout.addWidget(self.budengshi_quzhifanwei)


        self.gridLayout.addWidget(self.groupBox_39, 1, 0, 1, 1)

        self.groupBox_37 = QGroupBox(budengshi)
        self.groupBox_37.setObjectName(u"groupBox_37")
        self.gridLayout_3 = QGridLayout(self.groupBox_37)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.budengshi_yuanshi = QGraphicsView(self.groupBox_37)
        self.budengshi_yuanshi.setObjectName(u"budengshi_yuanshi")
        self.budengshi_yuanshi.setProperty(u"url", QUrl(u"about:blank"))

        self.gridLayout_3.addWidget(self.budengshi_yuanshi, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_37, 2, 0, 1, 1)

        self.groupBox_40 = QGroupBox(budengshi)
        self.groupBox_40.setObjectName(u"groupBox_40")
        self.gridLayout_4 = QGridLayout(self.groupBox_40)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.budengshi_jieji = QGraphicsView(self.groupBox_40)
        self.budengshi_jieji.setObjectName(u"budengshi_jieji")
        self.budengshi_jieji.setProperty(u"url", QUrl(u"about:blank"))

        self.gridLayout_4.addWidget(self.budengshi_jieji, 0, 0, 1, 1)

        self.budengshi_jieji_lineedit = QLineEdit(self.groupBox_40)
        self.budengshi_jieji_lineedit.setObjectName(u"budengshi_jieji_lineedit")

        self.gridLayout_4.addWidget(self.budengshi_jieji_lineedit, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_40, 3, 0, 1, 1)

        self.budengshi_qiujie = QPushButton(budengshi)
        self.budengshi_qiujie.setObjectName(u"budengshi_qiujie")

        self.gridLayout.addWidget(self.budengshi_qiujie, 4, 0, 1, 1)

        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(2, 3)
        self.gridLayout.setRowStretch(3, 4)
        self.gridLayout.setRowStretch(4, 1)

        self.retranslateUi(budengshi)

        QMetaObject.connectSlotsByName(budengshi)
    # setupUi

    def retranslateUi(self, budengshi):
        budengshi.setWindowTitle(QCoreApplication.translate("budengshi", u"Form", None))
        self.groupBox_38.setTitle(QCoreApplication.translate("budengshi", u"\u8f93\u5165\u4e0d\u7b49\u5f0f", None))
        self.budengshi_youshi.setText(QCoreApplication.translate("budengshi", u"0", None))
        self.groupBox_39.setTitle(QCoreApplication.translate("budengshi", u"\u9009\u9879", None))
        self.label_14.setText(QCoreApplication.translate("budengshi", u"\u4e3b\u5143\u7b26\u53f7\uff1a", None))
        self.budengshi_zhuyuanfuhao.setText(QCoreApplication.translate("budengshi", u"x", None))
        self.label_15.setText(QCoreApplication.translate("budengshi", u"\u4e3b\u5143\u53d6\u503c\u8303\u56f4\uff1a", None))
        self.budengshi_quzhifanwei.setText(QCoreApplication.translate("budengshi", u"Reals", None))
        self.groupBox_37.setTitle(QCoreApplication.translate("budengshi", u"\u539f\u4e0d\u7b49\u5f0f", None))
        self.groupBox_40.setTitle(QCoreApplication.translate("budengshi", u"\u89e3\u96c6", None))
        self.budengshi_qiujie.setText(QCoreApplication.translate("budengshi", u"\u6c42\u89e3", None))
    # retranslateUi

