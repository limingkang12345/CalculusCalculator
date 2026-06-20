# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dingyiSiFAID.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QWidget)

class Ui_dingyi(object):
    def setupUi(self, dingyi):
        if not dingyi.objectName():
            dingyi.setObjectName(u"dingyi")
        dingyi.setWindowModality(Qt.WindowModality.NonModal)
        dingyi.resize(801, 551)
        self.gridLayout_6 = QGridLayout(dingyi)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.groupBox_19 = QGroupBox(dingyi)
        self.groupBox_19.setObjectName(u"groupBox_19")
        self.gridLayout_4 = QGridLayout(self.groupBox_19)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.dingyi_hanshuliebiao = QListWidget(self.groupBox_19)
        self.dingyi_hanshuliebiao.setObjectName(u"dingyi_hanshuliebiao")

        self.gridLayout_4.addWidget(self.dingyi_hanshuliebiao, 0, 0, 1, 1)


        self.gridLayout_6.addWidget(self.groupBox_19, 0, 0, 2, 1)

        self.groupBox_20 = QGroupBox(dingyi)
        self.groupBox_20.setObjectName(u"groupBox_20")
        self.gridLayout_2 = QGridLayout(self.groupBox_20)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.dingyi_baocun = QPushButton(self.groupBox_20)
        self.dingyi_baocun.setObjectName(u"dingyi_baocun")

        self.gridLayout.addWidget(self.dingyi_baocun, 3, 2, 1, 1)

        self.dingyi_zibianliang = QLineEdit(self.groupBox_20)
        self.dingyi_zibianliang.setObjectName(u"dingyi_zibianliang")
        self.dingyi_zibianliang.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.dingyi_zibianliang.setClearButtonEnabled(True)

        self.gridLayout.addWidget(self.dingyi_zibianliang, 3, 1, 1, 1)

        self.label_7 = QLabel(self.groupBox_20)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)

        self.label_12 = QLabel(self.groupBox_20)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 3, 0, 1, 1)

        self.label_9 = QLabel(self.groupBox_20)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 2, 0, 1, 1)

        self.label_8 = QLabel(self.groupBox_20)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 1, 0, 1, 1)

        self.dingyi_shanchu = QPushButton(self.groupBox_20)
        self.dingyi_shanchu.setObjectName(u"dingyi_shanchu")

        self.gridLayout.addWidget(self.dingyi_shanchu, 3, 3, 1, 1)

        self.dingyi_dingyiyu = QLineEdit(self.groupBox_20)
        self.dingyi_dingyiyu.setObjectName(u"dingyi_dingyiyu")
        self.dingyi_dingyiyu.setClearButtonEnabled(True)

        self.gridLayout.addWidget(self.dingyi_dingyiyu, 2, 1, 1, 3)

        self.dingyi_biaodashi = QLineEdit(self.groupBox_20)
        self.dingyi_biaodashi.setObjectName(u"dingyi_biaodashi")
        self.dingyi_biaodashi.setClearButtonEnabled(True)

        self.gridLayout.addWidget(self.dingyi_biaodashi, 1, 1, 1, 3)

        self.dingyi_mingcheng = QLineEdit(self.groupBox_20)
        self.dingyi_mingcheng.setObjectName(u"dingyi_mingcheng")
        self.dingyi_mingcheng.setClearButtonEnabled(True)

        self.gridLayout.addWidget(self.dingyi_mingcheng, 0, 1, 1, 3)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 2, 2)


        self.gridLayout_6.addWidget(self.groupBox_20, 0, 1, 1, 1)

        self.groupBox_21 = QGroupBox(dingyi)
        self.groupBox_21.setObjectName(u"groupBox_21")
        self.gridLayout_3 = QGridLayout(self.groupBox_21)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.dingyi_hanshushuxing_cbx = QComboBox(self.groupBox_21)
        self.dingyi_hanshushuxing_cbx.setObjectName(u"dingyi_hanshushuxing_cbx")

        self.gridLayout_3.addWidget(self.dingyi_hanshushuxing_cbx, 0, 0, 1, 1)

        self.dingyi_hanshushuxing_lineedit = QLineEdit(self.groupBox_21)
        self.dingyi_hanshushuxing_lineedit.setObjectName(u"dingyi_hanshushuxing_lineedit")

        self.gridLayout_3.addWidget(self.dingyi_hanshushuxing_lineedit, 0, 1, 1, 1)

        self.dingyi_hanshushuxing = QWebEngineView(self.groupBox_21)
        self.dingyi_hanshushuxing.setObjectName(u"dingyi_hanshushuxing")
        self.dingyi_hanshushuxing.setUrl(QUrl(u"about:blank"))

        self.gridLayout_3.addWidget(self.dingyi_hanshushuxing, 1, 0, 1, 2)


        self.gridLayout_6.addWidget(self.groupBox_21, 1, 1, 1, 1)

        self.groupBox_22 = QGroupBox(dingyi)
        self.groupBox_22.setObjectName(u"groupBox_22")
        self.gridLayout_5 = QGridLayout(self.groupBox_22)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_11 = QLabel(self.groupBox_22)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_5.addWidget(self.label_11, 0, 0, 1, 1)

        self.dingyi_zibianliangzhi = QLineEdit(self.groupBox_22)
        self.dingyi_zibianliangzhi.setObjectName(u"dingyi_zibianliangzhi")
        self.dingyi_zibianliangzhi.setClearButtonEnabled(True)

        self.gridLayout_5.addWidget(self.dingyi_zibianliangzhi, 0, 1, 1, 1)

        self.dingyi_qiuzhi = QWebEngineView(self.groupBox_22)
        self.dingyi_qiuzhi.setObjectName(u"dingyi_qiuzhi")
        self.dingyi_qiuzhi.setUrl(QUrl(u"about:blank"))

        self.gridLayout_5.addWidget(self.dingyi_qiuzhi, 1, 0, 1, 2)

        self.dingyi_qiuzhi_lineedit = QLineEdit(self.groupBox_22)
        self.dingyi_qiuzhi_lineedit.setObjectName(u"dingyi_qiuzhi_lineedit")

        self.gridLayout_5.addWidget(self.dingyi_qiuzhi_lineedit, 2, 0, 1, 2)


        self.gridLayout_6.addWidget(self.groupBox_22, 2, 0, 1, 2)

        self.gridLayout_6.setRowStretch(0, 1)
        self.gridLayout_6.setRowStretch(1, 2)
        self.gridLayout_6.setRowStretch(2, 3)
        self.gridLayout_6.setColumnStretch(0, 2)
        self.gridLayout_6.setColumnStretch(1, 3)

        self.retranslateUi(dingyi)

        self.dingyi_hanshushuxing_cbx.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(dingyi)
    # setupUi

    def retranslateUi(self, dingyi):
        dingyi.setWindowTitle(QCoreApplication.translate("dingyi", u"Form", None))
        self.groupBox_19.setTitle(QCoreApplication.translate("dingyi", u"\u51fd\u6570\u5217\u8868", None))
        self.groupBox_20.setTitle(QCoreApplication.translate("dingyi", u"\u51fd\u6570\u7f16\u8f91\u533a", None))
        self.dingyi_baocun.setText(QCoreApplication.translate("dingyi", u"\u4fdd\u5b58", None))
        self.dingyi_zibianliang.setText(QCoreApplication.translate("dingyi", u"x", None))
        self.label_7.setText(QCoreApplication.translate("dingyi", u"\u51fd\u6570\u540d\u79f0\uff1a", None))
        self.label_12.setText(QCoreApplication.translate("dingyi", u"\u51fd\u6570\u81ea\u53d8\u91cf\uff1a", None))
        self.label_9.setText(QCoreApplication.translate("dingyi", u"\u51fd\u6570\u5b9a\u4e49\u57df\uff1a", None))
        self.label_8.setText(QCoreApplication.translate("dingyi", u"\u51fd\u6570\u8868\u8fbe\u5f0f\uff1a", None))
        self.dingyi_shanchu.setText(QCoreApplication.translate("dingyi", u"\u5220\u9664", None))
        self.dingyi_dingyiyu.setText(QCoreApplication.translate("dingyi", u"Reals", None))
        self.dingyi_mingcheng.setText(QCoreApplication.translate("dingyi", u"f", None))
        self.groupBox_21.setTitle(QCoreApplication.translate("dingyi", u"\u51fd\u6570\u5c5e\u6027\u533a", None))
        self.groupBox_22.setTitle(QCoreApplication.translate("dingyi", u"\u51fd\u6570\u6c42\u503c", None))
        self.label_11.setText(QCoreApplication.translate("dingyi", u"\u81ea\u53d8\u91cf\u503c\uff1a", None))
        self.dingyi_zibianliangzhi.setText(QCoreApplication.translate("dingyi", u"0", None))
    # retranslateUi

