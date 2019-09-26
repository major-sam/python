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
import zipfile
from pprint import pprint


class TextAnalyse:

    def __init__(self, file_name):
        self.file_name = file_name
        self.stat = {}
        self.sorted_stat = {}

    def unzip(self):
        zfile = zipfile.ZipFile(self.file_name, 'r')
        for filename in zfile.namelist():
            zfile.extract(filename, path='python_snippets\\')
            self.file_name = 'python_snippets\\' + filename
            break  # читаю 1 файл

    def collect(self, sort_type):
        if self.file_name.endswith('.zip'):
            self.unzip()
        with open(self.file_name, 'r', encoding='cp1251') as file:
            for line in file:
                self._get_stat(line=line[:-1])
        if sort_type == 0:
            self.sorted_stat = sorted(self.stat.items(), key=lambda x: x[1])
            return self.sorted_stat
        elif sort_type == 1:
            self.sorted_stat = sorted(self.stat.items(), key=lambda x: x[0])
        elif sort_type == 2:
            self.sorted_stat = sorted(self.stat.items(), key=lambda x: x[0], reverse=True)
            return self.sorted_stat
        else:
            print(sort_type, 'not supported')

    def _get_stat(self, line):
        for char in line:
            if char.isalpha():
                if char in self.stat:
                    self.stat[char] += 1
                else:
                    self.stat[char] = 1
            else:
                continue


analyse = TextAnalyse(file_name='python_snippets\\voyna-i-mir.txt.zip')
res = analyse.collect(sort_type=0)  # или нужно свой алгоритм сортировки реализовать?
pprint(res)

# После выполнения первого этапа нужно сделать упорядочивание статистики
#  - по частоте по возрастанию
#  - по алфавиту по возрастанию
#  - по алфавиту по убыванию
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828
