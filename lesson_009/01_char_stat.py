# -*- coding: utf-8 -*-

# Подсчитать статистику по буквам в романе Война и Мир.
# Входные параметры: файл для сканирования
# Статистику считать только для букв алфавита (см функцию .isalpha() для строк)
#
# Вывести на консоль упорядоченную статистику в виде
# +---------+----------+
# |  буква  | частота  |
# +---------+----------+
# |    А    |   77777  |
# |    Б    |   55555  |
# |   ...   |   .....  |
# |    a    |   33333  |
# |    б    |   11111  |
# |   ...   |   .....  |
# +---------+----------+
# |  итого  | 9999999  |
# +---------+----------+
#
# Упорядочивание по частоте - по убыванию. Ширину таблицы подберите по своему вкусу
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.
import os
import zipfile


class TextAnalyse:

    def __init__(self, path_to_file):
        self.result = []
        self.file_name = path_to_file
        self.stat = {}
        self.sorted_stat = []
        self.spacer = '+{txt:-^21}+'.format(txt='+')

    def start_analyze(self, sort_type=0, sort_reverse=False):
        self.open_file()
        self.sort_lines(sort_type=sort_type, reverse=sort_reverse)
        self.print_result()

    def unzip(self, source_file_name, destination_file_name=None):
        if self.file_name.endswith('.zip'):
            zfile = zipfile.ZipFile(source_file_name, 'r')
            unzipped_file = None
            for filename in zfile.namelist():
                zfile.extract(filename, path=destination_file_name)
                if destination_file_name:
                    unzipped_file = filename
                else:
                    unzipped_file = os.path.join(os.path.dirname(source_file_name), filename)
            return unzipped_file
        else:
            return self.file_name

    def open_file(self):
        file_to_open = self.unzip(source_file_name=self.file_name)
        with open(file_to_open, 'r', encoding='cp1251') as file:
            for line in file:
                self._get_stat(line=line[:-1])

    def sort_lines(self, sort_type, reverse):
        if sort_type == 0:
            self.sorted_stat = sorted(self.stat.items(), key=lambda x: x[1])
        elif sort_type == 1:
            self.sorted_stat = sorted(self.stat.items(), key=lambda x: x[1], reverse=reverse)
        elif sort_type == 2:
            self.sorted_stat = sorted(self.stat.items(), key=lambda x: x[0])
        elif sort_type == 3:
            self.sorted_stat = sorted(self.stat.items(), key=lambda x: x[0], reverse=reverse)
        else:
            print(sort_type, 'not supported')

    def print_result(self):
        print(self.spacer)
        print('|{txt0:^10}|{txt1:^10}|'.format(txt0='буква', txt1='количество'))
        print(self.spacer)
        for char in self.sorted_stat:
            print('|{txt0:^10}|{txt1:^10}|'.format(txt0=char[0], txt1=char[1]))
        print(self.spacer)

    def _get_stat(self, line):
        for char in line:
            if char.isalpha():
                if char in self.stat:
                    self.stat[char] += 1
                else:
                    self.stat[char] = 1
            else:
                continue


analyse = TextAnalyse(path_to_file='python_snippets\\voyna-i-mir.txt.zip')
analyse.start_analyze()
# После выполнения первого этапа нужно сделать упорядочивание статистики
#  - по частоте по возрастанию
#  - по алфавиту по возрастанию
#  - по алфавиту по убыванию
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828
#зачет!