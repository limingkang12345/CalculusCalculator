# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'fangchengFaHYoK.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGraphicsView, QGridLayout,
    QGroupBox, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QWidget)

class Ui_fangcheng(object):
    def setupUi(self, fangcheng):
        if not fangcheng.objectName():
            fangcheng.setObjectName(u"fangcheng")
        fangcheng.resize(801, 551)
        self.gridLayout = QGridLayout(fangcheng)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_14 = QGroupBox(fangcheng)
        self.groupBox_14.setObjectName(u"groupBox_14")
        self.gridLayout_2 = QGridLayout(self.groupBox_14)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.fangcheng_zuoshi = QLineEdit(self.groupBox_14)
        self.fangcheng_zuoshi.setObjectName(u"fangcheng_zuoshi")
        self.fangcheng_zuoshi.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.fangcheng_zuoshi, 0, 0, 1, 2)

        self.label_4 = QLabel(self.groupBox_14)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)

        self.fangcheng_youshi = QLineEdit(self.groupBox_14)
        self.fangcheng_youshi.setObjectName(u"fangcheng_youshi")
        self.fangcheng_youshi.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.fangcheng_youshi, 1, 1, 1, 1)


        self.gridLayout.addWidget(self.groupBox_14, 0, 0, 1, 1)

        self.groupBox_15 = QGroupBox(fangcheng)
        self.groupBox_15.setObjectName(u"groupBox_15")
        self.gridLayout_3 = QGridLayout(self.groupBox_15)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_5 = QLabel(self.groupBox_15)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 0, 0, 1, 1)

        self.fangcheng_zhuyuanfuhao = QLineEdit(self.groupBox_15)
        self.fangcheng_zhuyuanfuhao.setObjectName(u"fangcheng_zhuyuanfuhao")
        self.fangcheng_zhuyuanfuhao.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.fangcheng_zhuyuanfuhao, 0, 1, 1, 1)

        self.label_6 = QLabel(self.groupBox_15)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_3.addWidget(self.label_6, 0, 2, 1, 1)

        self.fangcheng_quzhifanwei = QLineEdit(self.groupBox_15)
        self.fangcheng_quzhifanwei.setObjectName(u"fangcheng_quzhifanwei")
        self.fangcheng_quzhifanwei.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.fangcheng_quzhifanwei, 0, 3, 1, 1)

        self.fangcheng_weifenfangcheng = QCheckBox(self.groupBox_15)
        self.fangcheng_weifenfangcheng.setObjectName(u"fangcheng_weifenfangcheng")

        self.gridLayout_3.addWidget(self.fangcheng_weifenfangcheng, 0, 4, 1, 1)


        self.gridLayout.addWidget(self.groupBox_15, 1, 0, 1, 1)

        self.groupBox_18 = QGroupBox(fangcheng)
        self.groupBox_18.setObjectName(u"groupBox_18")
        self.gridLayout_4 = QGridLayout(self.groupBox_18)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.fangcheng_yuanfangcheng = QGraphicsView(self.groupBox_18)
        self.fangcheng_yuanfangcheng.setObjectName(u"fangcheng_yuanfangcheng")
        self.fangcheng_yuanfangcheng.setProperty(u"url", QUrl(u"about:blank"))

        self.gridLayout_4.addWidget(self.fangcheng_yuanfangcheng, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_18, 2, 0, 1, 1)

        self.groupBox_17 = QGroupBox(fangcheng)
        self.groupBox_17.setObjectName(u"groupBox_17")
        self.gridLayout_5 = QGridLayout(self.groupBox_17)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.fangcheng_jieji = QGraphicsView(self.groupBox_17)
        self.fangcheng_jieji.setObjectName(u"fangcheng_jieji")
        self.fangcheng_jieji.setProperty(u"url", QUrl(u"about:blank"))

        self.gridLayout_5.addWidget(self.fangcheng_jieji, 0, 0, 1, 1)

        self.fangcheng_jieji_lineedit = QLineEdit(self.groupBox_17)
        self.fangcheng_jieji_lineedit.setObjectName(u"fangcheng_jieji_lineedit")

        self.gridLayout_5.addWidget(self.fangcheng_jieji_lineedit, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_17, 3, 0, 1, 1)

        self.fangcheng_qiujie = QPushButton(fangcheng)
        self.fangcheng_qiujie.setObjectName(u"fangcheng_qiujie")

        self.gridLayout.addWidget(self.fangcheng_qiujie, 4, 0, 1, 1)

        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(2, 4)
        self.gridLayout.setRowStretch(3, 5)
        self.gridLayout.setRowStretch(4, 1)

        self.retranslateUi(fangcheng)

        QMetaObject.connectSlotsByName(fangcheng)
    # setupUi

    def retranslateUi(self, fangcheng):
        fangcheng.setWindowTitle(QCoreApplication.translate("fangcheng", u"Form", None))
        self.groupBox_14.setTitle(QCoreApplication.translate("fangcheng", u"\u8f93\u5165\u65b9\u7a0b", None))
        self.label_4.setText(QCoreApplication.translate("fangcheng", u"=", None))
        self.fangcheng_youshi.setText(QCoreApplication.translate("fangcheng", u"0", None))
        self.groupBox_15.setTitle(QCoreApplication.translate("fangcheng", u"\u9009\u9879", None))
        self.label_5.setText(QCoreApplication.translate("fangcheng", u"\u4e3b\u5143\u7b26\u53f7\uff1a", None))
        self.fangcheng_zhuyuanfuhao.setText(QCoreApplication.translate("fangcheng", u"x", None))
        self.label_6.setText(QCoreApplication.translate("fangcheng", u"\u4e3b\u5143\u53d6\u503c\u8303\u56f4\uff1a", None))
        self.fangcheng_quzhifanwei.setText(QCoreApplication.translate("fangcheng", u"Reals", None))
        self.fangcheng_weifenfangcheng.setText(QCoreApplication.translate("fangcheng", u"\u5fae\u5206\u65b9\u7a0b", None))
        self.groupBox_18.setTitle(QCoreApplication.translate("fangcheng", u"\u539f\u65b9\u7a0b", None))
        self.groupBox_17.setTitle(QCoreApplication.translate("fangcheng", u"\u89e3\u96c6", None))
        self.fangcheng_qiujie.setText(QCoreApplication.translate("fangcheng", u"\u6c42\u89e3", None))
    # retranslateUi

