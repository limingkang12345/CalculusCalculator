# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'shouyeSLMgwv.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QSizePolicy,
    QWidget)

class Ui_shouye(object):
    def setupUi(self, shouye):
        if not shouye.objectName():
            shouye.setObjectName(u"shouye")
        shouye.setWindowModality(Qt.WindowModality.NonModal)
        shouye.resize(801, 551)
        self.gridLayoutWidget = QWidget(shouye)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(0, 0, 801, 551))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.shouye_welcome = QLabel(self.gridLayoutWidget)
        self.shouye_welcome.setObjectName(u"shouye_welcome")
        self.shouye_welcome.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 120, 240, 255), stop:1 rgba(255, 255, 255, 255));")
        self.shouye_welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.shouye_welcome, 0, 0, 1, 1)


        self.retranslateUi(shouye)

        QMetaObject.connectSlotsByName(shouye)
    # setupUi

    def retranslateUi(self, shouye):
        shouye.setWindowTitle(QCoreApplication.translate("shouye", u"Form", None))
        self.shouye_welcome.setText(QCoreApplication.translate("shouye", u"<html><head/><body><p><span style=\" font-size:50pt; font-weight:700; color:#000000; font-family:'Times New Roman',Times,serif;\">CalculusCalculator</span></p><p><span style=\" font-size:18pt; font-family:'Times New Roman',Times,serif;\">Author: Li Mingkang</span></p><p><span style=\" font-size:18pt; font-family:'Times New Roman',Times,serif;\">Contributor: CuberAHZ</span></p></body></html>", None))
    # retranslateUi

