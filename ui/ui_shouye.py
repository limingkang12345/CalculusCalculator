# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'shouyeboFPZG.ui'
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
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QGridLayout, QSizePolicy, QWidget)

class Ui_shouye(object):
    def setupUi(self, shouye):
        if not shouye.objectName():
            shouye.setObjectName(u"shouye")
        shouye.setWindowModality(Qt.WindowModality.NonModal)
        shouye.resize(801, 551)
        self.gridLayout_2 = QGridLayout(shouye)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.webEngineView = QWebEngineView(shouye)
        self.webEngineView.setObjectName(u"webEngineView")

        self.gridLayout.addWidget(self.webEngineView, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(shouye)

        QMetaObject.connectSlotsByName(shouye)
    # setupUi

    def retranslateUi(self, shouye):
        shouye.setWindowTitle(QCoreApplication.translate("shouye", u"Form", None))
    # retranslateUi

