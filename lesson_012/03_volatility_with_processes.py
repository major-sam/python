# -*- coding: utf-8 -*-


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПРОЦЕССНОМ стиле
#
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
# -*- coding: utf-8 -*-


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПРОЦЕССНОМ стиле
#
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
import itertools
import os
import statistics
import multiprocessing

from utils import time_track


class TickerClass(multiprocessing.Process):

    def __init__(self, files, query, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sec_id_volatility = {}
        self.ticker_dictionary = {}
        self.files = files
        self.query = query

    def list_files(self, source_folder):
        for file in os.listdir(source_folder):
            file_path = os.path.join(source_folder, file)
            yield file_path, os.path.getsize(file_path)

    def read_file(self, file):
        with open(file, 'r') as file:
            file.readline()
            for line in file:
                yield line

    def get_data(self):
        for file in self.files:
            if file is None:
                break
            lines = self.read_file(file)
            for line in lines:
                sec_id, trade_time, price, quantity = line.replace("\n", "").split(",")
                if self.ticker_dictionary.get(sec_id) is None:
                    self.ticker_dictionary[sec_id] = [[trade_time], [price], [int(quantity)]]
                else:
                    self.ticker_dictionary[sec_id][0].append(trade_time)
                    self.ticker_dictionary[sec_id][1].append(price)
                    self.ticker_dictionary[sec_id][2].append(quantity)

    def do_math(self):
        sec_id_volatility = {}
        for key in self.ticker_dictionary.keys():
            min_val = min(float(sub) for sub in self.ticker_dictionary.get(key)[1])
            max_val = max(float(sub) for sub in self.ticker_dictionary.get(key)[1])
            mean_val = float("%.2f" % statistics.mean((float(sub) for sub in self.ticker_dictionary.get(key)[1])))
            volatility = ((max_val - min_val) * 100) / mean_val
            sec_id_volatility[key] = volatility
        return sec_id_volatility

    def run(self):
        self.get_data()
        self.sec_id_volatility = {**self.sec_id_volatility, **self.do_math()}
        self.query.put(self.sec_id_volatility)


@time_track
def sort_and_print(data):
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


@time_track
def main():
    queue = multiprocessing.Queue()
    files = TickerClass(None, queue).list_files(source_folder="trades")
    sum_dict = {}
    big_files = []
    small_files = []
    for file in files:
        if file[1] > 1000000:
            big_files.append(file[0])
        else:
            small_files.append(file[0])
    processes = [TickerClass([file, None], queue) for file in big_files]
    multi_file_process = TickerClass(small_files, queue)
    multi_file_process.start()
    multi_file_process.join()
    for proc in processes:
        proc.start()
    for proc in processes:
        proc.join()
    while not queue.empty():
        sum_dict = {**sum_dict, **queue.get()}
    sort_and_print(sum_dict)


if __name__ == '__main__':
    main()
