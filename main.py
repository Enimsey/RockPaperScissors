import sys
import random
from getpass import getpass

POSSIBLE_CHOICES = [0, 1, 2]  # rock, paper, scissors
POSSIBLE_CHOICES_LABELS = {0: "Rock", 1: "Paper", 2: "Scissors"}


# POSSIBLE_CHOICES = [0, 1, 2, 3, 4]  # rock, paper, scissors, Lizard, Spock
# POSSIBLE_CHOICES_LABELS = {0: "Rock", 1: "Paper", 2: "Scissors", 3: "Lizard", 4: "Spock"}


class Player:
    # This Class represents the Player and their choice.
    def __init__(self, _name):
        self.name = _name
        self.choice = Choice(-1)
        self.opponent_choice = None

    def __str__(self):
        return self.name

    def set_choice(self, input_choice):
        self.choice.value = input_choice

    def get_choice_value(self):
        return int(self.choice.value)


class Choice:
    # This Class represents the choice of a player
    def __init__(self, input_choice):
        self.value = input_choice

    def __gt__(self, other_choice):
        # Overriding the operator greater then to compare two choices
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
        if validate_input(self.value):
            return POSSIBLE_CHOICES_LABELS[int(self.value)]
        return str(self.value)


def validate_input(input):
    # This function validates a choice (whether it is an int and one of the possible choices)
    return input in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] and int(
        input) in POSSIBLE_CHOICES


def play_with_computer_object(player):
    # This Function, takes a human player,
    # creates a bot player with a random choice,
    # and returns the winner among them

    bot_player = Player("Computer")
    bot_player.set_choice(random.randint(0, max(POSSIBLE_CHOICES)))

    return determine_who_wins(player, bot_player)


def play_with_computer(human_choice, human_name):
    # Same as the above, but with different inputs instead
    if not (validate_input(human_choice)):
        sys.stdout.write(human_choice + " is not a possible choice, choose among: " + str(POSSIBLE_CHOICES) + "\n")
        return
    human_player = Player(human_name)
    human_player.set_choice(int(human_choice))

    return play_with_computer_object(human_player)


def determine_who_wins(player1, player2):
    # This function determines who among the two players wins.
    # If it is a draw, it return None
    # Else, it returns the player who wins
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


def two_players_game(player_name1, player_name2, player_choice1, player_choice2):
    # This function takes two players names and their choices.
    # It returns who wins/None if their choices are valid
    if validate_input(player_choice1) and validate_input(player_choice2):
        human_player1 = Player(player_name1)
        human_player1.set_choice(int(player_choice1))
        human_player2 = Player(player_name2)
        human_player2.set_choice(int(player_choice2))

        return determine_who_wins(human_player1, human_player2)

    sys.stderr.write(player_choice1 + " or " + player_choice2 + " is not a possible choice, choose among: " + str(
        POSSIBLE_CHOICES) + "\n")
    return


def compute_score(winner, players, scores, rounds):
    rounds += 1
    if winner is None:
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


def get_final_score(winner, players, scores, rounds):
    sys.stdout.write(' /*\/*\/*\/*\/*\ Final Score /*\/*\/*\/*\/*\ ' + "\n")
    [scores, _] = compute_score(winner, players, scores, rounds)
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
                do_continue = "Y"
                scores = [0, 0]
                rounds = 0
                players = ["Human", "Computer"]
                while do_continue != 'n':
                    user_input = input("Your choice \n")
                    winner = play_with_computer(user_input, "Human")
                    sys.stdout.write("****** Score ******\n")
                    [scores, rounds] = compute_score(winner, players, scores, rounds)
                    do_continue = input("continue?  [Y/n]")
                get_final_score(winner, players, scores, rounds)
            else:
                if sys.argv[1] == '2':
                    user_input = "Y"
                    scores = [0, 0]
                    rounds = 0
                    players = ["player1", "player2"]
                    while user_input != 'n':
                        user_input1 = getpass("first player choice \n")
                        user_input2 = getpass("second player choice \n")
                        winner = two_players_game("player1", "player2", user_input1, user_input2)
                        sys.stdout.write("****** Score ******\n")
                        [scores, rounds] = compute_score(winner, players, scores, rounds)
                        user_input = input("continue?  [Y/n]")
                    get_final_score(winner, players, scores, rounds)
        else:
            sys.stderr.write("too many input arguments\n")
