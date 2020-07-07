# -*- coding: utf-8 -*-

# Подземелье было выкопано ящеро-подобными монстрами рядом с аномальной рекой, постоянно выходящей из берегов.
# Из-за этого подземелье регулярно затапливается, монстры выживают, но не герои, рискнувшие спуститься к ним в поисках
# приключений.
# Почуяв безнаказанность, ящеры начали совершать набеги на ближайшие деревни. На защиту всех деревень не хватило
# солдат и вас, как известного в этих краях героя, наняли для их спасения.
#
# Карта подземелья представляет собой json-файл под названием rpg.json. Каждая локация в лабиринте описывается объектом,
# в котором находится единственный ключ с названием, соответствующем формату "Location_<N>_tm<T>",
# где N - это номер локации (целое число), а T (вещественное число) - это время,
# которое необходимо для перехода в эту локацию. Например, если игрок заходит в локацию "Location_8_tm30000",
# то он тратит на это 30000 секунд.
# По данному ключу находится список, который содержит в себе строки с описанием монстров а также другие локации.
# Описание монстра представляет собой строку в формате "Mob_exp<K>_tm<M>", где K (целое число) - это количество опыта,
# которое получает игрок, уничтожив данного монстра, а M (вещественное число) - это время,
# которое потратит игрок для уничтожения данного монстра.
# Например, уничтожив монстра "Boss_exp10_tm20", игрок потратит 20 секунд и получит 10 единиц опыта.
# Гарантируется, что в начале пути будет две локации и один монстр
# (то есть в коренном json-объекте содержится список, содержащий два json-объекта, одного монстра и ничего больше).
#
# На прохождение игры игроку дается 123456.0987654321 секунд.
# Цель игры: за отведенное время найти выход ("Hatch")
#
# По мере прохождения вглубь подземелья, оно начинает затапливаться, поэтому
# в каждую локацию можно попасть только один раз,
# и выйти из нее нельзя (то есть двигаться можно только вперед).
#
# Чтобы открыть люк ("Hatch") и выбраться через него на поверхность, нужно иметь не менее 280 очков опыта.
# Если до открытия люка время заканчивается - герой задыхается и умирает, воскрешаясь перед входом в подземелье,
# готовый к следующей попытке (игра начинается заново).
#
# Гарантируется, что искомый путь только один, и будьте аккуратны в рассчетах!
# При неправильном использовании библиотеки decimal человек, играющий с вашим скриптом рискует никогда не найти путь.
#
# Также, при каждом ходе игрока ваш скрипт должен запоминать следущую информацию:
# - текущую локацию
# - текущее количество опыта
# - текущие дату и время (для этого используйте библиотеку datetime)
# После успешного или неуспешного завершения игры вам необходимо записать
# всю собранную информацию в csv файл dungeon.csv.
# Названия столбцов для csv файла: current_location, current_experience, current_date
#
#
# Пример взаимодействия с игроком:
#
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
# Прошло времени: 00:00
#
# Внутри вы видите:
# — Вход в локацию: Location_1_tm1040
# — Вход в локацию: Location_2_tm123456
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Сдаться и выйти из игры
#
# Вы выбрали переход в локацию Location_2_tm1234567890
#
# Вы находитесь в Location_2_tm1234567890
# У вас 0 опыта и осталось 0.0987654321 секунд до наводнения
# Прошло времени: 20:00
#
# Внутри вы видите:
# — Монстра Mob_exp10_tm10
# — Вход в локацию: Location_3_tm55500
# — Вход в локацию: Location_4_tm66600
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Сдаться и выйти из игры
#
# Вы выбрали сражаться с монстром
#
# Вы находитесь в Location_2_tm0
# У вас 10 опыта и осталось -9.9012345679 секунд до наводнения
#
# Вы не успели открыть люк!!! НАВОДНЕНИЕ!!! Алярм!
#
# У вас темнеет в глазах... прощай, принцесса...
# Но что это?! Вы воскресли у входа в пещеру... Не зря матушка дала вам оберег :)
# Ну, на этот-то раз у вас все получится! Трепещите, монстры!
# Вы осторожно входите в пещеру... (текст умирания/воскрешения можно придумать свой ;)
#
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
# Прошло уже 0:00:00
# Внутри вы видите:
#  ...
#  ...
#
# и так далее...

import json
import re
from datetime import datetime
from decimal import Decimal
import csv

remaining_time = '123456.0987654321'
# если изначально не писать число в виде строки - теряется точность!
field_names = ['current_location', 'current_experience', 'current_date']


# Учитывая время и опыт, не забывайте о точности вычислений!

