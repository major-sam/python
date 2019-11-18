# -*- coding: utf-8 -*-


# Описание предметной области:
#
# При торгах на бирже совершаются сделки - один купил, второй продал.
# Покупают и продают ценные бумаги (акции, облигации, фьючерсы, етс). Ценные бумаги - это по сути долговые расписки.
# Ценные бумаги выпускаются партиями, от десятка до несколько миллионов штук.
# Каждая такая партия (выпуск) имеет свой торговый код на бирже - тикер - https://goo.gl/MJQ5Lq
# Все бумаги из этой партии (выпуска) одинаковы в цене, поэтому говорят о цене одной бумаги.
# У разных выпусков бумаг - разные цены, которые могут отличаться в сотни и тысячи раз.
# Каждая биржевая сделка характеризуется:
#   тикер ценнной бумаги
#   время сделки
#   цена сделки
#   обьем сделки (сколько ценных бумаг было куплено)
#
# В ходе торгов цены сделок могут со временем расти и понижаться. Величина изменения цен называтея волатильностью.
# Например, если бумага №1 торговалась с ценами 11, 11, 12, 11, 12, 11, 11, 11 - то она мало волатильна.
# А если у бумаги №2 цены сделок были: 20, 15, 23, 56, 100, 50, 3, 10 - то такая бумага имеет большую волатильность.
# Волатильность можно считать разными способами, мы будем считать сильно упрощенным способом -
# отклонение в процентах от средней цены за торговую сессию:
#   средняя цена = (максимальная цена + минимальная цена) / 2
#   волатильность = ((максимальная цена - минимальная цена) / средняя цена) * 100%
# Например для бумаги №1:
#   average_price = (12 + 11) / 2 = 11.5
#   volatility = ((12 - 11) / average_price) * 100 = 8.7%
# Для бумаги №2:
#   average_price = (100 + 3) / 2 = 51.5
#   volatility = ((100 - 3) / average_price) * 100 = 188.34%
#
# В реальности волатильность рассчитывается так: https://goo.gl/VJNmmY
#
# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью.
# Бумаги с нулевой волатильностью вывести отдельно.
# Результаты вывести на консоль в виде:
#   Максимальная волатильность:
#       ТИКЕР1 - ХХХ.ХХ %
#       ТИКЕР2 - ХХХ.ХХ %
#       ТИКЕР3 - ХХХ.ХХ %
#   Минимальная волатильность:
#       ТИКЕР4 - ХХХ.ХХ %
#       ТИКЕР5 - ХХХ.ХХ %
#       ТИКЕР6 - ХХХ.ХХ %
#   Нулевая волатильность:
#       ТИКЕР7, ТИКЕР8, ТИКЕР9, ТИКЕР10, ТИКЕР11, ТИКЕР12
# Волатильности указывать в порядке убывания. Тикеры с нулевой волатильностью упорядочить по имени.
#
# Подготовка исходных данных
# 1. Скачать файл https://drive.google.com/file/d/1l5sia-9c-t91iIPiGyBc1s9mQ8RgTNqb/view?usp=sharing
#       (обратите внимание на значок скачивания в правом верхнем углу,
#       см https://drive.google.com/file/d/1M6mW1jI2RdZhdSCEmlbFi5eoAXOR3u6G/view?usp=sharing)
# 2. Раззиповать средствами операционной системы содержимое архива
#       в папку python_base_source/lesson_012/trades
# 3. В каждом файле в папке trades содержится данные по сделакам по одному тикеру, разделенные запятыми.
#   Первая строка - название колонок:
#       SECID - тикер
#       TRADETIME - время сделки
#       PRICE - цена сделки
#       QUANTITY - количество бумаг в этой сделке
#   Все последующие строки в файле - данные о сделках
#
# Подсказка: нужно последовательно открывать каждый файл, вычитывать данные, высчитывать волатильность и запоминать.
# Вывод на консоль можно сделать только после обработки всех файлов.
#
# Для плавного перехода к мультипоточности, код оформить в обьектном стиле, используя следующий каркас
#
# class <Название класса>:
#
#     def __init__(self, <параметры>):
#         <сохранение параметров>
#
#     def run(self):
#         <обработка данных>
import itertools
import os
import statistics


class TickerClass:

    def __init__(self):
        self.source_folder = 'trades'
        self.bad_big_dictionary = {}
        self.sec_id_volatility = {}

    def list_files(self):
        for file in os.listdir(self.source_folder):
            yield os.path.join(self.source_folder, file)

    def read_file(self, file):
        with open(file, 'r') as file:
            file.readline()
            for line in file:
                yield line

    def get_data(self):
        files = self.list_files()
        for file in files:
            lines = self.read_file(file)
            for line in lines:
                line_to_arr = line.replace("\n", "").split(",")
                sec_id, trade_time, price, quantity = line_to_arr
                if self.bad_big_dictionary.get(sec_id) is None:
                    # print(f'found {sec_id}')
                    self.bad_big_dictionary[sec_id] = [[trade_time], [price], [int(quantity)]]
                else:
                    self.bad_big_dictionary[sec_id][0].append(trade_time)
                    self.bad_big_dictionary[sec_id][1].append(price)
                    self.bad_big_dictionary[sec_id][2].append(quantity)
            # print(f'scan {file}\n')

    def do_math(self):
        my_dict = self.bad_big_dictionary
        for key in my_dict.keys():
            # print(f'do math for {key}')
            min_val = min(float(sub) for sub in my_dict.get(key)[1])
            max_val = max(float(sub) for sub in my_dict.get(key)[1])
            mean_val = float("%.2f" % statistics.mean((float(sub) for sub in my_dict.get(key)[1])))
            volatility = ((max_val - min_val) * 100) / mean_val
            self.sec_id_volatility[key] = volatility

    def do_sort_and_print(self):
        data = self.sec_id_volatility
        zero_data = [k for k, v in data.items() if v == 0]
        data_sorted_min = {k: v for k, v in sorted(data.items(), key=lambda x: x[1]) if v != 0}
        out_min = dict(itertools.islice(data_sorted_min.items(), 3))
        data_sorted_max = {k: v for k, v in sorted(data.items(), key=lambda x: x[1], reverse=True)}
        out_max = dict(itertools.islice(data_sorted_max.items(), 3))
        print("\n\r+++++++++++++++++++++++++++++++\n\r   Максимальная волатильность:")
        for key, value in out_max.items():
            print(f'{key}  :  {value}  %')

        print("   Минимальная волатильность:")
        for key, value in out_min.items():
            print(f'{key}  :  {value}  %')
        print("Нулевая волатильность")
        print(', '.join(zero_data))

    def run(self):
        self.get_data()
        self.do_math()
        self.do_sort_and_print()


TickerClass().run()
# Возможно ли вместо словаря использовать объекты класса? у меня получилось только создавать объекты и складывать
# ссылки на них в список. При попытки вытащить их - начинался бардак.

# Не очень понял, по сути вы можете написать Класс, похожий на словарь :) и его использовать, так что ответ да, возможно

# оставил на словаре - гдето на stackoverflow замеряли время между заполнением словаря и созданием объектов
# - словарь оказался бысрее на 15%
#зачет!