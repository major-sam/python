# -*- coding: utf-8 -*-

import simple_draw as sd


# Часть 1.
# Написать функции рисования равносторонних геометрических фигур:
# - треугольника


def triangle(triangle_start, angle, length):
    side_a = sd.get_vector(start_point=triangle_start, angle=angle, length=length)
    side_a.draw()
    side_b = sd.get_vector(start_point=side_a.end_point, angle=angle + 120, length=length)
    side_b.draw()
    side_c = sd.get_vector(start_point=side_b.end_point, angle=angle + 240, length=length)
    side_c.draw()


# - квадрата

def quadro(quadro_start, angle, length):
    side_a = sd.get_vector(start_point=quadro_start, angle=angle, length=length)
    side_a.draw()
    side_b = sd.get_vector(start_point=side_a.end_point, angle=angle + 90, length=length)
    side_b.draw()
    side_c = sd.get_vector(start_point=side_b.end_point, angle=angle + 180, length=length)
    side_c.draw()
    side_d = sd.get_vector(start_point=side_c.end_point, angle=angle + 270, length=length)
    side_d.draw()


# - пятиугольника
def pento(pento_start, angle, length):
    side_a = sd.get_vector(start_point=pento_start, angle=angle, length=length)
    side_a.draw()
    side_b = sd.get_vector(start_point=side_a.end_point, angle=angle + 72, length=length)
    side_b.draw()
    side_c = sd.get_vector(start_point=side_b.end_point, angle=angle + 144, length=length)
    side_c.draw()
    side_d = sd.get_vector(start_point=side_c.end_point, angle=angle + 216, length=length)
    side_d.draw()
    side_e = sd.get_vector(start_point=side_d.end_point, angle=angle + 288, length=length)
    side_e.draw()


# - шестиугольника
def hexagon(hexagon_start, angle, length):
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
    side_f = sd.get_vector(start_point=side_e.end_point, angle=angle + 300, length=length)
    side_f.draw()


point_1 = sd.get_point(100, 100)
point_2 = sd.get_point(100, 400)
point_3 = sd.get_point(400, 100)
point_4 = sd.get_point(400, 400)
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
def circul_vector(sides, start_point, additional_angle=0, length=100):
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


point = sd.get_point(200, 200)
circul_vector(3, point, 0, 100)  # TODO решение хорошее :) но не соответствует ТЗ
# TODO должна быть одна общая функция схожая с вашей и по функции на каждую из 4 фигур.
# TODO каждая функция для каждой фигуры должна принимать по 3 парамтера (точка, угол, длина линии)
# TODO и должна вызывать внутри себя общую, дополняя её параметрами
# TODO Например функция треугольника при вызове передаст 3 полученных параметра и информацию, что должно быть 3 угла
# почему съезжает пиксель я без понятия - должно работать
# странно, я не заметил съезжающего пикселя, вы верно использовали sd.line() для последней стороны

sd.pause()
