# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dingyixiangliangSoZiwa.ui'
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

class Ui_dingyixiangliang(object):
    def setupUi(self, dingyixiangliang):
        if not dingyixiangliang.objectName():
            dingyixiangliang.setObjectName(u"dingyixiangliang")
        dingyixiangliang.setWindowModality(Qt.WindowModality.NonModal)
        dingyixiangliang.resize(801, 551)
        self.groupBox_20 = QGroupBox(dingyixiangliang)
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

        self.dingyixiangliang_mingcheng = QLineEdit(self.formLayoutWidget)
        self.dingyixiangliang_mingcheng.setObjectName(u"dingyixiangliang_mingcheng")
        self.dingyixiangliang_mingcheng.setClearButtonEnabled(True)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.dingyixiangliang_mingcheng)

        self.label_8 = QLabel(self.formLayoutWidget)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_8)

        self.label_9 = QLabel(self.formLayoutWidget)
        self.label_9.setObjectName(u"label_9")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_9)

        self.dingyixiangliang_y = QLineEdit(self.formLayoutWidget)
        self.dingyixiangliang_y.setObjectName(u"dingyixiangliang_y")
        self.dingyixiangliang_y.setClearButtonEnabled(True)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.dingyixiangliang_y)

        self.dingyixiangliang_x = QLineEdit(self.formLayoutWidget)
        self.dingyixiangliang_x.setObjectName(u"dingyixiangliang_x")
        self.dingyixiangliang_x.setClearButtonEnabled(True)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.dingyixiangliang_x)

        self.dingyixiangliang_shanchu = QPushButton(self.groupBox_20)
        self.dingyixiangliang_shanchu.setObjectName(u"dingyixiangliang_shanchu")
        self.dingyixiangliang_shanchu.setGeometry(QRect(440, 120, 81, 26))
        self.dingyixiangliang_baocun = QPushButton(self.groupBox_20)
        self.dingyixiangliang_baocun.setObjectName(u"dingyixiangliang_baocun")
        self.dingyixiangliang_baocun.setGeometry(QRect(350, 120, 81, 26))
        self.groupBox_21 = QGroupBox(dingyixiangliang)
        self.groupBox_21.setObjectName(u"groupBox_21")
        self.groupBox_21.setGeometry(QRect(250, 170, 531, 141))
        self.dingyixiangliang_xiangliangshuxing_cbx = QComboBox(self.groupBox_21)
        self.dingyixiangliang_xiangliangshuxing_cbx.setObjectName(u"dingyixiangliang_xiangliangshuxing_cbx")
        self.dingyixiangliang_xiangliangshuxing_cbx.setGeometry(QRect(10, 20, 151, 20))
        self.dingyixiangliang_xiangliangshuxing = QWebEngineView(self.groupBox_21)
        self.dingyixiangliang_xiangliangshuxing.setObjectName(u"dingyixiangliang_xiangliangshuxing")
        self.dingyixiangliang_xiangliangshuxing.setGeometry(QRect(10, 50, 511, 81))
        self.dingyixiangliang_xiangliangshuxing.setUrl(QUrl(u"about:blank"))
        self.dingyixiangliang_xiangliangshuxing_lineedit = QLineEdit(self.groupBox_21)
        self.dingyixiangliang_xiangliangshuxing_lineedit.setObjectName(u"dingyixiangliang_xiangliangshuxing_lineedit")
        self.dingyixiangliang_xiangliangshuxing_lineedit.setGeometry(QRect(170, 20, 351, 21))
        self.groupBox_19 = QGroupBox(dingyixiangliang)
        self.groupBox_19.setObjectName(u"groupBox_19")
        self.groupBox_19.setGeometry(QRect(10, 10, 221, 301))
        self.dingyixiangliang_xiangliangliebiao = QListWidget(self.groupBox_19)
        self.dingyixiangliang_xiangliangliebiao.setObjectName(u"dingyixiangliang_xiangliangliebiao")
        self.dingyixiangliang_xiangliangliebiao.setGeometry(QRect(10, 20, 201, 271))
        self.groupBox = QGroupBox(dingyixiangliang)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 310, 771, 231))
        self.dingyixiangliang_xiangliang1 = QComboBox(self.groupBox)
        self.dingyixiangliang_xiangliang1.setObjectName(u"dingyixiangliang_xiangliang1")
        self.dingyixiangliang_xiangliang1.setGeometry(QRect(70, 30, 241, 21))
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 30, 69, 19))
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(320, 30, 69, 19))
        self.dingyixiangliang_xiangliang2 = QComboBox(self.groupBox)
        self.dingyixiangliang_xiangliang2.setObjectName(u"dingyixiangliang_xiangliang2")
        self.dingyixiangliang_xiangliang2.setGeometry(QRect(380, 30, 241, 21))
        self.dingyixiangliang_jisuan = QWebEngineView(self.groupBox)
        self.dingyixiangliang_jisuan.setObjectName(u"dingyixiangliang_jisuan")
        self.dingyixiangliang_jisuan.setGeometry(QRect(10, 60, 751, 101))
        self.dingyixiangliang_jisuan.setUrl(QUrl(u"about:blank"))
        self.dingyixiangliang_jisuan_button = QPushButton(self.groupBox)
        self.dingyixiangliang_jisuan_button.setObjectName(u"dingyixiangliang_jisuan_button")
        self.dingyixiangliang_jisuan_button.setGeometry(QRect(10, 200, 751, 27))
        self.dingyixiangliang_jisuanfangfa = QComboBox(self.groupBox)
        self.dingyixiangliang_jisuanfangfa.setObjectName(u"dingyixiangliang_jisuanfangfa")
        self.dingyixiangliang_jisuanfangfa.setGeometry(QRect(640, 30, 121, 21))
        self.dingyixiangliang_jisuan_lineedit = QLineEdit(self.groupBox)
        self.dingyixiangliang_jisuan_lineedit.setObjectName(u"dingyixiangliang_jisuan_lineedit")
        self.dingyixiangliang_jisuan_lineedit.setGeometry(QRect(10, 170, 751, 25))

        self.retranslateUi(dingyixiangliang)

        self.dingyixiangliang_xiangliangshuxing_cbx.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(dingyixiangliang)
    # setupUi

    def retranslateUi(self, dingyixiangliang):
        dingyixiangliang.setWindowTitle(QCoreApplication.translate("dingyixiangliang", u"Form", None))
        self.groupBox_20.setTitle(QCoreApplication.translate("dingyixiangliang", u"\u5411\u91cf\u7f16\u8f91\u533a", None))
        self.label_7.setText(QCoreApplication.translate("dingyixiangliang", u"\u5411\u91cf\u540d\u79f0\uff1a", None))
        self.dingyixiangliang_mingcheng.setText(QCoreApplication.translate("dingyixiangliang", u"v", None))
        self.label_8.setText(QCoreApplication.translate("dingyixiangliang", u"\u5411\u91cfx\u5750\u6807\uff1a", None))
        self.label_9.setText(QCoreApplication.translate("dingyixiangliang", u"\u5411\u91cfy\u5750\u6807\uff1a", None))
        self.dingyixiangliang_y.setText("")
        self.dingyixiangliang_shanchu.setText(QCoreApplication.translate("dingyixiangliang", u"\u5220\u9664", None))
        self.dingyixiangliang_baocun.setText(QCoreApplication.translate("dingyixiangliang", u"\u4fdd\u5b58", None))
        self.groupBox_21.setTitle(QCoreApplication.translate("dingyixiangliang", u"\u5411\u91cf\u5c5e\u6027\u533a", None))
        self.groupBox_19.setTitle(QCoreApplication.translate("dingyixiangliang", u"\u5411\u91cf\u5217\u8868", None))
        self.groupBox.setTitle(QCoreApplication.translate("dingyixiangliang", u"\u5411\u91cf\u8fd0\u7b97", None))
        self.label.setText(QCoreApplication.translate("dingyixiangliang", u"\u5411\u91cf1\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("dingyixiangliang", u"\u5411\u91cf2\uff1a", None))
        self.dingyixiangliang_jisuan_button.setText(QCoreApplication.translate("dingyixiangliang", u"\u8ba1\u7b97", None))
    # retranslateUi

