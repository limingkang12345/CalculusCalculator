# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'helpAvKpkU.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QSizePolicy, QWidget)
import resources_rc

class Ui_help(object):
    def setupUi(self, help):
        if not help.objectName():
            help.setObjectName(u"help")
        help.resize(801, 551)
        self.gridLayout = QGridLayout(help)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.webEngineView = QWebEngineView(help)
        self.webEngineView.setObjectName(u"webEngineView")
        self.webEngineView.setUrl(QUrl(u"qrc:///help.html"))

        self.gridLayout.addWidget(self.webEngineView, 0, 0, 1, 1)


        self.retranslateUi(help)

        QMetaObject.connectSlotsByName(help)
    # setupUi

    def retranslateUi(self, help):
        help.setWindowTitle(QCoreApplication.translate("help", u"Form", None))
    # retranslateUi

