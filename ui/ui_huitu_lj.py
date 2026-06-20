# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'huitu_ljNCJfcq.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QWidget)

class Ui_huitu_lj(object):
    def setupUi(self, huitu_lj):
        if not huitu_lj.objectName():
            huitu_lj.setObjectName(u"huitu_lj")
        huitu_lj.resize(801, 551)
        self.gridLayout = QGridLayout(huitu_lj)
        self.gridLayout.setObjectName(u"gridLayout")
        self.huitu_pingji = QWidget(huitu_lj)
        self.huitu_pingji.setObjectName(u"huitu_pingji")

        self.gridLayout.addWidget(self.huitu_pingji, 0, 0, 1, 1)

        self.huitu_lj_list = QListWidget(huitu_lj)
        self.huitu_lj_list.setObjectName(u"huitu_lj_list")
        self.huitu_lj_list.setWordWrap(False)
        self.huitu_lj_list.setSelectionRectVisible(False)
        self.huitu_lj_list.setSortingEnabled(False)

        self.gridLayout.addWidget(self.huitu_lj_list, 0, 1, 1, 1)

        self.huitu_lj_button = QPushButton(huitu_lj)
        self.huitu_lj_button.setObjectName(u"huitu_lj_button")

        self.gridLayout.addWidget(self.huitu_lj_button, 1, 0, 1, 2)

        self.gridLayout.setColumnStretch(0, 4)
        self.gridLayout.setColumnStretch(1, 1)

        self.retranslateUi(huitu_lj)

        QMetaObject.connectSlotsByName(huitu_lj)
    # setupUi

    def retranslateUi(self, huitu_lj):
        huitu_lj.setWindowTitle(QCoreApplication.translate("huitu_lj", u"Form", None))
        self.huitu_lj_button.setText(QCoreApplication.translate("huitu_lj", u"\u7ed8\u5236or\u66f4\u65b0", None))
    # retranslateUi

