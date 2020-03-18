from random import randint


class ScoreError(Exception):
    pass


class Bowling:

    def __init__(self, rounds=10, skittles=10, attempts=2):
        self.skittles = skittles
        self.attempts = attempts
        self.rounds = rounds
        self.results = []
        self.index = 0
        self.roll_result = 0
        self.game_result_points = 0
        self.next_round = False

    # TODO Формировать результат вам по сути не нужно
    # TODO Нжуно принимать готовую строку и выдавать расчёт
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
        try:  # TODO Здесь try/except не нужен, тут только raise исключений
            # TODO А вызов функции уже можно оборачивать в try/except
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
                # TODO Как подобные if/elif блоки учитывают ситуацию
                # TODO Когда результатом будет например строка 9999999?
        except ValueError:
            raise ScoreError("Only X,/,- character and numbers allowed for bowling score")
        return self.game_result_points
    # TODO Где проверяется размер строки? Должно быть ровно 10 фреймов

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


#Bowling().play_bowling()
