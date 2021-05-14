# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'asrInterface.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(380, 700)
        MainWindow.setWindowOpacity(0.8)
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 初始页面label
        self.initStyle = "QLabel{font-family:Calibri; font-size:15pt;color:rgb(240,248,255);}"

        self.helloLabel = QtWidgets.QLabel(self.centralwidget)
        self.helloLabel.setGeometry(QtCore.QRect(20, 220, 370, 51))
        self.helloLabel.setStyleSheet("QLabel{font-family:Calibri; font-size:15pt;color:rgb(132, 112, 255);}")
        self.helloLabel.setObjectName("helloLabel")
        self.helloLabel.setVisible(True)

        self.noteLabel = QtWidgets.QLabel(self.centralwidget)
        self.noteLabel.setGeometry(QtCore.QRect(50, 300, 381, 41))
        self.noteLabel.setStyleSheet("QLabel{font-family:Calibri; font-size:12pt;color:rgb(240, 248, 255);}")
        self.noteLabel.setObjectName("noteLabel")
        self.noteLabel.setVisible(True)

        # 唤醒页面label
        self.actLabel=QtWidgets.QLabel(self.centralwidget)
        self.actLabel.setGeometry(QtCore.QRect(30, 300, 370, 51))
        self.actLabel.setStyleSheet("QLabel{font-family:Calibri; font-size:15pt;color:rgb(240,248,255);}")
        self.actLabel.setObjectName("actLabel")
        self.actLabel.setAutoFillBackground(False)

        # 识别失败label
        self.failLabel=QtWidgets.QLabel(self.centralwidget)
        self.failLabel.setGeometry(QtCore.QRect(30, 300, 370, 51))
        self.failLabel.setStyleSheet("QLabel{font-family:Calibri; font-size:15pt;color:rgb(240,248,255);}")
        self.failLabel.setObjectName("failLabel")
        self.failLabel.setAutoFillBackground(False)

        # note页面的label
        self.funcStyle = "QLabel{font-family:Calibri;font-size=14;color:rgb(255,255,255);}"
        self.comStyle = "QLabel{font-family:Calibri;font-size=10;color:rgb(255,255,255);}"

        self.func1Label = QtWidgets.QLabel(self.centralwidget)
        self.func1Label.setGeometry(QtCore.QRect(40, 250, 381, 31))
        self.func1Label.setStyleSheet( "QLabel{font-family:Calibri;font-size:15pt;color:rgb(255, 106, 106);}")
        self.func1Label.setObjectName("func1Label")
        self.func1Label.setAutoFillBackground(False)

        self.com1Label = QtWidgets.QLabel(self.centralwidget)
        self.com1Label.setGeometry(QtCore.QRect(80, 290, 261, 31))
        self.com1Label.setStyleSheet("QLabel{font-family:Calibri;font-size:10pt;color:rgb(255, 240, 245);}")
        self.com1Label.setObjectName("com1Label")
        self.com1Label.setAutoFillBackground(False)

        self.reply1Label=QtWidgets.QLabel(self.centralwidget)
        self.reply1Label.setGeometry(QtCore.QRect(40, 250, 300, 31))
        self.reply1Label.setStyleSheet("QLabel{font-family:Calibri;font-size:15pt;color:rgb(193, 255, 193);}")
        self.reply1Label.setObjectName("reply1Label")
        self.reply1Label.setAutoFillBackground(False)

        self.func2Label = QtWidgets.QLabel(self.centralwidget)
        self.func2Label.setGeometry(QtCore.QRect(40, 340, 421, 31))
        self.func2Label.setStyleSheet("QLabel{font-family:Calibri;font-size:15pt;color:rgb(255, 106, 106);}")
        self.func2Label.setObjectName("func2Label")
        self.func2Label.setAutoFillBackground(False)

        self.com2Label = QtWidgets.QLabel(self.centralwidget)
        self.com2Label.setGeometry(QtCore.QRect(80, 380, 271, 31))
        self.com2Label.setStyleSheet("QLabel{font-family:Calibri;font-size:10pt;color:rgb(255, 240, 245);}")
        self.com2Label.setObjectName("com2Label")
        self.com2Label.setAutoFillBackground(False)

        self.reply2Label = QtWidgets.QLabel(self.centralwidget)
        self.reply2Label.setGeometry(QtCore.QRect(40, 250, 300, 31))
        self.reply2Label.setStyleSheet("QLabel{font-family:Calibri;font-size:15pt;color:rgb(193, 255, 193);}")
        self.reply2Label.setObjectName("reply2Label")
        self.reply2Label.setAutoFillBackground(False)

        self.func3Label = QtWidgets.QLabel(self.centralwidget)
        self.func3Label.setGeometry(QtCore.QRect(40, 430, 421, 31))
        self.func3Label.setStyleSheet("QLabel{font-family:Calibri;font-size:15pt;color:rgb(255, 106, 106);}")
        self.func3Label.setObjectName("func3Label")
        self.func3Label.setAutoFillBackground(False)

        self.com3Label = QtWidgets.QLabel(self.centralwidget)
        self.com3Label.setGeometry(QtCore.QRect(80, 480, 271, 31))
        self.com3Label.setStyleSheet("QLabel{font-family:Calibri;font-size:10pt;color:rgb(255, 240, 245);}")
        self.com3Label.setObjectName("com3Label")
        self.com3Label.setAutoFillBackground(False)

        self.reply3Label = QtWidgets.QLabel(self.centralwidget)
        self.reply3Label.setGeometry(QtCore.QRect(40, 250, 261, 31))
        self.reply3Label.setStyleSheet("QLabel{font-family:Calibri;font-size:15pt;color:rgb(193, 255, 193);}")
        self.reply3Label.setObjectName("reply3Label")
        self.reply3Label.setAutoFillBackground(False)

        self.ansLabel = QtWidgets.QLabel(self.centralwidget)
        self.ansLabel.setGeometry(QtCore.QRect(80, 300, 400, 300),)
        self.ansLabel.setStyleSheet("QLabel{font-family:Calibri;font-size:12pt;color:rgb(151, 255, 255);}")
        self.ansLabel.setObjectName("ansLabel")
        self.ansLabel.setAutoFillBackground(False)

        self.guessLabel = QtWidgets.QLabel(self.centralwidget)
        self.guessLabel.setGeometry(QtCore.QRect(30, 300, 370, 51))
        self.guessLabel.setStyleSheet("QLabel{font-family:Calibri;font-size:12pt;color:rgb(255,255,255);}")
        self.guessLabel.setObjectName("guessLabel")
        self.guessLabel.setAutoFillBackground(False)

        self.func1Label.setVisible(False)
        self.func2Label.setVisible(False)
        self.func3Label.setVisible(False)
        self.com1Label.setVisible(False)
        self.com2Label.setVisible(False)
        self.com3Label.setVisible(False)
        self.actLabel.setVisible(False)
        self.reply1Label.setVisible(False)
        self.reply2Label.setVisible(False)
        self.reply3Label.setVisible(False)
        self.failLabel.setVisible(False)
        self.ansLabel.setVisible(False)
        self.guessLabel.setVisible(False)

        # 动图
        self.voiceFig = QtWidgets.QLabel(self.centralwidget)
        self.voiceFig.setGeometry(QtCore.QRect(30, 10, 300, 220))
        self.voiceFig.setText("")
        self.gif = QMovie("../resource/icon/voice.gif")
        self.voiceFig.setMovie(self.gif)
        self.gif.start()
        self.voiceFig.setScaledContents(True)
        self.voiceFig.setObjectName("voiceFig")

        self.siriFig = QtWidgets.QLabel(self.centralwidget)
        self.siriFig.setGeometry(QtCore.QRect(30, 500, 300, 220))
        self.siriFig.setText("")
        self.gifs= QMovie("../resource/icon/siri.gif")
        self.siriFig.setMovie(self.gifs)
        self.gifs.start()
        self.siriFig.setScaledContents(True)
        self.siriFig.setObjectName("siriFig")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Kami"))

        self.helloLabel.setText(_translate("MainWindow", "'Kami' to Wake Me!"))
        self.noteLabel.setText(_translate("MainWindow", "Double Click to See More!"))

        self.func1Label.setText(_translate("MainWindow", "1.Enjoy Music by Saying"))
        self.com1Label.setText(_translate("MainWindow", "Play [Song Name]"))
        self.reply1Label.setText(_translate("MainWindow", "Playing "))

        self.func2Label.setText(_translate("MainWindow", "2.Check Weather by Saying"))
        self.com2Label.setText(_translate("MainWindow", "Weather"))
        self.reply2Label.setText(_translate("MainWindow","Weather of Shanghai:"))

        self.func3Label.setText(_translate("MainWindow", "3.Visit BiliBili"))
        self.com3Label.setText(_translate("MainWindow", "Visit Bilibili"))
        self.reply3Label.setText(_translate("MainWindow","Showing "))


        self.actLabel.setText(_translate("MainWindow", "What can I do for you?"))
        self.failLabel.setText(_translate("MainWindow", "Sorry, I can not hear you!"))
        self.guessLabel.setText(_translate("MainWindow","I guess you want to "))