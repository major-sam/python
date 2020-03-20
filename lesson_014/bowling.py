from __future__ import annotations
from abc import ABC, abstractmethod
from random import randint


class ScoreError(Exception):
    pass


class Context(ABC):
    _state = None

    def __init__(self, state: State) -> None:
        self.prev_round = 0
        self.transition_to(state, self.prev_round)

    def transition_to(self, state: State, prev_round):
        self._state = state
        self._state.context = self
        self.prev_round = prev_round

    def roll_it(self, points):
        return self._state.roll(points, self.prev_round)


class State(ABC):

    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    def roll(self, points, prev_round) -> tuple:
        pass


class FirstRoll(State):
    def roll(self, points, prev_round) -> tuple:
        if points == '/':
            raise ScoreError("Round can't start with /")
        elif points == 'X':
            return 20, True
        elif points == '-':
            self.context.transition_to(SecondRoll(), prev_round=0)
            return 0, False
        elif points.isdigit():
            self.context.transition_to(SecondRoll(), prev_round=points)
            return 0, False
            # print(f'FIRST ROLL IS {points}')
            # print("NEXT ROLL.")
        else:
            raise ScoreError(f"{points} is illegal character")


class SecondRoll(State):

    def roll(self, points, prev_round) -> tuple:
        if points == 'X':
            raise ScoreError("Second round can't ends with X")
        elif points == '/':
            self.context.transition_to(FirstRoll(), 0)
            return 15, True
        elif points == '-':
            self.context.transition_to(FirstRoll(), 0)
            return int(prev_round), True
        elif not points.isdigit():
            raise ScoreError(f"{points} is illegal character")
        elif (int(points) + int(prev_round)) > 10:
            raise ScoreError(f"There too match points({points}) for {10 - int(prev_round)} skittles")
        elif (int(points) + int(prev_round)) == 10:
            raise ScoreError(f"Wrong character ({points}) mast be '/'")
        else:
            self.context.transition_to(FirstRoll(), 0)
            return (int(points) + int(prev_round)), True


class Bowling:

    def __init__(self):
        self.game_state = None
        self.round_state = False
        self.round_points = 0
        self.game_points = 0
        self.context = Context(FirstRoll())

    def get_result(self, result):
        for item in result:
            round_info = self.check_result(item)
            self.round_state = round_info[1]
            self.round_points = round_info[0]
            self.game_points += self.round_points
        if self.round_state:
            return self.game_points
        else:
            raise ScoreError("Round not ended")

    def check_result(self, item):
        return self.context.roll_it(item)


class BowlingGame:

    def __init__(self, rounds=10, skittles=10, attempts=2):
        self.skittles = skittles
        self.attempts = attempts
        self.rounds = rounds
        self.results = []
        self.index = 0
        self.roll_result = 0
        self.game_result_points = 0
        self.next_round = False
        self.game_tarted = False

    def roll_the_ball(self):
        self.roll_result = randint(0, self.skittles)
        self.skittles = self.skittles - self.roll_result

    def get_score(self):
        if self.roll_result == 10:
            self.results.append("X")
        elif self.roll_result == 0:
            self.results.append("-")
        elif self.skittles == 0:
            self.results.append("/")
        else:
            self.results.append(self.roll_result)

    def get_result(self, game_result):
        try:
            for result in game_result:
                if result == "X":
                    self.game_result_points += 20
                elif result == "/":
                    if self.index == 0:
                        raise ScoreError("Score can't start with /")
                    self.game_result_points += 15
                    try:
                        self.game_result_points -= int(game_result[self.index - 1])
                    except ValueError:
                        raise ScoreError("// and X/ is impossible state for bowling score")
                elif result == '-':
                    self.index += 1
                    continue
                else:
                    self.game_result_points += int(result)
                self.index += 1
        except ValueError:
            raise ScoreError("Only X,/,- character and numbers allowed for bowling score")
        return self.game_result_points

    def play_bowling(self):
        attempts = self.attempts
        while self.rounds > 0:
            self.roll_the_ball()
            attempts -= 1
            self.get_score()
            if self.skittles == 0:
                self.skittles = 10
                attempts = self.attempts
                self.rounds -= 1
                continue
            elif attempts == 0:
                self.skittles = 10
                attempts = 2
                self.rounds -= 1
                continue
        res_line = ''.join(map(str, self.results))
        self.get_result(res_line)
        return res_line


# BowlingGame().play_bowling()
# try:
#     test_score = '3545-6X9-9-X6/1/26'
#     print(f"for {test_score} total score is {Bowling().get_result(test_score)}")
# except Exception as exc:
#     print(exc)
