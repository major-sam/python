from bowling import Bowling, BowlingGame, ScoreError
import unittest


class BowlingScoreTest(unittest.TestCase):

    def test_sum(self):
        result = Bowling().get_result('3545-6X9-9-X6/1/26')
        self.assertEqual(result, 119)
        result = Bowling().get_result('XXXXXXXXXX')
        self.assertEqual(result, 200)

    def test_score_wrong_char_placement(self):
        with self.assertRaises(ScoreError):
            Bowling().get_result('X/XXXXXXXX')
        with self.assertRaises(ScoreError):
            Bowling().get_result('X5XXXXXXXX')
        with self.assertRaises(ScoreError):
            Bowling().get_result('X55XXXXXXX')
        with self.assertRaises(ScoreError):
            Bowling().get_result('X59XXXXXXX')

    def test_score_start_w_slash(self):
        with self.assertRaises(ScoreError):
            Bowling().get_result('/3545-6X9-9-X6/1/26')

    def test_score_double_slash(self):
        with self.assertRaises(ScoreError):
            Bowling().get_result('3545-6X9-9-X6//1/26')

    def test_score_illegal_char(self):
        with self.assertRaises(ScoreError):
            Bowling().get_result('asdfqf6')

    def test_empty_score(self):
        with self.assertRaises(ScoreError):
            Bowling().get_result('')

    def test_round_count(self):
        score = BowlingGame().play_bowling()
        rounds = 10
        result = (len(score)+score.count('X'))/2
        print("")
        self.assertEqual(result, rounds)
