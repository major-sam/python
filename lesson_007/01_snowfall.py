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
        # TODO так ли нам нужна point? При рисовании мы можем создавать точку из координат выше.
        self.point = sd.get_point(self.snowflake_x, self.snowflake_y)

    def __del__(self):
        print('')

    def clear_previous_picture(self):
        # TODO давайте сыграем в игру - найдите 5 отличий между этим методом и draw
        # TODO проигравший должен убрать лишнее дублирование! :)
        sd.start_drawing()  # TODO попробуйте запустить без всех start и finish
        self.snowflake_color = sd.background_color
        sd.snowflake(self.point, self.snowflake_size, self.snowflake_color)
        sd.finish_drawing()

    def draw(self):
        sd.start_drawing()
        self.snowflake_color = sd.COLOR_WHITE  # TODO цвет можно задать параметром
        self.point = sd.get_point(self.snowflake_x, self.snowflake_y)
        sd.snowflake(self.point, self.snowflake_size, self.snowflake_color)
        # TODO сюда можно передать объект sd.Point(с координатами из атрибутов выше)
        sd.finish_drawing()
        # TODO Ранее в одной из работ со снежинками уже был этот вопрос, но
        # TODO Нужно ли нам рисовать снежинки, которые can_fall = False?

    def move(self):
        self.snowflake_y -= sd.random_number(1, 15)
        self.snowflake_x -= sd.random_number(-10, 10)
        # TODO изменение координат - это уже передвижение снежинки
        self.point = sd.get_point(self.snowflake_x, self.snowflake_y)

    def can_fall(self):
        return self.snowflake_y - self.snowflake_size > 0
    # TODO думаю лучше просто сравнить y и size - получается на одну операцию меньше


def get_flakes(count):
    flake_list = []
    for new_flake in range(count):
        new_flake = Snowflake()
        flake_list.append(new_flake)
    return flake_list


def get_fallen_flakes():  # TODO fallen_flakes по сути не требует создания списка, нужно просто посчитать
    global flakes
    flakes_on_flour = []
    for flake_on_flour in flakes:
        if not flake_on_flour.can_fall():
            flakes_on_flour.append(flake_on_flour)
            flakes.remove(flake_on_flour)
            del flake_on_flour
    return flakes_on_flour


def append_flakes(count):
    global flakes
    for new_flake in range(count):
        new_flake = Snowflake()  # TODO можно обойтись без передатчика
        flakes.append(new_flake)  # TODO сразу сюда подавать Snowflake()


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
