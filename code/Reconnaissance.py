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
import ListePossibilite
from PIL import Image

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

class Canvas(QtWidgets.QLabel):

    def __init__(self,first,valuePen):
        super().__init__()
        if first:
            self.valuePen = valuePen
            self.setPixmap(QtGui.QPixmap("images/blanc1.png"))
            self.pen_color = QtGui.QColor('#000000')
        else :
            self.setPixmap(QtGui.QPixmap("images/blanc.png"))
            self.pen_color = QtGui.QColor('#FFFFFF')
        self.last_x, self.last_y = None, None
        self.pix = self.pixmap()
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

    def start(self):
        if (self.startV):
            return True
        else:
            return False

    def setStart(self,etat):
        self.startV = etat

    def setAuto(self, etat):
        self.auto = etat


class Ui_Reconnaissance(object):

    def timeout(self):
        if (self.canvas.start()):
            self.reconnaissanceT()
            self.canvas.setStart(False)

    def clear(self):
        global crayon
        crayon = "none"
        self.canvas.setPixmap(QtGui.QPixmap("images/blanc1.png"))
        self.canvas.pix = self.canvas.pixmap()
        self.canvas.setStart(False)

    def openImage(self, MainWindow):
        filename, _ = QFileDialog.getOpenFileName(MainWindow, 'Open Image File', r"<Default dir>",
                                                   "Image files (*.jpg *.jpeg *.gif *.png)")
        filen = ""
        keep = False
        for n in filename.split("/"):
            if keep:
                if not "jpg" in n and not "png" in n:
                    filen += n+"/"
                else :
                    filen += n
            if n == "PixGui":
                keep = True
        img = QImage(filen)
        img = img.scaled(550,550)
        img.save("monDessin.jpg", "JPG")
        self.canvas.setPixmap(QtGui.QPixmap(img))
        self.canvas.pix = self.canvas.pixmap()
        self.nonAuto()

    def openImageKeepColor(self, filename):
        img = Image.open(filename + '.jpg')
        data = np.array(img, dtype='uint8')
        image = np.zeros((28, 28))
        for i in range(0, 27):
            for j in range(0, 27):
                image[i][j] = data[i][j][0]
        return image

    def openImageInverseColor(self, filename):
        # 0 = blanc et 1 = noir en binary
        img = Image.open(filename + '.jpg')
        data = np.array(img, dtype='uint8')
        image = np.zeros((28, 28))
        for i in range(0, 27):
            for j in range(0, 27):
                if (data[i][j][0] > 120):
                    image[i][j] = 0
                else:
                    image[i][j] = 255
        return image

    def apprentissage(self):
        self.progress.setText("⚙")
        draw_classNumbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        file = open("draws", "r")
        draw_classDrawings = list()
        for ligne in file:
            draw_classDrawings.append(ligne.split("\n")[0])
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
        model = tf.keras.models.load_model("model")
        img = self.openImageInverseColor("monDessin")
        img /= 255
        img = img.reshape(-1, 28, 28, 1)
        prediction = model.predict(img)
        self.progress.setText("")
        self.label.setText(str(self.labels[np.argmax(prediction)]))
        image = "images/reponses/"+str(self.labels[np.argmax(prediction)])+".jpg"
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
        #TODO doubler le trait quand on enregistre
        img = QImage(self.canvas.pix)
        img = img.scaled(28,28)
        img.save("monDessin.jpg", "JPG")

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

    def annuler(self):
        #self.canvas.setPixmap(QtGui.QPixmap("../images/blanc1.png"))
        self.canvas.setPixmap(self.canvas.annuler())
        self.canvas.pix = self.canvas.pixmap()

    def revenir(self):
        self.canvas.setPixmap(self.canvas.revenir())
        self.canvas.pix = self.canvas.pixmap()

    def menu(self, MainWindow):
        # TODO show create an instance of menu here ?
        self.menu = QtWidgets.QMainWindow()
        self.ui = menu.Ui_MainWindow()
        self.ui.setupUi(self.menu)
        self.menu.show()
        MainWindow.close()

    def on_spinbox_change(self):
        valuePen = self.spinbox.value()
        self.canvas.setValuePen(valuePen)

    def auto(self):
        self.canvas.setAuto(True)
        self.pushButton_5.hide()

    def nonAuto(self):
        self.canvas.setAuto(False)
        self.pushButton_5.show()

    def listePoss(self):
        self.liste = QtWidgets.QMainWindow()
        self.ui = ListePossibilite.Ui_listePossibilite()
        self.ui.setupUi(self.liste)
        self.liste.show()

    def setupUi(self, MainWindow):
        global status, crayon
        minPen = 12
        maxPen = 50
        self.timer = QtCore.QTimer()
        status = True
        crayon = "black"
        MainWindow.setObjectName("MainWindow")
        self.height = QtWidgets.QApplication.desktop().screenGeometry().height() - 10
        self.width = QtWidgets.QApplication.desktop().screenGeometry().width()
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
        self.spinbox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinbox.setMinimumSize(1, 1)
        self.spinbox.setMaximum(maxPen)
        self.spinbox.setMinimum(minPen)
        self.spinbox.setGeometry(QtCore.QRect(450, 45, 87, 29))
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
        self.label_2.setGeometry(QtCore.QRect(540, 10, 41, 81))
        self.progress = QtWidgets.QLabel(self.centralwidget)
        self.progress.setGeometry(QtCore.QRect(925, 85, 100, 100))
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
        self.pushButton_4.setGeometry(QtCore.QRect(590, 40, 220, 29))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setIcon(QtGui.QIcon("images/learn.png"))
        self.pushButton_4.setIconSize(QtCore.QSize(100, 70))
        self.pushButton_4bis = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_4bis.setGeometry(QtCore.QRect(820, 40, 150, 29))
        self.pushButton_4bis.setObjectName("pushButton_4bis")
        self.pushButton_5 = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_5.setGeometry(QtCore.QRect(1000, 40, 87, 29))
        self.pushButton_5.setObjectName("pushButton_5")
        self.widget_4 = QtWidgets.QWidget(self.widget_2)
        self.widget_4.setGeometry(QtCore.QRect(945, 200, 7, 401))
        self.widget_4.setStyleSheet("background-color: rgb(69, 69, 69);")
        self.widget_4.setObjectName("widget_4")
        self.widget_6 = QtWidgets.QWidget(self.widget_2)
        self.widget_6.setGeometry(QtCore.QRect(20, 90, 960, 1))
        self.widget_6.setStyleSheet("background-color: rgb(69, 69, 69);")
        self.widget_6.setObjectName("widget_6")
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1540, 25))
        self.menubar.setStyleSheet("background-color: rgb(255,255,255)")
        self.menubar.setObjectName("menubar")
        self.menuFichier = QtWidgets.QMenu(self.menubar)
        self.menuFichier.setObjectName("menuFichier")
        self.menuListe_Possibilit_es = QtWidgets.QAction(MainWindow)
        self.menuListe_Possibilit_es.setObjectName("menuListe_Possibilit_es")
        self.menuEdition = QtWidgets.QMenu(self.menubar)
        self.menuEdition.setObjectName("menuEdition")
        self.menuParametre = QtWidgets.QMenu(self.menubar)
        self.menuParametre.setObjectName("menuParametre")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionAuto = QtWidgets.QAction(MainWindow)
        self.actionAuto.setObjectName("actionAuto")
        self.actionNonAuto = QtWidgets.QAction(MainWindow)
        self.actionNonAuto.setObjectName("actionNonAuto")
        self.actionQuitter = QtWidgets.QAction(MainWindow)
        self.actionQuitter.setObjectName("actionQuitter")
        self.actionClear = QtWidgets.QAction(MainWindow)
        self.actionClear.setObjectName("actionClear")
        self.actionAnnuler = QtWidgets.QAction(MainWindow)
        self.actionAnnuler.setObjectName("actionAnnuler")
        self.actionRevenir = QtWidgets.QAction(MainWindow)
        self.actionRevenir.setObjectName("actionRevenir")
        self.actionOuvrir = QtWidgets.QAction(MainWindow)
        self.actionOuvrir.setObjectName("actionOuvrir")
        self.actionMenu = QtWidgets.QAction(MainWindow)
        self.actionMenu.setObjectName("actionMenu")
        self.actionParam_tres = QtWidgets.QAction(MainWindow)
        self.actionParam_tres.setObjectName("actionParam_tres")
        self.menuFichier.addAction(self.actionOuvrir)
        self.menuFichier.addAction(self.actionMenu)
        self.menuFichier.addAction(self.actionSave)
        self.menuFichier.addAction(self.menuListe_Possibilit_es)
        self.menuFichier.addAction(self.actionQuitter)
        self.menuEdition.addAction(self.actionClear)
        self.menuEdition.addAction(self.actionAnnuler)
        self.menuEdition.addAction(self.actionRevenir)
        self.menuParametre.addAction(self.actionAuto)
        self.menuParametre.addAction(self.actionNonAuto)
        self.menubar.addAction(self.menuFichier.menuAction())
        self.menubar.addAction(self.menuEdition.menuAction())
        self.menubar.addAction(self.menuParametre.menuAction())

        self.actionSave.triggered.connect(self.save)
        self.actionOuvrir.triggered.connect(lambda: self.openImage(MainWindow))
        self.actionAuto.triggered.connect(self.auto)
        self.actionNonAuto.triggered.connect(self.nonAuto)
        self.actionMenu.triggered.connect(lambda: self.menu(MainWindow))
        self.pushButton_5.clicked.connect(self.reconnaissanceT)
        self.actionClear.triggered.connect(self.clear)
        self.actionAnnuler.triggered.connect(self.annuler)
        self.pushButton.clicked.connect(self.pen)
        self.pushButton_2.clicked.connect(self.gomme)
        self.pushButton_3.clicked.connect(self.clear)
        self.pushButton.clicked.connect(self.changePen)
        self.pushButton_2.clicked.connect(self.changePen)
        self.pushButton_3.clicked.connect(self.changePen)
        self.pushButton_4.clicked.connect(self.apprentissageT)
        self.pushButton_4bis.clicked.connect(self.listePoss)
        self.spinbox.valueChanged.connect(self.on_spinbox_change)
        self.menuListe_Possibilit_es.triggered.connect(self.listePoss)
        self.actionRevenir.triggered.connect(self.revenir)

        self.timer.timeout.connect(self.timeout)
        self.timer.start()
        self.timer.setInterval(1000)

        self.retranslateUi(MainWindow)

        self.canvas = Canvas(True,minPen)
        self.canvas.setStyleSheet("border: 2px solid #235342")
        w = QtWidgets.QWidget(self.centralwidget)
        l = QtWidgets.QVBoxLayout(self.centralwidget)
        w.setLayout(l)
        w.setGeometry(QtCore.QRect(155, 135, 550, 550))
        #w.setGeometry(QtCore.QRect(30, 120, 870, 600))
        l.addWidget(self.canvas)

        self.canvas2 = Canvas(False,12)
        self.w = QtWidgets.QWidget(self.centralwidget)
        self.canvas2.setStyleSheet("border: 2px solid #235342")
        l = QtWidgets.QVBoxLayout(self.centralwidget)
        self.w.setLayout(l)
        self.w.setGeometry(QtCore.QRect(1035, 190, 400, 400))
        l.addWidget(self.canvas2)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.actionClear.setShortcut("Ctrl+R")
        self.actionRevenir.setShortcut("Ctrl+Y")
        self.actionSave.setShortcut("Ctrl+S")
        self.actionOuvrir.setShortcut("Ctrl+O")
        self.actionQuitter.setShortcut("Ctrl+D")
        self.actionMenu.setShortcut("Ctrl+M")
        self.actionAuto.setShortcut("Ctrl+B")
        self.actionAnnuler.setShortcut("Ctrl+T")
        self.actionNonAuto.setShortcut("Ctrl+N")
        self.menuListe_Possibilit_es.setShortcut("Ctrl+P")

        self.pen()
        self.changePen()
        self.apprentissageT()
        self.pushButton_5.hide()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pix - Reconnaissance de dessin"))
        self.label.setText(_translate("MainWindow", ""))
        self.pushButton.setText(_translate("MainWindow", "→"))
        self.menuFichier.setTitle(_translate("MainWindow", "Fichier"))
        self.menuListe_Possibilit_es.setText(_translate("MainWindow", "Que puis-je dessiner ?"))
        self.menuEdition.setTitle(_translate("MainWindow", "Edition"))
        self.menuParametre.setTitle(_translate("MainWindow", "Paramètre"))
        self.actionQuitter.setText(_translate("MainWindow", "Quitter"))
        self.actionClear.setText(_translate("MainWindow", "Effacer"))
        self.actionAnnuler.setText(_translate("MainWindow", "Annuler"))
        self.actionRevenir.setText(_translate("MainWindow", "Revenir"))
        self.actionOuvrir.setText(_translate("MainWindow", "Ouvrir"))
        self.actionMenu.setText(_translate("MainWindow", "Menu Principal"))
        self.actionSave.setText(_translate("MainWindow", "Enregistrer image"))
        self.actionAuto.setText(_translate("MainWindow", "Mode Automatique"))
        self.actionNonAuto.setText(_translate("MainWindow", "Mode Button"))
        self.label.setText(_translate("MainWindow", ""))
        self.pushButton.setText(_translate("MainWindow", "🖉"))
        self.pushButton_2.setText(_translate("MainWindow", "🖉"))
        self.pushButton_3.setText(_translate("MainWindow", "🗑"))
        self.label_2.setText(_translate("MainWindow", "|"))
        self.pushButton_4.setText(_translate("MainWindow", "Apprendre !"))
        self.pushButton_4bis.setText(_translate("MainWindow", "Que puis-je dessiner ?"))
        self.pushButton_5.setText(_translate("MainWindow", "Chercher !"))


