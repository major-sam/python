from bowling import Bowling, ScoreError
import unittest

# TODO Тестов нужно будет побольше
# TODO Как минимум должны быть: неправильные (пустые, длинные, с неверными символами, с верными символами в неверном
# TODO порядке), правильные (простые, сложные)
class BowlingScoreTest(unittest.TestCase):

    def test_sum(self):
        result = Bowling().get_result('3545-6X9-9-X6/1/26')
        self.assertEqual(result, 119)

    def test_score_start_w_slash(self):
        with self.assertRaises(ScoreError):
            Bowling().get_result('/3545-6X9-9-X6/1/26')

    def test_score_double_slash(self):
        with self.assertRaises(ScoreError):
            Bowling().get_result('3545-6X9-9-X6//1/26')

    def test_score_illegal_char(self):
        with self.assertRaises(ScoreError):
            Bowling().get_result('asdfqf6')

    def test_round_count(self):
        rounds = Bowling().rounds
        score = list(Bowling().play_bowling())
        result = (len(score)+score.count('X'))/2
        print("")
        self.assertEqual(result, rounds)
