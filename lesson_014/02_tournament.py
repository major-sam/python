# -*- coding: utf-8 -*-

# Прибежал менеджер и сказал что нужно срочно просчитать протокол турнира по боулингу в файле tournament.txt
#
# Пример записи из лога турнира
#   ### Tour 1
#   Алексей	35612/----2/8-6/3/4/
#   Татьяна	62334/6/4/44X361/X
#   Давид	--8/--8/4/8/-224----
#   Павел	----15623113-95/7/26
#   Роман	7/428/--4-533/34811/
#   winner is .........
#
# Нужно сформировать выходной файл tournament_result.txt c записями вида
#   ### Tour 1
#   Алексей	35612/----2/8-6/3/4/    98
#   Татьяна	62334/6/4/44X361/X      131
#   Давид	--8/--8/4/8/-224----    68
#   Павел	----15623113-95/7/26    69
#   Роман	7/428/--4-533/34811/    94
#   winner is Татьяна

# Код обаботки файла расположить отдельном модуле, модуль bowling использовать для получения количества очков
# одного участника. Если захочется изменить содержимое модуля bowling - тесты должны помочь.
#
# Из текущего файла сделать консольный скрипт для формирования файла с результатами турнира.
# Параметры скрипта: --input <файл протокола турнира> и --output <файл результатов турнира>

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

    def get_data(self):
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
                    points = Bowling().get_result(score)
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
my_namespace = parser.parse_args()

# print(f'input file  = {my_namespace.input[0]}')
# # print(f'output file = {my_namespace.output[0]}')
try:
    TournamentResult(input_file=my_namespace.input[0], output_file=my_namespace.output[0]).get_data()
except Exception as exc:
    print(exc)

# Усложненное задание (делать по желанию)
#
# После обработки протокола турнира вывести на консоль рейтинг игроков в виде таблицы:
#
# +----------+------------------+--------------+
# | Игрок    |  сыграно матчей  |  всего побед |
# +----------+------------------+--------------+
# | Татьяна  |        99        |      23      |
# ...
# | Алексей  |        20        |       5      |
# +----------+------------------+--------------+
#зачет!