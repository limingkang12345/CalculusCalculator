# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dingyi_ljPZewnr.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QWidget)

class Ui_dingyi_lj(object):
    def setupUi(self, dingyi_lj):
        if not dingyi_lj.objectName():
            dingyi_lj.setObjectName(u"dingyi_lj")
        dingyi_lj.resize(801, 551)
        self.gridLayout = QGridLayout(dingyi_lj)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(dingyi_lj)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.dingyi_lj_fangfa = QComboBox(self.groupBox)
        self.dingyi_lj_fangfa.addItem("")
        self.dingyi_lj_fangfa.addItem("")
        self.dingyi_lj_fangfa.addItem("")
        self.dingyi_lj_fangfa.addItem("")
        self.dingyi_lj_fangfa.addItem("")
        self.dingyi_lj_fangfa.addItem("")
        self.dingyi_lj_fangfa.addItem("")
        self.dingyi_lj_fangfa.addItem("")
        self.dingyi_lj_fangfa.addItem("")
        self.dingyi_lj_fangfa.addItem("")
        self.dingyi_lj_fangfa.addItem("")
        self.dingyi_lj_fangfa.addItem("")
        self.dingyi_lj_fangfa.addItem("")
        self.dingyi_lj_fangfa.setObjectName(u"dingyi_lj_fangfa")

        self.gridLayout_2.addWidget(self.dingyi_lj_fangfa, 0, 1, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)

        self.dingyi_lj_mingcheng = QLineEdit(self.groupBox)
        self.dingyi_lj_mingcheng.setObjectName(u"dingyi_lj_mingcheng")

        self.gridLayout_2.addWidget(self.dingyi_lj_mingcheng, 1, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)

        self.dingyi_lj_canshu = QLineEdit(self.groupBox)
        self.dingyi_lj_canshu.setObjectName(u"dingyi_lj_canshu")

        self.gridLayout_2.addWidget(self.dingyi_lj_canshu, 2, 1, 1, 1)

        self.dingyi_lj_baocun = QPushButton(self.groupBox)
        self.dingyi_lj_baocun.setObjectName(u"dingyi_lj_baocun")

        self.gridLayout_2.addWidget(self.dingyi_lj_baocun, 3, 0, 1, 2)

        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 5)

        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 5)

        self.groupBox_2 = QGroupBox(dingyi_lj)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_3 = QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.dingyi_lj_dian = QListWidget(self.groupBox_2)
        self.dingyi_lj_dian.setObjectName(u"dingyi_lj_dian")

        self.gridLayout_3.addWidget(self.dingyi_lj_dian, 0, 0, 1, 1)

        self.dingyi_lj_dian_read = QPushButton(self.groupBox_2)
        self.dingyi_lj_dian_read.setObjectName(u"dingyi_lj_dian_read")

        self.gridLayout_3.addWidget(self.dingyi_lj_dian_read, 1, 0, 1, 1)

        self.dingyi_lj_dian_delete = QPushButton(self.groupBox_2)
        self.dingyi_lj_dian_delete.setObjectName(u"dingyi_lj_dian_delete")

        self.gridLayout_3.addWidget(self.dingyi_lj_dian_delete, 2, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 1)

        self.groupBox_3 = QGroupBox(dingyi_lj)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_4 = QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.dingyi_lj_zhixian = QListWidget(self.groupBox_3)
        self.dingyi_lj_zhixian.setObjectName(u"dingyi_lj_zhixian")

        self.gridLayout_4.addWidget(self.dingyi_lj_zhixian, 0, 0, 1, 1)

        self.dingyi_lj_zhixian_read = QPushButton(self.groupBox_3)
        self.dingyi_lj_zhixian_read.setObjectName(u"dingyi_lj_zhixian_read")

        self.gridLayout_4.addWidget(self.dingyi_lj_zhixian_read, 1, 0, 1, 1)

        self.dingyi_lj_zhixian_delete = QPushButton(self.groupBox_3)
        self.dingyi_lj_zhixian_delete.setObjectName(u"dingyi_lj_zhixian_delete")

        self.gridLayout_4.addWidget(self.dingyi_lj_zhixian_delete, 2, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_3, 1, 1, 1, 1)

        self.groupBox_4 = QGroupBox(dingyi_lj)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_5 = QGridLayout(self.groupBox_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.dingyi_lj_pingmian = QListWidget(self.groupBox_4)
        self.dingyi_lj_pingmian.setObjectName(u"dingyi_lj_pingmian")

        self.gridLayout_5.addWidget(self.dingyi_lj_pingmian, 0, 0, 1, 1)

        self.dingyi_lj_pingmian_read = QPushButton(self.groupBox_4)
        self.dingyi_lj_pingmian_read.setObjectName(u"dingyi_lj_pingmian_read")

        self.gridLayout_5.addWidget(self.dingyi_lj_pingmian_read, 1, 0, 1, 1)

        self.dingyi_lj_pingmian_delete = QPushButton(self.groupBox_4)
        self.dingyi_lj_pingmian_delete.setObjectName(u"dingyi_lj_pingmian_delete")

        self.gridLayout_5.addWidget(self.dingyi_lj_pingmian_delete, 2, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_4, 1, 2, 1, 1)

        self.groupBox_5 = QGroupBox(dingyi_lj)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.gridLayout_6 = QGridLayout(self.groupBox_5)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.dingyi_lj_xianduan = QListWidget(self.groupBox_5)
        self.dingyi_lj_xianduan.setObjectName(u"dingyi_lj_xianduan")

        self.gridLayout_6.addWidget(self.dingyi_lj_xianduan, 0, 0, 1, 1)

        self.dingyi_lj_xianduan_read = QPushButton(self.groupBox_5)
        self.dingyi_lj_xianduan_read.setObjectName(u"dingyi_lj_xianduan_read")

        self.gridLayout_6.addWidget(self.dingyi_lj_xianduan_read, 1, 0, 1, 1)

        self.dingyi_lj_xianduan_delete = QPushButton(self.groupBox_5)
        self.dingyi_lj_xianduan_delete.setObjectName(u"dingyi_lj_xianduan_delete")

        self.gridLayout_6.addWidget(self.dingyi_lj_xianduan_delete, 2, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_5, 1, 3, 1, 1)

        self.groupBox_7 = QGroupBox(dingyi_lj)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.gridLayout_7 = QGridLayout(self.groupBox_7)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.label_4 = QLabel(self.groupBox_7)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_7.addWidget(self.label_4, 0, 0, 1, 1)

        self.dingyi_lj_shuxing_mingcheng = QLineEdit(self.groupBox_7)
        self.dingyi_lj_shuxing_mingcheng.setObjectName(u"dingyi_lj_shuxing_mingcheng")

        self.gridLayout_7.addWidget(self.dingyi_lj_shuxing_mingcheng, 1, 0, 1, 1)

        self.label_5 = QLabel(self.groupBox_7)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_7.addWidget(self.label_5, 2, 0, 1, 1)

        self.dingyi_lj_shuxing_fangcheng = QLineEdit(self.groupBox_7)
        self.dingyi_lj_shuxing_fangcheng.setObjectName(u"dingyi_lj_shuxing_fangcheng")

        self.gridLayout_7.addWidget(self.dingyi_lj_shuxing_fangcheng, 3, 0, 1, 1)

        self.gridLayout_7.setRowStretch(0, 1)
        self.gridLayout_7.setRowStretch(1, 1)
        self.gridLayout_7.setRowStretch(2, 1)
        self.gridLayout_7.setRowStretch(3, 1)

        self.gridLayout.addWidget(self.groupBox_7, 1, 4, 1, 1)

        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 3)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(3, 1)
        self.gridLayout.setColumnStretch(4, 1)

        self.retranslateUi(dingyi_lj)

        QMetaObject.connectSlotsByName(dingyi_lj)
    # setupUi

    def retranslateUi(self, dingyi_lj):
        dingyi_lj.setWindowTitle(QCoreApplication.translate("dingyi_lj", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("dingyi_lj", u"\u521b\u5efa\u5bf9\u8c61", None))
        self.label.setText(QCoreApplication.translate("dingyi_lj", u"\u521b\u5efa\u5bf9\u8c61\u65b9\u6cd5\uff1a", None))
        self.dingyi_lj_fangfa.setItemText(0, QCoreApplication.translate("dingyi_lj", u"\u672a\u9009\u62e9", None))
        self.dingyi_lj_fangfa.setItemText(1, QCoreApplication.translate("dingyi_lj", u"\u901a\u8fc7\u5750\u6807\u521b\u5efa\u70b9[\u53c2\u6570\uff1ax\u5750\u6807,y\u5750\u6807,z\u5750\u6807]", None))
        self.dingyi_lj_fangfa.setItemText(2, QCoreApplication.translate("dingyi_lj", u"\u901a\u8fc7\u4e24\u70b9\u521b\u5efa\u76f4\u7ebf[\u53c2\u6570\uff1a\u70b91\u540d\u79f0,\u70b92\u540d\u79f0]", None))
        self.dingyi_lj_fangfa.setItemText(3, QCoreApplication.translate("dingyi_lj", u"\u8fc7\u4e00\u70b9\u4f5c\u5df2\u77e5\u5e73\u9762\u7684\u5e73\u884c\u5e73\u9762[\u53c2\u6570\uff1a\u5e73\u9762\u540d\u79f0,\u70b9\u540d\u79f0]", None))
        self.dingyi_lj_fangfa.setItemText(4, QCoreApplication.translate("dingyi_lj", u"\u8fc7\u4e00\u70b9\u4f5c\u5df2\u77e5\u76f4\u7ebf\u7684\u5782\u76f4\u5e73\u9762[\u53c2\u6570\uff1a\u76f4\u7ebf\u540d\u79f0,\u70b9\u540d\u79f0]", None))
        self.dingyi_lj_fangfa.setItemText(5, QCoreApplication.translate("dingyi_lj", u"\u8fc7\u4e00\u70b9\u4f5c\u5df2\u77e5\u76f4\u7ebf\u7684\u5e73\u884c\u7ebf[\u53c2\u6570\uff1a\u70b9\u540d\u79f0,\u76f4\u7ebf\u540d\u79f0]", None))
        self.dingyi_lj_fangfa.setItemText(6, QCoreApplication.translate("dingyi_lj", u"\u8fc7\u4e00\u70b9\u4f5c\u5df2\u77e5\u76f4\u7ebf\u7684\u5782\u7ebf[\u53c2\u6570\uff1a\u70b9\u540d\u79f0,\u76f4\u7ebf\u540d\u79f0]", None))
        self.dingyi_lj_fangfa.setItemText(7, QCoreApplication.translate("dingyi_lj", u"\u8fc7\u4e00\u70b9\u4f5c\u5df2\u77e5\u5e73\u9762\u7684\u5782\u7ebf[\u53c2\u6570\uff1a\u70b9\u540d\u79f0,\u5e73\u9762\u540d\u79f0]", None))
        self.dingyi_lj_fangfa.setItemText(8, QCoreApplication.translate("dingyi_lj", u"\u8fc7\u4e00\u76f4\u7ebf\u548c\u7ebf\u5916\u4e00\u70b9\u4f5c\u5e73\u9762[\u53c2\u6570\uff1a\u76f4\u7ebf\u540d\u79f0,\u70b9\u540d\u79f0]", None))
        self.dingyi_lj_fangfa.setItemText(9, QCoreApplication.translate("dingyi_lj", u"\u8fc7\u4e24\u76f8\u4ea4/\u5e73\u884c\u76f4\u7ebf\u4f5c\u5e73\u9762[\u53c2\u6570\uff1a\u76f4\u7ebf1\u540d\u79f0,\u76f4\u7ebf2\u540d\u79f0]", None))
        self.dingyi_lj_fangfa.setItemText(10, QCoreApplication.translate("dingyi_lj", u"\u70b9\u5230\u5e73\u9762\u7684\u5782\u8db3[\u53c2\u6570\uff1a\u70b9\u540d\u79f0,\u5e73\u9762\u540d\u79f0]", None))
        self.dingyi_lj_fangfa.setItemText(11, QCoreApplication.translate("dingyi_lj", u"\u70b9\u5230\u76f4\u7ebf\u7684\u5782\u8db3[\u53c2\u6570\uff1a\u70b9\u540d\u79f0,\u76f4\u7ebf\u540d\u79f0]", None))
        self.dingyi_lj_fangfa.setItemText(12, QCoreApplication.translate("dingyi_lj", u"\u901a\u8fc7\u4e24\u70b9\u6784\u9020\u4e09\u7ef4\u7ebf\u6bb5[\u53c2\u6570\uff1a\u70b91\u540d\u79f0,\u70b92\u540d\u79f0]", None))

        self.label_3.setText(QCoreApplication.translate("dingyi_lj", u"\u5bf9\u8c61\u540d\u79f0\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("dingyi_lj", u"\u53c2\u6570(\u76f4\u63a5\u8f93\u5165\uff0c\u4ee5\u82f1\u6587\u534a\u89d2\u9017\u53f7\u5206\u9694)\uff1a", None))
        self.dingyi_lj_baocun.setText(QCoreApplication.translate("dingyi_lj", u"\u4fdd\u5b58", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("dingyi_lj", u"\u70b9", None))
        self.dingyi_lj_dian_read.setText(QCoreApplication.translate("dingyi_lj", u"\u8bfb\u53d6\u9009\u4e2d\u9879", None))
        self.dingyi_lj_dian_delete.setText(QCoreApplication.translate("dingyi_lj", u"\u5220\u9664\u9009\u4e2d\u9879", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("dingyi_lj", u"\u76f4\u7ebf", None))
        self.dingyi_lj_zhixian_read.setText(QCoreApplication.translate("dingyi_lj", u"\u8bfb\u53d6\u9009\u4e2d\u9879", None))
        self.dingyi_lj_zhixian_delete.setText(QCoreApplication.translate("dingyi_lj", u"\u5220\u9664\u9009\u4e2d\u9879", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("dingyi_lj", u"\u5e73\u9762", None))
        self.dingyi_lj_pingmian_read.setText(QCoreApplication.translate("dingyi_lj", u"\u8bfb\u53d6\u9009\u4e2d\u9879", None))
        self.dingyi_lj_pingmian_delete.setText(QCoreApplication.translate("dingyi_lj", u"\u5220\u9664\u9009\u4e2d\u9879", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("dingyi_lj", u"\u7ebf\u6bb5", None))
        self.dingyi_lj_xianduan_read.setText(QCoreApplication.translate("dingyi_lj", u"\u8bfb\u53d6\u9009\u4e2d\u9879", None))
        self.dingyi_lj_xianduan_delete.setText(QCoreApplication.translate("dingyi_lj", u"\u5220\u9664\u9009\u4e2d\u9879", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("dingyi_lj", u"\u5bf9\u8c61\u5c5e\u6027", None))
        self.label_4.setText(QCoreApplication.translate("dingyi_lj", u"\u5bf9\u8c61\u540d\u79f0\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("dingyi_lj", u"\u5bf9\u8c61\u65b9\u7a0b\uff1a", None))
    # retranslateUi

