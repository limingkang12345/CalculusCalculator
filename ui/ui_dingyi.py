# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dingyiNSOByB.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGroupBox,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QWidget)

class Ui_dingyi(object):
    def setupUi(self, dingyi):
        if not dingyi.objectName():
            dingyi.setObjectName(u"dingyi")
        dingyi.setWindowModality(Qt.WindowModality.NonModal)
        dingyi.resize(801, 551)
        self.groupBox_20 = QGroupBox(dingyi)
        self.groupBox_20.setObjectName(u"groupBox_20")
        self.groupBox_20.setGeometry(QRect(250, 10, 531, 151))
        self.formLayoutWidget = QWidget(self.groupBox_20)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 30, 511, 91))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(6)
        self.formLayout.setVerticalSpacing(6)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label_7 = QLabel(self.formLayoutWidget)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_7)

        self.dingyi_mingcheng = QLineEdit(self.formLayoutWidget)
        self.dingyi_mingcheng.setObjectName(u"dingyi_mingcheng")
        self.dingyi_mingcheng.setClearButtonEnabled(True)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.dingyi_mingcheng)

        self.label_8 = QLabel(self.formLayoutWidget)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_8)

        self.label_9 = QLabel(self.formLayoutWidget)
        self.label_9.setObjectName(u"label_9")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_9)

        self.dingyi_dingyiyu = QLineEdit(self.formLayoutWidget)
        self.dingyi_dingyiyu.setObjectName(u"dingyi_dingyiyu")
        self.dingyi_dingyiyu.setClearButtonEnabled(True)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.dingyi_dingyiyu)

        self.dingyi_biaodashi = QLineEdit(self.formLayoutWidget)
        self.dingyi_biaodashi.setObjectName(u"dingyi_biaodashi")
        self.dingyi_biaodashi.setClearButtonEnabled(True)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.dingyi_biaodashi)

        self.dingyi_shanchu = QPushButton(self.groupBox_20)
        self.dingyi_shanchu.setObjectName(u"dingyi_shanchu")
        self.dingyi_shanchu.setGeometry(QRect(440, 120, 81, 26))
        self.dingyi_baocun = QPushButton(self.groupBox_20)
        self.dingyi_baocun.setObjectName(u"dingyi_baocun")
        self.dingyi_baocun.setGeometry(QRect(350, 120, 81, 26))
        self.label_12 = QLabel(self.groupBox_20)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(10, 120, 84, 24))
        self.dingyi_zibianliang = QLineEdit(self.groupBox_20)
        self.dingyi_zibianliang.setObjectName(u"dingyi_zibianliang")
        self.dingyi_zibianliang.setGeometry(QRect(107, 120, 231, 25))
        self.dingyi_zibianliang.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.dingyi_zibianliang.setClearButtonEnabled(True)
        self.groupBox_22 = QGroupBox(dingyi)
        self.groupBox_22.setObjectName(u"groupBox_22")
        self.groupBox_22.setGeometry(QRect(10, 310, 771, 231))
        self.label_11 = QLabel(self.groupBox_22)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(10, 20, 71, 18))
        self.dingyi_zibianliangzhi = QLineEdit(self.groupBox_22)
        self.dingyi_zibianliangzhi.setObjectName(u"dingyi_zibianliangzhi")
        self.dingyi_zibianliangzhi.setGeometry(QRect(90, 20, 671, 21))
        self.dingyi_zibianliangzhi.setClearButtonEnabled(True)
        self.dingyi_qiuzhi = QWebEngineView(self.groupBox_22)
        self.dingyi_qiuzhi.setObjectName(u"dingyi_qiuzhi")
        self.dingyi_qiuzhi.setGeometry(QRect(10, 50, 751, 141))
        self.dingyi_qiuzhi.setUrl(QUrl(u"about:blank"))
        self.dingyi_qiuzhi_lineedit = QLineEdit(self.groupBox_22)
        self.dingyi_qiuzhi_lineedit.setObjectName(u"dingyi_qiuzhi_lineedit")
        self.dingyi_qiuzhi_lineedit.setGeometry(QRect(10, 200, 751, 21))
        self.groupBox_21 = QGroupBox(dingyi)
        self.groupBox_21.setObjectName(u"groupBox_21")
        self.groupBox_21.setGeometry(QRect(250, 170, 531, 141))
        self.dingyi_hanshushuxing_cbx = QComboBox(self.groupBox_21)
        self.dingyi_hanshushuxing_cbx.setObjectName(u"dingyi_hanshushuxing_cbx")
        self.dingyi_hanshushuxing_cbx.setGeometry(QRect(10, 20, 151, 20))
        self.dingyi_hanshushuxing = QWebEngineView(self.groupBox_21)
        self.dingyi_hanshushuxing.setObjectName(u"dingyi_hanshushuxing")
        self.dingyi_hanshushuxing.setGeometry(QRect(10, 50, 511, 81))
        self.dingyi_hanshushuxing.setUrl(QUrl(u"about:blank"))
        self.dingyi_hanshushuxing_lineedit = QLineEdit(self.groupBox_21)
        self.dingyi_hanshushuxing_lineedit.setObjectName(u"dingyi_hanshushuxing_lineedit")
        self.dingyi_hanshushuxing_lineedit.setGeometry(QRect(170, 20, 351, 21))
        self.groupBox_19 = QGroupBox(dingyi)
        self.groupBox_19.setObjectName(u"groupBox_19")
        self.groupBox_19.setGeometry(QRect(10, 10, 221, 301))
        self.dingyi_hanshuliebiao = QListWidget(self.groupBox_19)
        self.dingyi_hanshuliebiao.setObjectName(u"dingyi_hanshuliebiao")
        self.dingyi_hanshuliebiao.setGeometry(QRect(10, 20, 201, 271))

        self.retranslateUi(dingyi)

        self.dingyi_hanshushuxing_cbx.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(dingyi)
    # setupUi

    def retranslateUi(self, dingyi):
        dingyi.setWindowTitle(QCoreApplication.translate("dingyi", u"Form", None))
        self.groupBox_20.setTitle(QCoreApplication.translate("dingyi", u"\u51fd\u6570\u7f16\u8f91\u533a", None))
        self.label_7.setText(QCoreApplication.translate("dingyi", u"\u51fd\u6570\u540d\u79f0\uff1a", None))
        self.dingyi_mingcheng.setText(QCoreApplication.translate("dingyi", u"f", None))
        self.label_8.setText(QCoreApplication.translate("dingyi", u"\u51fd\u6570\u8868\u8fbe\u5f0f\uff1a", None))
        self.label_9.setText(QCoreApplication.translate("dingyi", u"\u51fd\u6570\u5b9a\u4e49\u57df\uff1a", None))
        self.dingyi_dingyiyu.setText(QCoreApplication.translate("dingyi", u"Reals", None))
        self.dingyi_shanchu.setText(QCoreApplication.translate("dingyi", u"\u5220\u9664", None))
        self.dingyi_baocun.setText(QCoreApplication.translate("dingyi", u"\u4fdd\u5b58", None))
        self.label_12.setText(QCoreApplication.translate("dingyi", u"\u51fd\u6570\u81ea\u53d8\u91cf\uff1a", None))
        self.dingyi_zibianliang.setText(QCoreApplication.translate("dingyi", u"x", None))
        self.groupBox_22.setTitle(QCoreApplication.translate("dingyi", u"\u51fd\u6570\u6c42\u503c", None))
        self.label_11.setText(QCoreApplication.translate("dingyi", u"\u81ea\u53d8\u91cf\u503c\uff1a", None))
        self.dingyi_zibianliangzhi.setText(QCoreApplication.translate("dingyi", u"0", None))
        self.groupBox_21.setTitle(QCoreApplication.translate("dingyi", u"\u51fd\u6570\u5c5e\u6027\u533a", None))
        self.groupBox_19.setTitle(QCoreApplication.translate("dingyi", u"\u51fd\u6570\u5217\u8868", None))
    # retranslateUi

