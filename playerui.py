# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'player.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import socket

class Ui_MainWindow(object):
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    score = 0
    opponentScore = 0
    rounds = 0
    name = ""
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(300, 250)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 270, 200))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEditPlayer = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        self.textEditPlayer.setObjectName("textEditPlayer")
        self.verticalLayout.addWidget(self.textEditPlayer)
        self.pushButtonRock = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButtonRock.setObjectName("pushButtonRock")
        self.verticalLayout.addWidget(self.pushButtonRock)
        self.pushButtonPaper = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButtonPaper.setObjectName("pushButtonPaper")
        self.verticalLayout.addWidget(self.pushButtonPaper)
        self.pushButtonScissors = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButtonScissors.setObjectName("pushButtonScissors")
        self.verticalLayout.addWidget(self.pushButtonScissors)
        self.horizontalLayout.addLayout(self.verticalLayout)
        
        self.verticalLayout2 = QtWidgets.QVBoxLayout()
        self.verticalLayout2.setObjectName("verticalLayout2")
        self.textGameInteraction = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        self.textGameInteraction.setObjectName("textGameInteraction")
        self.textGameInteraction.setEnabled(False)
        self.textGameInteraction.setPlainText("Welcome to Rock Paper Scissors")
        self.verticalLayout2.addWidget(self.textGameInteraction)
        self.pushButtonConnect = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButtonConnect.setObjectName("pushButtonConnect")
        self.verticalLayout2.addWidget(self.pushButtonConnect)
        self.pushButtonRestart = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButtonRestart.setObjectName("pushButtonRestart")
        self.verticalLayout2.addWidget(self.pushButtonRestart)
        self.pushButtonConnect.clicked.connect(self.connect)
        self.pushButtonRestart.clicked.connect(self.restart)
        self.horizontalLayout.addLayout(self.verticalLayout2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 219, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.pushButtonRock.clicked.connect(lambda: self.choice(0))
        self.pushButtonPaper.clicked.connect(lambda: self.choice(1))
        self.pushButtonScissors.clicked.connect(lambda: self.choice(2))

        self.horizentalLayoutGameMode = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.radioButtonAgainstComputer = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.radioButtonTwoPlayer = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.horizentalLayoutGameMode.addWidget(self.radioButtonAgainstComputer)
        self.horizentalLayoutGameMode.addWidget(self.radioButtonTwoPlayer)
        self.verticalLayout2.addLayout(self.horizentalLayoutGameMode)
        self.restart()

        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textEditPlayer.setPlaceholderText(_translate("MainWindow", "Player name"))
        self.pushButtonRock.setText(_translate("MainWindow", "Rock"))
        self.pushButtonPaper.setText(_translate("MainWindow", "Paper"))
        self.pushButtonScissors.setText(_translate("MainWindow", "Scissors"))
        self.pushButtonConnect.setText(_translate("MainWindow", "Connect"))
        self.pushButtonRestart.setText(_translate("MainWindow", "Restart"))
        self.radioButtonAgainstComputer.setText("1")
        self.radioButtonTwoPlayer.setText("2")

    def connect(self):
        if(len(self.textEditPlayer.toPlainText()) != 0):
            hote = "localhost"
            port = 1111
            self.name = self.textEditPlayer.toPlainText()
            playerInformation = str(self.radioButtonAgainstComputer.isChecked())+"@"+self.name
            try:
                self.socket.connect((hote, port))
                self.socket.send(playerInformation.encode("Utf8"))
                self.pushButtonRock.setDisabled(False)
                self.pushButtonPaper.setDisabled(False)
                self.pushButtonScissors.setDisabled(False)
                if self.radioButtonAgainstComputer.isChecked():
                    self.textGameInteraction.setPlainText("Connected: play against Computer")
                else:
                    serverResponse = ""
                    while serverResponse == "":
                        serverResponse = self.socket.recv(255)
                    self.textGameInteraction.setPlainText(serverResponse.decode(encoding="utf-8")+"\n")
                    
            except:
                self.textGameInteraction.setPlainText("Unable to connect to server")
                
            
    
    def choice(self, playerChoice):
        name = self.textEditPlayer.toPlainText()
        choiceStr = name + '@' + str(playerChoice)
        try:          
            self.socket.send(choiceStr.encode("Utf8"))
            # Disable the name/game mode editing
            self.radioButtonTwoPlayer.setDisabled(True)
            self.radioButtonAgainstComputer.setDisabled(True)
            self.textEditPlayer.setDisabled(True)
        except:
            print("unable to send choice, try again")
         
        self.handleDecision()
        
        
    def handleDecision(self):
        decision = self.socket.recv(255).decode(encoding="utf-8")
        if self.radioButtonAgainstComputer.isChecked():
            while not(self.isRelevent(decision)):
                decision = self.socket.recv(255).decode(encoding="utf-8")
            self.rounds += 1
            if decision != "Draw":
                if self.name in decision:
                    self.score += 1
                else:
                    self.opponentScore += 1
            self.textGameInteraction.clear()     
            self.textGameInteraction.setPlainText(decision + "\nscore: "+str(self.score) + " against " + str(self.opponentScore)+"\n"+"Number of rounds: "+ str(self.rounds))
            return
        if self.radioButtonTwoPlayer.isChecked():
            while not(self.isRelevent(decision)):
                print(decision)
                decision = self.socket.recv(255).decode(encoding="utf-8")
            self.rounds += 1
            if decision != "Draw":
                if self.name in decision:
                    self.score += 1
                else:
                    self.opponentScore += 1
            self.textGameInteraction.clear()     
            self.textGameInteraction.setPlainText(decision + "\nscore: "+str(self.score) + " against " + str(self.opponentScore)+"\n"+"Number of rounds: "+ str(self.rounds))
             
    
    def isRelevent(self,decision):
        return "Draw" in decision or "wins" in decision
    
    def restart(self):
        self.textEditPlayer.setDisabled(False)
        self.textEditPlayer.clear()

        self.pushButtonRock.setDisabled(True)
        self.pushButtonPaper.setDisabled(True)
        self.pushButtonScissors.setDisabled(True)
        
        self.radioButtonTwoPlayer.setCheckable(True)
        self.radioButtonAgainstComputer.setCheckable(True)
        self.radioButtonAgainstComputer.setChecked(True)
        
        self.socket.close()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.textGameInteraction.setPlainText("Welcome to Rock Paper Scissors")
        self.score = 0
        self.opponentScore = 0
        self.rounds = 0        
        
        
        
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
