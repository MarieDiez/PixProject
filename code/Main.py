# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!
#TODO : liste contenant les fonctions de transformation, si annuler eneleve la derniere modif -> supp de la liste et reapplique tous
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image, ImageTk #, ImageGrab
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage, QPainter
from threading import Thread
import tensorflow as tf
from sklearn.model_selection import train_test_split #pip install sklearn
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
import time

class Action(Thread):

    def __init__(self, fonction, status):
        Thread.__init__(self)
        self.fonction = fonction
        self.status = status

    def run(self):
        if self.status:
            self.fonction()
        else:
            reply = QtWidgets.QMessageBox.question(MainWindow,
                                                   'Attention',
                                                   'Sauvegarder avant de continuer')

class Ui_retoucheImage(QtWidgets.QWidget):

    def save(self):
        name, ext = file_name.split("/")[-1].split(".")
        reply = QtWidgets.QMessageBox.question(MainWindow,
                                     'Sauvegarder',
                                     'Sauvegarder en tant que '+name+"Bis."+ext+' ?',
                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                     QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            if ext == "jpg" or ext == "jpeg" :
               img.save("../mesImagesEnregistrees/"+name+"Bis.jpg", "JPG")
            elif ext == "gif":
                img.save("../mesImagesEnregistrees/"+name + "Bis.gif", "GIF")
            elif ext == "png":
                img.save("../mesImagesEnregistrees/"+name + "Bis.png", "PNG")


    def niveauDeGris(self):
        global imgPre
        imgPre = img.copy(0,0,img.width(),img.height())

        for i in range(img.width()):
            for j in range(img.height()):
                rgb = img.pixel(i, j)
                mean = (QtGui.qRed(rgb) + QtGui.qGreen(rgb) + QtGui.qBlue(rgb) ) // 3
                color = QtGui.qRgb(mean,mean,mean)
                img.setPixel(i, j, color)
        self.label_4.setPixmap(QtGui.QPixmap(img).scaled(width, height))

    def niveauDeGrisT(self):
        global status
        #TODO : attention si je fais 2 traitements en meme temps
        action = Action(self.niveauDeGris,status)
        action.start()
        status = True

    def negatif(self):
        global imgPre
        imgPre = img.copy(0,0,img.width(),img.height())
        for i in range(img.width()):
            for j in range(img.height()):
                rgb = img.pixel(i, j)
                color = QtGui.qRgb(255-QtGui.qRed(rgb), 255-QtGui.qGreen(rgb), 255-QtGui.qBlue(rgb))
                img.setPixel(i, j, color)
        self.label_4.setPixmap(QtGui.QPixmap(img).scaled(width, height))

    def negatifT(self):
        global status
        # TODO : attention si je fais 2 traitements en meme temps
        action = Action(self.negatif,status)
        action.start()
        status = True

    def photomaton(self):
        global imgPre
        imgPre = img.copy(0,0,img.width(),img.height())
        imgCopy = img.copy(0,0,img.width(),img.height())
        x = 0
        y = 0

        for h in range(height + 1):
            for w in range(width + 1):
                if w % 2 != 0 and h % 2 != 0:
                    rgb = imgCopy.pixel(w, h)
                    color = QtGui.qRgb(QtGui.qRed(rgb), QtGui.qGreen(rgb), QtGui.qBlue(rgb))
                    img.setPixel(x, y, color)
                    img.setPixel(x + width // 2, y, color)
                    img.setPixel(x, y + height // 2, color)
                    img.setPixel(x + width // 2, y + height // 2, color)
                    x += 1
                    if (w == width):
                        y += 1
                        x = 0

        self.label_4.setPixmap(QtGui.QPixmap(img).scaled(width, height))

    def photomatonT(self):
        global status
        #TODO : attention si je fais 2 traitements en meme temps
        action = Action(self.photomaton,status)
        action.start()
        status = True

    def mirroir(self):
        global imgPre
        imgPre = img.copy(0,0,img.width(),img.height())
        imgCopy = img.copy(0, 0, img.width(), img.height())

        for h in range(height + 1):
            for w in range((width // 2) + 1):
                rgb = imgCopy.pixel(w, h)
                color = QtGui.qRgb(QtGui.qRed(rgb), QtGui.qGreen(rgb), QtGui.qBlue(rgb))
                rgb1 = imgCopy.pixel(width - w, h)
                color1 = QtGui.qRgb(QtGui.qRed(rgb1), QtGui.qGreen(rgb1), QtGui.qBlue(rgb1))
                img.setPixel(width - w, h, color)
                img.setPixel(w, h, color1)
        self.label_4.setPixmap(QtGui.QPixmap(img).scaled(width, height))

    def mirroirT(self):
        global status
        #TODO : attention si je fais 2 traitements en meme temps
        action = Action(self.mirroir,status)
        action.start()
        status = True

    def rotation_180(self):
        global imgPre
        imgPre = img.copy(0,0,img.width(),img.height())
        imgCopy = img.copy(0, 0, img.width(), img.height())

        for h in range((height // 2) + 1):
            for w in range(width + 1):
                rgb = imgCopy.pixel(w, h)
                color = QtGui.qRgb(QtGui.qRed(rgb), QtGui.qGreen(rgb), QtGui.qBlue(rgb))
                rgb1 = imgCopy.pixel(w, height - h)
                color1 = QtGui.qRgb(QtGui.qRed(rgb1), QtGui.qGreen(rgb1), QtGui.qBlue(rgb1))
                img.setPixel(w, height - h, color)
                img.setPixel(w, h, color1)
        self.label_4.setPixmap(QtGui.QPixmap(img).scaled(width, height))

    def rotation_180T(self):
        global status
        #TODO : attention si je fais 2 traitements en meme temps
        action = Action(self.rotation_180,status)
        action.start()
        status = True

    def rotation_90(self):
        global imgPre
        imgPre = img.copy(0, 0, img.width(), img.height())
        self.horizontalSlider.hide()
        self.horizontalSlider_2.hide()
        self.horizontalSlider_3.hide()
        self.lcdNumber.hide()
        self.lcdNumber_2.hide()
        self.lcdNumber_3.hide()
        self.label_6.hide()
        self.rgb.hide()
        imgPre = img.copy(0, 0, img.width(), img.height())
        transform90 = QtGui.QTransform()
        transform90.rotate(90)
        self.label_2.setGeometry(QtCore.QRect(1000, 70, 181, 21))
        self.widget_2.setGeometry(QtCore.QRect(820, 100, 491, 661))
        self.label_4.resize(height, width)
        self.label_4.setPixmap(QtGui.QPixmap(img).transformed(transform90))

    def rotation_90T(self):
        global status
        #TODO : attention si je fais 2 traitements en meme temps
        action = Action(self.rotation_90, status)
        action.start()
        status = False

    def rotation_91(self):
        global imgPre
        imgPre = img.copy(0, 0, img.width(), img.height())
        self.horizontalSlider.hide()
        self.horizontalSlider_2.hide()
        self.horizontalSlider_3.hide()
        self.lcdNumber.hide()
        self.lcdNumber_2.hide()
        self.lcdNumber_3.hide()
        self.label_6.hide()
        self.rgb.hide()

        imgPre = img.copy(0, 0, img.width(), img.height())
        transform90 = QtGui.QTransform()
        transform90.rotate(-90)
        self.label_2.setGeometry(QtCore.QRect(1000, 70, 181, 21))
        self.widget_2.setGeometry(QtCore.QRect(820, 100, 491, 661))
        self.label_4.resize(height, width)
        self.label_4.setPixmap(QtGui.QPixmap(img).transformed(transform90))

    def rotation_91T(self):
        global status
        #TODO : attention si je fais 2 traitements en meme temps
        action = Action(self.rotation_91,status)
        action.start()
        status = False

    def slider(self):
        global red, green, blue, imgPre
        imgPre = img.copy(0, 0, img.width(), img.height())

        for i in range(width):
            for j in range(height):
                rgb1 = img.pixel(i, j)
                redColor = QtGui.qRed(rgb1)
                greenColor = QtGui.qGreen(rgb1)
                blueColor = QtGui.qBlue(rgb1)
                if red:
                    redColor = self.horizontalSlider.value()
                if green:
                    greenColor = self.horizontalSlider_2.value()
                if blue:
                    blueColor = self.horizontalSlider_3.value()

                color = QtGui.qRgb((QtGui.qRed(rgb1) + redColor)//2,(QtGui.qGreen(rgb1) + greenColor)//2,
                                   (QtGui.qBlue(rgb1) + blueColor)//2)
                img.setPixel(i, j, color)
        self.label_4.setPixmap(QtGui.QPixmap(img).scaled(width, height))
        red = False
        green = False
        blue = False

    def redChange(self):
        global red
        red = True
    def greenChange(self):
        global green
        green = True
    def blueChange(self):
        global blue
        blue = True

    def ouvrir(self):
        global img, x, y, width, height, file_name, status, red, green, blue
        red = False
        green = False
        blue = False

        status = True
        file_name, _ = QFileDialog.getOpenFileName(MainWindow, 'Open Image File', r"<Default dir>",
                                                "Image files (*.jpg *.jpeg *.gif *.png)")
        img = QImage(file_name)
        x = img.width()
        y = img.height()
        maxX = 641
        maxY = 471
        if (x > maxX or y > maxY):
            if (x > y):
                coeff = (maxX/x)
            else:
                coeff = (maxY)/y
            width = int(coeff*x)
            height = int(coeff*y)
            img = img.scaled(width, height)
            self.label_5.resize(width, height)
            self.label_4.resize(width, height)
            self.widget_3.setGeometry(QtCore.QRect(40, 150, width+20, height+20))
            self.widget_2.setGeometry(QtCore.QRect(830, 150, width+20, height+20))
        else:
            img = img.scaled(maxX, maxY)
            width = int(img.width())
            height = int(img.height())
            self.label_5.resize(width, height)
            self.label_4.resize(width, height)
            self.widget_3.setGeometry(QtCore.QRect(40, 150, width+20, height+20))
            self.widget_2.setGeometry(QtCore.QRect(830, 150, width+20, height+20))
        self.label_5.setPixmap(QtGui.QPixmap(img))
        self.label_4.clear()

        # reinitialisation
        self.label_2.setGeometry(QtCore.QRect(1130, 100, 181, 21))
        self.horizontalSlider.show()
        self.horizontalSlider_2.show()
        self.horizontalSlider_3.show()
        self.lcdNumber.show()
        self.lcdNumber_2.show()
        self.lcdNumber_3.show()
        self.label_6.show()
        self.rgb.show()

    def annuler(self):
        global  imgPre,img
        img = imgPre
        self.label_4.setPixmap(QtGui.QPixmap(img).scaled(width, height))

    def quitter(self):
        QtCore.QCoreApplication.instance().quit()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1611, 826)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(115,115, 115);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(830, 150, 661, 491))
        self.widget_2.setStyleSheet("background-color: rgb(0,0,0)")
        self.widget_2.setObjectName("widget_2")
        self.label_4 = QtWidgets.QLabel(self.widget_2)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 641, 471))
        self.label_4.setStyleSheet("background-color: rgb(255,255,255)")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(270, 110, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1130, 100, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.rgb = QtWidgets.QPushButton(self.centralwidget)
        self.rgb.setGeometry(QtCore.QRect(850, 690, 100, 29))
        self.rgb.setObjectName("rgb")

        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setGeometry(QtCore.QRect(40, 150, 661, 491))
        self.widget_3.setStyleSheet("background-color: rgb(0,0,0)")
        self.widget_3.setObjectName("widget_3")
        self.label_5 = QtWidgets.QLabel(self.widget_3)
        self.label_5.setGeometry(QtCore.QRect(10, 10, 641, 471))
        self.label_5.setStyleSheet("background-color: rgb(255,255,255)")
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(730, 350, 61, 61))
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(1110, 670, 160, 18))
        self.horizontalSlider.setStyleSheet("selection-background-color: rgb(255, 0, 0);")
        self.horizontalSlider.setMaximum(255)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider_2 = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_2.setGeometry(QtCore.QRect(1110, 700, 160, 18))
        self.horizontalSlider_2.setStyleSheet("selection-background-color: rgb(0, 255, 0);")
        self.horizontalSlider_2.setMaximum(255)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.horizontalSlider_3 = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_3.setGeometry(QtCore.QRect(1110, 730, 160, 18))
        self.horizontalSlider_3.setStyleSheet("selection-background-color: rgb(0, 0, 255);")
        self.horizontalSlider_3.setMaximum(255)
        self.horizontalSlider_3.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_3.setObjectName("horizontalSlider_3")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(1290, 670, 64, 23))
        self.lcdNumber.setObjectName("lcdNumber")
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_2.setGeometry(QtCore.QRect(1290, 700, 64, 23))
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        self.lcdNumber_3 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_3.setGeometry(QtCore.QRect(1290, 730, 64, 23))
        self.lcdNumber_3.setObjectName("lcdNumber_3")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(980, 650, 111, 111))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("../images/220px-Colors-i54-ring.png"))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(70, 50, 63, 20))
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(70, 90, 63, 20))
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(20, 10, 101, 91))
        self.label_9.setText("")
        self.label_9.setPixmap(QtGui.QPixmap("../images/retouche.png"))
        self.label_9.setObjectName("label_9")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1611, 25))
        self.menubar.setTabletTracking(False)
        self.menubar.setStyleSheet("background-color:rgb(255,255,255)")
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setStyleSheet("")
        self.menuFile.setObjectName("menuFile")
        self.menuTraitement = QtWidgets.QMenu(self.menubar)
        self.menuTraitement.setObjectName("menuTraitement")
        self.menuRetouche = QtWidgets.QMenu(self.menubar)
        self.menuRetouche.setObjectName("menuRetouche")
        self.menuEdition = QtWidgets.QMenu(self.menubar)
        self.menuEdition.setObjectName("menuEdition")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOuvrir = QtWidgets.QAction(MainWindow)
        self.actionOuvrir.setObjectName("actionOuvrir")
        self.actionEnregistrer_image = QtWidgets.QAction(MainWindow)
        self.actionEnregistrer_image.setObjectName("actionEnregistrer_image")
        self.actionQuitter = QtWidgets.QAction(MainWindow)
        self.actionQuitter.setObjectName("actionQuitter")
        self.actionRotation_180 = QtWidgets.QAction(MainWindow)
        self.actionRotation_180.setObjectName("actionRotation_180")
        self.actionRotation_90 = QtWidgets.QAction(MainWindow)
        self.actionRotation_90.setObjectName("actionRotation_90")
        self.actionRotation_91 = QtWidgets.QAction(MainWindow)
        self.actionRotation_91.setObjectName("actionRotation_91")
        self.actionNiveau_de_gris = QtWidgets.QAction(MainWindow)
        self.actionNiveau_de_gris.setObjectName("actionNiveau_de_gris")
        self.actionN_gatif = QtWidgets.QAction(MainWindow)
        self.actionN_gatif.setObjectName("actionN_gatif")
        self.actionPhotomaton = QtWidgets.QAction(MainWindow)
        self.actionPhotomaton.setObjectName("actionPhotomaton")
        self.actionPhotomaton_2 = QtWidgets.QAction(MainWindow)
        self.actionPhotomaton_2.setObjectName("actionPhotomaton_2")
        self.actionAnnuler = QtWidgets.QAction(MainWindow)
        self.actionAnnuler.setObjectName("actionAnnuler")
        self.actionMirroir = QtWidgets.QAction(MainWindow)
        self.actionMirroir.setObjectName("actionMirroir")
        self.menuFile.addAction(self.actionOuvrir)
        self.menuFile.addAction(self.actionEnregistrer_image)
        self.menuFile.addAction(self.actionQuitter)
        self.menuTraitement.addSeparator()
        self.menuTraitement.addAction(self.actionRotation_180)
        self.menuTraitement.addAction(self.actionMirroir)
        self.menuTraitement.addAction(self.actionRotation_90)
        self.menuTraitement.addAction(self.actionRotation_91)
        self.menuRetouche.addAction(self.actionNiveau_de_gris)
        self.menuRetouche.addAction(self.actionN_gatif)
        self.menuRetouche.addAction(self.actionPhotomaton)
        self.menuEdition.addAction(self.actionAnnuler)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdition.menuAction())
        self.menubar.addAction(self.menuTraitement.menuAction())
        self.menubar.addAction(self.menuRetouche.menuAction())

        self.retranslateUi(MainWindow)
        self.horizontalSlider.valueChanged['int'].connect(self.lcdNumber.display)
        self.horizontalSlider_2.valueChanged['int'].connect(self.lcdNumber_2.display)
        self.horizontalSlider_3.valueChanged['int'].connect(self.lcdNumber_3.display)
        self.horizontalSlider.valueChanged['int'].connect(self.redChange)
        self.horizontalSlider_2.valueChanged['int'].connect(self.greenChange)
        self.horizontalSlider_3.valueChanged['int'].connect(self.blueChange)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.actionOuvrir.setShortcut("Ctrl+O")
        self.actionEnregistrer_image.setShortcut("Ctrl+S")
        self.actionQuitter.setShortcut("Ctrl+D")
        self.actionAnnuler.setShortcut("Ctrl+Z")

        self.actionQuitter.triggered.connect(self.quitter)
        self.actionOuvrir.triggered.connect(self.ouvrir)
        self.actionNiveau_de_gris.triggered.connect(self.niveauDeGrisT)
        self.actionN_gatif.triggered.connect(self.negatifT)
        self.actionAnnuler.triggered.connect(self.annuler)
        self.actionEnregistrer_image.triggered.connect(self.save)
        self.actionPhotomaton.triggered.connect(self.photomatonT)
        self.actionMirroir.triggered.connect(self.mirroirT)
        self.actionRotation_180.triggered.connect(self.rotation_180T)
        self.actionRotation_90.triggered.connect(self.rotation_90T)
        self.actionRotation_91.triggered.connect(self.rotation_91T)
        self.rgb.clicked.connect(self.slider)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pix - Retouche d\'image"))
        self.label.setText(_translate("MainWindow", "Image normale"))
        self.label_2.setText(_translate("MainWindow", "Image retouchée"))
        self.label_3.setText(_translate("MainWindow", "→"))
        self.menuFile.setTitle(_translate("MainWindow", "Fichier"))
        self.menuTraitement.setTitle(_translate("MainWindow", "Traitement"))
        self.menuRetouche.setTitle(_translate("MainWindow", "Retouche"))
        self.menuEdition.setTitle(_translate("MainWindow", "Edition"))
        self.actionOuvrir.setText(_translate("MainWindow", "Ouvrir"))
        self.actionEnregistrer_image.setText(_translate("MainWindow", "Enregistrer image"))
        self.actionQuitter.setText(_translate("MainWindow", "Quitter"))
        self.actionRotation_180.setText(_translate("MainWindow", "Rotation 180°"))
        self.actionRotation_90.setText(_translate("MainWindow", "Rotation 90°"))
        self.actionRotation_91.setText(_translate("MainWindow", "Rotation -90°"))
        self.actionNiveau_de_gris.setText(_translate("MainWindow", "Niveau de gris"))
        self.actionN_gatif.setText(_translate("MainWindow", "Négatif"))
        self.actionPhotomaton.setText(_translate("MainWindow", "Photomaton"))
        self.actionPhotomaton_2.setText(_translate("MainWindow", "Photomaton +"))
        self.actionAnnuler.setText(_translate("MainWindow", "Annuler"))
        self.actionMirroir.setText(_translate("MainWindow", "Mirroir"))
        self.rgb.setText(_translate("MainWindow", "Valider RGB"))

