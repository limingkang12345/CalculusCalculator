# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'huancunexbFhu.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QListWidgetItem,
    QSizePolicy, QWidget)

from ui.widgets import ListWidgetWithDelete

class Ui_huancun(object):
    def setupUi(self, huancun):
        if not huancun.objectName():
            huancun.setObjectName(u"huancun")
        huancun.resize(801, 551)
        self.gridLayout_2 = QGridLayout(huancun)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.groupBox = QGroupBox(huancun)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.huancunqu = ListWidgetWithDelete(self.groupBox)
        self.huancunqu.setObjectName(u"huancunqu")

        self.gridLayout.addWidget(self.huancunqu, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)


        self.retranslateUi(huancun)

        QMetaObject.connectSlotsByName(huancun)
    # setupUi

    def retranslateUi(self, huancun):
        huancun.setWindowTitle(QCoreApplication.translate("huancun", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("huancun", u"\u7f13\u5b58\u533a\uff08\u53cc\u51fb\u9009\u62e9\uff09", None))
    # retranslateUi

