# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'shezhiKXUvqH.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QListWidget, QListWidgetItem, QPushButton, QRadioButton,
    QSizePolicy, QVBoxLayout, QWidget)

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

        self.groupBox_3 = QGroupBox(shezhi)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout = QGridLayout(self.groupBox_3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.shezhi_cundang = QListWidget(self.groupBox_3)
        __qlistwidgetitem = QListWidgetItem(self.shezhi_cundang)
        __qlistwidgetitem.setCheckState(Qt.Checked)
        __qlistwidgetitem1 = QListWidgetItem(self.shezhi_cundang)
        __qlistwidgetitem1.setCheckState(Qt.Checked)
        __qlistwidgetitem2 = QListWidgetItem(self.shezhi_cundang)
        __qlistwidgetitem2.setCheckState(Qt.Checked)
        __qlistwidgetitem3 = QListWidgetItem(self.shezhi_cundang)
        __qlistwidgetitem3.setCheckState(Qt.Checked)
        __qlistwidgetitem4 = QListWidgetItem(self.shezhi_cundang)
        __qlistwidgetitem4.setCheckState(Qt.Checked)
        __qlistwidgetitem5 = QListWidgetItem(self.shezhi_cundang)
        __qlistwidgetitem5.setCheckState(Qt.Checked)
        __qlistwidgetitem6 = QListWidgetItem(self.shezhi_cundang)
        __qlistwidgetitem6.setCheckState(Qt.Checked)
        __qlistwidgetitem7 = QListWidgetItem(self.shezhi_cundang)
        __qlistwidgetitem7.setCheckState(Qt.Checked)
        __qlistwidgetitem8 = QListWidgetItem(self.shezhi_cundang)
        __qlistwidgetitem8.setCheckState(Qt.Checked)
        __qlistwidgetitem9 = QListWidgetItem(self.shezhi_cundang)
        __qlistwidgetitem9.setCheckState(Qt.Checked)
        __qlistwidgetitem10 = QListWidgetItem(self.shezhi_cundang)
        __qlistwidgetitem10.setCheckState(Qt.Checked)
        self.shezhi_cundang.setObjectName(u"shezhi_cundang")
        self.shezhi_cundang.setSelectionRectVisible(False)

        self.gridLayout.addWidget(self.shezhi_cundang, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_3)

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
        self.groupBox_3.setTitle(QCoreApplication.translate("shezhi", u"\u5b58\u6863\u8bbe\u7f6e\uff08\u4fdd\u5b58\u65f6\uff09", None))

        __sortingEnabled = self.shezhi_cundang.isSortingEnabled()
        self.shezhi_cundang.setSortingEnabled(False)
        ___qlistwidgetitem = self.shezhi_cundang.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("shezhi", u"\u51fd\u6570\u5217\u8868", None))
        ___qlistwidgetitem1 = self.shezhi_cundang.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("shezhi", u"\u65b9\u7a0b\u5217\u8868\uff08\u65b9\u7a0b\u7ec4\uff09", None))
        ___qlistwidgetitem2 = self.shezhi_cundang.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("shezhi", u"\u4e0d\u7b49\u5f0f\u5217\u8868\uff08\u4e0d\u7b49\u5f0f\u7ec4\uff09", None))
        ___qlistwidgetitem3 = self.shezhi_cundang.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("shezhi", u"\u5411\u91cf\u5217\u8868", None))
        ___qlistwidgetitem4 = self.shezhi_cundang.item(4)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("shezhi", u"\u6240\u6709\u7f13\u5b58\u533a\u5185\u5bb9", None))
        ___qlistwidgetitem5 = self.shezhi_cundang.item(5)
        ___qlistwidgetitem5.setText(QCoreApplication.translate("shezhi", u"\u5e73\u9762\u51e0\u4f55\u5bf9\u8c61\u5217\u8868", None))
        ___qlistwidgetitem6 = self.shezhi_cundang.item(6)
        ___qlistwidgetitem6.setText(QCoreApplication.translate("shezhi", u"\u7acb\u4f53\u51e0\u4f55\u5bf9\u8c61\u5217\u8868", None))
        ___qlistwidgetitem7 = self.shezhi_cundang.item(7)
        ___qlistwidgetitem7.setText(QCoreApplication.translate("shezhi", u"\u6240\u6709\u6587\u672c\u6846\u6587\u672c", None))
        ___qlistwidgetitem8 = self.shezhi_cundang.item(8)
        ___qlistwidgetitem8.setText(QCoreApplication.translate("shezhi", u"\u6240\u6709\u9009\u62e9\u6846\u9009\u9879", None))
        ___qlistwidgetitem9 = self.shezhi_cundang.item(9)
        ___qlistwidgetitem9.setText(QCoreApplication.translate("shezhi", u"\u6240\u6709\u8868\u8fbe\u5f0f\u663e\u793a\u6846\u5185\u5bb9", None))
        ___qlistwidgetitem10 = self.shezhi_cundang.item(10)
        ___qlistwidgetitem10.setText(QCoreApplication.translate("shezhi", u"\u6240\u6709\u8bbe\u7f6e\u9009\u9879", None))
        self.shezhi_cundang.setSortingEnabled(__sortingEnabled)

        self.shezhi_yingyong.setText(QCoreApplication.translate("shezhi", u"\u5e94\u7528", None))
    # retranslateUi

