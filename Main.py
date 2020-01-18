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
from PyQt5.QtGui import QImage
from threading import Thread

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
               img.save(name+"Bis.jpg", "JPG")
            elif ext == "gif":
                img.save(name + "Bis.gif", "GIF")
            elif ext == "png":
                img.save(name + "Bis.png", "PNG")


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
        for i in range(width):
            for j in range(height):
                rgb1 = img.pixel(i, j)
                color = QtGui.qRgb((QtGui.qRed(rgb1) + (self.horizontalSlider.value()))//2,(QtGui.qGreen(rgb1) + (self.horizontalSlider_2.value()))//2,
                                   (QtGui.qBlue(rgb1) + (self.horizontalSlider_3.value())) // 2)
                img.setPixel(i, j, color)
        self.label_4.setPixmap(QtGui.QPixmap(img).scaled(width, height))

    def ouvrir(self):
        global img, x, y, width, height, file_name, status
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
        self.label_6.setPixmap(QtGui.QPixmap("220px-Colors-i54-ring.png"))
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
        self.label_9.setPixmap(QtGui.QPixmap("retouche.png"))
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
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

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



class Ui_Reconnaissance(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtWidgets.QApplication.desktop().screenGeometry().width(),
                          QtWidgets.QApplication.desktop().screenGeometry().height() - 10)
        MainWindow.setStyleSheet("background-color:rgb(150,150,150)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 40, 581, 451))
        self.widget.setStyleSheet("background-color: rgb(255,255,255)")
        self.widget.setObjectName("widget")
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(670, 160, 251, 261))
        self.widget_2.setStyleSheet("background-color: rgb(255,255,255)")
        self.widget_2.setObjectName("widget_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(770, 120, 63, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(610, 260, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(750, 440, 101, 29))
        self.pushButton.setObjectName("pushButton")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 956, 25))
        self.menubar.setStyleSheet("background-color: rgb(255,255,255)")
        self.menubar.setObjectName("menubar")
        self.menuFichier = QtWidgets.QMenu(self.menubar)
        self.menuFichier.setObjectName("menuFichier")
        self.menuListe_Possibilit_es = QtWidgets.QMenu(self.menuFichier)
        self.menuListe_Possibilit_es.setObjectName("menuListe_Possibilit_es")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
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
        self.menuListe_Possibilit_es.addSeparator()
        self.menuListe_Possibilit_es.addAction(self.actionLapin)
        self.menuListe_Possibilit_es.addAction(self.actionChien)
        self.menuListe_Possibilit_es.addAction(self.actionOeil)
        self.menuListe_Possibilit_es.addAction(self.actionTour_Eiffel)
        self.menuListe_Possibilit_es.addAction(self.actionVisage)
        self.menuFichier.addAction(self.menuListe_Possibilit_es.menuAction())
        self.menuFichier.addAction(self.actionQuitter)
        self.menubar.addAction(self.menuFichier.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pix - Reconnaissance de dessin"))
        self.label.setText(_translate("MainWindow", "Réponse"))
        self.label_2.setText(_translate("MainWindow", " →"))
        self.pushButton.setText(_translate("MainWindow", "Je vois ..."))
        self.menuFichier.setTitle(_translate("MainWindow", "Fichier"))
        self.menuListe_Possibilit_es.setTitle(_translate("MainWindow", "Liste Possibilitées"))
        self.actionQuitter.setText(_translate("MainWindow", "Quitter"))
        self.actionLapin.setText(_translate("MainWindow", "Lapin"))
        self.actionChien.setText(_translate("MainWindow", "Chien"))
        self.actionOeil.setText(_translate("MainWindow", "Oeil"))
        self.actionTour_Eiffel.setText(_translate("MainWindow", "Tour Eiffel"))
        self.actionVisage.setText(_translate("MainWindow", "Visage"))


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
        self.label_2.setPixmap(QtGui.QPixmap("PixLogo.gif"))
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
        icon.addPixmap(QtGui.QPixmap("ReconnaissanceImage.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setIconSize(QtCore.QSize(300, 300))
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setStyleSheet("background-color:rgb(215,215,215)")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("paint.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon1)
        self.pushButton_3.setIconSize(QtCore.QSize(300, 300))
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setStyleSheet("background-color:rgb(215,215,215)")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("dessin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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

    def openPaint(self):
        print("pas fini")

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
