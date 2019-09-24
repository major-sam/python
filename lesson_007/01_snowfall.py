# -*- coding: utf-8 -*-

import simple_draw as sd


# Шаг 1: Реализовать падение снежинки через класс. Внести в методы:
#  - создание снежинки с нужными параметрами
#  - отработку изменений координат
#  - отрисовку


class Snowflake:
    def __init__(self):
        self.snowflake_size = sd.random_number(10, 20)
        self.snowflake_y = sd.random_number(500, 790)
        self.snowflake_x = sd.random_number(10, 590)
        self.snowflake_color = sd.COLOR_WHITE

    def __del__(self):
        print('')

    def draw(self, color=sd.COLOR_WHITE):
        if self.can_fall():
            self.snowflake_color = color
            flake_center = sd.Point(self.snowflake_x, self.snowflake_y)
            sd.snowflake(flake_center, self.snowflake_size, self.snowflake_color)
        # если не могут упасть то экземпляр объекта удаляется

    def move(self):
        self.snowflake_x -= sd.random_number(-10, 10)
        self.snowflake_y -= sd.random_number(1, 15)
        if self.snowflake_size > self.snowflake_y:
            self.snowflake_y = self.snowflake_size

    def can_fall(self):
        return self.snowflake_y > self.snowflake_size

    def clear_previous_picture(self):
        return self.draw(color=sd.background_color)


def get_flakes(count):
    flake_list = []
    for new_flake in range(count):
        new_flake = Snowflake()
        flake_list.append(new_flake)
    return flake_list


def get_fallen_flakes():
    global flakes
    flakes_on_flour = []
    for flake_on_flour in flakes:
        if not flake_on_flour.can_fall():
            flakes_on_flour.append(flake_on_flour)
            flakes.remove(flake_on_flour)
            del flake_on_flour  # удаляю же объекты по списку.
            # если не удалять он же память не отпустит
    return flakes_on_flour


def append_flakes(count):
    global flakes
    for new_flake in range(count):
        flakes.append(Snowflake())


# flake = Snowflake()
#
# while True:
#     flake.clear_previous_picture()
#     flake.move()
#     flake.draw()
#     if not flake.can_fall():
#         break
#     sd.sleep(0.1)
#     if sd.user_want_exit():
#         break

# шаг 2: создать снегопад - список объектов Снежинка в отдельном списке, обработку примерно так:


N = 25
flakes = get_flakes(count=N)  # создать список снежинок
while True:
    for flake in flakes:
        flake.clear_previous_picture()
        flake.move()
        flake.draw()
    fallen_flakes = get_fallen_flakes()  # подчитать сколько снежинок уже упало
    if fallen_flakes:
        append_flakes(count=len(fallen_flakes))  # добавить еще сверху
    sd.sleep(0.1)
    if sd.user_want_exit():
        break

sd.pause()
#зачет!