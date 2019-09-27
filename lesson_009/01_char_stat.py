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


class TextAnalyse:

    def __init__(self, file_name):
        self.result = []
        self.file_name = file_name  # TODO Чтобы не путаться - назовите путь_к_файлу
        self.stat = {}
        self.sorted_stat = []
        self.spacer = '+{txt:-^21}+'.format(txt='+')

    def unzip(self):  # TODO Было бы лучше, если бы этот метод получал два пути
        # TODO Один путь к архиву, другой - место назначения.
        zfile = zipfile.ZipFile(self.file_name, 'r')
        for filename in zfile.namelist():
            zfile.extract(filename, path='\\python_snippets\\')
            # TODO строка выдает ошибку, лишние "\\" перед пайтон сниппетс
            # TODO С путями много проблем, особенно из-за различий в ОС-и. В данном случае проще
            self.file_name = 'python_snippets\\' + filename  # TODO Тогда и тут путь будет без пайтон_сниппетс
            break  # читаю 1 файл

    def collect(self, sort_type):
        if self.file_name.endswith('.zip'):
            self.unzip()
        with open(self.file_name, 'r', encoding='cp1251') as file:
            # TODO Всю конструкцию, касающуюся получения данных из файлов - в один метод
            # TODO И назвать как-нибудь вроде чтение_файла, вместо анзип.
            # TODO Если методу даём зип - делается анзип, читается файл
            # TODO Открыли файл - прочли - вернули его ретурном
            # TODO Или можно yield-ом возвращать по одной линии
            for line in file:
                self._get_stat(line=line[:-1])
        if sort_type == 0:  # TODO Сортировку вынести в отдельный метод
            # TODO А где сортировка по частоте - по убыванию?
            self.sorted_stat = sorted(self.stat.items(), key=lambda x: x[1])
            return self.sorted_stat
        elif sort_type == 1:
            self.sorted_stat = sorted(self.stat.items(), key=lambda x: x[0])
        elif sort_type == 2:
            self.sorted_stat = sorted(self.stat.items(), key=lambda x: x[0], reverse=True)  # TODO в reverse
            # TODO Можно передать значение параметром:
            # TODO сортировка(по_алфавиту/по-частоте, reverse=True/False)
            return self.sorted_stat
        else:
            print(sort_type, 'not supported')

    def printresult(self, sort_type):  # TODO Тут бы в названии "_" не помешал
        self.collect(sort_type=sort_type)
        print(self.spacer)
        print('|{txt0:^10}|{txt1:^10}|'.format(txt0='буква', txt1='количество'))
        print(self.spacer)
        for i in range(len(self.sorted_stat)):  # TODO почему не for stat in self.sorted_stat:
            # TODO stat[0] & stat[1] были бы - красивее же
            print('|{txt0:^10}|{txt1:^10}|'.format(txt0=self.sorted_stat[i][0], txt1=self.sorted_stat[i][1]))
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


analyse = TextAnalyse(file_name='python_snippets\\voyna-i-mir.txt.zip')
analyse.printresult(sort_type=1)  # или нужно свой алгоритм сортировки реализовать?
# После выполнения первого этапа нужно сделать упорядочивание статистики
#  - по частоте по возрастанию
#  - по алфавиту по возрастанию
#  - по алфавиту по убыванию
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828
