import unittest
from random import randint
from unittest.mock import MagicMock

from bowling import FirstRoll, ScoreError, SecondRoll, FirstXRoll, DoubleXRoll, LastXRoll, SlashRoll


class TestFirstRoll(unittest.TestCase):

    def test_x(self):
        self.roll = FirstRoll()
        self.roll.context = MagicMock()
        self.roll.get_roll_state_advanced("X", 0, False)
        self.assertEqual(self.roll.score, 10)
        self.assertEqual(self.roll.round_ends, True)

    def test_slash(self):
        with self.assertRaises(ScoreError):
            roll = FirstRoll()
            roll.get_roll_state("/", 0)

    def test_num(self):
        points = str(randint(1, 10))
        self.roll = FirstRoll()
        self.roll.context = MagicMock()
        self.roll.get_roll_state(points=points, prev_round=0)
        self.assertEqual(self.roll.score, 0)
        self.assertEqual(self.roll.round_ends, False)


class TestSecondRoll(unittest.TestCase):

    def test_x(self):
        with self.assertRaises(ScoreError):
            roll = SecondRoll()
            roll.get_roll_state_advanced("X", 0, round_end=False)

    def test_slash(self):
        self.roll = SecondRoll()
        self.roll.context = MagicMock()
        self.roll.get_roll_state_advanced(points='/', prev_round=0, round_end=False)
        self.assertEqual(self.roll.score, 10)

    def test_num(self):
        points = str(randint(1, 10))
        self.roll = SecondRoll()
        self.roll.context = MagicMock()
        if points == "10":
            with self.assertRaises(ScoreError):
                self.roll.get_roll_state_advanced(points=points, prev_round=0, round_end=False)
        else:
            self.roll.get_roll_state_advanced(points=points, prev_round=0, round_end=False)
            self.assertEqual(self.roll.score, int(points))
            self.assertEqual(self.roll.round_ends, True)


class TestFirstXRoll(unittest.TestCase):

    def test_x(self):
        self.roll = FirstXRoll()
        self.roll.context = MagicMock()
        self.roll.get_roll_state_advanced(points='X', prev_round=0, round_end=False)
        self.assertEqual(self.roll.score, 20)

    def test_slash(self):
        with self.assertRaises(ScoreError):
            roll = FirstXRoll()
            roll.get_roll_state_advanced("/", 0, round_end=False)

    def test_num(self):
        points = str(randint(1, 10))
        self.roll = SecondRoll()
        self.roll.context = MagicMock()
        self.roll.get_roll_state_advanced(points=points, prev_round=0, round_end=False)
        self.assertEqual(self.roll.score, int(points))
        self.assertEqual(self.roll.round_ends, True)


class TestLastXRoll(unittest.TestCase):

    def test_x(self):
        self.roll = LastXRoll()
        with self.assertRaises(ScoreError):
            self.roll.get_roll_state_advanced("/", 0, round_end=False)

    def test_slash(self):
        self.roll = LastXRoll()
        self.roll.context = MagicMock()
        self.roll.get_roll_state_advanced(points="/", prev_round=1, round_end=False)
        self.assertEqual(self.roll.score, 19)
        self.assertEqual(self.roll.round_ends, True)

    def test_num(self):
        points = str(randint(1, 10))
        self.roll = LastXRoll()
        self.roll.context = MagicMock()
        self.roll.get_roll_state_advanced(points=points, prev_round=0, round_end=False)
        self.assertEqual(self.roll.score, int(points)*2)
        self.assertEqual(self.roll.round_ends, True)


class TestDoubleXRoll(unittest.TestCase):

    def test_x(self):
        self.roll = DoubleXRoll()
        self.roll.context = MagicMock()
        self.roll.get_roll_state_advanced(points="X", prev_round=0, round_end=True)
        self.assertEqual(self.roll.score, 30)
        self.assertEqual(self.roll.round_ends, True)

    def test_slash(self):
        self.roll = DoubleXRoll()
        with self.assertRaises(ScoreError):
            self.roll.get_roll_state_advanced("/", 0, round_end=False)

    def test_num(self):
        points = str(randint(1, 10))
        self.roll = DoubleXRoll()
        self.roll.context = MagicMock()
        self.roll.get_roll_state_advanced(points=points, prev_round=0, round_end=False)
        self.assertEqual(self.roll.score, int(points)*2)
        self.assertEqual(self.roll.round_ends, False)


class TestSlashRoll(unittest.TestCase):

    def test_x(self):
        self.roll = SlashRoll()
        self.roll.context = MagicMock()
        self.roll.get_roll_state_advanced(points="X", prev_round=0, round_end=True)
        self.assertEqual(self.roll.score, 20)
        self.assertEqual(self.roll.round_ends, True)

    def test_slash(self):
        self.roll = SlashRoll()
        with self.assertRaises(ScoreError):
            self.roll.get_roll_state_advanced("/", 0, round_end=False)

    def test_num(self):
        points = str(randint(1, 10))
        self.roll = SlashRoll()
        self.roll.context = MagicMock()
        self.roll.get_roll_state_advanced(points=points, prev_round=0, round_end=False)
        self.assertEqual(self.roll.score, int(points))
        self.assertEqual(self.roll.round_ends, False)
