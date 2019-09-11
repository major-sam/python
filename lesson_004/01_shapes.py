# -*- coding: utf-8 -*-

import simple_draw as sd


# Часть 1.
# Написать функции рисования равносторонних геометрических фигур:
# - треугольника


def triangle(triangle_start, angle, length):
    buffer = triangle_start
    side_a = sd.get_vector(start_point=triangle_start, angle=angle, length=length)
    side_a.draw()
    side_b = sd.get_vector(start_point=side_a.end_point, angle=angle + 120, length=length)
    side_b.draw()
    sd.line(buffer, side_b.end_point)


# - квадрата
def quadro(quadro_start, angle, length):
    buffer = quadro_start
    side_a = sd.get_vector(start_point=quadro_start, angle=angle, length=length)
    side_a.draw()
    side_b = sd.get_vector(start_point=side_a.end_point, angle=angle + 90, length=length)
    side_b.draw()
    side_c = sd.get_vector(start_point=side_b.end_point, angle=angle + 180, length=length)
    side_c.draw()
    sd.line(buffer, side_c.end_point)


# - пятиугольника
def pento(pento_start, angle, length):
    buffer = pento_start
    side_a = sd.get_vector(start_point=pento_start, angle=angle, length=length)
    side_a.draw()
    side_b = sd.get_vector(start_point=side_a.end_point, angle=angle + 72, length=length)
    side_b.draw()
    side_c = sd.get_vector(start_point=side_b.end_point, angle=angle + 144, length=length)
    side_c.draw()
    side_d = sd.get_vector(start_point=side_c.end_point, angle=angle + 216, length=length)
    side_d.draw()
    sd.line(buffer, side_d.end_point)


# - шестиугольника
def hexagon(hexagon_start, angle, length):
    buffer = hexagon_start
    side_a = sd.get_vector(start_point=hexagon_start, angle=angle, length=length)
    side_a.draw()
    side_b = sd.get_vector(start_point=side_a.end_point, angle=angle + 60, length=length)
    side_b.draw()
    side_c = sd.get_vector(start_point=side_b.end_point, angle=angle + 120, length=length)
    side_c.draw()
    side_d = sd.get_vector(start_point=side_c.end_point, angle=angle + 180, length=length)
    side_d.draw()
    side_e = sd.get_vector(start_point=side_d.end_point, angle=angle + 240, length=length)
    side_e.draw()
    sd.line(buffer, side_e.end_point)


def choosing_figure(figure_id, start_point, additional_angle=0, length=100):
    if figure_id == 0:
        triangle(start_point, additional_angle, length)
    elif figure_id == 1:
        quadro(start_point, additional_angle, length)
    elif figure_id == 2:
        pento(start_point, additional_angle, length)
    elif figure_id == 3:
        hexagon(start_point, additional_angle, length)


# choosing_figure(1, point, 10, 120)
# point_1 = sd.get_point(100, 100)
# point_2 = sd.get_point(100, 400)
# point_3 = sd.get_point(400, 100)
# point_4 = sd.get_point(400, 400)
# triangle(triangle_start=point_1, angle=321, length=100)
# quadro(quadro_start=point_2, angle=10, length=100)
# pento(pento_start=point_3, angle=22, length=100)
# hexagon(hexagon_start=point_4, angle=0, length=100)


# Все функции должны принимать 3 параметра:
# - точка начала рисования
# - угол наклона
# - длина стороны

# Использование копи-пасты - обязательно! Даже тем кто уже знает про её пагубность. Для тренировки.
# Как работает копипаста:
#   - одну функцию написали,
#   - копипастим её, меняем название, чуть подправляем код,
#   - копипастим её, меняем название, чуть подправляем код,
#   - и так далее.
# В итоге должен получиться ПОЧТИ одинаковый код в каждой функции

# Пригодятся функции
# sd.get_point()
# sd.get_vector()
# sd.line()
# Результат решения см lesson_004/results/exercise_01_shapes.jpg


# Часть 1-бис.
# Попробуйте прикинуть обьем работы, если нужно будет внести изменения в этот код.
# Скажем, связывать точки не линиями, а дугами. Или двойными линиями. Или рисовать круги в угловых точках. Или...
# А если таких функций не 4, а 44?

# Часть 2 (делается после зачета первой части)
#
# Надо сформировать функцию, параметризированную в местах где была "небольшая правка".
# Это называется "Выделить общую часть алгоритма в отдельную функцию"
# Потом надо изменить функции рисования конкретных фигур - вызывать общую функцию вместо "почти" одинакового кода.
#
# В итоге должно получиться:
#   - одна общая функция со множеством параметров,
#   - все функции отрисовки треугольника/квадрата/етс берут 3 параметра и внутри себя ВЫЗЫВАЮТ общую функцию.
#
# Не забудте в этой общей функции придумать, как устранить разрыв
#   в начальной/конечной точках рисуемой фигуры (если он есть)

# Часть 2-бис.
# А теперь - сколько надо работы что бы внести изменения в код? Выгода на лицо :)
# Поэтому среди программистов есть принцип D.R.Y. https://clck.ru/GEsA9
# Будьте ленивыми, не используйте копи-пасту!
#


def circle_vector(sides, start_point, additional_angle=0, length=100):
    if sides < 3:
        print('3+ sides needed for a figure')
        return
    base_angle = 360 / sides
    buffer_point = start_point
    for side in range(0, sides - 1):
        side_a = sd.get_vector(start_point=buffer_point, angle=additional_angle + base_angle * side, length=length)
        side_a.draw()
        buffer_point = side_a.end_point
    sd.line(buffer_point, start_point)


# circle_vector(12, point, 0, 100)


def get_triangle(start_point, additional_angle=0, length=100):
    sides = 3
    circle_vector(sides, start_point, additional_angle, length)


def get_quadro(start_point, additional_angle=0, length=100):
    sides = 4
    circle_vector(sides, start_point, additional_angle, length)


def get_pento(start_point, additional_angle=0, length=100):
    sides = 5
    circle_vector(sides, start_point, additional_angle, length)


def get_hex(start_point, additional_angle=0, length=100):
    sides = 6
    circle_vector(sides, start_point, additional_angle, length)


point = sd.get_point(200, 200)
sd.pause()
