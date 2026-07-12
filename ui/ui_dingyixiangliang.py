# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dingyixiangliangwYAbNN.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGraphicsView,
    QGridLayout, QGroupBox, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QWidget)

class Ui_dingyixiangliang(object):
    def setupUi(self, dingyixiangliang):
        if not dingyixiangliang.objectName():
            dingyixiangliang.setObjectName(u"dingyixiangliang")
        dingyixiangliang.setWindowModality(Qt.WindowModality.NonModal)
        dingyixiangliang.resize(801, 551)
        self.gridLayout = QGridLayout(dingyixiangliang)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_19 = QGroupBox(dingyixiangliang)
        self.groupBox_19.setObjectName(u"groupBox_19")
        self.gridLayout_2 = QGridLayout(self.groupBox_19)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.dingyixiangliang_xiangliangliebiao = QListWidget(self.groupBox_19)
        self.dingyixiangliang_xiangliangliebiao.setObjectName(u"dingyixiangliang_xiangliangliebiao")

        self.gridLayout_2.addWidget(self.dingyixiangliang_xiangliangliebiao, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_19, 0, 0, 2, 1)

        self.groupBox_20 = QGroupBox(dingyixiangliang)
        self.groupBox_20.setObjectName(u"groupBox_20")
        self.gridLayout_3 = QGridLayout(self.groupBox_20)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(6)
        self.formLayout.setVerticalSpacing(6)
        self.label_7 = QLabel(self.groupBox_20)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_7)

        self.dingyixiangliang_mingcheng = QLineEdit(self.groupBox_20)
        self.dingyixiangliang_mingcheng.setObjectName(u"dingyixiangliang_mingcheng")
        self.dingyixiangliang_mingcheng.setClearButtonEnabled(True)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.dingyixiangliang_mingcheng)

        self.label_8 = QLabel(self.groupBox_20)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_8)

        self.label_9 = QLabel(self.groupBox_20)
        self.label_9.setObjectName(u"label_9")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_9)

        self.dingyixiangliang_y = QLineEdit(self.groupBox_20)
        self.dingyixiangliang_y.setObjectName(u"dingyixiangliang_y")
        self.dingyixiangliang_y.setClearButtonEnabled(True)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.dingyixiangliang_y)

        self.dingyixiangliang_x = QLineEdit(self.groupBox_20)
        self.dingyixiangliang_x.setObjectName(u"dingyixiangliang_x")
        self.dingyixiangliang_x.setClearButtonEnabled(True)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.dingyixiangliang_x)


        self.gridLayout_3.addLayout(self.formLayout, 0, 0, 1, 2)

        self.dingyixiangliang_baocun = QPushButton(self.groupBox_20)
        self.dingyixiangliang_baocun.setObjectName(u"dingyixiangliang_baocun")

        self.gridLayout_3.addWidget(self.dingyixiangliang_baocun, 1, 0, 1, 1)

        self.dingyixiangliang_shanchu = QPushButton(self.groupBox_20)
        self.dingyixiangliang_shanchu.setObjectName(u"dingyixiangliang_shanchu")

        self.gridLayout_3.addWidget(self.dingyixiangliang_shanchu, 1, 1, 1, 1)


        self.gridLayout.addWidget(self.groupBox_20, 0, 1, 1, 1)

        self.groupBox_21 = QGroupBox(dingyixiangliang)
        self.groupBox_21.setObjectName(u"groupBox_21")
        self.gridLayout_4 = QGridLayout(self.groupBox_21)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.dingyixiangliang_xiangliangshuxing_cbx = QComboBox(self.groupBox_21)
        self.dingyixiangliang_xiangliangshuxing_cbx.setObjectName(u"dingyixiangliang_xiangliangshuxing_cbx")

        self.gridLayout_4.addWidget(self.dingyixiangliang_xiangliangshuxing_cbx, 0, 0, 1, 1)

        self.dingyixiangliang_xiangliangshuxing_lineedit = QLineEdit(self.groupBox_21)
        self.dingyixiangliang_xiangliangshuxing_lineedit.setObjectName(u"dingyixiangliang_xiangliangshuxing_lineedit")

        self.gridLayout_4.addWidget(self.dingyixiangliang_xiangliangshuxing_lineedit, 0, 1, 1, 1)

        self.dingyixiangliang_xiangliangshuxing = QGraphicsView(self.groupBox_21)
        self.dingyixiangliang_xiangliangshuxing.setObjectName(u"dingyixiangliang_xiangliangshuxing")
        self.dingyixiangliang_xiangliangshuxing.setProperty(u"url", QUrl(u"about:blank"))

        self.gridLayout_4.addWidget(self.dingyixiangliang_xiangliangshuxing, 1, 0, 1, 2)


        self.gridLayout.addWidget(self.groupBox_21, 1, 1, 1, 1)

        self.groupBox = QGroupBox(dingyixiangliang)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_5 = QGridLayout(self.groupBox)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1)

        self.dingyixiangliang_xiangliang1 = QComboBox(self.groupBox)
        self.dingyixiangliang_xiangliang1.setObjectName(u"dingyixiangliang_xiangliang1")

        self.gridLayout_5.addWidget(self.dingyixiangliang_xiangliang1, 0, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_5.addWidget(self.label_2, 0, 2, 1, 1)

        self.dingyixiangliang_xiangliang2 = QComboBox(self.groupBox)
        self.dingyixiangliang_xiangliang2.setObjectName(u"dingyixiangliang_xiangliang2")

        self.gridLayout_5.addWidget(self.dingyixiangliang_xiangliang2, 0, 3, 1, 1)

        self.dingyixiangliang_jisuanfangfa = QComboBox(self.groupBox)
        self.dingyixiangliang_jisuanfangfa.setObjectName(u"dingyixiangliang_jisuanfangfa")

        self.gridLayout_5.addWidget(self.dingyixiangliang_jisuanfangfa, 0, 4, 1, 1)

        self.dingyixiangliang_jisuan = QGraphicsView(self.groupBox)
        self.dingyixiangliang_jisuan.setObjectName(u"dingyixiangliang_jisuan")
        self.dingyixiangliang_jisuan.setProperty(u"url", QUrl(u"about:blank"))

        self.gridLayout_5.addWidget(self.dingyixiangliang_jisuan, 1, 0, 1, 5)

        self.dingyixiangliang_jisuan_lineedit = QLineEdit(self.groupBox)
        self.dingyixiangliang_jisuan_lineedit.setObjectName(u"dingyixiangliang_jisuan_lineedit")

        self.gridLayout_5.addWidget(self.dingyixiangliang_jisuan_lineedit, 2, 0, 1, 5)

        self.dingyixiangliang_jisuan_button = QPushButton(self.groupBox)
        self.dingyixiangliang_jisuan_button.setObjectName(u"dingyixiangliang_jisuan_button")

        self.gridLayout_5.addWidget(self.dingyixiangliang_jisuan_button, 3, 0, 1, 5)


        self.gridLayout.addWidget(self.groupBox, 2, 0, 1, 2)

        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 2)
        self.gridLayout.setRowStretch(2, 3)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 2)

        self.retranslateUi(dingyixiangliang)

        self.dingyixiangliang_xiangliangshuxing_cbx.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(dingyixiangliang)
    # setupUi

    def retranslateUi(self, dingyixiangliang):
        dingyixiangliang.setWindowTitle(QCoreApplication.translate("dingyixiangliang", u"Form", None))
        self.groupBox_19.setTitle(QCoreApplication.translate("dingyixiangliang", u"\u5411\u91cf\u5217\u8868", None))
        self.groupBox_20.setTitle(QCoreApplication.translate("dingyixiangliang", u"\u5411\u91cf\u7f16\u8f91\u533a", None))
        self.label_7.setText(QCoreApplication.translate("dingyixiangliang", u"\u5411\u91cf\u540d\u79f0\uff1a", None))
        self.dingyixiangliang_mingcheng.setText(QCoreApplication.translate("dingyixiangliang", u"v", None))
        self.label_8.setText(QCoreApplication.translate("dingyixiangliang", u"\u5411\u91cfx\u5750\u6807\uff1a", None))
        self.label_9.setText(QCoreApplication.translate("dingyixiangliang", u"\u5411\u91cfy\u5750\u6807\uff1a", None))
        self.dingyixiangliang_y.setText("")
        self.dingyixiangliang_baocun.setText(QCoreApplication.translate("dingyixiangliang", u"\u4fdd\u5b58", None))
        self.dingyixiangliang_shanchu.setText(QCoreApplication.translate("dingyixiangliang", u"\u5220\u9664", None))
        self.groupBox_21.setTitle(QCoreApplication.translate("dingyixiangliang", u"\u5411\u91cf\u5c5e\u6027\u533a", None))
        self.groupBox.setTitle(QCoreApplication.translate("dingyixiangliang", u"\u5411\u91cf\u8fd0\u7b97", None))
        self.label.setText(QCoreApplication.translate("dingyixiangliang", u"\u5411\u91cf1\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("dingyixiangliang", u"\u5411\u91cf2\uff1a", None))
        self.dingyixiangliang_jisuan_button.setText(QCoreApplication.translate("dingyixiangliang", u"\u8ba1\u7b97", None))
    # retranslateUi

