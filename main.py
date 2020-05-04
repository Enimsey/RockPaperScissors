# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 09:15:05 2020

@author: ynajar
"""
import sys
import random

possibleChoices = [0, 1, 2]  # rock, paper, scissors
possibleChoicesLabel = {0: "Rock", 1: "Paper", 2: "Scissors"}
# possibleChoices = [0, 1, 2, 3, 4]  # rock, paper, scissors, Lizard, Spock
# possibleChoicesLabel = {0: "Rock", 1: "Paper", 2: "Scissors", 3: "Lizard", 4: "Spock"}

from getpass import getpass


class Player:
    def __init__(self, _name):
        self.name = _name
        self.choice = Choice(-1)
        self.opponent_choice = None

    def __str__(self):
        return self.name

    def setChoice(self, inputChoice):
        self.choice.value = inputChoice

    def setName(self, name):
        self.name = name

    def getChoiceValue(self):
        return int(self.choice.value)


class Choice:
    def __init__(self, input_choice):
        self.value = input_choice

    def __gt__(self, other_choice):
        if self.value == 0:
            # Rock only wins against Scissors or Lizard
            return other_choice.value == 2 or other_choice.value == 3
        if self.value == 1:
            # Paper only wins against Rock or Spock
            return other_choice.value == 0 or other_choice.value == 4
        if self.value == 2:
            # Scissors only wins against Paper or Lizard
            return other_choice.value == 1 or other_choice.value == 3
        if self.value == 3:
            # Lizard only wins against Paper or Spock
            return other_choice.value == 2 or other_choice.value == 4
        if self.value == 4:
            # Spock only wins against Rock or Scissors
            return other_choice.value == 0 or other_choice.value == 2

    def __str__(self):
        if validateInput(self.value):
            return possibleChoicesLabel[int(self.value)]
        return str(self.value)


def validateInput(input):
    return input in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] and int(
        input) in possibleChoices


def playWithComputer(humanChoice, humanName):
    if not (validateInput(humanChoice)):
        sys.stdout.write(humanChoice + " is not a possible choice, choose among: " + str(possibleChoices) +"\n")
        return
    humanPlayer = Player(humanName)
    humanPlayer.setChoice(int(humanChoice))

    return playWithComputerObject(humanPlayer)


def playWithComputerObject(player):
    botPlayer = Player("Computer")
    botPlayer.setChoice(random.randint(0, max(possibleChoices)))

    return determineWhoWins(player, botPlayer)


def determineWhoWins(player1, player2):
    if int(player1.choice.value) == int(player2.choice.value):
        sys.stdout.write("         Draw\n")
        return
    else:
        if player1.choice > player2.choice:
            sys.stdout.write("         " +
                             player1.__str__() + " wins with " + player1.choice.__str__() + " againts " + player2.choice.__str__() + "\n")
            player1.opponent_choice = player2.choice
            return player1
        else:
            sys.stdout.write("         " +
                             player2.__str__() + " wins with " + player2.choice.__str__() + " againts " + player1.choice.__str__() + "\n")
            player2.opponent_choice = player1.choice
            return player2


def twoPlayersGame(player_name1, player_name2, player_choice1, player_choice2):
    if validateInput(player_choice1) and validateInput(player_choice2):
        human_player1 = Player(player_name1)
        human_player1.setChoice(int(player_choice1))
        human_player2 = Player(player_name2)
        human_player2.setChoice(int(player_choice2))

        return determineWhoWins(human_player1, human_player2)

    sys.stderr.write(player_choice1 + " or " + player_choice2 + " is not a possible choice, choose among: " + str(possibleChoices) +"\n")
    return


def computeScore(winner, players, scores, rounds):
    rounds += 1
    if winner == None:
        sys.stdout.write(players[0].__str__() + " : " + str(scores[0]) + "\n")
        sys.stdout.write(players[1].__str__() + " : " + str(scores[1]) + "\n")
        return scores, rounds
    if winner.name == players[0]:
        scores[0] += 1
    else:
        scores[1] += 1

    sys.stdout.write(players[0].__str__() + " : " + str(scores[0]) + "\n")
    sys.stdout.write(players[1].__str__() + " : " + str(scores[1]) + "\n")
    return scores, rounds


def getFinalScore(winner, players, scores, rounds):
    sys.stdout.write(' /*\/*\/*\/*\/*\ Final Score /*\/*\/*\/*\/*\ ' + "\n")
    [scores, _] = computeScore(winner, players, scores, rounds)
    if scores[0] == scores[1]:
        sys.stdout.write("Draw\n")
    else:
        if scores[0] > scores[1]:
            sys.stdout.write(players[0] + " wins\n")
        else:
            sys.stdout.write(players[1] + " wins\n")
    sys.stdout.write("See you soon!\n")
    return scores


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.stderr.write("no input arguments\n")
    else:
        if len(sys.argv) == 2:
            if sys.argv[1] == '1':
                sys.stdout.write("Playing with the computer\n")
                # winner = playWithComputer(sys.argv[1], "Human")
                do_continue = "Y"
                scores = [0, 0]
                rounds = 0
                players = ["Human", "Computer"]
                # [scores, rounds] = computeScore(winner, players, scores, rounds)
                while do_continue != 'n':
                    user_input = input("Your choice \n")
                    winner = playWithComputer(user_input, "Human")
                    sys.stdout.write("****** Score ******\n")
                    [scores, rounds] = computeScore(winner, players, scores, rounds)
                    do_continue = input("continue?  [Y/n]")
                getFinalScore(winner, players, scores, rounds)
            else:
                if sys.argv[1] == '2':
                    # winner = twoPlayersGame("player1", "player2", sys.argv[1], sys.argv[2])
                    user_input = "Y"
                    scores = [0, 0]
                    rounds = 0
                    players = ["player1", "player2"]
                    # [scores, rounds] = computeScore(winner, players, scores, rounds)
                    while user_input != 'n':
                        user_input1 = getpass("first player choice \n")
                        user_input2 = getpass("second player choice \n")
                        winner = twoPlayersGame("player1", "player2", user_input1, user_input2)
                        sys.stdout.write("****** Score ******\n")
                        [scores, rounds] = computeScore(winner, players, scores, rounds)
                        user_input = input("continue?  [Y/n]")
                    getFinalScore(winner, players, scores, rounds)
        else:
            sys.stderr.write("too many input arguments\n")
