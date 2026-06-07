# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'huitu_hanshutSrWPS.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QLabel,
    QLineEdit, QPushButton, QRadioButton, QSizePolicy,
    QWidget)

class Ui_huitu_hanshu(object):
    def setupUi(self, huitu_hanshu):
        if not huitu_hanshu.objectName():
            huitu_hanshu.setObjectName(u"huitu_hanshu")
        huitu_hanshu.resize(801, 551)
        self.groupBox = QGroupBox(huitu_hanshu)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 771, 80))
        self.huitu_hanshu_biaodashi = QLineEdit(self.groupBox)
        self.huitu_hanshu_biaodashi.setObjectName(u"huitu_hanshu_biaodashi")
        self.huitu_hanshu_biaodashi.setGeometry(QRect(90, 20, 671, 21))
        self.huitu_hanshu_biaodashi_radio = QRadioButton(self.groupBox)
        self.huitu_hanshu_biaodashi_radio.setObjectName(u"huitu_hanshu_biaodashi_radio")
        self.huitu_hanshu_biaodashi_radio.setGeometry(QRect(10, 20, 81, 23))
        self.huitu_hanshu_biaodashi_radio.setChecked(True)
        self.huitu_hanshu_hanshu_radio = QRadioButton(self.groupBox)
        self.huitu_hanshu_hanshu_radio.setObjectName(u"huitu_hanshu_hanshu_radio")
        self.huitu_hanshu_hanshu_radio.setGeometry(QRect(10, 50, 114, 23))
        self.huitu_hanshu_hanshu = QComboBox(self.groupBox)
        self.huitu_hanshu_hanshu.setObjectName(u"huitu_hanshu_hanshu")
        self.huitu_hanshu_hanshu.setEnabled(False)
        self.huitu_hanshu_hanshu.setGeometry(QRect(130, 50, 101, 25))
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(250, 50, 61, 19))
        self.huitu_hanshu_dingyiyu_left = QLineEdit(self.groupBox)
        self.huitu_hanshu_dingyiyu_left.setObjectName(u"huitu_hanshu_dingyiyu_left")
        self.huitu_hanshu_dingyiyu_left.setGeometry(QRect(310, 50, 201, 21))
        self.huitu_hanshu_dingyiyu_right = QLineEdit(self.groupBox)
        self.huitu_hanshu_dingyiyu_right.setObjectName(u"huitu_hanshu_dingyiyu_right")
        self.huitu_hanshu_dingyiyu_right.setGeometry(QRect(562, 50, 201, 21))
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(510, 50, 51, 20))
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.huitu_hanshu_huitu = QWidget(huitu_hanshu)
        self.huitu_hanshu_huitu.setObjectName(u"huitu_hanshu_huitu")
        self.huitu_hanshu_huitu.setGeometry(QRect(10, 100, 771, 411))
        self.huitu_hanshu_huizhi = QPushButton(huitu_hanshu)
        self.huitu_hanshu_huizhi.setObjectName(u"huitu_hanshu_huizhi")
        self.huitu_hanshu_huizhi.setGeometry(QRect(10, 520, 771, 27))

        self.retranslateUi(huitu_hanshu)

        QMetaObject.connectSlotsByName(huitu_hanshu)
    # setupUi

    def retranslateUi(self, huitu_hanshu):
        huitu_hanshu.setWindowTitle(QCoreApplication.translate("huitu_hanshu", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("huitu_hanshu", u"\u7ed8\u56fe\u53c2\u6570", None))
        self.huitu_hanshu_biaodashi_radio.setText(QCoreApplication.translate("huitu_hanshu", u"\u8868\u8fbe\u5f0f\uff1a", None))
        self.huitu_hanshu_hanshu_radio.setText(QCoreApplication.translate("huitu_hanshu", u"\u6216\u9009\u62e9\u51fd\u6570\uff1a", None))
        self.label.setText(QCoreApplication.translate("huitu_hanshu", u"\u5b9a\u4e49\u57df\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("huitu_hanshu", u"\u81f3", None))
        self.huitu_hanshu_huizhi.setText(QCoreApplication.translate("huitu_hanshu", u"\u7ed8\u5236", None))
    # retranslateUi

