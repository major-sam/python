# -*- coding: utf-8 -*-

import simple_draw as sd


# На основе вашего кода из решения lesson_004/01_shapes.py сделать функцию-фабрику,
# которая возвращает функции рисования треугольника, четырехугольника, пятиугольника и т.д.
#
# Функция рисования должна принимать параметры
# - точка начала рисования
# - угол наклона
# - длина стороны
#
# Функция-фабрика должна принимать параметр n - количество сторон.


def get_polygon(n):
    if n < 3:
        raise Exception('недостоаточно сторон')
    else:
        def polygon(point, angle, length):
            base_angle = 360 / n
            buffer_point = point
            for side in range(0, n - 1):
                current_edge = sd.get_vector(start_point=buffer_point, angle=angle + base_angle * side,
                                             length=length)
                current_edge.draw()
                buffer_point = current_edge.end_point
            sd.line(buffer_point, point)

        return polygon


draw_triangle = get_polygon(n=3)
draw_triangle(point=sd.get_point(200, 200), angle=13, length=100)

sd.pause()
