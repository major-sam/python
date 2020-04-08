# -*- coding: utf-8 -*-

# Прибежал менеджер и сказал что нужно срочно изменить правила подсчета очков в игре.
# "Выходим на внешний рынок, а там правила игры другие!" - сказал он.
#
# Правила подсчета очков изменяются так:
#
# Если во фрейме страйк, сумма очков за этот фрейм будет равна количеству сбитых кеглей в этом фрейме (10 кеглей)
# плюс количество фактически сбитых кеглей за два следующих броска (в одном или двух фреймах,
# в зависимости от того, был ли страйк в следующем броске).
# Если во фрейме сбит спэр, то сумма очков будет равна количеству сбитых кеглей в этом фрейме (10 кеглей)
# плюс количество фактически сбитых кеглей за первый бросок в следующем фрейме.
# Если фрейм остался открытым, то сумма очков будет равна количеству сбитых кеглей в этом фрейме.
# Страйк и спэр в последнем фрейме - по 10 очков.
#
# То есть для игры «Х4/34» сумма очков равна 10+10 + 10+3 + 3+4 = 40,
# а для игры «ХXX347/21» - 10+20 + 10+13 + 10+7 + 3+4 + 10+2 + 3 = 92

# Необходимые изменения сделать во всех модулях. Тесты - дополнить.

# "И да, старые правила должны остаться! для внутреннего рынка..." - уточнил менеджер напоследок.

from bowling import Bowling
import argparse


class TournamentResult:

    def __init__(self, input_file='tournament.txt', output_file='tournament_result.txt'):
        self.tournament_result_dict = {}
        self.file = input_file
        self.out_file = output_file
        self.tour = None
        self.total_score = {}

    def read_file(self, file):
        with open(file, encoding='utf8') as file:
            for line in file:
                yield line

    def get_winner(self, tour):
        sorted_table = sorted(tour, key=lambda i: i[2], reverse=True)
        return sorted_table[0][0]

    def get_data(self, rules_type=False):
        lines = self.read_file(self.file)
        for line in lines:
            line = line.replace("\n", "")
            if line.startswith("### Tour "):
                self.tour = line
                self.write_file(line)
                self.tournament_result_dict[self.tour] = []
            elif line == "":
                continue
            elif line == "winner is .........":
                winner = self.get_winner(self.tournament_result_dict[self.tour])
                self.tournament_result_dict[self.tour].append(f"winner is {winner}")
                self.write_file(f"winner is {winner}\n")
                self.total_score[winner][1] += 1
            else:
                name, score = line.split("\t")
                try:
                    points = Bowling().get_result(score, rules_type)
                except Exception as exc:
                    points = 0
                    # print(f'{exc} in score {score} - no points for {name}')
                self.tournament_result_dict[self.tour].append([name, score, points])
                self.write_file(f"{name}\t{score}\t{points}")
                if name in self.total_score and name is not None:
                    self.total_score[name][0] += 1
                else:
                    self.total_score[name] = [0, 0]
        self.print_total_score()

    def write_file(self, line, write_param='a+'):
        with open(file=self.out_file, mode=write_param, encoding='utf8') as source_file:
            source_file.write(f"{line}\n")

    def print_total_score(self):
        list_for_sort = []
        for player in self.total_score:
            total_games = self.total_score.get(player)[0]
            total_wins = self.total_score.get(player)[1]
            list_for_sort.append([player, total_games, total_wins])
        list_for_sort.sort(key=lambda i: i[2], reverse=True)
        print("+----------+------------------+--------------+\n" +
              "| Игрок    |  сыграно матчей  |  всего побед |\n" +
              "+----------+------------------+--------------+")
        for item in list_for_sort:
            print('|{name:<10}|{matches:^18}|{wins:^14}|'
                  .format(name=item[0], matches=item[1], wins=item[2]))
        print("+----------+------------------+--------------+\n")


parser = argparse.ArgumentParser()
parser.add_argument('--input', help='файл протокола турнира'
                    , required=True, nargs="+")
parser.add_argument('--output', help='файл результатов турнира'
                    , required=True, nargs='+')
parser.add_argument('--rules', default="1", help='0-расширенные правила\n1-простые правила(по умолчанию)')
my_namespace = parser.parse_args()

# print(f'input file  = {my_namespace.input[0]}')
# # print(f'output file = {my_namespace.output[0]}')
print(my_namespace.rules[0])
rules = True if my_namespace.rules[0] == '0' else False
try:
    TournamentResult(input_file=my_namespace.input[0],
                     output_file=my_namespace.output[0]).get_data(rules)
except Exception as exc:
    print(exc)