# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dessin.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage, QPainter
import matplotlib.pyplot as plt
import numpy as np
import os
import time
import MainWindow as menu
from PIL import Image

COLORS = [
    '#000000', '#141923', '#414168', '#3a7fa7', '#35e3e3', '#8fd970', '#5ebb49',
    '#458352', '#dcd37b', '#fffee5', '#ffd035', '#cc9245', '#a15c3e', '#a42f3b',
    '#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#ffffff',
    ]

class QPaletteButton(QtWidgets.QPushButton):

    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QtCore.QSize(24,24))
        self.color = color
        self.setStyleSheet("background-color: %s;" % color)

class Canvas(QtWidgets.QLabel):

    def __init__(self,valuePen):
        super().__init__()
        self.valuePen = valuePen
        self.setPixmap(QtGui.QPixmap("images/blancDessin.png"))
        self.pen_color = QtGui.QColor('#000000')
        self.last_x, self.last_y = None, None
        self.pix = self.pixmap()
        self.sauvBack = self.pix
        self.startV = False
        self.auto = True
        self.sauv = self.pixmap().copy()
        self.firstMove = True

    def set_pen_color(self, c):
        self.pen_color = QtGui.QColor(c)

    def setValuePen(self,value):
        self.valuePen = value

    def mouseMoveEvent(self, e):
        if self.firstMove:
            self.sauv = self.pixmap().copy()
            self.firstMove = False
        if self.last_x is None: # First event.
            self.last_x = e.x()
            self.last_y = e.y()
            return # Ignore the first time.

        self.painter = QtGui.QPainter(self.pixmap())
        self.p = self.painter.pen()
        #p.setWidth(17)
        self.p.setWidth(self.valuePen)
        self.p.setColor(self.pen_color)
        self.painter.setPen(self.p)
        self.painter.drawLine(self.last_x, self.last_y+8, e.x(), e.y()+8)
        self.painter.end()
        self.update()

        # Update the origin for next time.
        self.last_x = e.x()
        self.last_y = e.y()

    def annuler(self):
        self.sauvBack = self.pixmap().copy()
        return self.sauv

    def revenir(self):
        self.sauv = self.pixmap().copy()
        return self.sauvBack


    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None
        if (self.auto):
            self.startV = True
        self.firstMove = True

