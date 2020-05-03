# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import traceback, sys
from main import *

import socket

class Worker(QRunnable):
    def __init__(self, fn):
        super(Worker, self).__init__()
        self.fn = fn
        print ("New Worker")
        
    @pyqtSlot()
    def run(self):
        try:
            self.fn()
        except:
            print("issue running the worker function")
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
    
class Ui_Dialog():
    def __init__(self, Dialog):
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.dialog = Dialog
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.dialog)
        self.connections = []
        self.mode = True
        self.players = []
        self.clientSockets = []
        
    def setupUi(self, Dialog):
        self.dialog.setObjectName("Dialog")
        self.dialog.resize(250, 150)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 210, 110))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.pushButtonStart = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButtonStart.setObjectName("pushButtonStart")
        self.pushButtonStart.clicked.connect(self.start)
        
        self.pushButtonCancel = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.horizontalLayout.addWidget(self.pushButtonStart)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        
        self.textGameInfo = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        self.textGameInfo.setObjectName("textGameInfo")
        self.textGameInfo.setPlainText("textGameInfo")
        self.textGameInfo.setDisabled(True)
        
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.textGameInfo)
        
        self.pushButtonCancel.clicked.connect(self.closeWindow)
        
        self.retranslateUi(self.dialog)
        QtCore.QMetaObject.connectSlotsByName(self.dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButtonStart.setText(_translate("Dialog", "Start"))
        self.pushButtonCancel.setText(_translate("Dialog", "Cancel"))
    
    def openConnection(self):
        print ("Connecting")
        self.tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcpsock.bind(("",1111))
        self.tcpsock.listen()
        self.textGameInfo.setPlainText("Listening")
        # self.textGameInfo.setPlainText("Listening...")
        while len(self.connections) < 2:
            try:
                (clientsocket, (ip, port)) = self.tcpsock.accept()
            except:
                print("Lost connection with socket")
                return
            print(clientsocket)
            print(ip)
            print(port)
            connection = clientsocket.recv(255) 
            if connection != "" and not(port in self.connections):
                (player, mode) = self.parseConnection(connection)
                print (connection)
                self.mode = mode
                self.players.append(player)
                self.clientSockets.append(clientsocket)
                self.connections.append(port)

                if mode:
                    # if against computer, no need to listen to other connections
                    self.textGameInfo.setPlainText(player.__str__() + " wants to play against computer")
                    break
                else:
                    if len(self.connections) == 1:
                        self.textGameInfo.setPlainText(player.__str__() + " connected:\n Expect second player")
                        clientsocket.send((player.__str__() + " connected:\n Expect second player").encode("Utf8"))
                    if len(self.connections) == 2:
                        self.textGameInfo.setPlainText("Both players connected")
                        self.clientSockets[0].send(("You are playing against "+ self.players[1].__str__()+ "\n Make your choice").encode("Utf8"))
                        self.clientSockets[1].send(("You are playing against "+ self.players[0].__str__()+ "\n Make your choice").encode("Utf8"))
                        break;
                    
            
        if(self.mode):# against computer
            self.playAgainstComputer()
        else:
            self.playAgainstOpponent()
            
    def playAgainstComputer(self):
        noException = True
        while noException:
            try:
                choice = ""
                while(choice == ""):
                    choice = self.clientSockets[0].recv(255)
                print(choice)
                self.parseChoice(choice)
                winner = playWithComputerObject(self.players[0]) 
                
                if(winner == None):
                    self.textGameInfo.setPlainText("Draw")
                    self.clientSockets[0].send("Draw".encode("Utf8"))
                else:
                    self.textGameInfo.setPlainText(winner.__str__() + " wins")
                    self.clientSockets[0].send((winner.__str__() + " wins").encode("Utf8"))
            except:
                self.textGameInfo.setPlainText(self.players[0].__str__()+ " was disconnected")
                print(self.players[0].__str__()+ " was disconnected")
                noException = False
                self.tcpsock.close()
                # self.tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connections.clear()
                self.players.clear()
                self.clientSockets.clear()
                return
            
    def playAgainstOpponent(self):
        assert(len(self.players) == 2)
        worker_player0= Worker(lambda:self.listenToPlayer((0)))
        worker_player1 = Worker(lambda:self.listenToPlayer((1)))
        self.threadpool.start(worker_player0)
        self.threadpool.start(worker_player1)
        
    def listenToPlayer(self, clientIdx):
        noException = True
        while noException:
            try:
                choice = ""
                while(choice == ""):
                    choice = self.clientSockets[clientIdx].recv(255)
                print(choice)
                self.parseChoice(choice)
                if self.players[1-clientIdx].getChoiceValue() != 3:  
                    winner = determineWhoWins(self.players[clientIdx], self.players[1-clientIdx]) 
                    if(winner == None):
                        self.textGameInfo.setPlainText("Draw")
                        self.clientSockets[clientIdx].send("Draw".encode("Utf8"))
                        self.clientSockets[1-clientIdx].send("Draw".encode("Utf8"))
                        # self.tcpsock.sendall("Draw".encode("Utf8"))
                    else:
                        self.textGameInfo.setPlainText(winner.__str__() + " wins")
                        self.clientSockets[clientIdx].send((winner.__str__() + " wins").encode("Utf8"))
                        self.clientSockets[1-clientIdx].send((winner.__str__() + " wins").encode("Utf8"))
                    # Reset both choices
                    self.players[clientIdx].setChoice(3)
                    self.players[1-clientIdx].setChoice(3) 
                else:
                    self.clientSockets[clientIdx].send(("Expect " + self.players[1-clientIdx].__str__() + "'s choice").encode("Utf8"))
                    
            except:
                print("players were disconnected")
                noException = False
                self.tcpsock.close()
                # self.tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connections.clear()
                self.players.clear()
                self.clientSockets.clear()
            
    def parseConnection(self, connection):
        L = connection.decode(encoding="utf-8").split("@")
        player = Player(L[1])
        mode = L[0] == "True" # True is against computer, False is two players
        return (player, mode)
    
    def parseChoice(self, choice):
        L = choice.decode(encoding="utf-8").split("@")
        name = L[0]
        choice = L[1]
        for player in self.players:
            if player.name == name:
                player.setChoice(int(choice))
         
    def start(self):
        print ("Start")
        self.pushButtonStart.setText("Restart")
        self.threadpool.clear()
        worker = Worker(self.openConnection)
        self.threadpool.start(worker)
        print("Multithreading with maximum %d threads" % self.threadpool.activeThreadCount())
        
    def closeWindow(self):
        print ("Close")
        self.tcpsock.close()
        self.threadpool.clear()
        self.dialog.close()        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog(Dialog)
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
