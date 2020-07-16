# -*- coding: utf-8 -*-

# В очередной спешке, проверив приложение с прогнозом погоды, вы выбежали
# навстречу ревью вашего кода, которое ожидало вас в офисе.
# И тут же день стал хуже - вместо обещанной облачности вас встретил ливень.

# Вы промокли, настроение было испорчено, и на ревью вы уже пришли не в духе.
# В итоге такого сокрушительного дня вы решили написать свою программу для прогноза погоды
# из источника, которому вы доверяете.

# Для этого вам нужно:

# Создать модуль-движок с классом WeatherMaker, необходимым для получения и формирования предсказаний.
# В нём должен быть метод, получающий прогноз с выбранного вами сайта (парсинг + re) за некоторый диапазон дат,
# а затем, получив данные, сформировать их в словарь {погода: Облачная, температура: 10, дата:datetime...}

# Добавить класс ImageMaker.
# Снабдить его методом рисования открытки
# (использовать OpenCV, в качестве заготовки брать lesson_016/python_snippets/external_data/probe.jpg):
#   С текстом, состоящим из полученных данных (пригодится cv2.putText)
#   С изображением, соответствующим типу погоды
# (хранятся в lesson_016/python_snippets/external_data/weather_img ,но можно нарисовать/добавить свои)
#   В качестве фона добавить градиент цвета, отражающего тип погоды
# Солнечно - от желтого к белому
# Дождь - от синего к белому
# Снег - от голубого к белому
# Облачно - от серого к белому

# Добавить класс DatabaseUpdater с методами:
#   Получающим данные из базы данных за указанный диапазон дат.
#   Сохраняющим прогнозы в базу данных (использовать peewee)
# Сделать программу с консольным интерфейсом, постаравшись все выполняемые действия вынести в отдельные функции.
# Среди действий, доступных пользователю, должны быть:
#   Добавление прогнозов за диапазон дат в базу данных
#   Получение прогнозов за диапазон дат из базы
#   Создание открыток из полученных прогнозов
#   Выведение полученных прогнозов на консоль
# При старте консольная утилита должна загружать прогнозы за прошедшую неделю.

import argparse
import json
import re
import os
import datetime
from pprint import pprint
import DatabaseUpdater
from ImageMaker import ImageMaker
import pandas as pd

date, day, day_temperature, day_sky, day_temperature_fill, day_rain_prob, day_pressure, day_humidity = [None] * 8
data, night, night_temperature, night_sky, night_temperature_fill, night_rain_prob, night_pressure, night_humidity \
    = [None] * 8


def parse_stats(input_data):
    """
    :param input_data: str matched \w+:\(\w+,[\+-]\d+\)
    :return: list len 6
    """
    lst = ["Нет данных"] * 6
    res = re.sub('[()]', '', input_data.split(":")[1]).split(",")
    for i in range(0, len(res)):
        lst[i] = res[i]
    return lst


def run_a(namespace):
    file = namespace[0]
    console_data = None
    if os.path.isfile(file):
        print("data in file %s must be json like test.json file" % my_namespace.a[0])
        with open(file, 'r', encoding='utf8') as file:
            s = file.read()
            console_data = json.loads(s)
    elif len(my_namespace.a) == 3:
        date_input, day_input, night_input = list(my_namespace.a)
        date_match = re.match(r"\d\d\d\d-\d\d-\d\d", date_input)
        day_match = re.match(r"\w+:\(\w+,[\+-]\d+\)", day_input)
        night_match = re.match(r"\w+:\(\w+,[\+-]\d+\)", night_input)
        if day_match is None or date_match is None or night_match is None:
            print("чтото не так")
        else:
            print(f"date: \t{date_input}\nday: \t{day_input}\nnight: \t{night_input}")
            console_a_date = date_input
            a_day_sky, a_day_temperature, a_day_temperature_fill, a_day_pressure, a_day_rain_prob, a_day_humidity \
                = parse_stats(day_input)
            a_night_sky, a_night_temperature, a_night_temperature_fill, a_night_pressure, \
                a_night_rain_prob, a_night_humidity = parse_stats(night_input)
            console_data = {console_a_date: [
                {'День': {'temperature': a_day_temperature,
                          'sky': a_day_sky,
                          'temperature_feeling': a_day_temperature_fill,
                          'rain_probability': a_day_rain_prob,
                          'pressure': a_day_pressure,
                          'humidity': a_day_humidity},
                 'Ночь': {'temperature': a_night_temperature,
                          'sky': a_night_sky,
                          'temperature_feeling': a_night_temperature_fill,
                          'rain_probability': a_night_rain_prob,
                          'pressure': a_night_pressure,
                          'humidity': a_night_humidity}
                 }]}
    else:
        print("чтото не так")
    DatabaseUpdater.save_data(console_data)


