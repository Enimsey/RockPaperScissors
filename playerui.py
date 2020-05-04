from PyQt5 import QtCore, QtGui, QtWidgets
from socket import *
from main import POSSIBLE_CHOICES, POSSIBLE_CHOICES_LABELS
from functools import partial
import time


def is_relevant(decision):
    # Tests if a string received from the server is a relevant decision
    return "Draw" in decision or "wins" in decision


class Player_UI(object):
    socket = socket(AF_INET, SOCK_STREAM)
    socket.settimeout(3)
    score = 0
    opponent_score = 0
    rounds = 0
    name = ""
    buttons = {}

    def setup_ui(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.setFixedSize(300, 250)
        self.centralwidget = QtWidgets.QWidget(main_window)
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

        # set the buttons for choices
        for i in POSSIBLE_CHOICES:
            self.buttons[i] = QtWidgets.QPushButton()
            self.buttons[i].setObjectName("pushButton" + POSSIBLE_CHOICES_LABELS[i])
            self.buttons[i].clicked.connect(partial(self.choice, i))
            self.verticalLayout.addWidget(self.buttons[i])

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout2 = QtWidgets.QVBoxLayout()
        self.verticalLayout2.setObjectName("verticalLayout2")

        self.textGameInteraction = QtWidgets.QTextEdit()
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
        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 219, 26))
        self.menubar.setObjectName("menubar")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.horizentalLayoutGameMode = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.radioButtonAgainstComputer = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.radioButtonAgainstComputer.setChecked(True)
        self.radioButtonAgainstComputer.setObjectName("radioButtonAgainstComputer")
        self.radioButtonTwoPlayer = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.radioButtonTwoPlayer.setObjectName("radioButtonTwoPlayer")
        self.horizentalLayoutGameMode.addWidget(self.radioButtonAgainstComputer)
        self.horizentalLayoutGameMode.addWidget(self.radioButtonTwoPlayer)
        self.horizentalLayoutGameMode.setObjectName("gameMode")
        self.verticalLayout2.addLayout(self.horizentalLayoutGameMode)
        self.restart()

        app.aboutToQuit.connect(lambda: self.close_window(main_window))
        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textEditPlayer.setPlaceholderText(_translate("MainWindow", "Player name"))
        for i in POSSIBLE_CHOICES:
            self.buttons[i].setText(_translate("MainWindow", POSSIBLE_CHOICES_LABELS[i]))
        self.pushButtonConnect.setText(_translate("MainWindow", "Connect"))
        self.pushButtonRestart.setText(_translate("MainWindow", "Restart"))
        self.radioButtonAgainstComputer.setText("1")
        self.radioButtonTwoPlayer.setText("2")

    def connect(self):
        # Callback for the connect button
        # Connects to the server if it is up
        if len(self.textEditPlayer.toPlainText()) != 0:
            host = "localhost"
            port = 1111
            try:
                self.socket.connect((host, port))
                self.name = self.textEditPlayer.toPlainText()
                player_information = str(self.radioButtonAgainstComputer.isChecked()) + "@" + self.name
                self.socket.send(player_information.encode("Utf8"))
                if self.radioButtonAgainstComputer.isChecked():
                    self.textGameInteraction.setPlainText("Connected: play against Computer")
                else:
                    self.handle_two_player_mode_connection()

                for i in POSSIBLE_CHOICES:
                    self.buttons[i].setDisabled(False)

                self.pushButtonConnect.setDisabled(True)
                self.textEditPlayer.setDisabled(True)
            except:
                self.textGameInteraction.setPlainText("Unable to connect to server")
        else:
            self.textGameInteraction.setPlainText("Player name is mandatory")

    def handle_two_player_mode_connection(self):
        # Expects the server response when we connect
        server_response = ""
        while server_response == "":
            server_response = self.socket.recv(255).decode(encoding="utf-8")

        self.textGameInteraction.setPlainText(server_response + "\n")

    def choice(self, player_choice):
        # Callback for all the possible choices buttons
        # Send the player's choice to the server in the following form: name@choice
        # Expects and handles the response of the server
        choice_str = self.name + '@' + str(player_choice)
        try:
            self.socket.send(choice_str.encode("Utf8"))
        except:
            self.textGameInteraction.setPlainText("Connection with server lost")
            return

        # Disable the name/game mode editing
        self.radioButtonTwoPlayer.setDisabled(True)
        self.radioButtonAgainstComputer.setDisabled(True)
        self.textEditPlayer.setDisabled(True)
        # Disable sending another choice
        for i in POSSIBLE_CHOICES:
            self.buttons[i].setDisabled(True)

        self.handle_decision()

        # Enable sending another choice
        for i in POSSIBLE_CHOICES:
            self.buttons[i].setDisabled(False)

    def handle_decision(self):
        # Expects and handles the response of the server when a choice has been made by the player
        decision = self.socket.recv(255).decode(encoding="utf-8")
        if self.radioButtonAgainstComputer.isChecked():
            while not (is_relevant(decision)):
                decision = self.socket.recv(255).decode(encoding="utf-8")
            self.rounds += 1
            if decision != "Draw":
                if self.name in decision:
                    self.score += 1
                else:
                    self.opponent_score += 1
            self.textGameInteraction.clear()
            self.textGameInteraction.setPlainText(decision + "\nscore: " + str(self.score) + " against " + str(
                self.opponent_score) + "\n" + "Number of rounds: " + str(self.rounds))
            return
        if self.radioButtonTwoPlayer.isChecked():
            t0 = time.time()
            delta = 20  # wait 20 maximum seconds for decision
            while not (is_relevant(decision)):
                decision = self.socket.recv(255).decode(encoding="utf-8")
                if delta < time.time() - t0:
                    print("Unable to get decision")
                    return
            self.rounds += 1
            if decision != "Draw":
                if self.name in decision:
                    self.score += 1
                else:
                    self.opponent_score += 1
            self.textGameInteraction.clear()
            self.textGameInteraction.setPlainText(decision + "\nScore: " + str(self.score) + " against " + str(
                self.opponent_score) + "\n" + "Number of rounds: " + str(self.rounds))

    def restart(self):
        # Callback for the restart button
        # Re-initializes the socket and all variables related to a game
        self.textEditPlayer.setDisabled(False)
        self.pushButtonConnect.setDisabled(False)

        for i in POSSIBLE_CHOICES:
            self.buttons[i].setDisabled(True)

        self.socket.close()
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.textGameInteraction.setPlainText("Welcome to Rock Paper Scissors")
        self.score = 0
        self.opponent_score = 0
        self.rounds = 0

        self.radioButtonTwoPlayer.setDisabled(False)
        self.radioButtonAgainstComputer.setDisabled(False)

    def close_window(self, dialog):
        # Callback for the close window button
        self.socket.close()
        dialog.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Player_UI()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
