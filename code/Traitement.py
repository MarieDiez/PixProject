from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage, QPainter
from threading import Thread
import tensorflow as tf
from sklearn.model_selection import train_test_split #pip install sklearn
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import os
import time
import MainWindow as menu

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

class Ui_traitementImage(QtWidgets.QWidget):

    def menu(self, MainWindow):
        self.menu = QtWidgets.QMainWindow()
        self.ui = menu.Ui_MainWindow()
        self.ui.setupUi(self.menu)
        self.menu.show()
        MainWindow.close()

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

    def ouvrir(self, MainWindow):
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
        self.actionMenu = QtWidgets.QAction(MainWindow)
        self.actionMenu.setObjectName("actionMenu")
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
        self.menuFile.addAction(self.actionMenu)
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
        self.actionMenu.setShortcut("Ctrl+M")

        self.actionQuitter.triggered.connect(self.quitter)
        self.actionOuvrir.triggered.connect(lambda: self.ouvrir(MainWindow))
        self.actionMenu.triggered.connect(lambda: self.menu(MainWindow))
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
        self.actionMenu.setText(_translate("MainWindow", "Menu Principal"))
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