def run_g(date_range):
    start_y, start_m, start_d = date_range[0].split("-")
    end_y, end_m, end_d = date_range[1].split("-")
    start_date = datetime.date(int(start_y), int(start_m), int(start_d))
    end_date = datetime.date(int(end_y), int(end_m), int(end_d))
    date_list = pd.date_range(start_date, end_date).to_pydatetime().tolist()
    print(date_list)
    date_formatted_list = []
    for _date in date_list:
        if _date.day < 10:
            day_str = "0" + str(_date.day)
        else:
            day_str = str(_date.day)
        if _date.month < 10:
            month_str = "0" + str(_date.month)
        else:
            month_str = str(_date.month)
        _date_str = f"{str(_date.year)}-{month_str}-{day_str}"
        date_formatted_list.append(_date_str)
    run_p(date_formatted_list)


def run_c(input_data):
    forecast = DatabaseUpdater.get_data(input_data)
    stats_list = forecast.get(input_data[0])
    if stats_list[0] is None and stats_list[1] is None:
        print(f"no forecast for {input_data[0]}")
    else:
        ImageMaker().make_card(input_data[0])


def run_p(input_data):
    forecast = DatabaseUpdater.get_data([input_data])
    stats_list = forecast.get(input_data)
    if stats_list[0] is None and stats_list[1] is None:
        print(f"no forecast for{input_data}")
    else:
        pprint(forecast)


parser = argparse.ArgumentParser()
parser.add_argument('--a', help='add weather forecast to db'
                                '(format: yyyy-mm-dd day:(sunny,+10,+10,777,62,52) night:(clouds,-10,+10,777,62,52)'
                                ' weather params order: SKY,TEMPERATURE,TEMPERATURE_FILLING(OPTIONAL),'
                                'PRESSURE(OPTIONAL),RAIN_PROBABILITY(OPTIONAL),HUMIDITY(OPTIONAL))'
                                ' or put path to json file', required=False, nargs=argparse.REMAINDER)
parser.add_argument('--g', help='get weather forecast(format yyyy-mm-dd)', required=False, nargs='+')
parser.add_argument('--c', help='get card(format yyyy-mm-dd yyyy-mm-dd)', required=False, nargs='+')
parser.add_argument('--p', help='print weather forecast(format yyyy-mm-dd)', required=False, nargs='+')
my_namespace = parser.parse_args('--a lesson_016/test.json'.split())
# my_namespace = parser.parse_args('--a 1234-12-12 aaa:(sasa,+10) nnnn:(cdcdc,-10)'.split())
# my_namespace = parser.parse_args('--p 2020-07-14'.split())
# my_namespace = parser.parse_args('--g 2020-07-14 2020-07-16'.split())
# my_namespace = parser.parse_args('--c 2020-07-16'.split())
# my_namespace = parser.parse_args()
if my_namespace.a is not None:
    run_a(my_namespace.a)
elif my_namespace.g is not None:
    run_g(my_namespace.g)
elif my_namespace.c is not None:
    run_c(my_namespace.c)
elif my_namespace.p is not None:
    run_p(my_namespace.p)
else:
    print("please use help и консоль пашет только из корневого каталога")

# Рекомендации:
# Можно создать отдельный модуль для инициализирования базы данных.
# Как далее использовать эту базу данных в движке:
# Передавать DatabaseUpdater url-путь
# https://peewee.readthedocs.io/en/latest/peewee/playhouse.html#db-url
# Приконнектится по полученному url-пути к базе данных
# Инициализировать её через DatabaseProxy()
# https://peewee.readthedocs.io/en/latest/peewee/database.html#dynamically-defining-a-database
