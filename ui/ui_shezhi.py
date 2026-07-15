# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'shezhiOjlJDk.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QPushButton,
    QRadioButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_shezhi(object):
    def setupUi(self, shezhi):
        if not shezhi.objectName():
            shezhi.setObjectName(u"shezhi")
        shezhi.resize(801, 551)
        self.verticalLayout = QVBoxLayout(shezhi)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_2 = QGroupBox(shezhi)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.shezhi_zhongwen = QRadioButton(self.groupBox_2)
        self.shezhi_zhongwen.setObjectName(u"shezhi_zhongwen")

        self.horizontalLayout_2.addWidget(self.shezhi_zhongwen)

        self.shezhi_yingwen = QRadioButton(self.groupBox_2)
        self.shezhi_yingwen.setObjectName(u"shezhi_yingwen")

        self.horizontalLayout_2.addWidget(self.shezhi_yingwen)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(shezhi)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.shezhi_qianse = QRadioButton(self.groupBox)
        self.shezhi_qianse.setObjectName(u"shezhi_qianse")

        self.horizontalLayout.addWidget(self.shezhi_qianse)

        self.shezhi_shense = QRadioButton(self.groupBox)
        self.shezhi_shense.setObjectName(u"shezhi_shense")

        self.horizontalLayout.addWidget(self.shezhi_shense)


        self.verticalLayout.addWidget(self.groupBox)

        self.shezhi_yingyong = QPushButton(shezhi)
        self.shezhi_yingyong.setObjectName(u"shezhi_yingyong")

        self.verticalLayout.addWidget(self.shezhi_yingyong)


        self.retranslateUi(shezhi)

        QMetaObject.connectSlotsByName(shezhi)
    # setupUi

    def retranslateUi(self, shezhi):
        shezhi.setWindowTitle(QCoreApplication.translate("shezhi", u"Form", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("shezhi", u"\u754c\u9762\u8bed\u8a00(Language)", None))
        self.shezhi_zhongwen.setText(QCoreApplication.translate("shezhi", u"\u4e2d\u6587", None))
        self.shezhi_yingwen.setText(QCoreApplication.translate("shezhi", u"English", None))
        self.groupBox.setTitle(QCoreApplication.translate("shezhi", u"\u754c\u9762\u6837\u5f0f\u4e3b\u9898", None))
        self.shezhi_qianse.setText(QCoreApplication.translate("shezhi", u"\u6d45\u8272", None))
        self.shezhi_shense.setText(QCoreApplication.translate("shezhi", u"\u6df1\u8272", None))
        self.shezhi_yingyong.setText(QCoreApplication.translate("shezhi", u"\u5e94\u7528", None))
    # retranslateUi

