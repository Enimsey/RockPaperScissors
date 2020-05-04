from main import *
from serverui import parse_connection
from playerui import is_relevant
import unittest


class TestGame(unittest.TestCase):

    def test_validate_input(self):
        self.assertTrue(validate_input(0))
        self.assertTrue(validate_input(1))
        self.assertTrue(validate_input(2))
        self.assertFalse(validate_input('A'))
        self.assertFalse(validate_input('8'))

    def test_gt(self):
        choice1 = Choice(0)
        choice2 = Choice(2)

        self.assertTrue(choice1 > choice2)

        choice1 = Choice(1)
        choice2 = Choice(0)

        self.assertTrue(choice1 > choice2)

        choice1 = Choice(2)
        choice2 = Choice(1)

        self.assertTrue(choice1 > choice2)

    def test_determine_who_wins(self):
        player1 = Player("player1")
        player2 = Player("player2")

        player1.set_choice(0)
        player2.set_choice(2)

        self.assertEqual(determine_who_wins(player1, player2), player1)

        player1.set_choice(1)
        player2.set_choice(0)

        self.assertEqual(determine_who_wins(player1, player2), player1)

        player1.set_choice(2)
        player2.set_choice(1)

        self.assertEqual(determine_who_wins(player1, player2), player1)

    def test_scores(self):
        winner = None
        players = ['A', 'B']
        scores = [0, 0]
        rounds = 0
        [scores, rounds] = compute_score(winner, players, scores, rounds)
        self.assertEqual(scores, [0, 0])
        self.assertEqual(rounds, 1)

        winner = Player("A")
        [scores, rounds] = compute_score(winner, players, scores, rounds)
        self.assertEqual(scores, [1, 0])
        self.assertEqual(rounds, 2)

        winner = Player("B")
        [scores, rounds] = compute_score(winner, players, scores, rounds)
        self.assertEqual(scores, [1, 1])
        self.assertEqual(rounds, 3)

        scores_final = get_final_score(winner, players, scores, rounds)
        self.assertEqual(scores_final, [1, 2])

        scores_final = get_final_score(None, players, scores, rounds)
        self.assertEqual(scores_final, [1, 2])

    def test_parse_connection(self):
        connection_string = b'False@Yasmine'
        (player, mode) = parse_connection(connection_string)
        self.assertFalse(mode)
        self.assertTrue(player.name, "Yasmine")

    def test_is_relevant(self):
        self.assertTrue(is_relevant("Draw"))
        self.assertFalse(is_relevant("toto"))
        self.assertTrue(is_relevant("Human wins"))

    def test_two_players_game(self):
        winner = two_players_game("A", "B", 0, 0)
        self.assertEqual(winner, None)

        winner = two_players_game("A", "B", 0, 1)
        self.assertEqual(winner.name, "B")

        winner = two_players_game("A", "B", 1, 0)
        self.assertEqual(winner.name, "A")


if __name__ == '__main__':
    unittest.main()
