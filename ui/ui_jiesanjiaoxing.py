# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'jiesanjiaoxingzNUrEj.ui'
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
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QWidget)

class Ui_jiesanjiaoxing(object):
    def setupUi(self, jiesanjiaoxing):
        if not jiesanjiaoxing.objectName():
            jiesanjiaoxing.setObjectName(u"jiesanjiaoxing")
        jiesanjiaoxing.resize(801, 551)
        self.gridLayout = QGridLayout(jiesanjiaoxing)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(jiesanjiaoxing)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.jiesanjiaoxing_tiaojian1_cbx = QComboBox(self.groupBox)
        self.jiesanjiaoxing_tiaojian1_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian1_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian1_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian1_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian1_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian1_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian1_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian1_cbx.setObjectName(u"jiesanjiaoxing_tiaojian1_cbx")

        self.gridLayout_2.addWidget(self.jiesanjiaoxing_tiaojian1_cbx, 0, 1, 1, 1)

        self.jiesanjiaoxing_tiaojian1 = QLineEdit(self.groupBox)
        self.jiesanjiaoxing_tiaojian1.setObjectName(u"jiesanjiaoxing_tiaojian1")

        self.gridLayout_2.addWidget(self.jiesanjiaoxing_tiaojian1, 0, 2, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        self.jiesanjiaoxing_tiaojian2_cbx = QComboBox(self.groupBox)
        self.jiesanjiaoxing_tiaojian2_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian2_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian2_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian2_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian2_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian2_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian2_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian2_cbx.setObjectName(u"jiesanjiaoxing_tiaojian2_cbx")

        self.gridLayout_2.addWidget(self.jiesanjiaoxing_tiaojian2_cbx, 1, 1, 1, 1)

        self.jiesanjiaoxing_tiaojian2 = QLineEdit(self.groupBox)
        self.jiesanjiaoxing_tiaojian2.setObjectName(u"jiesanjiaoxing_tiaojian2")

        self.gridLayout_2.addWidget(self.jiesanjiaoxing_tiaojian2, 1, 2, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)

        self.jiesanjiaoxing_tiaojian3_cbx = QComboBox(self.groupBox)
        self.jiesanjiaoxing_tiaojian3_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian3_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian3_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian3_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian3_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian3_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian3_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian3_cbx.setObjectName(u"jiesanjiaoxing_tiaojian3_cbx")

        self.gridLayout_2.addWidget(self.jiesanjiaoxing_tiaojian3_cbx, 2, 1, 1, 1)

        self.jiesanjiaoxing_tiaojian3 = QLineEdit(self.groupBox)
        self.jiesanjiaoxing_tiaojian3.setObjectName(u"jiesanjiaoxing_tiaojian3")

        self.gridLayout_2.addWidget(self.jiesanjiaoxing_tiaojian3, 2, 2, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.groupBox_2 = QGroupBox(jiesanjiaoxing)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_3 = QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.jiesanjiaoxing_yuantiaojian = QWebEngineView(self.groupBox_2)
        self.jiesanjiaoxing_yuantiaojian.setObjectName(u"jiesanjiaoxing_yuantiaojian")
        self.jiesanjiaoxing_yuantiaojian.setUrl(QUrl(u"about:blank"))

        self.gridLayout_3.addWidget(self.jiesanjiaoxing_yuantiaojian, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 1)

        self.groupBox_3 = QGroupBox(jiesanjiaoxing)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_4 = QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.jiesanjiaoxing_jieguo = QWebEngineView(self.groupBox_3)
        self.jiesanjiaoxing_jieguo.setObjectName(u"jiesanjiaoxing_jieguo")
        self.jiesanjiaoxing_jieguo.setUrl(QUrl(u"about:blank"))

        self.gridLayout_4.addWidget(self.jiesanjiaoxing_jieguo, 0, 0, 1, 1)

        self.jiesanjiaoxing_jieguo_lineedit = QLineEdit(self.groupBox_3)
        self.jiesanjiaoxing_jieguo_lineedit.setObjectName(u"jiesanjiaoxing_jieguo_lineedit")

        self.gridLayout_4.addWidget(self.jiesanjiaoxing_jieguo_lineedit, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_3, 2, 0, 1, 1)

        self.jiesanjiaoxing_qiujie = QPushButton(jiesanjiaoxing)
        self.jiesanjiaoxing_qiujie.setObjectName(u"jiesanjiaoxing_qiujie")

        self.gridLayout.addWidget(self.jiesanjiaoxing_qiujie, 3, 0, 1, 1)


        self.retranslateUi(jiesanjiaoxing)

        QMetaObject.connectSlotsByName(jiesanjiaoxing)
    # setupUi

    def retranslateUi(self, jiesanjiaoxing):
        jiesanjiaoxing.setWindowTitle(QCoreApplication.translate("jiesanjiaoxing", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("jiesanjiaoxing", u"\u6761\u4ef6\u8f93\u5165", None))
        self.label.setText(QCoreApplication.translate("jiesanjiaoxing", u"\u6761\u4ef61\uff1a", None))
        self.jiesanjiaoxing_tiaojian1_cbx.setItemText(0, QCoreApplication.translate("jiesanjiaoxing", u"\u672a\u9009\u62e9", None))
        self.jiesanjiaoxing_tiaojian1_cbx.setItemText(1, QCoreApplication.translate("jiesanjiaoxing", u"\u89d2A", None))
        self.jiesanjiaoxing_tiaojian1_cbx.setItemText(2, QCoreApplication.translate("jiesanjiaoxing", u"\u89d2B", None))
        self.jiesanjiaoxing_tiaojian1_cbx.setItemText(3, QCoreApplication.translate("jiesanjiaoxing", u"\u89d2C", None))
        self.jiesanjiaoxing_tiaojian1_cbx.setItemText(4, QCoreApplication.translate("jiesanjiaoxing", u"\u8fb9a", None))
        self.jiesanjiaoxing_tiaojian1_cbx.setItemText(5, QCoreApplication.translate("jiesanjiaoxing", u"\u8fb9b", None))
        self.jiesanjiaoxing_tiaojian1_cbx.setItemText(6, QCoreApplication.translate("jiesanjiaoxing", u"\u8fb9c", None))

        self.label_2.setText(QCoreApplication.translate("jiesanjiaoxing", u"\u6761\u4ef62\uff1a", None))
        self.jiesanjiaoxing_tiaojian2_cbx.setItemText(0, QCoreApplication.translate("jiesanjiaoxing", u"\u672a\u9009\u62e9", None))
        self.jiesanjiaoxing_tiaojian2_cbx.setItemText(1, QCoreApplication.translate("jiesanjiaoxing", u"\u89d2A", None))
        self.jiesanjiaoxing_tiaojian2_cbx.setItemText(2, QCoreApplication.translate("jiesanjiaoxing", u"\u89d2B", None))
        self.jiesanjiaoxing_tiaojian2_cbx.setItemText(3, QCoreApplication.translate("jiesanjiaoxing", u"\u89d2C", None))
        self.jiesanjiaoxing_tiaojian2_cbx.setItemText(4, QCoreApplication.translate("jiesanjiaoxing", u"\u8fb9a", None))
        self.jiesanjiaoxing_tiaojian2_cbx.setItemText(5, QCoreApplication.translate("jiesanjiaoxing", u"\u8fb9b", None))
        self.jiesanjiaoxing_tiaojian2_cbx.setItemText(6, QCoreApplication.translate("jiesanjiaoxing", u"\u8fb9c", None))

        self.label_3.setText(QCoreApplication.translate("jiesanjiaoxing", u"\u6761\u4ef63\uff1a", None))
        self.jiesanjiaoxing_tiaojian3_cbx.setItemText(0, QCoreApplication.translate("jiesanjiaoxing", u"\u672a\u9009\u62e9", None))
        self.jiesanjiaoxing_tiaojian3_cbx.setItemText(1, QCoreApplication.translate("jiesanjiaoxing", u"\u89d2A", None))
        self.jiesanjiaoxing_tiaojian3_cbx.setItemText(2, QCoreApplication.translate("jiesanjiaoxing", u"\u89d2B", None))
        self.jiesanjiaoxing_tiaojian3_cbx.setItemText(3, QCoreApplication.translate("jiesanjiaoxing", u"\u89d2C", None))
        self.jiesanjiaoxing_tiaojian3_cbx.setItemText(4, QCoreApplication.translate("jiesanjiaoxing", u"\u8fb9a", None))
        self.jiesanjiaoxing_tiaojian3_cbx.setItemText(5, QCoreApplication.translate("jiesanjiaoxing", u"\u8fb9b", None))
        self.jiesanjiaoxing_tiaojian3_cbx.setItemText(6, QCoreApplication.translate("jiesanjiaoxing", u"\u8fb9c", None))

        self.groupBox_2.setTitle(QCoreApplication.translate("jiesanjiaoxing", u"\u539f\u6761\u4ef6", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("jiesanjiaoxing", u"\u7ed3\u679c", None))
        self.jiesanjiaoxing_qiujie.setText(QCoreApplication.translate("jiesanjiaoxing", u"\u6c42\u89e3", None))
    # retranslateUi

