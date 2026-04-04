# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainXMyOPG.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QTabWidget, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionshouye = QAction(MainWindow)
        self.actionshouye.setObjectName(u"actionshouye")
        self.actionqiudao = QAction(MainWindow)
        self.actionqiudao.setObjectName(u"actionqiudao")
        self.actionjifen = QAction(MainWindow)
        self.actionjifen.setObjectName(u"actionjifen")
        self.actionbianxing = QAction(MainWindow)
        self.actionbianxing.setObjectName(u"actionbianxing")
        self.actionfangcheng = QAction(MainWindow)
        self.actionfangcheng.setObjectName(u"actionfangcheng")
        self.actionfangchengzu = QAction(MainWindow)
        self.actionfangchengzu.setObjectName(u"actionfangchengzu")
        self.actionbudengshi = QAction(MainWindow)
        self.actionbudengshi.setObjectName(u"actionbudengshi")
        self.actionbudengshizu = QAction(MainWindow)
        self.actionbudengshizu.setObjectName(u"actionbudengshizu")
        self.actionhelp = QAction(MainWindow)
        self.actionhelp.setObjectName(u"actionhelp")
        self.actionguanyu = QAction(MainWindow)
        self.actionguanyu.setObjectName(u"actionguanyu")
        self.actionabout = QAction(MainWindow)
        self.actionabout.setObjectName(u"actionabout")
        self.actiongithub = QAction(MainWindow)
        self.actiongithub.setObjectName(u"actiongithub")
        self.actionwebsite = QAction(MainWindow)
        self.actionwebsite.setObjectName(u"actionwebsite")
        self.actiondingyi = QAction(MainWindow)
        self.actiondingyi.setObjectName(u"actiondingyi")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(-2, -1, 801, 581))
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 24))
        self.new_tab = QMenu(self.menubar)
        self.new_tab.setObjectName(u"new_tab")
        self.about = QMenu(self.menubar)
        self.about.setObjectName(u"about")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.new_tab.menuAction())
        self.menubar.addAction(self.about.menuAction())
        self.new_tab.addAction(self.actionshouye)
        self.new_tab.addAction(self.actiondingyi)
        self.new_tab.addAction(self.actionqiudao)
        self.new_tab.addAction(self.actionjifen)
        self.new_tab.addAction(self.actionbianxing)
        self.new_tab.addAction(self.actionfangcheng)
        self.new_tab.addAction(self.actionfangchengzu)
        self.new_tab.addAction(self.actionbudengshi)
        self.new_tab.addAction(self.actionbudengshizu)
        self.new_tab.addAction(self.actionhelp)
        self.about.addAction(self.actiongithub)
        self.about.addAction(self.actionwebsite)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"CalculusCalculator", None))
        self.actionshouye.setText(QCoreApplication.translate("MainWindow", u"\u9996\u9875", None))
        self.actionqiudao.setText(QCoreApplication.translate("MainWindow", u"\u6c42\u5bfc", None))
        self.actionjifen.setText(QCoreApplication.translate("MainWindow", u"\u79ef\u5206", None))
        self.actionbianxing.setText(QCoreApplication.translate("MainWindow", u"\u53d8\u5f62", None))
        self.actionfangcheng.setText(QCoreApplication.translate("MainWindow", u"\u65b9\u7a0b", None))
        self.actionfangchengzu.setText(QCoreApplication.translate("MainWindow", u"\u65b9\u7a0b\u7ec4", None))
        self.actionbudengshi.setText(QCoreApplication.translate("MainWindow", u"\u4e0d\u7b49\u5f0f", None))
        self.actionbudengshizu.setText(QCoreApplication.translate("MainWindow", u"\u4e0d\u7b49\u5f0f\u7ec4", None))
        self.actionhelp.setText(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9", None))
        self.actionguanyu.setText(QCoreApplication.translate("MainWindow", u"guanyu", None))
        self.actionabout.setText(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
        self.actiongithub.setText(QCoreApplication.translate("MainWindow", u"Github\u94fe\u63a5", None))
        self.actionwebsite.setText(QCoreApplication.translate("MainWindow", u"\u7f51\u9875\u7248", None))
        self.actiondingyi.setText(QCoreApplication.translate("MainWindow", u"\u5b9a\u4e49", None))
        self.new_tab.setTitle(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa", None))
        self.about.setTitle(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
    # retranslateUi

