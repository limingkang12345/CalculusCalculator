# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ljjisuanriUTVP.ui'
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

class Ui_ljjisuan(object):
    def setupUi(self, ljjisuan):
        if not ljjisuan.objectName():
            ljjisuan.setObjectName(u"ljjisuan")
        ljjisuan.resize(801, 551)
        self.groupBox = QGroupBox(ljjisuan)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 771, 131))
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 30, 71, 19))
        self.ljjisuan_fangfa = QComboBox(self.groupBox)
        self.ljjisuan_fangfa.addItem("")
        self.ljjisuan_fangfa.addItem("")
        self.ljjisuan_fangfa.addItem("")
        self.ljjisuan_fangfa.addItem("")
        self.ljjisuan_fangfa.addItem("")
        self.ljjisuan_fangfa.addItem("")
        self.ljjisuan_fangfa.addItem("")
        self.ljjisuan_fangfa.addItem("")
        self.ljjisuan_fangfa.addItem("")
        self.ljjisuan_fangfa.addItem("")
        self.ljjisuan_fangfa.addItem("")
        self.ljjisuan_fangfa.addItem("")
        self.ljjisuan_fangfa.addItem("")
        self.ljjisuan_fangfa.addItem("")
        self.ljjisuan_fangfa.addItem("")
        self.ljjisuan_fangfa.addItem("")
        self.ljjisuan_fangfa.addItem("")
        self.ljjisuan_fangfa.addItem("")
        self.ljjisuan_fangfa.addItem("")
        self.ljjisuan_fangfa.addItem("")
        self.ljjisuan_fangfa.addItem("")
        self.ljjisuan_fangfa.addItem("")
        self.ljjisuan_fangfa.addItem("")
        self.ljjisuan_fangfa.setObjectName(u"ljjisuan_fangfa")
        self.ljjisuan_fangfa.setGeometry(QRect(90, 30, 671, 25))
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 70, 751, 19))
        self.ljjisuan_canshu = QLineEdit(self.groupBox)
        self.ljjisuan_canshu.setObjectName(u"ljjisuan_canshu")
        self.ljjisuan_canshu.setGeometry(QRect(10, 100, 751, 25))
        self.groupBox_2 = QGroupBox(ljjisuan)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 150, 771, 361))
        self.ljjisuan_result_lineedit = QLineEdit(self.groupBox_2)
        self.ljjisuan_result_lineedit.setObjectName(u"ljjisuan_result_lineedit")
        self.ljjisuan_result_lineedit.setGeometry(QRect(10, 330, 751, 25))
        self.ljjisuan_result = QWebEngineView(self.groupBox_2)
        self.ljjisuan_result.setObjectName(u"ljjisuan_result")
        self.ljjisuan_result.setGeometry(QRect(10, 20, 751, 301))
        self.ljjisuan_result.setUrl(QUrl(u"about:blank"))
        self.ljjisuan_jisuan = QPushButton(ljjisuan)
        self.ljjisuan_jisuan.setObjectName(u"ljjisuan_jisuan")
        self.ljjisuan_jisuan.setGeometry(QRect(10, 520, 771, 27))

        self.retranslateUi(ljjisuan)

        QMetaObject.connectSlotsByName(ljjisuan)
    # setupUi

    def retranslateUi(self, ljjisuan):
        ljjisuan.setWindowTitle(QCoreApplication.translate("ljjisuan", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("ljjisuan", u"\u7acb\u4f53\u51e0\u4f55\u8ba1\u7b97", None))
        self.label.setText(QCoreApplication.translate("ljjisuan", u"\u8ba1\u7b97\u65b9\u6cd5\uff1a", None))
        self.ljjisuan_fangfa.setItemText(0, QCoreApplication.translate("ljjisuan", u"\u672a\u9009\u62e9", None))
        self.ljjisuan_fangfa.setItemText(1, QCoreApplication.translate("ljjisuan", u"\u4e24\u70b9\u95f4\u8ddd\u79bb[\u53c2\u6570\uff1a\u70b91\u540d\u79f0,\u70b92\u540d\u79f0]", None))
        self.ljjisuan_fangfa.setItemText(2, QCoreApplication.translate("ljjisuan", u"\u4e2d\u70b9\u5750\u6807[\u53c2\u6570\uff1a\u70b91\u540d\u79f0,\u70b92\u540d\u79f0]", None))
        self.ljjisuan_fangfa.setItemText(3, QCoreApplication.translate("ljjisuan", u"\u70b9\u5230\u5e73\u9762\u8ddd\u79bb[\u53c2\u6570\uff1a\u70b9\u540d\u79f0,\u5e73\u9762\u540d\u79f0]", None))
        self.ljjisuan_fangfa.setItemText(4, QCoreApplication.translate("ljjisuan", u"\u70b9\u5230\u76f4\u7ebf\u8ddd\u79bb[\u53c2\u6570\uff1a\u70b9\u540d\u79f0,\u76f4\u7ebf\u540d\u79f0]", None))
        self.ljjisuan_fangfa.setItemText(5, QCoreApplication.translate("ljjisuan", u"\u70b9\u5728\u5e73\u9762\u7684\u6295\u5f71\u5750\u6807[\u53c2\u6570\uff1a\u70b9\u540d\u79f0,\u5e73\u9762\u540d\u79f0]", None))
        self.ljjisuan_fangfa.setItemText(6, QCoreApplication.translate("ljjisuan", u"\u70b9\u5728\u76f4\u7ebf\u7684\u6295\u5f71\u5750\u6807[\u53c2\u6570\uff1a\u70b9\u540d\u79f0,\u76f4\u7ebf\u540d\u79f0]", None))
        self.ljjisuan_fangfa.setItemText(7, QCoreApplication.translate("ljjisuan", u"\u5224\u65ad\u591a\u70b9\u662f\u5426\u5171\u9762[\u53c2\u6570\uff1a\u70b91\u540d\u79f0,\u70b92\u540d\u79f0,...,\u70b9n\u540d\u79f0]", None))
        self.ljjisuan_fangfa.setItemText(8, QCoreApplication.translate("ljjisuan", u"\u76f4\u7ebf\u65b9\u5411\u5411\u91cf[\u53c2\u6570\uff1a\u76f4\u7ebf\u540d\u79f0(\u6216\u76f4\u7ebf\u4e0a\u4e24\u70b9)]", None))
        self.ljjisuan_fangfa.setItemText(9, QCoreApplication.translate("ljjisuan", u"\u4e24\u76f4\u7ebf\u4ea4\u70b9[\u53c2\u6570\uff1a\u76f4\u7ebf1\u540d\u79f0(\u6216\u76f4\u7ebf\u4e0a\u4e24\u70b9),\u76f4\u7ebf2\u540d\u79f0(\u6216\u76f4\u7ebf\u4e0a\u4e24\u70b9)]", None))
        self.ljjisuan_fangfa.setItemText(10, QCoreApplication.translate("ljjisuan", u"\u4e24\u76f4\u7ebf\u5939\u89d2[\u53c2\u6570\uff1a\u76f4\u7ebf1\u540d\u79f0(\u6216\u76f4\u7ebf\u4e0a\u4e24\u70b9),\u76f4\u7ebf2\u540d\u79f0(\u6216\u76f4\u7ebf\u4e0a\u4e24\u70b9)]", None))
        self.ljjisuan_fangfa.setItemText(11, QCoreApplication.translate("ljjisuan", u"\u5224\u65ad\u4e24\u76f4\u7ebf\u662f\u5426\u5e73\u884c[\u53c2\u6570\uff1a\u76f4\u7ebf1\u540d\u79f0(\u6216\u76f4\u7ebf\u4e0a\u4e24\u70b9),\u76f4\u7ebf2\u540d\u79f0(\u6216\u76f4\u7ebf\u4e0a\u4e24\u70b9)]", None))
        self.ljjisuan_fangfa.setItemText(12, QCoreApplication.translate("ljjisuan", u"\u5224\u65ad\u4e24\u76f4\u7ebf\u662f\u5426\u5782\u76f4[\u53c2\u6570\uff1a\u76f4\u7ebf1\u540d\u79f0(\u6216\u76f4\u7ebf\u4e0a\u4e24\u70b9),\u76f4\u7ebf2\u540d\u79f0(\u6216\u76f4\u7ebf\u4e0a\u4e24\u70b9)]", None))
        self.ljjisuan_fangfa.setItemText(13, QCoreApplication.translate("ljjisuan", u"\u76f4\u7ebf\u5728\u5e73\u9762\u4e0a\u7684\u6295\u5f71[\u53c2\u6570\uff1a\u76f4\u7ebf\u540d\u79f0(\u6216\u76f4\u7ebf\u4e0a\u4e24\u70b9),\u5e73\u9762\u540d\u79f0]", None))
        self.ljjisuan_fangfa.setItemText(14, QCoreApplication.translate("ljjisuan", u"\u7ecf\u8fc7\u4e09\u70b9\u7684\u5e73\u9762\u65b9\u7a0b Ax+By+Cz+D=0[\u53c2\u6570\uff1a\u70b91\u540d\u79f0,\u70b92\u540d\u79f0,\u70b93\u540d\u79f0]", None))
        self.ljjisuan_fangfa.setItemText(15, QCoreApplication.translate("ljjisuan", u"\u5e73\u9762\u6cd5\u5411\u91cf[\u53c2\u6570\uff1a\u5e73\u9762\u540d\u79f0]", None))
        self.ljjisuan_fangfa.setItemText(16, QCoreApplication.translate("ljjisuan", u"\u4e24\u5e73\u9762\u5939\u89d2[\u53c2\u6570\uff1a\u5e73\u97621\u540d\u79f0,\u5e73\u97622\u540d\u79f0]", None))
        self.ljjisuan_fangfa.setItemText(17, QCoreApplication.translate("ljjisuan", u"\u4e24\u5e73\u9762\u4ea4\u7ebf[\u53c2\u6570\uff1a\u5e73\u97621\u540d\u79f0,\u5e73\u97622\u540d\u79f0]", None))
        self.ljjisuan_fangfa.setItemText(18, QCoreApplication.translate("ljjisuan", u"\u5224\u65ad\u4e24\u5e73\u9762\u662f\u5426\u5e73\u884c[\u53c2\u6570\uff1a\u5e73\u97621\u540d\u79f0,\u5e73\u97622\u540d\u79f0]", None))
        self.ljjisuan_fangfa.setItemText(19, QCoreApplication.translate("ljjisuan", u"\u5224\u65ad\u4e24\u5e73\u9762\u662f\u5426\u5782\u76f4[\u53c2\u6570\uff1a\u5e73\u97621\u540d\u79f0,\u5e73\u97622\u540d\u79f0]", None))
        self.ljjisuan_fangfa.setItemText(20, QCoreApplication.translate("ljjisuan", u"\u5e73\u9762\u4e0e\u76f4\u7ebf\u4ea4\u70b9[\u53c2\u6570\uff1a\u5e73\u9762\u540d\u79f0,\u76f4\u7ebf\u540d\u79f0]", None))
        self.ljjisuan_fangfa.setItemText(21, QCoreApplication.translate("ljjisuan", u"\u56db\u9762\u4f53\u4f53\u79ef[\u53c2\u6570\uff1a\u56db\u9876\u70b9\u540d\u79f0]", None))
        self.ljjisuan_fangfa.setItemText(22, QCoreApplication.translate("ljjisuan", u"\u76f4\u7ebf\u4e0e\u5e73\u9762\u7684\u5939\u89d2[\u53c2\u6570\uff1a\u76f4\u7ebf\u540d\u79f0,\u5e73\u9762\u540d\u79f0]", None))

        self.label_2.setText(QCoreApplication.translate("ljjisuan", u"\u53c2\u6570\u8f93\u5165(\u53c2\u6570\u4e4b\u95f4\u53ea\u7528\u9017\u53f7\u95f4\u9694)\uff1a", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("ljjisuan", u"\u8ba1\u7b97\u7ed3\u679c", None))
        self.ljjisuan_jisuan.setText(QCoreApplication.translate("ljjisuan", u"\u8ba1\u7b97", None))
    # retranslateUi