class RpgGame:

    def __init__(self):
        self.dungeon_file = "python_base/lesson_015/rpg.json"
        self.exp = 0
        self.position = None
        self.remaining_time = Decimal(remaining_time)
        self.values = None
        self.re_exp = r'exp(\d+)'
        self.re_time = r'tm(\d+)'
        self.log_buffer = []

    def log_to_csv(self):
        with open('python_base/lesson_015/dungeon.csv', 'w', newline='') as out_csv:
            writer = csv.DictWriter(out_csv, delimiter=',', fieldnames=field_names)
            writer.writeheader()
            writer.writerows(self.log_buffer[0])

    def log_to_buffer(self, location, experience, date):
        event_list = [{field_names[0]: location, field_names[1]: experience, field_names[2]: date}]
        self.log_buffer.append(event_list)

    def get_dungeon(self):
        with open(self.dungeon_file, 'r') as read_file:
            loaded_dungeon = json.load(read_file)
        return loaded_dungeon

    def get_position(self, dungeon):
        self.position = list(dungeon.keys())[0]
        self.values = list(dungeon.values())[0]
        return self.position, self.values

    def get_option_list(self, actions):
        room_list = []
        mob_list = []
        for i in actions:
            if type(i) is str:
                mob_list.append(i)
            elif type(i) is dict:
                room_list.append(str(list(i.keys())[0]))
        return mob_list, room_list

    def print_position(self):
        print(f'Вы находитесь в {self.position}\n'
              f'У вас {self.exp} опыта и осталось {self.remaining_time} секунд до наводнения'
              f'Прошло уже 0:00:00')
        if self.remaining_time < 0:
            self.death("time")
        self.log_to_buffer(self.position, self.exp, str(datetime.now()))

    def print_option_list(self, mob_list, room_list):
        self.print_position()
        print("Внутри вы видите:")
        if len(mob_list) > 0:
            for mob in mob_list:
                print(f' — Монстра {mob}')
        for room in room_list:
            print(f' — Вход в локацию:{room}')

    def fight_mob(self, mob_list):
        kill_mob = mob_list.pop()
        self.exp += int(re.search(self.re_exp, kill_mob)[1])
        self.remaining_time -= Decimal(re.search(self.re_time, kill_mob)[1])
        return mob_list

    def action(self, mob_list, room_list):
        if len(mob_list) > 0:
            act = input('Выберите действие:\n'
                        '1.Атаковать монстра\n'
                        '2.Перейти в другую локацию\n'
                        '3.Сдаться и выйти из игры\n')
            if act == "1":
                mob_list = self.fight_mob(mob_list)
                self.print_option_list(mob_list, room_list)
                self.action(mob_list, room_list)
                print("out of range")
            elif act == "2":
                self.change_room(room_list)
            elif act == "3":
                self.death()
            else:
                print("wrong command")
                self.action(mob_list, room_list)
        else:
            act = input('Выберите действие:\n'
                        '1.Перейти в другую локацию\n'
                        '2.Сдаться и выйти из игры\n')
            if act == "1":
                self.change_room(room_list)
            elif act == "2":
                self.death()
            else:
                print("wrong command")
                self.action(mob_list, room_list)

    def change_room(self, rooms):
        index = 1
        if len(rooms) == 1 and rooms[0] == "Hatch_tm159.098765432":
            if self.exp < 280:
                self.death("exp")
            else:
                for val in self.values:
                    if type(val) is dict:
                        print(val.get(rooms[0]))
                        self.log_to_csv()
                        exit(0)
        elif len(rooms) == 1:
            self.position = rooms[0]
        elif len(rooms) == 0:
            self.death("dead end")
        else:
            print('Выберите комнату')
            for room in rooms:
                print(f'{index}. {room}')
                index += 1
            choose_index = input()
            if int(choose_index) and len(rooms) >= int(choose_index) > 0:
                self.position = rooms[int(choose_index) - 1]
            else:
                print("wrong command")
                self.change_room(rooms)
        self.remaining_time -= Decimal(re.search(self.re_time, self.position)[1])
        for item in self.values:
            if type(item) is dict and list(item.keys())[0] is self.position:
                self.values = item
        pos, val = self.get_position(self.values)
        mob_list, room_list = self.get_option_list(val)
        self.print_option_list(mob_list, room_list)
        self.action(mob_list, room_list)

    def death(self, reason=None):
        self.log_to_csv()
        if reason == "exp":
            print("Недостаточно опыта для открытия люка")
        elif reason == "time_off":
            print("Время вышло. Воздух тоже")
        elif reason == "dead end":
            print("Тут тупик, деваться некуда")
        else:
            print("Удачно упавший камень с потолка заканчивает ваш рейд")
            exit(0)
        self.resurrection()

    def resurrection(self):
        print("Вас благополучно воскресили, не спрашивайте как.")
        self.log_buffer = []
        self.start()

    def start(self):
        dungeon = self.get_dungeon()
        self.position, self.values = self.get_position(dungeon)
        mobs, rooms = self.get_option_list(self.values)
        self.print_option_list(mobs, rooms)
        self.action(mobs, rooms)


RpgGame().start()