class Ui_Dessin(object):

    def on_spinbox_change(self):
        valuePen = self.spinBox.value()
        self.canvas.setValuePen(valuePen)

    def clear(self):
        self.canvas.setPixmap(QtGui.QPixmap("images/blancDessin.png"))
        self.canvas.pix = self.canvas.pixmap()

    def menu(self, MainWindow):
        self.menu = QtWidgets.QMainWindow()
        self.ui = menu.Ui_MainWindow()
        self.ui.setupUi(self.menu)
        self.menu.show()
        MainWindow.close()

    def save(self,MainWindow):
        # TODO doubler le trait quand on enregistre
        img = QImage(self.canvas.pix)
        name = "draw.jpg"

        reply = QtWidgets.QMessageBox.question(MainWindow,
                                               'Sauvegarder',
                                               'Sauvegarder en tant que ' + name + ' ?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            img.save("mesImagesEnregistrees/" + name, "JPG")

    def ouvrir(self, MainWindow):
        global img, x, y, width, height, file_name, status, red, green, blue
        red = False
        green = False
        blue = False

        status = True
        file_name, _ = QFileDialog.getOpenFileName(MainWindow, 'Open Image File', r"<Default dir>",
                                                   "Image files (*.jpg *.jpeg *.gif *.png)")
        img = QImage(file_name)
        img = img.scaled(self.W, self.H)
        self.canvas.setPixmap(QtGui.QPixmap(img))
        self.canvas.pix = self.canvas.pixmap()

    def quitter(self):
        QtCore.QCoreApplication.instance().quit()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1540, 881)
        MainWindow.setStyleSheet("background-color:rgb(150,150,150)")
        minPen = 10
        maxPen = 50
        self.H = 710
        self.W = 1271
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(90, 110, 45, 29))
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setMaximum(maxPen)
        self.spinBox.setMinimum(minPen)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 110, 21, 21))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("images/pen.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.spinBox.raise_()
        self.label.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1540, 25))
        self.menubar.setStyleSheet("background-color: rgb(255,255,255)")
        self.menubar.setObjectName("menubar")
        self.menuFichier = QtWidgets.QMenu(self.menubar)
        self.menuFichier.setObjectName("menuFichier")
        self.menuEdition = QtWidgets.QMenu(self.menubar)
        self.menuEdition.setObjectName("menuEdition")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAnnuler = QtWidgets.QAction(MainWindow)
        self.actionAnnuler.setObjectName("actionAnnuler")
        self.actionRevenir = QtWidgets.QAction(MainWindow)
        self.actionRevenir.setObjectName("actionRevenir")
        self.actionOuvrir = QtWidgets.QAction(MainWindow)
        self.actionOuvrir.setObjectName("actionOuvrir")
        self.actionSauvegarder = QtWidgets.QAction(MainWindow)
        self.actionSauvegarder.setObjectName("actionSauvegarder")
        self.actionQuitter = QtWidgets.QAction(MainWindow)
        self.actionQuitter.setObjectName("actionQuitter")
        self.actionClear = QtWidgets.QAction(MainWindow)
        self.actionClear.setObjectName("actionClear")
        self.actionMenu = QtWidgets.QAction(MainWindow)
        self.actionMenu.setObjectName("actionMenu")
        self.menuFichier.addAction(self.actionOuvrir)
        self.menuFichier.addAction(self.actionSauvegarder)
        self.menuFichier.addAction(self.actionQuitter)
        self.menuFichier.addAction(self.actionMenu)

        self.menuEdition.addAction(self.actionAnnuler)
        self.menuEdition.addAction(self.actionClear)
        self.menuEdition.addSeparator()
        self.menuEdition.addAction(self.actionRevenir)
        self.menubar.addAction(self.menuFichier.menuAction())
        self.menubar.addAction(self.menuEdition.menuAction())

        self.actionClear.triggered.connect(self.clear)
        self.actionOuvrir.triggered.connect(lambda: self.ouvrir(MainWindow))
        self.actionSauvegarder.triggered.connect(lambda: self.save(MainWindow))
        self.actionMenu.triggered.connect(lambda: self.menu(MainWindow))
        self.actionQuitter.triggered.connect(self.quitter)
        self.actionAnnuler.triggered.connect(self.annuler)
        self.actionRevenir.triggered.connect(self.revenir)
        self.spinBox.valueChanged.connect(self.on_spinbox_change)
        self.retranslateUi(MainWindow)

        self.canvas = Canvas(minPen)
        self.canvas.setStyleSheet("border: 2px solid #235342")
        w = QtWidgets.QWidget(self.centralwidget)
        l = QtWidgets.QVBoxLayout(self.centralwidget)
        w.setLayout(l)
        w.setGeometry(QtCore.QRect(220, 30, 1271, 710))
        palette = QtWidgets.QHBoxLayout()
        self.add_palette_buttons(palette)
        l.addLayout(palette)
        l.addWidget(self.canvas)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.actionClear.setShortcut("Ctrl+R")
        self.actionRevenir.setShortcut("Ctrl+Y")
        self.actionSauvegarder.setShortcut("Ctrl+S")
        self.actionOuvrir.setShortcut("Ctrl+O")
        self.actionQuitter.setShortcut("Ctrl+D")
        self.actionMenu.setShortcut("Ctrl+M")
        self.actionAnnuler.setShortcut("Ctrl+T")

    def annuler(self):
        self.canvas.setPixmap(self.canvas.annuler())
        self.canvas.pix = self.canvas.pixmap()

    def revenir(self):
        self.canvas.setPixmap(self.canvas.revenir())
        self.canvas.pix = self.canvas.pixmap()
    def add_palette_buttons(self, layout):
        for c in COLORS:
            b = QPaletteButton(c)
            b.pressed.connect(lambda c=c: self.canvas.set_pen_color(c))
            layout.addWidget(b)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pix - Reconnaissance de dessin"))
        self.menuFichier.setTitle(_translate("MainWindow", "Fichier"))
        self.actionClear.setText(_translate("MainWindow", "Effacer"))
        self.menuEdition.setTitle(_translate("MainWindow", "Edition"))
        self.actionQuitter.setText(_translate("MainWindow", "Quitter"))
        self.actionAnnuler.setText(_translate("MainWindow", "Annuler"))
        self.actionRevenir.setText(_translate("MainWindow", "Revenir"))
        self.actionOuvrir.setText(_translate("MainWindow", "Ouvrir"))
        self.actionMenu.setText(_translate("MainWindow", "Menu"))
        self.actionSauvegarder.setText(_translate("MainWindow", "Sauvegarder"))
