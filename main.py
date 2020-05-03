# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 09:15:05 2020

@author: ynajar
"""
import sys
import random

possibleChoices = [0, 1, 2] # rock, paper, scissors
possibleChoicesLabel = {0:"rock", 1:"paper", 2:"scissors"}

def connectActions(self):
    self.pushButtonRock.connect(setGameAndPlay)
    self.pushButtonPaper.connect()
    self.pushButtonScissos.connect()
    actionQuit.triggered.connect(QtGui.qApp.quit)
    self.actionOpen.triggered.connect(self.openImage)
    

class Player:
     def __init__(self, _name):
         self.name = _name
         self.choice = Choice(3)
         
     def __str__(self):
         return self.name
     
     def setChoice(self, inputChoice):
         self.choice.value = inputChoice
     
     def setName(self, name):
         self.name = name
     
     def getChoiceValue(self):
         return int(self.choice.value)
         

class Choice:
    def __init__(self, _inputChoice):
        self.value = _inputChoice
        
    def __gt__(self, otherChoice):
        if self.value == 0:
            # 0 only wins against 2
            return otherChoice.value == 2
        if self.value == 1:
            # 1 only wins against 0
            return otherChoice.value == 0
        if self.value == 2:
            # 2 only wins against 1
            return otherChoice.value == 1
    
    def __str__(self):
        return possibleChoicesLabel[int(self.value)]
        
    
def validateInput(input):
    return int(input) in possibleChoices
      

def playWithComputer(humanChoice, humanName):
    
    if not(validateInput(humanChoice)):
        sys.stdout.write(humanChoice + " is not a possible choice, choose among: 0,1,2\n" )
        print(humanChoice + " is not a possible choice, choose among: 0,1,2\n" )
        return
    humanPlayer = Player(humanName)
    humanPlayer.setChoice(int(humanChoice))
    
    return playWithComputerObject(humanPlayer)

def playWithComputerObject(player):
    botPlayer = Player("Computer")
    botPlayer.setChoice(random.randint(0, 2))
    
    return(determineWhoWins(player, botPlayer))
    
def determineWhoWins(player1, player2):
        print(player1.__str__() + " : " + player1.choice.__str__()+"\n")
        print(player2.__str__() + " : " + player2.choice.__str__()+"\n")
        if(int(player1.choice.value) == int(player2.choice.value)):
            sys.stdout.write("Draw\n")
            print("Draw\n")
            return
        else:
            if player1.choice>player2.choice:
                print(player1.__str__() + " wins with " + player1.choice.__str__() + " againts " + player2.choice.__str__()+"\n")
                sys.stdout.write(player1.__str__() + " wins with " + player1.choice.__str__() + " againts " + player2.choice.__str__()+"\n")
                return player1
            else:
                print(player2.__str__() + " wins with " + player2.choice.__str__() + " againts " + player1.choice.__str__()+"\n")
                sys.stdout.write(player2.__str__() + " wins with " + player2.choice.__str__() + " againts " + player1.choice.__str__()+"\n")
                return player2
    
def twoPlayersGame(player1Name, player2Name, playerChoice1, playerChoice2):
    if not(validateInput(playerChoice1) or not(validateInput(playerChoice1))):
        sys.stdout.write(humanChoice + " is not a possible choice, choose among: 0,1,2\n" )
        return
    humanPlayer1 = Player(player1Name)
    humanPlayer1.setChoice(int(playerChoice1))
    humanPlayer2 = Player(player2Name)
    humanPlayer2.setChoice(int(playerChoice2))
    
    
    return(determineWhoWins(humanPlayer1, humanPlayer2))

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Game()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
# =============================================================================
#     
#     if len(sys.argv) == 1:
#         sys.stderr.write("no input arguments\n")
#     else: 
#         if len(sys.argv) == 2:
#             sys.stdout.write("Playing with the computer\n")
#             playWithComputer(sys.argv[1],"Human")
#         else:
#             if len(sys.argv) == 3:
#                 twoPlayersGame(sys.argv[1], sys.argv[2])
#             else:
#                 sys.stderr.write("too many input arguments\n")
#         
# =============================================================================
    
    
