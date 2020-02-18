# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import Traitement as traitement
import Reconnaissance as reconnaissance


class Ui_MainWindow(object):

    def traitement(self,MainWindow):
        self.traitementImage = QtWidgets.QMainWindow()
        self.ui = traitement.Ui_traitementImage()
        self.ui.setupUi(self.traitementImage)
        self.traitementImage.show()
        MainWindow.close()

    def reconnaissance(self,MainWindow):
        self.reconnaissanceImage = QtWidgets.QMainWindow()
        self.ui = reconnaissance.Ui_Reconnaissance()
        self.ui.setupUi(self.reconnaissanceImage)
        self.reconnaissanceImage.show()
        MainWindow.close()

    def paint(self):
        print("Pour bientôt !")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Pix")
        MainWindow.resize(QtWidgets.QApplication.desktop().screenGeometry().width(),
                          QtWidgets.QApplication.desktop().screenGeometry().height() - 10)
        MainWindow.setStyleSheet("background-color: rgb(163, 163, 163);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 10, 1505, 801))
        self.widget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.widget.setObjectName("widget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.widget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(210, 600, 1121, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton_3 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(40, 220, 491, 341))
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("../images/traitement.jpg"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(570, 220, 491, 341))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("../images/art.jpg"))
        self.label_3.setScaledContents(False)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(1090, 220, 331, 341))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("../images/dessin.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setGeometry(QtCore.QRect(680, 80, 131, 71))
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        font.setPointSize(48)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(1320, 710, 161, 41))
        font = QtGui.QFont()
        font.setFamily("MathJax_Caligraphic")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1495, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.exitAct = QtWidgets.QPushButton(self.centralwidget) #Keybind
        self.exitAct.setGeometry(0,0,0,0)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(lambda: self.traitement(MainWindow))
        self.pushButton_2.clicked.connect(lambda: self.reconnaissance(MainWindow))
        self.pushButton_3.clicked.connect(self.paint)
        self.exitAct.clicked.connect(QtWidgets.QApplication.exit)

        self.exitAct.setShortcut("Ctrl+X")
        self.pushButton.setShortcut("Ctrl+T")
        self.pushButton_2.setShortcut("Ctrl+D")
        self.pushButton_3.setShortcut("Ctrl+P")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Traitement d\'image"))
        self.pushButton_3.setText(_translate("MainWindow", "Paint"))
        self.pushButton_2.setText(_translate("MainWindow", "Reconnaissance de Dessin"))
        self.label_5.setText(_translate("MainWindow", "Pix"))
        self.label.setText(_translate("MainWindow", "Marie Diez"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
