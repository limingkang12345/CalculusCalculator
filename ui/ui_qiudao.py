# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qiudaoiRReQR.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
    QLineEdit, QPushButton, QSizePolicy, QWidget)

class Ui_qiudao(object):
    def setupUi(self, qiudao):
        if not qiudao.objectName():
            qiudao.setObjectName(u"qiudao")
        qiudao.resize(801, 551)
        self.gridLayout = QGridLayout(qiudao)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox1 = QGroupBox(qiudao)
        self.groupBox1.setObjectName(u"groupBox1")
        self.gridLayout_2 = QGridLayout(self.groupBox1)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.qiudao_input = QLineEdit(self.groupBox1)
        self.qiudao_input.setObjectName(u"qiudao_input")
        self.qiudao_input.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.qiudao_input, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox1, 0, 0, 1, 6)

        self.groupBox = QGroupBox(qiudao)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.qiudao_zibianliang = QLineEdit(self.groupBox)
        self.qiudao_zibianliang.setObjectName(u"qiudao_zibianliang")
        self.qiudao_zibianliang.setClearButtonEnabled(True)

        self.gridLayout_3.addWidget(self.qiudao_zibianliang, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)

        self.groupBox_4 = QGroupBox(qiudao)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_4 = QGridLayout(self.groupBox_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.qiudao_yinbianliang = QLineEdit(self.groupBox_4)
        self.qiudao_yinbianliang.setObjectName(u"qiudao_yinbianliang")
        self.qiudao_yinbianliang.setEnabled(False)
        self.qiudao_yinbianliang.setClearButtonEnabled(True)

        self.gridLayout_4.addWidget(self.qiudao_yinbianliang, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_4, 1, 1, 1, 1)

        self.groupBox_3 = QGroupBox(qiudao)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_5 = QGridLayout(self.groupBox_3)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.qiudao_qiudaocishu = QLineEdit(self.groupBox_3)
        self.qiudao_qiudaocishu.setObjectName(u"qiudao_qiudaocishu")
        self.qiudao_qiudaocishu.setClearButtonEnabled(True)

        self.gridLayout_5.addWidget(self.qiudao_qiudaocishu, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_3, 1, 2, 1, 1)

        self.groupBox_6 = QGroupBox(qiudao)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.gridLayout_6 = QGridLayout(self.groupBox_6)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.qiudao_zibianliangzhi = QLineEdit(self.groupBox_6)
        self.qiudao_zibianliangzhi.setObjectName(u"qiudao_zibianliangzhi")
        self.qiudao_zibianliangzhi.setEnabled(False)
        self.qiudao_zibianliangzhi.setClearButtonEnabled(True)

        self.gridLayout_6.addWidget(self.qiudao_zibianliangzhi, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_6, 1, 3, 1, 1)

        self.qiudao_yinhanshu = QCheckBox(qiudao)
        self.qiudao_yinhanshu.setObjectName(u"qiudao_yinhanshu")

        self.gridLayout.addWidget(self.qiudao_yinhanshu, 1, 4, 1, 1)

        self.qiudao_qiuchujutizhi = QCheckBox(qiudao)
        self.qiudao_qiuchujutizhi.setObjectName(u"qiudao_qiuchujutizhi")

        self.gridLayout.addWidget(self.qiudao_qiuchujutizhi, 1, 5, 1, 1)

        self.groupBox2 = QGroupBox(qiudao)
        self.groupBox2.setObjectName(u"groupBox2")
        self.gridLayout_7 = QGridLayout(self.groupBox2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.qiudao_yuanhanshu = QWebEngineView(self.groupBox2)
        self.qiudao_yuanhanshu.setObjectName(u"qiudao_yuanhanshu")
        self.qiudao_yuanhanshu.setUrl(QUrl(u"about:blank"))

        self.gridLayout_7.addWidget(self.qiudao_yuanhanshu, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox2, 2, 0, 1, 6)

        self.groupBox3 = QGroupBox(qiudao)
        self.groupBox3.setObjectName(u"groupBox3")
        self.gridLayout_8 = QGridLayout(self.groupBox3)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.qiudao_daohanshu = QWebEngineView(self.groupBox3)
        self.qiudao_daohanshu.setObjectName(u"qiudao_daohanshu")
        self.qiudao_daohanshu.setUrl(QUrl(u"about:blank"))

        self.gridLayout_8.addWidget(self.qiudao_daohanshu, 0, 0, 1, 1)

        self.qiudao_daohanshu_lineedit = QLineEdit(self.groupBox3)
        self.qiudao_daohanshu_lineedit.setObjectName(u"qiudao_daohanshu_lineedit")

        self.gridLayout_8.addWidget(self.qiudao_daohanshu_lineedit, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox3, 3, 0, 1, 6)

        self.groupBox_5 = QGroupBox(qiudao)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.gridLayout_9 = QGridLayout(self.groupBox_5)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.qiudao_daoshuzhi = QWebEngineView(self.groupBox_5)
        self.qiudao_daoshuzhi.setObjectName(u"qiudao_daoshuzhi")
        self.qiudao_daoshuzhi.setUrl(QUrl(u"about:blank"))

        self.gridLayout_9.addWidget(self.qiudao_daoshuzhi, 0, 0, 1, 1)

        self.qiudao_daoshuzhi_lineedit = QLineEdit(self.groupBox_5)
        self.qiudao_daoshuzhi_lineedit.setObjectName(u"qiudao_daoshuzhi_lineedit")

        self.gridLayout_9.addWidget(self.qiudao_daoshuzhi_lineedit, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_5, 4, 0, 1, 6)

        self.qiudao_qiudao_button = QPushButton(qiudao)
        self.qiudao_qiudao_button.setObjectName(u"qiudao_qiudao_button")

        self.gridLayout.addWidget(self.qiudao_qiudao_button, 5, 0, 1, 6)

        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(2, 4)
        self.gridLayout.setRowStretch(3, 5)
        self.gridLayout.setRowStretch(4, 5)

        self.retranslateUi(qiudao)

        QMetaObject.connectSlotsByName(qiudao)
    # setupUi

    def retranslateUi(self, qiudao):
        qiudao.setWindowTitle(QCoreApplication.translate("qiudao", u"Form", None))
        self.groupBox1.setTitle(QCoreApplication.translate("qiudao", u"\u8f93\u5165\u8868\u8fbe\u5f0f", None))
        self.groupBox.setTitle(QCoreApplication.translate("qiudao", u"\u81ea\u53d8\u91cf", None))
        self.qiudao_zibianliang.setText(QCoreApplication.translate("qiudao", u"x", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("qiudao", u"\u56e0\u53d8\u91cf(\u4ec5\u9690\u51fd\u6570)", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("qiudao", u"\u6c42\u5bfc\u6b21\u6570", None))
        self.qiudao_qiudaocishu.setText(QCoreApplication.translate("qiudao", u"1", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("qiudao", u"\u81ea\u53d8\u91cf\u503c", None))
        self.qiudao_yinhanshu.setText(QCoreApplication.translate("qiudao", u"\u9690\u51fd\u6570", None))
        self.qiudao_qiuchujutizhi.setText(QCoreApplication.translate("qiudao", u"\u6c42\u51fa\u5177\u4f53\u503c", None))
        self.groupBox2.setTitle(QCoreApplication.translate("qiudao", u"\u539f\u51fd\u6570", None))
        self.groupBox3.setTitle(QCoreApplication.translate("qiudao", u"\u5bfc\u51fd\u6570", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("qiudao", u"\u5bfc\u6570\u503c", None))
        self.qiudao_qiudao_button.setText(QCoreApplication.translate("qiudao", u"\u6c42\u5bfc", None))
    # retranslateUi

