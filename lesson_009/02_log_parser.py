# -*- coding: utf-8 -*-

# Имеется файл events.txt вида:
#
# [2018-05-17 01:55:52.665804] NOK
# [2018-05-17 01:56:23.665804] OK
# [2018-05-17 01:56:55.665804] OK
# [2018-05-17 01:57:16.665804] NOK
# [2018-05-17 01:57:58.665804] OK
# ...
#
# Напишите программу, которая считывает файл
# и выводит число событий NOK за каждую минуту в другой файл в формате
#
# [2018-05-17 01:57] 1234
# [2018-05-17 01:58] 4321
# ...
#
# Входные параметры: файл для анализа, файл результата
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.


class LogParser:

    def __init__(self, file_name):
        self.print_line = None
        self.condition = 0
        self.splitted_line = []
        self.file = file_name
        self.ok_counter, self.nok_counter, self.sort_lvl = 0, 0, 0
        self.prev_year, self.prev_month, self.prev_day,\
            self.prev_hour, self.prev_min = -1, -1, -1, -1, -1
        self.log_year, self.log_month, self.log_day, \
            self.log_hour, self.log_min, self.log_status = 0, 0, 0, 0, 0, 0
        self.time_separator = ':'
        self.date_separator = '-'

    def parse(self, sort_lvl):
        self.sort_lvl = sort_lvl
        with open(self.file, 'r') as file:
            for line in file:
                self.split_line(line)
                self.sort()
                self.print_nok()
            self.print_nok(last=True)

    def split_line(self, line):
        formatted_line = ''.join(char for char in line if char not in '[]\n')
        split_line = formatted_line.split(sep=' ')
        log_date = split_line[0]
        self.log_year = log_date.split(sep=self.date_separator)[0]
        self.log_month = log_date.split(sep=self.date_separator)[1]
        self.log_day = log_date.split(sep=self.date_separator)[2]
        log_time = split_line[1]
        self.log_hour = log_time.split(sep=self.time_separator)[0]
        self.log_min = log_time.split(sep=self.time_separator)[1]
        self.log_status = split_line[2]

    def sort(self):
        if self.sort_lvl == 0:  # min
            condition = (self.log_min != self.prev_min)
            print_line = f'[{self.log_year}-{self.log_month}-{self.log_day} {self.prev_hour}:{self.prev_min}] {self.nok_counter}'
        elif self.sort_lvl == 1:  # hour
            condition = (self.log_hour != self.prev_hour)
            print_line = f'[{self.log_year}-{self.log_month}-{self.log_day} {self.prev_hour}] {self.nok_counter}'
        elif self.sort_lvl == 2:  # day
            condition = ({self.log_day} != self.prev_day)
            print_line = f'[{self.log_year}-{self.log_month}-{self.log_day}] {self.nok_counter}'
        elif self.sort_lvl == 3:  # mouth
            condition = (self.log_month != self.prev_month)
            print_line = f'[{self.log_year}-{self.log_month}] {self.nok_counter}'
        elif self.sort_lvl == 4:  # year
            condition = (self.log_year != self.prev_year)
            print_line = f'[{self.log_year}] {self.nok_counter}'
        else:
            print_line = 'sort level must be in range from 0 to 4'
            condition = False
            exit(1)
        self.condition = condition
        self.print_line = print_line

    def print_nok(self, last=False):
        if self.prev_day == -1:
            self.shift()
        elif last:
            self.sort()
            print(self.print_line)
        elif self.condition:
            print(self.print_line)
            self.nok_counter, self.ok_counter = 0, 0
        elif self.log_status == 'NOK':
            self.nok_counter += 1
        elif self.log_status == 'OK':
            self.ok_counter += 1
        self.shift()

    def shift(self):
        self.prev_year, self.prev_month, self.prev_day, self.prev_hour, self.prev_min =\
            self.log_year, self.log_month, self.log_day, self.log_hour, self.log_min


#
log_file = 'events.txt'
action = LogParser(file_name=log_file)
action.parse(0)
# ok_counter = 0
# nok_counter = 0
# prev_hour = -1
# prev_min = -1
# prev_date = -1
#
#
# with open(log_file, 'r') as file:
#     for line in file:
#         formatted_line = ''.join(char for char in line if char not in '[]\n')
#         split_line = formatted_line.split(sep=' ')
#         log_date = split_line[0]
#         log_time = split_line[1]
#         log_status = split_line[2]
#         log_hour = log_time.split(sep=':')[0]
#         log_min = log_time.split(sep=':')[1]
#         log_sec = log_time.split(sep=':')[2]
#         if prev_date == -1:
#             prev_date = log_date
#             prev_hour = log_hour
#             prev_min = log_min
#         elif log_min != prev_min or log_hour != prev_hour:
#             print(f'[{log_date} {prev_hour}:{prev_min}] {nok_counter}')
#             nok_counter, ok_counter = 0, 0
#         if log_status == 'NOK':
#             nok_counter += 1
#         elif log_status == 'OK':
#             ok_counter += 1
#         prev_date = log_date
#         prev_hour = log_hour
#         prev_min = log_min
#     print(f'[{log_date} {prev_hour}:{prev_min}] {nok_counter}')
#  break
# После выполнения первого этапа нужно сделать группировку событий
#  - по часам
#  - по месяцу
#  - по году
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828
