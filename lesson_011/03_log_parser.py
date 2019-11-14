# -*- coding: utf-8 -*-

# На основе своего кода из lesson_009/02_log_parser.py напишите итератор (или генератор)
# котрый читает исходный файл events.txt и выдает число событий NOK за каждую минуту
# <время> <число повторений>
#
# пример использования:
#
# grouped_events = <создание итератора/генератора>
# for group_time, event_count in grouped_events:
#     print(f'[{group_time}] {event_count}')
#
# на консоли должно появится что-то вроде
#
# [2018-05-17 01:57] 1234
import re


def open_file(file):
    with open(file, 'r') as file:
        for line in file:
            yield line


def get_data():
    lines = open_file('events.txt')
    counter = 0
    prev_date = None
    for line in lines:
        if re.match("^\[.*\]\s\D*", line):
            line = line.split("] ")
            date = re.sub(":\d\d\\.\d{6}", "", line[0] + "]")
            state = line[1]
            if prev_date is None:
                if state.startswith("NOK"):
                    counter += 1
                prev_date = date
                continue
            if prev_date != date:
                yield prev_date, counter
                counter = 0
                if state.startswith("NOK"):
                    counter += 1
            else:
                if state.startswith("NOK"):
                    counter += 1
            prev_date = date
    yield prev_date, counter


arr = get_data()
for a, b in arr:
    print(a, b)