class Canvas(QtWidgets.QLabel):

    def __init__(self,first):
        super().__init__()
        if first:
            self.setPixmap(QtGui.QPixmap("../images/blanc1.png"))
            self.pen_color = QtGui.QColor('#000000')
        else :
            self.setPixmap(QtGui.QPixmap("../images/blanc.png"))
            self.pen_color = QtGui.QColor('#FFFFFF')
        self.last_x, self.last_y = None, None
        self.pix = self.pixmap()

    def set_pen_color(self, c):
        self.pen_color = QtGui.QColor(c)

    def mouseMoveEvent(self, e):
        if self.last_x is None: # First event.
            self.last_x = e.x()
            self.last_y = e.y()
            return # Ignore the first time.

        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        #p.setWidth(17)
        p.setWidth(22)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        painter.end()
        self.update()

        # Update the origin for next time.
        self.last_x = e.x()
        self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None


class Ui_Reconnaissance(object):

    def clear(self):
        global crayon
        crayon = "none"
        self.canvas.setPixmap(QtGui.QPixmap("../images/blanc1.png"))
        self.canvas.pix = self.canvas.pixmap()

    def openImage(self, filename):
        img = Image.open(filename + '.jpg')
        data = np.array(img, dtype='uint8')
        image = np.zeros((28, 28))

        for i in range(0, 27):
            for j in range(0, 27):
                if (data[i][j][0] > 100):
                    image[i][j] = 0
                else:
                    image[i][j] = 255

        # plt.imshow(image,cmap="binary")
        return image

    def openImageKeepColor(self, filename):
        img = Image.open(filename + '.jpg')
        data = np.array(img, dtype='uint8')
        image = np.zeros((28, 28))
        for i in range(0, 27):
            for j in range(0, 27):
                image[i][j] = data[i][j][0]
        return image

    def openImageInverseColor(self,filename):
        # 0 = blanc et 1 = noir en binary
        img = Image.open(filename + '.jpg')
        data = np.array(img, dtype='uint8')
        image = np.zeros((28, 28))
        for i in range(0, 27):
            for j in range(0, 27):
                if (data[i][j][0] > 100):
                    image[i][j] = 0
                else:
                    image[i][j] = 255
        return image

    def apprentissage(self):
        self.progress.setText("⚙")
        draw_classNumbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        dataset_dir = "../quick_draw_dataset"  # Dossier
        files = [name for name in os.listdir(dataset_dir) if ".npy" in name]
        draw_classDrawings = []
        for name in files:
            # Open each dataset and add the new class
            draw_classDrawings.append(name.replace("full_numpy_bitmap_", "").replace(".npy", ""))

        self.labels = draw_classNumbers + draw_classDrawings
        self.progress.setText("")
        self.pushButton_4.setText("Chargé !")



    def apprentissageT(self):
        global status
        action = Action(self.apprentissage, status)
        action.start()
        status = True

    def reconnaissance(self):
        self.save()
        self.progress.setText("⚙")
        img = self.openImageInverseColor("../monDessin")
        img /= 255
        img = img.reshape(-1, 28, 28, 1)
        model = tf.keras.models.load_model("../model")
        prediction = model.predict(img)
        self.progress.setText("")
        self.label.setText(str(self.labels[np.argmax(prediction)]))
        image = "../images/reponses/"+str(self.labels[np.argmax(prediction)])+".jpg"
        pixmap = QtGui.QPixmap(image)

        if (pixmap.width() > pixmap.height()):
            ratio = pixmap.height() / pixmap.width()
            pixmap = pixmap.scaled(451, int(451 * ratio))
            h = self.height - pixmap.height()
            w = self.width - 900 - pixmap.width()
            self.w.setGeometry(QtCore.QRect(900 + w//2, h//2,451, int(451 * ratio)))
        else:
            ratio = pixmap.width() / pixmap.height()
            pixmap = pixmap.scaled(int(391*ratio), 391)
            h = self.height - pixmap.height()
            w = self.width - 900 - pixmap.width()
            self.w.setGeometry(QtCore.QRect(900 + w//2, h//2,int(391*ratio), 391))

        self.canvas2.setPixmap(pixmap)
        self.canvas2.pix = self.canvas2.pixmap()

    def reconnaissanceT(self):
        global status
        # TODO : attention si je fais 2 traitements en meme temps
        action = Action(self.reconnaissance, status)
        action.start()
        status = True

    def save(self):
        img = QImage(self.canvas.pix)
        img = img.scaled(28,28)
        img.save("../monDessin.jpg", "JPG")

    def gomme(self):
        global crayon
        crayon = "white"
        self.canvas.pen_color = QtGui.QColor('#FFFFFF')

    def pen(self):
        global crayon
        crayon = "black"
        self.canvas.pen_color = QtGui.QColor('#000000')

    def changePen(self):
        global crayon
        if (crayon == "white"):
            self.pushButton.setStyleSheet("border: 1px solid #333333;border-radius:5px; background-color:rgb(0,0,0); color:white; font-size: 20px;")
            self.pushButton_2.setStyleSheet("border: 2px solid #f7ff48;border-radius:5px; background-color:rgb(255,255,255); color:black; font-size: 20px;")
            self.pushButton_3.setStyleSheet("border: 1px solid #333333;border-radius:5px;")

        if (crayon == "black"):
            self.pushButton.setStyleSheet("border: 2px solid #f7ff48; border-radius:5px; background-color:rgb(0,0,0); color:white; font-size: 20px;")
            self.pushButton_2.setStyleSheet("border: 1px solid #333333;border-radius:5px; background-color:rgb(255,255,255); color:black; font-size: 20px;")
            self.pushButton_3.setStyleSheet("border: 1px solid #333333;border-radius:5px;")

        if (crayon == "none"):
            self.pushButton.setStyleSheet("border: 1px solid #333333; border-radius:5px;background-color:rgb(0,0,0); color:white; font-size: 20px;")
            self.pushButton_2.setStyleSheet("border: 1px solid #333333;border-radius:5px; background-color:rgb(255,255,255); color:black; font-size: 25px;")
            self.pushButton_3.setStyleSheet("border: 2px solid #333333;border-radius:5px;")
            self.pen()
            self.changePen()

    def setupUi(self, MainWindow):
        global status, crayon
        status = True
        crayon = "black"
        MainWindow.setObjectName("MainWindow")
        self.height = 800
        self.width = 1534
        MainWindow.resize(self.width, self.height)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1534, 740))
        self.widget.setStyleSheet("background-color: rgb(247, 255, 72);")
        self.widget.setObjectName("widget")
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setGeometry(QtCore.QRect(5, 5, 1524, 730))
        self.widget_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.widget_2.setObjectName("widget_2")
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setGeometry(QtCore.QRect(1150, 122, 300, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.widget_2)
        self.pushButton.setGeometry(QtCore.QRect(50, 40, 87, 29))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_2.setGeometry(QtCore.QRect(180, 40, 87, 29))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_3.setGeometry(QtCore.QRect(310, 40, 87, 29))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_2 = QtWidgets.QLabel(self.widget_2)
        self.label_2.setGeometry(QtCore.QRect(440, 10, 41, 81))
        self.progress = QtWidgets.QLabel(self.centralwidget)
        self.progress.setGeometry(QtCore.QRect(922, 30, 100, 100))
        self.progress.setFont(QtGui.QFont('SansSerif', 50))
        self.progress.setStyleSheet("color: rgb(120,120,120)")
        self.progress.setObjectName("progress")
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.pushButton_4 = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_4.setGeometry(QtCore.QRect(490, 40, 220, 29))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setIcon(QtGui.QIcon("../images/learn.png"))
        self.pushButton_4.setIconSize(QtCore.QSize(100, 70))
        self.pushButton_5 = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_5.setGeometry(QtCore.QRect(740, 40, 87, 29))
        self.pushButton_5.setObjectName("pushButton_5")
        self.widget_4 = QtWidgets.QWidget(self.widget_2)
        self.widget_4.setGeometry(QtCore.QRect(945, 200, 7, 401))
        self.widget_4.setStyleSheet("background-color: rgb(69, 69, 69);")
        self.widget_4.setObjectName("widget_4")
        self.widget_6 = QtWidgets.QWidget(self.widget_2)
        self.widget_6.setGeometry(QtCore.QRect(20, 90, 771, 1))
        self.widget_6.setStyleSheet("background-color: rgb(69, 69, 69);")
        self.widget_6.setObjectName("widget_6")
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1540, 25))
        self.menubar.setStyleSheet("background-color: rgb(255,255,255)")
        self.menubar.setObjectName("menubar")
        self.menuFichier = QtWidgets.QMenu(self.menubar)
        self.menuFichier.setObjectName("menuFichier")
        self.menuListe_Possibilit_es = QtWidgets.QMenu(self.menuFichier)
        self.menuListe_Possibilit_es.setObjectName("menuListe_Possibilit_es")
        self.menuEdition = QtWidgets.QMenu(self.menubar)
        self.menuEdition.setObjectName("menuEdition")
        self.menuApprentissage = QtWidgets.QMenu(self.menubar)
        self.menuApprentissage.setObjectName("menuApprentissage")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionQuitter = QtWidgets.QAction(MainWindow)
        self.actionQuitter.setObjectName("actionQuitter")
        self.actionLapin = QtWidgets.QAction(MainWindow)
        self.actionLapin.setObjectName("actionLapin")
        self.actionChien = QtWidgets.QAction(MainWindow)
        self.actionChien.setObjectName("actionChien")
        self.actionOeil = QtWidgets.QAction(MainWindow)
        self.actionOeil.setObjectName("actionOeil")
        self.actionTour_Eiffel = QtWidgets.QAction(MainWindow)
        self.actionTour_Eiffel.setObjectName("actionTour_Eiffel")
        self.actionVisage = QtWidgets.QAction(MainWindow)
        self.actionVisage.setObjectName("actionVisage")
        self.actionAunuler = QtWidgets.QAction(MainWindow)
        self.actionAunuler.setObjectName("actionAunuler")
        self.actionClear = QtWidgets.QAction(MainWindow)
        self.actionClear.setObjectName("actionClear")
        self.actionRevenir = QtWidgets.QAction(MainWindow)
        self.actionRevenir.setObjectName("actionRevenir")
        self.actionOuvrir = QtWidgets.QAction(MainWindow)
        self.actionOuvrir.setObjectName("actionOuvrir")
        self.actionLancer = QtWidgets.QAction(MainWindow)
        self.actionLancer.setObjectName("actionLancer")
        self.actionParam_tres = QtWidgets.QAction(MainWindow)
        self.actionParam_tres.setObjectName("actionParam_tres")
        self.menuListe_Possibilit_es.addSeparator()
        self.menuListe_Possibilit_es.addAction(self.actionLapin)
        self.menuListe_Possibilit_es.addAction(self.actionChien)
        self.menuListe_Possibilit_es.addAction(self.actionOeil)
        self.menuListe_Possibilit_es.addAction(self.actionTour_Eiffel)
        self.menuListe_Possibilit_es.addAction(self.actionVisage)
        self.menuFichier.addAction(self.menuListe_Possibilit_es.menuAction())
        self.menuFichier.addAction(self.actionOuvrir)
        self.menuFichier.addAction(self.actionSave)
        self.menuFichier.addAction(self.actionQuitter)
        self.menuEdition.addAction(self.actionAunuler)
        self.menuEdition.addAction(self.actionClear)
        self.menuEdition.addSeparator()
        self.menuEdition.addAction(self.actionRevenir)
        self.menuApprentissage.addAction(self.actionLancer)
        self.menuApprentissage.addAction(self.actionParam_tres)
        self.menubar.addAction(self.menuFichier.menuAction())
        self.menubar.addAction(self.menuEdition.menuAction())
        self.menubar.addAction(self.menuApprentissage.menuAction())

        self.actionClear.setShortcut("Ctrl+C")
        self.actionLancer.setShortcut("Ctrl+L")
        self.actionSave.setShortcut("Ctrl+S")
        self.actionQuitter.setShortcut("Ctrl+D")

        self.actionSave.triggered.connect(self.save)
        self.actionLancer.triggered.connect(self.apprentissageT)
        self.pushButton_5.clicked.connect(self.reconnaissanceT)
        self.actionClear.triggered.connect(self.clear)
        self.pushButton.clicked.connect(self.pen)
        self.pushButton_2.clicked.connect(self.gomme)
        self.pushButton_3.clicked.connect(self.clear)
        self.pushButton.clicked.connect(self.changePen)
        self.pushButton_2.clicked.connect(self.changePen)
        self.pushButton_3.clicked.connect(self.changePen)
        self.pushButton_4.clicked.connect(self.apprentissageT)

        self.retranslateUi(MainWindow)

        self.canvas = Canvas(True)
        self.canvas.setStyleSheet("border: 2px solid #235342")
        w = QtWidgets.QWidget(self.centralwidget)
        l = QtWidgets.QVBoxLayout(self.centralwidget)
        w.setLayout(l)
        w.setGeometry(QtCore.QRect(150, 160, 550, 550))
        l.addWidget(self.canvas)

        self.canvas2 = Canvas(False)
        self.w = QtWidgets.QWidget(self.centralwidget)
        self.canvas2.setStyleSheet("border: 2px solid #235342")
        l = QtWidgets.QVBoxLayout(self.centralwidget)
        self.w.setLayout(l)
        self.w.setGeometry(QtCore.QRect(1070, 237, 400, 400))
        l.addWidget(self.canvas2)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pen()
        self.changePen()
        self.apprentissageT()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pix - Reconnaissance de dessin"))
        self.label.setText(_translate("MainWindow", ""))
        self.pushButton.setText(_translate("MainWindow", "→"))
        self.menuFichier.setTitle(_translate("MainWindow", "Fichier"))
        self.menuListe_Possibilit_es.setTitle(_translate("MainWindow", "Liste Possibilitées"))
        self.menuEdition.setTitle(_translate("MainWindow", "Edition"))
        self.menuApprentissage.setTitle(_translate("MainWindow", "Apprentissage"))
        self.actionQuitter.setText(_translate("MainWindow", "Quitter"))
        self.actionLapin.setText(_translate("MainWindow", "Lapin"))
        self.actionChien.setText(_translate("MainWindow", "Chien"))
        self.actionOeil.setText(_translate("MainWindow", "Oeil"))
        self.actionTour_Eiffel.setText(_translate("MainWindow", "Tour Eiffel"))
        self.actionVisage.setText(_translate("MainWindow", "Visage"))
        self.actionAunuler.setText(_translate("MainWindow", "Aunuler"))
        self.actionClear.setText(_translate("MainWindow", "Effacer"))
        self.actionRevenir.setText(_translate("MainWindow", "Revenir"))
        self.actionOuvrir.setText(_translate("MainWindow", "Ouvrir"))
        self.actionLancer.setText(_translate("MainWindow", "Lancer"))
        self.actionParam_tres.setText(_translate("MainWindow", "Paramètres"))
        self.actionSave.setText(_translate("MainWindow", "Enregistrer image"))
        self.label.setText(_translate("MainWindow", ""))
        self.pushButton.setText(_translate("MainWindow", "🖉"))
        self.pushButton_2.setText(_translate("MainWindow", "🖉"))
        self.pushButton_3.setText(_translate("MainWindow", "🗑"))
        self.label_2.setText(_translate("MainWindow", "|"))
        self.pushButton_4.setText(_translate("MainWindow", "Apprendre !"))
        self.pushButton_5.setText(_translate("MainWindow", "Chercher !"))



class Ui_MainWindow(QtWidgets.QWidget):

    def setupUi(self):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtWidgets.QApplication.desktop().screenGeometry().width(), QtWidgets.QApplication.desktop().screenGeometry().height()- 10)
        MainWindow.setStyleSheet("background-color:rgb(170,170,170)\n"
"")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(100, 30, 63, 20))
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 121, 101))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("../images/PixLogo.gif"))
        self.label_2.setObjectName("label_2")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(150, 160, 1171, 611))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setStyleSheet("background-color:rgb(215,215,215)\n"
"")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../images/ReconnaissanceImage.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setIconSize(QtCore.QSize(300, 300))
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setStyleSheet("background-color:rgb(215,215,215)")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../images/paint.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon1)
        self.pushButton_3.setIconSize(QtCore.QSize(300, 300))
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setStyleSheet("background-color:rgb(215,215,215)")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../images/dessin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon2)
        self.pushButton.setIconSize(QtCore.QSize(300, 300))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(1330, 764, 71, 20))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1444, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton.clicked.connect(self.openReconnaissance)
        self.pushButton_2.clicked.connect(self.openRetouche)
        self.pushButton_3.clicked.connect(self.openPaint)


    def openRetouche(self):
        self.retoucheImage = QtWidgets.QMainWindow()
        self.ui2 = Ui_retoucheImage()
        self.ui2.setupUi(self.retoucheImage)
        self.retoucheImage.show()
        MainWindow.close()

    def openReconnaissance(self):
        self.reconnaissance = QtWidgets.QMainWindow()
        self.ui2 = Ui_Reconnaissance()
        self.ui2.setupUi(self.reconnaissance)
        self.reconnaissance.show()
        MainWindow.close()

    def openPaint(self):
        print("pas fini")
        MainWindow.close()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_2.setText(_translate("MainWindow", "Traitement d\'image"))
        self.pushButton_3.setText(_translate("MainWindow", "Paint"))
        self.pushButton.setText(_translate("MainWindow", "Reconnaissance de Dessin"))
        self.label_3.setText(_translate("MainWindow", "Marie Diez"))

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(MainWindow,
                                    'Quitter',
                                    'Voulez-vous vraiment quitter ?',
                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                    QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    global MainWindow
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi()
    MainWindow.show()
    sys.exit(app.exec_())
