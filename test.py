from main import *
import unittest


class TestGame(unittest.TestCase):

    def test_validateInput(self):
        self.assertTrue(validateInput(0))
        self.assertTrue(validateInput(1))
        self.assertTrue(validateInput(2))
        self.assertFalse(validateInput(5))

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

    def test_determineWhoWins(self):
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

    def test_computeScore(self):
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


if __name__ == '__main__':
    unittest.main()
