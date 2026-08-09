# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'blocklyBmsMST.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QSizePolicy, QWidget)

class Ui_blockly(object):
    def setupUi(self, blockly):
        if not blockly.objectName():
            blockly.setObjectName(u"blockly")
        blockly.resize(801, 551)
        self.horizontalLayout = QHBoxLayout(blockly)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.view = QWebEngineView(blockly)
        self.view.setObjectName(u"view")
        self.view.setUrl(QUrl(u"about:blank"))

        self.horizontalLayout.addWidget(self.view)


        self.retranslateUi(blockly)

        QMetaObject.connectSlotsByName(blockly)
    # setupUi

    def retranslateUi(self, blockly):
        blockly.setWindowTitle(QCoreApplication.translate("blockly", u"Form", None))
    # retranslateUi

