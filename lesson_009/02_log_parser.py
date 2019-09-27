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
        self.file = file_name
        self.ok_counter, self.nok_counter, self.sort_lvl = 0, 0, 0
        # TODO Вместо 5 переменных для прошлого и настоящего не лучше ли завести по словарю с ними?
        self.prev_year, self.prev_month, self.prev_day,\
            self.prev_hour, self.prev_min = -1, -1, -1, -1, -1
        self.log_year, self.log_month, self.log_day, \
            self.log_hour, self.log_min, self.log_status = 0, 0, 0, 0, 0, 0
        self.time_separator = ':'  # TODO Вот это интересный способ, но лучше передавать эти разделители
        self.date_separator = '-'  # TODO В функцию, параметрами. Они ведь используются только в одном методе.

    def parse(self, sort_lvl):
        # TODO Разделяем обязанности - один метод для чтения файла
        # TODO Другой для обработки данных
        # TODO Чтобы получать по одной линии - можно использовать yield line в цикле
        # TODO Тогда при каждом обращении будет выдаваться по строке

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
        # TODO Этот метод можно переименовать в формирование записи лога.
        # TODO Перенести сюда часть из сорт, которая это делает
        # TODO А return-ом возвращать строку.
        # TODO Тогда при простом вызове - это обновит текущие данные
        # TODO А при вызове в принте - выведет строку на консоль (или запишет в файл)

    def sort(self):  # TODO Название пишите без сокращений пожалуйста и поподробнее
        # TODO Здесь выполняется 2 логики, которые стоит разделить на разные методы
        # TODO 1) Проверка на новый день - условие можно возвращать ретурном
        # TODO Это избавит нас от одного из атрибутов
        # TODO 2) Формирование записи лога - print_line можно будет возвращать ретурном при вызове
        # TODO Это избавит нас от другого атрибута
        if self.sort_lvl == 0:  # min
            condition = (self.log_min != self.prev_min)
            print_line = f'[{self.log_year}-{self.log_month}-{self.log_day} {self.prev_hour}:{self.prev_min}] {self.nok_counter}'
        elif self.sort_lvl == 1:  # hour
            condition = (self.log_hour != self.prev_hour)
            print_line = f'[{self.log_year}-{self.log_month}-{self.log_day} {self.prev_hour}] {self.nok_counter}'
        elif self.sort_lvl == 2:  # day
            condition = (self.log_day != self.prev_day)
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
        # TODO Считаются ли события, которые попадают в первый, последний день и в смену дней?
        # TODO Это одна из причин, почему плохо смешивать разные обязанности в одном методе.
        # TODO Если этот метод должен выводить информацию - пусть выводит
        # TODO Счёт же ведите в другом.
        if self.prev_day == -1:  # TODO В первый день выходит шифт сработает и тут...
            self.shift()
        elif last:
            self.sort()
            print(self.print_line)
        elif self.condition:  # TODO первая дата (например 14 число) не попадает сюда
            print(self.print_line)  # TODO Печатается дата после смены (15 число) и счетчик.нок для 14-ого числа
            self.nok_counter, self.ok_counter = 0, 0
        elif self.log_status == 'NOK':
            self.nok_counter += 1
        elif self.log_status == 'OK':
            self.ok_counter += 1
        self.shift()  # TODO ...И тут?

    def shift(self):
        self.prev_year, self.prev_month, self.prev_day, self.prev_hour, self.prev_min =\
            self.log_year, self.log_month, self.log_day, self.log_hour, self.log_min


#
log_file = 'events.txt'
action = LogParser(file_name=log_file)
action.parse(2)
# ok_counter = 0
# nok_counter = 0
# prev_hour = -1
# prev_min = -1
# prev_date = -1
#
# TODO Запись в файл оформить в виде метода класса
# TODO И попроще - метод получает строку - пишет её в файл.
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
