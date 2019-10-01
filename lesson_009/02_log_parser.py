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
        self.print_line, self.condition = None, None
        self.file = file_name
        self.out_file = None
        self.ok_counter, self.nok_counter, self.sort_lvl, self.log_status = 0, 0, 0, 0
        self.current_date_status = {'year': 0,
                                    'month': 0,
                                    'day': 0,
                                    'hour': 0,
                                    'min': 0
                                    }
        self.previous_date_status = {'year': None,
                                     'month': None,
                                     'day': None,
                                     'hour': None,
                                     'min': None
                                     }

    def parse(self, sort_lvl='min', out_file='res.txt', date_separator='-', time_separator=':'):
        self.out_file = out_file
        match_param = self._get_match_params(sort_lvl)
        self.clear_result_file(out_file)
        lines = self.open_file()
        for line in lines:
            split_line = self.split_line_by_special_char_and_spaces(line)
            self.split_line_to_dict(split_line, date_separator, time_separator)
            self.match_prev_line(condition=match_param, sort_lvl=sort_lvl)
        self.match_prev_line(condition=match_param, sort_lvl=sort_lvl, last=True)

    def open_file(self):
        with open(self.file, 'r') as file:
            for line in file:
                yield line

    @staticmethod
    def clear_result_file(out_file):
        with open(out_file, 'w') as file:
            file.truncate(0)

    @staticmethod
    def write_result_to_file(out_file, line):
        with open(out_file, 'a+') as file:
            file.write(line + '\n')

    @staticmethod
    def split_line_by_special_char_and_spaces(line):
        formatted_line = ''.join(char for char in line if char not in '[](){}><\n')
        split_line = formatted_line.split(sep=' ')
        return split_line

    def split_line_to_dict(self, split_line, date_separator, time_separator):
        log_date = split_line[0]
        self.current_date_status['year'] = int(log_date.split(sep=date_separator)[0])
        self.current_date_status['month'] = int(log_date.split(sep=date_separator)[1])
        self.current_date_status['day'] = int(log_date.split(sep=date_separator)[2])
        log_time = split_line[1]
        self.current_date_status['hour'] = int(log_time.split(sep=time_separator)[0])
        self.current_date_status['min'] = int(log_time.split(sep=time_separator)[1])
        self.log_status = split_line[2]

    @staticmethod
    def _get_match_params(sort_lvl):
        if sort_lvl in ['min', 'Min', 'MIN', 'minute']:
            _condition = 'min'
        elif sort_lvl in ['hour', 'Hour', 'HOUR', 'h', 'H']:  # hour
            _condition = 'hour'
        elif sort_lvl in ['day', 'Day', 'DAY', 'd', 'D']:  # day
            _condition = 'day'
        elif sort_lvl in ['month', 'Month', 'MONTH']:  # mouth
            _condition = 'mouth'
        elif sort_lvl in ['year', 'Year', 'YEAR', 'y', 'Y']:  # year
            _condition = 'year'
        else:
            _condition = False
            exit(1)
        return _condition

    def _get_print_params(self, sort_lvl):
        if sort_lvl in ['min', 'Min', 'MIN', 'minute']:
            _print_line = '[{}-{:0>2}-{:0>2} {:0>2}:{:0>2}] {}'.format(self.previous_date_status['year'],
                                                                       self.previous_date_status['month'],
                                                                       self.previous_date_status['day'],
                                                                       self.previous_date_status['hour'],
                                                                       self.previous_date_status['min'],
                                                                       self.nok_counter, )
        elif sort_lvl in ['hour', 'Hour', 'HOUR', 'h', 'H']:
            _print_line = '[{}-{:0>2}-{:0>2} {:0>2}] {}'.format(self.previous_date_status['year'],
                                                                self.previous_date_status['month'],
                                                                self.previous_date_status['day'],
                                                                self.previous_date_status['hour'],
                                                                self.nok_counter, )
        elif sort_lvl in ['day', 'Day', 'DAY', 'd', 'D']:
            _print_line = '[{}-{:0>2}-{:0>2}] {}'.format(self.previous_date_status['year'],
                                                         self.previous_date_status['month'],
                                                         self.previous_date_status['day'],
                                                         self.nok_counter)
        elif sort_lvl in ['month', 'Month', 'MONTH']:
            _print_line = '[{}-{:0>2}] {}'.format(self.previous_date_status['year'],
                                                  self.previous_date_status['month'],
                                                  self.nok_counter)
        elif sort_lvl in ['year', 'Year', 'YEAR', 'y', 'Y']:
            _print_line = '[{}] {}'.format(self.previous_date_status['year'], self.nok_counter)
        else:
            _print_line = 'sort level must be in range from 0 to 4'
            _condition = False
            exit(1)
        return _print_line

    def match_prev_line(self, condition, sort_lvl, last=False):
        if self.previous_date_status[condition] is None:
            self.shift()
        elif last:
            self._print_nok(sort_lvl)
        elif self.previous_date_status[condition] != self.current_date_status[condition]:
            self._print_nok(sort_lvl)
            self.nok_counter = 0
            self.ok_counter = 0
            self.shift()
        if self.log_status == 'NOK':
            self.nok_counter += 1
        elif self.log_status == 'OK':
            self.ok_counter += 1

    def _print_nok(self, sort_lvl):
        line = self._get_print_params(sort_lvl)
        self.write_result_to_file(self.out_file, line)
        print(line + ' NOK of', self.nok_counter + self.ok_counter)

    def shift(self):
        self.previous_date_status = self.current_date_status.copy()


log_file = 'events.txt'
action = LogParser(file_name=log_file)
action.parse(sort_lvl='min')

# После выполнения первого этапа нужно сделать группировку событий
#  - по часам
#  - по месяцу
#  - по году
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828
