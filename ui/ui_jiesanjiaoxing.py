# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'jiesanjiaoxingTiRCyx.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QWidget)

class Ui_jiesanjiaoxing(object):
    def setupUi(self, jiesanjiaoxing):
        if not jiesanjiaoxing.objectName():
            jiesanjiaoxing.setObjectName(u"jiesanjiaoxing")
        jiesanjiaoxing.resize(801, 551)
        self.groupBox = QGroupBox(jiesanjiaoxing)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 771, 131))
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 30, 69, 19))
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 60, 69, 19))
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 90, 69, 19))
        self.jiesanjiaoxing_tiaojian1 = QLineEdit(self.groupBox)
        self.jiesanjiaoxing_tiaojian1.setObjectName(u"jiesanjiaoxing_tiaojian1")
        self.jiesanjiaoxing_tiaojian1.setGeometry(QRect(170, 30, 591, 21))
        self.jiesanjiaoxing_tiaojian2 = QLineEdit(self.groupBox)
        self.jiesanjiaoxing_tiaojian2.setObjectName(u"jiesanjiaoxing_tiaojian2")
        self.jiesanjiaoxing_tiaojian2.setGeometry(QRect(170, 60, 591, 21))
        self.jiesanjiaoxing_tiaojian3 = QLineEdit(self.groupBox)
        self.jiesanjiaoxing_tiaojian3.setObjectName(u"jiesanjiaoxing_tiaojian3")
        self.jiesanjiaoxing_tiaojian3.setGeometry(QRect(170, 90, 591, 21))
        self.jiesanjiaoxing_tiaojian1_cbx = QComboBox(self.groupBox)
        self.jiesanjiaoxing_tiaojian1_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian1_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian1_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian1_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian1_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian1_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian1_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian1_cbx.setObjectName(u"jiesanjiaoxing_tiaojian1_cbx")
        self.jiesanjiaoxing_tiaojian1_cbx.setGeometry(QRect(70, 30, 83, 21))
        self.jiesanjiaoxing_tiaojian2_cbx = QComboBox(self.groupBox)
        self.jiesanjiaoxing_tiaojian2_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian2_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian2_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian2_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian2_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian2_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian2_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian2_cbx.setObjectName(u"jiesanjiaoxing_tiaojian2_cbx")
        self.jiesanjiaoxing_tiaojian2_cbx.setGeometry(QRect(70, 60, 83, 21))
        self.jiesanjiaoxing_tiaojian3_cbx = QComboBox(self.groupBox)
        self.jiesanjiaoxing_tiaojian3_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian3_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian3_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian3_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian3_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian3_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian3_cbx.addItem("")
        self.jiesanjiaoxing_tiaojian3_cbx.setObjectName(u"jiesanjiaoxing_tiaojian3_cbx")
        self.jiesanjiaoxing_tiaojian3_cbx.setGeometry(QRect(70, 90, 83, 21))
        self.jiesanjiaoxing_qiujie = QPushButton(jiesanjiaoxing)
        self.jiesanjiaoxing_qiujie.setObjectName(u"jiesanjiaoxing_qiujie")
        self.jiesanjiaoxing_qiujie.setGeometry(QRect(10, 510, 771, 27))
        self.groupBox_2 = QGroupBox(jiesanjiaoxing)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 150, 771, 171))
        self.jiesanjiaoxing_yuantiaojian = QWebEngineView(self.groupBox_2)
        self.jiesanjiaoxing_yuantiaojian.setObjectName(u"jiesanjiaoxing_yuantiaojian")
        self.jiesanjiaoxing_yuantiaojian.setGeometry(QRect(10, 20, 751, 141))
        self.jiesanjiaoxing_yuantiaojian.setUrl(QUrl(u"about:blank"))
        self.groupBox_3 = QGroupBox(jiesanjiaoxing)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(10, 330, 771, 171))
        self.jiesanjiaoxing_jieguo = QWebEngineView(self.groupBox_3)
        self.jiesanjiaoxing_jieguo.setObjectName(u"jiesanjiaoxing_jieguo")
        self.jiesanjiaoxing_jieguo.setGeometry(QRect(10, 20, 751, 111))
        self.jiesanjiaoxing_jieguo.setUrl(QUrl(u"about:blank"))
        self.jiesanjiaoxing_jieguo_lineedit = QLineEdit(self.groupBox_3)
        self.jiesanjiaoxing_jieguo_lineedit.setObjectName(u"jiesanjiaoxing_jieguo_lineedit")
        self.jiesanjiaoxing_jieguo_lineedit.setGeometry(QRect(10, 140, 751, 21))

        self.retranslateUi(jiesanjiaoxing)

        QMetaObject.connectSlotsByName(jiesanjiaoxing)
    # setupUi

    def retranslateUi(self, jiesanjiaoxing):
        jiesanjiaoxing.setWindowTitle(QCoreApplication.translate("jiesanjiaoxing", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("jiesanjiaoxing", u"\u6761\u4ef6\u8f93\u5165", None))
        self.label.setText(QCoreApplication.translate("jiesanjiaoxing", u"\u6761\u4ef61\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("jiesanjiaoxing", u"\u6761\u4ef62\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("jiesanjiaoxing", u"\u6761\u4ef63\uff1a", None))
        self.jiesanjiaoxing_tiaojian1_cbx.setItemText(0, QCoreApplication.translate("jiesanjiaoxing", u"\u672a\u9009\u62e9", None))
        self.jiesanjiaoxing_tiaojian1_cbx.setItemText(1, QCoreApplication.translate("jiesanjiaoxing", u"\u89d2A", None))
        self.jiesanjiaoxing_tiaojian1_cbx.setItemText(2, QCoreApplication.translate("jiesanjiaoxing", u"\u89d2B", None))
        self.jiesanjiaoxing_tiaojian1_cbx.setItemText(3, QCoreApplication.translate("jiesanjiaoxing", u"\u89d2C", None))
        self.jiesanjiaoxing_tiaojian1_cbx.setItemText(4, QCoreApplication.translate("jiesanjiaoxing", u"\u8fb9a", None))
        self.jiesanjiaoxing_tiaojian1_cbx.setItemText(5, QCoreApplication.translate("jiesanjiaoxing", u"\u8fb9b", None))
        self.jiesanjiaoxing_tiaojian1_cbx.setItemText(6, QCoreApplication.translate("jiesanjiaoxing", u"\u8fb9c", None))

        self.jiesanjiaoxing_tiaojian2_cbx.setItemText(0, QCoreApplication.translate("jiesanjiaoxing", u"\u672a\u9009\u62e9", None))
        self.jiesanjiaoxing_tiaojian2_cbx.setItemText(1, QCoreApplication.translate("jiesanjiaoxing", u"\u89d2A", None))
        self.jiesanjiaoxing_tiaojian2_cbx.setItemText(2, QCoreApplication.translate("jiesanjiaoxing", u"\u89d2B", None))
        self.jiesanjiaoxing_tiaojian2_cbx.setItemText(3, QCoreApplication.translate("jiesanjiaoxing", u"\u89d2C", None))
        self.jiesanjiaoxing_tiaojian2_cbx.setItemText(4, QCoreApplication.translate("jiesanjiaoxing", u"\u8fb9a", None))
        self.jiesanjiaoxing_tiaojian2_cbx.setItemText(5, QCoreApplication.translate("jiesanjiaoxing", u"\u8fb9b", None))
        self.jiesanjiaoxing_tiaojian2_cbx.setItemText(6, QCoreApplication.translate("jiesanjiaoxing", u"\u8fb9c", None))

        self.jiesanjiaoxing_tiaojian3_cbx.setItemText(0, QCoreApplication.translate("jiesanjiaoxing", u"\u672a\u9009\u62e9", None))
        self.jiesanjiaoxing_tiaojian3_cbx.setItemText(1, QCoreApplication.translate("jiesanjiaoxing", u"\u89d2A", None))
        self.jiesanjiaoxing_tiaojian3_cbx.setItemText(2, QCoreApplication.translate("jiesanjiaoxing", u"\u89d2B", None))
        self.jiesanjiaoxing_tiaojian3_cbx.setItemText(3, QCoreApplication.translate("jiesanjiaoxing", u"\u89d2C", None))
        self.jiesanjiaoxing_tiaojian3_cbx.setItemText(4, QCoreApplication.translate("jiesanjiaoxing", u"\u8fb9a", None))
        self.jiesanjiaoxing_tiaojian3_cbx.setItemText(5, QCoreApplication.translate("jiesanjiaoxing", u"\u8fb9b", None))
        self.jiesanjiaoxing_tiaojian3_cbx.setItemText(6, QCoreApplication.translate("jiesanjiaoxing", u"\u8fb9c", None))

        self.jiesanjiaoxing_qiujie.setText(QCoreApplication.translate("jiesanjiaoxing", u"\u6c42\u89e3", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("jiesanjiaoxing", u"\u539f\u6761\u4ef6", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("jiesanjiaoxing", u"\u7ed3\u679c", None))
    # retranslateUi

