# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'huitu_pjIeSilS.ui'
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
from PySide6.QtWidgets import (QApplication, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QWidget)

class Ui_huitu_pj(object):
    def setupUi(self, huitu_pj):
        if not huitu_pj.objectName():
            huitu_pj.setObjectName(u"huitu_pj")
        huitu_pj.resize(801, 551)
        self.huitu_pingji = QWidget(huitu_pj)
        self.huitu_pingji.setObjectName(u"huitu_pingji")
        self.huitu_pingji.setGeometry(QRect(10, 10, 601, 511))
        self.huitu_pj_button = QPushButton(huitu_pj)
        self.huitu_pj_button.setObjectName(u"huitu_pj_button")
        self.huitu_pj_button.setGeometry(QRect(10, 520, 781, 27))
        self.huitu_pj_list = QListWidget(huitu_pj)
        self.huitu_pj_list.setObjectName(u"huitu_pj_list")
        self.huitu_pj_list.setGeometry(QRect(620, 10, 171, 511))
        self.huitu_pj_list.setWordWrap(False)
        self.huitu_pj_list.setSelectionRectVisible(False)
        self.huitu_pj_list.setSortingEnabled(False)

        self.retranslateUi(huitu_pj)

        QMetaObject.connectSlotsByName(huitu_pj)
    # setupUi

    def retranslateUi(self, huitu_pj):
        huitu_pj.setWindowTitle(QCoreApplication.translate("huitu_pj", u"Form", None))
        self.huitu_pj_button.setText(QCoreApplication.translate("huitu_pj", u"\u7ed8\u5236or\u66f4\u65b0", None))
    # retranslateUi

