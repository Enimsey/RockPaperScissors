import time
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
import traceback
from main import *

import socket


class Worker(QRunnable, QObject):
    def __init__(self, fn):
        super(Worker, self).__init__()
        self.fn = fn

    @pyqtSlot()
    def run(self):
        try:
            self.fn()
        except:
            print("Issue running the worker function")
            traceback.print_exc()


class Server_UI:
    def __init__(self, dialog):
        self.dialog = dialog
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.dialog)
        self.thread_pool = QThreadPool()

    def setup_ui(self):
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
        self.textGameInfo.setPlainText("Welcome to Rock Paper Scissors")
        self.textGameInfo.setDisabled(True)

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.textGameInfo)

        self.pushButtonCancel.clicked.connect(self.close_window)
        app.aboutToQuit.connect(self.close_window)
        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self.dialog)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButtonStart.setText(_translate("Dialog", "Start"))
        self.pushButtonCancel.setText(_translate("Dialog", "Cancel"))

    def close_event(self, event):
        # Callback for the Close Window and Cancel buttons
        self.close_window()
        event.accept()

    def close_window(self):
        # Callback for Close/Close window buttons
        self.reset()
        self.thread_pool.clear()
        self.dialog.close()

    def open_connection(self):
        pass

    def start(self):
        # Callback for Start/Restart button
        # It re-initializes all the variables related to the tcp socket,
        # the threads and the players
        self.reset()
        worker = Worker(self.open_connection)
        self.thread_pool.start(worker)

    def reset(self):
        self.thread_pool.clear()


class Game(Server_UI):
    def __init__(self, dialog):
        super().__init__(dialog)
        self.connections = []
        self.mode = True
        self.players = []
        self.client_sockets = []
        self.tcpsock = None
        self.session_number = 0

    def open_connection(self):
        # Callback for the Start button
        self.tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcpsock.bind(("localhost", 1111))
        self.tcpsock.listen()
        while len(self.connections) < 2:
            try:
                (client_socket, (ip, port)) = self.tcpsock.accept()
                connection = client_socket.recv(255)
                if connection != "" and not (port in self.connections):
                    (player, mode) = parse_connection(connection)
                    self.mode = mode
                    self.players.append(player)
                    self.client_sockets.append(client_socket)
                    self.connections.append(port)

                    if mode:
                        # if against computer, no need to listen to other connections
                        break
                    else:
                        self.handle_multi_player_connection(player, client_socket)
            except:
                print("Lost connection with socket")
                return

        if self.mode:  # against computer
            self.play_against_computer()
        else:
            self.play_against_opponent()

    def handle_multi_player_connection(self, player, client_socket):
        # Handles the connection of two players to the socket
        # Sends information about the connection to the players
        if len(self.connections) == 1:
            client_socket.send((player.__str__() + " connected:\nExpect second player").encode("Utf8"))
        if len(self.connections) == 2:
            self.client_sockets[0].send(
                ("You are playing against " + self.players[1].__str__() + "\n Make your choice").encode(
                    "Utf8"))
            self.client_sockets[1].send(
                ("You are playing against " + self.players[0].__str__() + "\n Make your choice").encode(
                    "Utf8"))

    def play_against_computer(self):
        # Handles a Game against the computer
        while True:
            try:
                choice = ""
                while choice == "":
                    choice = self.client_sockets[0].recv(255)
                self.parse_choice(choice)
                winner = play_with_computer_object(self.players[0])

                if winner == None:
                    # self.textGameInfo.setPlainText("Draw")
                    self.client_sockets[0].send("Draw".encode("Utf8"))
                else:
                    self.client_sockets[0].send((
                            winner.__str__() + " wins with " + winner.choice.__str__() + " against " + winner.opponent_choice.__str__()).encode(
                        "Utf8"))
            except:
                print("Disconnected")
                self.tcpsock.close()
                self.connections.clear()
                self.players.clear()
                self.client_sockets.clear()
                break

    def play_against_opponent(self):
        # Handles a Game for two players.
        # It opens starts two threads for each player, to listen to their choices
        # Each thread, runs the method listen_to_player
        assert (len(self.players) == 2)
        worker_player0 = Worker(lambda: self.listen_to_player(0))
        worker_player1 = Worker(lambda: self.listen_to_player(1))
        self.thread_pool.start(worker_player0)
        self.thread_pool.start(worker_player1)

    def parse_choice(self, choice):
        # Parse the received choice and setting it to the corresponding player
        # Example of input: b'Yasmine@1'
        l = choice.decode(encoding="utf-8").split("@")
        name = l[0]
        choice = l[1]
        for player in self.players:
            if player.name == name:
                player.set_choice(int(choice))

    def listen_to_player(self, client_idx):
        # Runs in a separate thread.
        # It listens to one player's choices
        # Send the results to both players, if both choices have been made
        no_exception = True
        while no_exception:
            try:
                choice = ""
                t0 = time.time()
                delta = 10  # wait 10 maximum seconds for decision, otherwise reset the choices
                while choice == "":
                    choice = self.client_sockets[client_idx].recv(255)
                    if self.players[1 - client_idx].get_choice_value() > 0 and delta < time.time() - t0:
                        print("Unable to get choice")
                        self.players[1 - client_idx].set_choice(-1)
                        self.players[client_idx].set_choice(-1)
                        break
                if choice != "":
                    self.parse_choice(choice)
                    if self.players[1 - client_idx].get_choice_value() != -1:
                        winner = determine_who_wins(self.players[client_idx], self.players[1 - client_idx])
                        if winner == None:
                            self.client_sockets[client_idx].send("Draw".encode("Utf8"))
                            self.client_sockets[1 - client_idx].send("Draw".encode("Utf8"))
                        else:
                            self.client_sockets[client_idx].send((
                                    winner.__str__() + " wins with " + winner.choice.__str__() + " against " + winner.opponent_choice.__str__()).encode(
                                "Utf8"))
                            self.client_sockets[1 - client_idx].send((
                                    winner.__str__() + " wins with " + winner.choice.__str__() + " against " + winner.opponent_choice.__str__()).encode(
                                "Utf8"))

                        # Reset both choices
                        self.players[client_idx].set_choice(-1)
                        self.players[1 - client_idx].set_choice(-1)
                    else:
                        self.client_sockets[client_idx].send(
                            ("Expect " + self.players[1 - client_idx].__str__() + "'s choice").encode("Utf8"))
            except:
                print("Players were disconnected")
                no_exception = False
                self.tcpsock.close()
                self.connections.clear()
                self.players.clear()
                self.client_sockets.clear()

    def reset(self):
        self.connections = []
        self.mode = True
        self.players = []
        self.client_sockets = []
        if self.tcpsock is not None:
            self.tcpsock.close()
        self.thread_pool.clear()
        self.tcpsock = None
        self.session_number += 1
        self.textGameInfo.setPlainText("Session " + str(self.session_number))
        self.pushButtonStart.setText("Restart")


def parse_connection(connection):
    # Parses the received string from a client to determine the name of the player
    # and whether they are playing against the computer (mode = True)
    # or against another player (mode = False)
    # Example of input: b'False@Yasmine'
    # Output should be ("Yasmine", False)

    L = connection.decode(encoding="utf-8").split("@")
    player = Player(L[1])
    mode = L[0] == "True"  # True is against computer, False is two players
    return player, mode


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Game(Dialog)
    ui.setup_ui()
    Dialog.show()
    sys.exit(app.exec_())
