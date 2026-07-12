# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dingyi_pjMIvFId.ui'
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

class Ui_dingyi_pj(object):
    def setupUi(self, dingyi_pj):
        if not dingyi_pj.objectName():
            dingyi_pj.setObjectName(u"dingyi_pj")
        dingyi_pj.resize(824, 551)
        self.gridLayout = QGridLayout(dingyi_pj)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_7 = QGroupBox(dingyi_pj)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.gridLayout_8 = QGridLayout(self.groupBox_7)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.label_4 = QLabel(self.groupBox_7)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_8.addWidget(self.label_4, 0, 0, 1, 1)

        self.dingyi_pj_shuxing_mingcheng = QLineEdit(self.groupBox_7)
        self.dingyi_pj_shuxing_mingcheng.setObjectName(u"dingyi_pj_shuxing_mingcheng")

        self.gridLayout_8.addWidget(self.dingyi_pj_shuxing_mingcheng, 1, 0, 1, 1)

        self.label_5 = QLabel(self.groupBox_7)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_8.addWidget(self.label_5, 2, 0, 1, 1)

        self.dingyi_pj_shuxing_fangcheng = QLineEdit(self.groupBox_7)
        self.dingyi_pj_shuxing_fangcheng.setObjectName(u"dingyi_pj_shuxing_fangcheng")

        self.gridLayout_8.addWidget(self.dingyi_pj_shuxing_fangcheng, 3, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_7, 1, 5, 1, 1)

        self.groupBox_4 = QGroupBox(dingyi_pj)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_5 = QGridLayout(self.groupBox_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.dingyi_pj_xianduan = QListWidget(self.groupBox_4)
        self.dingyi_pj_xianduan.setObjectName(u"dingyi_pj_xianduan")

        self.gridLayout_5.addWidget(self.dingyi_pj_xianduan, 0, 0, 1, 1)

        self.dingyi_pj_xianduan_read = QPushButton(self.groupBox_4)
        self.dingyi_pj_xianduan_read.setObjectName(u"dingyi_pj_xianduan_read")

        self.gridLayout_5.addWidget(self.dingyi_pj_xianduan_read, 1, 0, 1, 1)

        self.dingyi_pj_xianduan_delete = QPushButton(self.groupBox_4)
        self.dingyi_pj_xianduan_delete.setObjectName(u"dingyi_pj_xianduan_delete")

        self.gridLayout_5.addWidget(self.dingyi_pj_xianduan_delete, 2, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_4, 1, 2, 1, 1)

        self.groupBox_3 = QGroupBox(dingyi_pj)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_4 = QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.dingyi_pj_zhixian = QListWidget(self.groupBox_3)
        self.dingyi_pj_zhixian.setObjectName(u"dingyi_pj_zhixian")

        self.gridLayout_4.addWidget(self.dingyi_pj_zhixian, 0, 0, 1, 1)

        self.dingyi_pj_zhixian_read = QPushButton(self.groupBox_3)
        self.dingyi_pj_zhixian_read.setObjectName(u"dingyi_pj_zhixian_read")

        self.gridLayout_4.addWidget(self.dingyi_pj_zhixian_read, 1, 0, 1, 1)

        self.dingyi_pj_zhixian_delete = QPushButton(self.groupBox_3)
        self.dingyi_pj_zhixian_delete.setObjectName(u"dingyi_pj_zhixian_delete")

        self.gridLayout_4.addWidget(self.dingyi_pj_zhixian_delete, 2, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_3, 1, 1, 1, 1)

        self.groupBox_2 = QGroupBox(dingyi_pj)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_3 = QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.dingyi_pj_dian = QListWidget(self.groupBox_2)
        self.dingyi_pj_dian.setObjectName(u"dingyi_pj_dian")

        self.gridLayout_3.addWidget(self.dingyi_pj_dian, 0, 0, 1, 1)

        self.dingyi_pj_dian_read = QPushButton(self.groupBox_2)
        self.dingyi_pj_dian_read.setObjectName(u"dingyi_pj_dian_read")

        self.gridLayout_3.addWidget(self.dingyi_pj_dian_read, 1, 0, 1, 1)

        self.dingyi_pj_dian_delete = QPushButton(self.groupBox_2)
        self.dingyi_pj_dian_delete.setObjectName(u"dingyi_pj_dian_delete")

        self.gridLayout_3.addWidget(self.dingyi_pj_dian_delete, 2, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 1)

        self.groupBox_6 = QGroupBox(dingyi_pj)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.gridLayout_7 = QGridLayout(self.groupBox_6)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.dingyi_pj_yuan = QListWidget(self.groupBox_6)
        self.dingyi_pj_yuan.setObjectName(u"dingyi_pj_yuan")

        self.gridLayout_7.addWidget(self.dingyi_pj_yuan, 0, 0, 1, 1)

        self.dingyi_pj_yuan_read = QPushButton(self.groupBox_6)
        self.dingyi_pj_yuan_read.setObjectName(u"dingyi_pj_yuan_read")

        self.gridLayout_7.addWidget(self.dingyi_pj_yuan_read, 1, 0, 1, 1)

        self.dingyi_pj_yuan_delete = QPushButton(self.groupBox_6)
        self.dingyi_pj_yuan_delete.setObjectName(u"dingyi_pj_yuan_delete")

        self.gridLayout_7.addWidget(self.dingyi_pj_yuan_delete, 2, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_6, 1, 4, 1, 1)

        self.groupBox_5 = QGroupBox(dingyi_pj)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.gridLayout_6 = QGridLayout(self.groupBox_5)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.dingyi_pj_duobianxing = QListWidget(self.groupBox_5)
        self.dingyi_pj_duobianxing.setObjectName(u"dingyi_pj_duobianxing")

        self.gridLayout_6.addWidget(self.dingyi_pj_duobianxing, 0, 0, 1, 1)

        self.dingyi_pj_duobianxing_read = QPushButton(self.groupBox_5)
        self.dingyi_pj_duobianxing_read.setObjectName(u"dingyi_pj_duobianxing_read")

        self.gridLayout_6.addWidget(self.dingyi_pj_duobianxing_read, 1, 0, 1, 1)

        self.dingyi_pj_duobianxing_delete = QPushButton(self.groupBox_5)
        self.dingyi_pj_duobianxing_delete.setObjectName(u"dingyi_pj_duobianxing_delete")

        self.gridLayout_6.addWidget(self.dingyi_pj_duobianxing_delete, 2, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_5, 1, 3, 1, 1)

        self.groupBox = QGroupBox(dingyi_pj)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.dingyi_pj_fangfa = QComboBox(self.groupBox)
        self.dingyi_pj_fangfa.addItem("")
        self.dingyi_pj_fangfa.addItem("")
        self.dingyi_pj_fangfa.addItem("")
        self.dingyi_pj_fangfa.addItem("")
        self.dingyi_pj_fangfa.addItem("")
        self.dingyi_pj_fangfa.addItem("")
        self.dingyi_pj_fangfa.addItem("")
        self.dingyi_pj_fangfa.addItem("")
        self.dingyi_pj_fangfa.addItem("")
        self.dingyi_pj_fangfa.addItem("")
        self.dingyi_pj_fangfa.addItem("")
        self.dingyi_pj_fangfa.addItem("")
        self.dingyi_pj_fangfa.addItem("")
        self.dingyi_pj_fangfa.addItem("")
        self.dingyi_pj_fangfa.addItem("")
        self.dingyi_pj_fangfa.addItem("")
        self.dingyi_pj_fangfa.addItem("")
        self.dingyi_pj_fangfa.addItem("")
        self.dingyi_pj_fangfa.addItem("")
        self.dingyi_pj_fangfa.addItem("")
        self.dingyi_pj_fangfa.setObjectName(u"dingyi_pj_fangfa")

        self.gridLayout_2.addWidget(self.dingyi_pj_fangfa, 0, 1, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)

        self.dingyi_pj_mingcheng = QLineEdit(self.groupBox)
        self.dingyi_pj_mingcheng.setObjectName(u"dingyi_pj_mingcheng")

        self.gridLayout_2.addWidget(self.dingyi_pj_mingcheng, 1, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)

        self.dingyi_pj_canshu = QLineEdit(self.groupBox)
        self.dingyi_pj_canshu.setObjectName(u"dingyi_pj_canshu")

        self.gridLayout_2.addWidget(self.dingyi_pj_canshu, 2, 1, 1, 1)

        self.dingyi_pj_baocun = QPushButton(self.groupBox)
        self.dingyi_pj_baocun.setObjectName(u"dingyi_pj_baocun")

        self.gridLayout_2.addWidget(self.dingyi_pj_baocun, 3, 0, 1, 2)

        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 5)

        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 6)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(3, 1)
        self.gridLayout.setColumnStretch(4, 1)
        self.gridLayout.setColumnStretch(5, 1)

        self.retranslateUi(dingyi_pj)

        QMetaObject.connectSlotsByName(dingyi_pj)
    # setupUi

    def retranslateUi(self, dingyi_pj):
        dingyi_pj.setWindowTitle(QCoreApplication.translate("dingyi_pj", u"Form", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("dingyi_pj", u"\u5bf9\u8c61\u5c5e\u6027", None))
        self.label_4.setText(QCoreApplication.translate("dingyi_pj", u"\u5bf9\u8c61\u540d\u79f0\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("dingyi_pj", u"\u5bf9\u8c61\u65b9\u7a0b\uff1a", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("dingyi_pj", u"\u7ebf\u6bb5", None))
        self.dingyi_pj_xianduan_read.setText(QCoreApplication.translate("dingyi_pj", u"\u8bfb\u53d6\u9009\u4e2d\u9879", None))
        self.dingyi_pj_xianduan_delete.setText(QCoreApplication.translate("dingyi_pj", u"\u5220\u9664\u9009\u4e2d\u9879", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("dingyi_pj", u"\u76f4\u7ebf", None))
        self.dingyi_pj_zhixian_read.setText(QCoreApplication.translate("dingyi_pj", u"\u8bfb\u53d6\u9009\u4e2d\u9879", None))
        self.dingyi_pj_zhixian_delete.setText(QCoreApplication.translate("dingyi_pj", u"\u5220\u9664\u9009\u4e2d\u9879", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("dingyi_pj", u"\u70b9", None))
        self.dingyi_pj_dian_read.setText(QCoreApplication.translate("dingyi_pj", u"\u8bfb\u53d6\u9009\u4e2d\u9879", None))
        self.dingyi_pj_dian_delete.setText(QCoreApplication.translate("dingyi_pj", u"\u5220\u9664\u9009\u4e2d\u9879", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("dingyi_pj", u"\u5706", None))
        self.dingyi_pj_yuan_read.setText(QCoreApplication.translate("dingyi_pj", u"\u8bfb\u53d6\u9009\u4e2d\u9879", None))
        self.dingyi_pj_yuan_delete.setText(QCoreApplication.translate("dingyi_pj", u"\u5220\u9664\u9009\u4e2d\u9879", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("dingyi_pj", u"\u4e09\u89d2\u5f62\u4e0e\u591a\u8fb9\u5f62", None))
        self.dingyi_pj_duobianxing_read.setText(QCoreApplication.translate("dingyi_pj", u"\u8bfb\u53d6\u9009\u4e2d\u9879", None))
        self.dingyi_pj_duobianxing_delete.setText(QCoreApplication.translate("dingyi_pj", u"\u5220\u9664\u9009\u4e2d\u9879", None))
        self.groupBox.setTitle(QCoreApplication.translate("dingyi_pj", u"\u521b\u5efa\u5bf9\u8c61", None))
        self.label.setText(QCoreApplication.translate("dingyi_pj", u"\u521b\u5efa\u5bf9\u8c61\u65b9\u6cd5\uff1a", None))
        self.dingyi_pj_fangfa.setItemText(0, QCoreApplication.translate("dingyi_pj", u"\u672a\u9009\u62e9", None))
        self.dingyi_pj_fangfa.setItemText(1, QCoreApplication.translate("dingyi_pj", u"\u901a\u8fc7\u5750\u6807\u521b\u5efa\u70b9[\u53c2\u6570\uff1ax\u5750\u6807,y\u5750\u6807]", None))
        self.dingyi_pj_fangfa.setItemText(2, QCoreApplication.translate("dingyi_pj", u"\u901a\u8fc7\u4e24\u70b9\u521b\u5efa\u76f4\u7ebf[\u53c2\u6570\uff1a\u70b91\u540d\u79f0,\u70b92\u540d\u79f0]", None))
        self.dingyi_pj_fangfa.setItemText(3, QCoreApplication.translate("dingyi_pj", u"\u901a\u8fc7\u5706\u5fc3\u548c\u534a\u5f84\u521b\u5efa\u5706[\u53c2\u6570\uff1a\u5706\u5fc3\u540d\u79f0,\u534a\u5f84\u957f\u5ea6]", None))
        self.dingyi_pj_fangfa.setItemText(4, QCoreApplication.translate("dingyi_pj", u"\u901a\u8fc7\u4e09\u70b9\u521b\u5efa\u5706\uff08\u5916\u63a5\u5706\uff09[\u53c2\u6570\uff1a\u70b91\u540d\u79f0,\u70b92\u540d\u79f0,\u70b93\u540d\u79f0]", None))
        self.dingyi_pj_fangfa.setItemText(5, QCoreApplication.translate("dingyi_pj", u"\u901a\u8fc7\u4e09\u70b9\u521b\u5efa\u4e09\u89d2\u5f62[\u53c2\u6570\uff1a\u70b91\u540d\u79f0,\u70b92\u540d\u79f0,\u70b93\u540d\u79f0]", None))
        self.dingyi_pj_fangfa.setItemText(6, QCoreApplication.translate("dingyi_pj", u"\u901a\u8fc7\u9876\u70b9\u5217\u8868\u521b\u5efa\u591a\u8fb9\u5f62[\u53c2\u6570\uff1a\u70b91\u540d\u79f0,\u70b92\u540d\u79f0,\u2026\u2026,\u70b9n\u540d\u79f0]", None))
        self.dingyi_pj_fangfa.setItemText(7, QCoreApplication.translate("dingyi_pj", u"\u4ee5\u4e24\u70b9\u4e3a\u76f4\u5f84\u7aef\u70b9\u4f5c\u5706[\u53c2\u6570\uff1a\u70b91\u540d\u79f0,\u70b92\u540d\u79f0]", None))
        self.dingyi_pj_fangfa.setItemText(8, QCoreApplication.translate("dingyi_pj", u"\u4ee5\u5706\u5fc3\u548c\u5706\u4e0a\u4e00\u70b9\u4f5c\u5706[\u53c2\u6570\uff1a\u70b91\u540d\u79f0,\u70b92\u540d\u79f0]", None))
        self.dingyi_pj_fangfa.setItemText(9, QCoreApplication.translate("dingyi_pj", u"\u7ebf\u6bb5\u7684\u4e2d\u5782\u7ebf[\u53c2\u6570\uff1a\u7ebf\u6bb5\u540d\u79f0]", None))
        self.dingyi_pj_fangfa.setItemText(10, QCoreApplication.translate("dingyi_pj", u"\u8fc7\u4e00\u70b9\u4f5c\u5df2\u77e5\u76f4\u7ebf\u7684\u5e73\u884c\u7ebf[\u53c2\u6570\uff1a\u70b9\u540d\u79f0,\u7ebf\u6bb5\u540d\u79f0]", None))
        self.dingyi_pj_fangfa.setItemText(11, QCoreApplication.translate("dingyi_pj", u"\u8fc7\u4e00\u70b9\u4f5c\u5df2\u77e5\u76f4\u7ebf\u7684\u5782\u7ebf[\u53c2\u6570\uff1a\u70b9\u540d\u79f0,\u7ebf\u6bb5\u540d\u79f0]", None))
        self.dingyi_pj_fangfa.setItemText(12, QCoreApplication.translate("dingyi_pj", u"\u4e24\u76f8\u4ea4\u76f4\u7ebf\u7684\u89d2\u5e73\u5206\u7ebf[\u53c2\u6570\uff1a\u76f4\u7ebf\u540d\u79f0,\u76f4\u7ebf\u540d\u79f0]", None))
        self.dingyi_pj_fangfa.setItemText(13, QCoreApplication.translate("dingyi_pj", u"\u89d2 p1-p2-p3 \u7684\u89d2\u5e73\u5206\u7ebf\uff08p2 \u4e3a\u9876\u70b9\uff09[\u53c2\u6570\uff1a\u70b91\u540d\u79f0,\u70b92\u540d\u79f0,\u70b93\u540d\u79f0]", None))
        self.dingyi_pj_fangfa.setItemText(14, QCoreApplication.translate("dingyi_pj", u"\u4e09\u89d2\u5f62\u7684\u4e2d\u7ebf[\u53c2\u6570\uff1a\u4e09\u89d2\u5f62\u540d\u79f0,\u9876\u70b9\u540d\u79f0]", None))
        self.dingyi_pj_fangfa.setItemText(15, QCoreApplication.translate("dingyi_pj", u"\u4e09\u89d2\u5f62\u7684\u9ad8\u7ebf[\u53c2\u6570\uff1a\u4e09\u89d2\u5f62\u540d\u79f0,\u9876\u70b9\u540d\u79f0]", None))
        self.dingyi_pj_fangfa.setItemText(16, QCoreApplication.translate("dingyi_pj", u"\u4e09\u89d2\u5f62\u7684\u4e2d\u4f4d\u7ebf[\u53c2\u6570\uff1a\u4e09\u89d2\u5f62\u540d\u79f0,\u9876\u70b9\u540d\u79f0]", None))
        self.dingyi_pj_fangfa.setItemText(17, QCoreApplication.translate("dingyi_pj", u"\u4e09\u89d2\u5f62\u7684\u5185\u5207\u5706[\u53c2\u6570\uff1a\u4e09\u89d2\u5f62\u540d\u79f0]", None))
        self.dingyi_pj_fangfa.setItemText(18, QCoreApplication.translate("dingyi_pj", u"\u4e09\u89d2\u5f62\u7684\u65c1\u5207\u5706[\u53c2\u6570\uff1a\u4e09\u89d2\u5f62\u540d\u79f0,\u9876\u70b9\u540d\u79f0]", None))
        self.dingyi_pj_fangfa.setItemText(19, QCoreApplication.translate("dingyi_pj", u"\u901a\u8fc7\u4e24\u70b9\u6784\u9020\u7ebf\u6bb5[\u53c2\u6570\uff1a\u70b91\u540d\u79f0,\u70b92\u540d\u79f0]", None))

        self.label_3.setText(QCoreApplication.translate("dingyi_pj", u"\u5bf9\u8c61\u540d\u79f0\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("dingyi_pj", u"\u53c2\u6570(\u76f4\u63a5\u8f93\u5165\uff0c\u4ee5\u82f1\u6587\u534a\u89d2\u9017\u53f7\u5206\u9694)\uff1a", None))
        self.dingyi_pj_baocun.setText(QCoreApplication.translate("dingyi_pj", u"\u4fdd\u5b58", None))
    # retranslateUi

