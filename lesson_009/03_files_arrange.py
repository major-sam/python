# -*- coding: utf-8 -*-

import datetime
import os
import shutil
# Нужно написать скрипт для упорядочивания фотографий (вообще любых файлов)
# Скрипт должен разложить файлы из одной папки по годам и месяцам в другую.
# Например, так:
#   исходная папка
#       icons/cat.jpg
#       icons/man.jpg
#       icons/new_year_01.jpg
#   результирующая папка
#       icons_by_year/2018/05/cat.jpg
#       icons_by_year/2018/05/man.jpg
#       icons_by_year/2017/12/new_year_01.jpg
#
# Входные параметры основной функции: папка для сканирования, целевая папка.
# Имена файлов в процессе работы скрипта не менять, год и месяц взять из времени создания файла.
# Обработчик файлов делать в обьектном стиле - на классах.
#
# Файлы для работы взять из архива icons.zip - раззиповать проводником в папку icons перед написанием кода.
# Имя целевой папки - icons_by_year (тогда она не попадет в коммит)
#
# Пригодятся функции:
#   os.walk
#   os.path.dirname
#   os.path.join
#   os.path.normpath
#   os.path.getmtime
#   time.gmtime
#   os.makedirs
#   shutil.copy2
#
# Чтение документации/гугла по функциям - приветствуется. Как и поиск альтернативных вариантов :)
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.
import zipfile


class HomeLib:

    def __init__(self, filename):
        self.file_name = filename

    def unzip_file(self):
        with zipfile.ZipFile(self.file_name, 'r') as zfile:
            for info in zfile.infolist():
                if info.is_dir():
                    continue
                zfile.extract(info)
                file_name = os.path.basename(info.filename)
                creation_date = datetime.datetime(*info.date_time)
                source_file = info.filename
                destination_file = os.path.normpath(f'icons_by_year\\{creation_date.year}\\{creation_date.month}\\{file_name}')
                os.makedirs(destination_file, exist_ok=True)
                shutil.copy2(source_file, destination_file)

    def unzip(self):
        with zipfile.ZipFile(self.file_name, 'r') as zfile:
            for info in zfile.infolist():
                if info.is_dir():
                    continue
                file_name = os.path.basename(info.filename)
                creation_date = datetime.datetime(*info.date_time)
                source = zfile.open(info)
                destination_file = os.path.normpath(f'icons_by_year\\{creation_date.year}\\{creation_date.month}\\{file_name}')
                destination_path = os.path.normpath(f'icons_by_year\\{creation_date.year}\\{creation_date.month}\\')
                os.makedirs(destination_path, exist_ok=True)
                with open(destination_file, 'wb') as destination:
                    with source, destination:
                        shutil.copyfileobj(source, destination)


lib = HomeLib('icons.zip')
lib.unzip()
# lib.unzip_file()
# Усложненное задание (делать по желанию)  TODO С этим справились отлично! :)
# Нужно обрабатывать zip-файл, содержащий фотографии, без предварительного извлечения файлов в папку.
# Основная функция должна брать параметром имя zip-файла и имя целевой папки.
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828
