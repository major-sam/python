# -*- coding: utf-8 -*-
import simple_draw as sd

# Добавить цвет в функции рисования геом. фигур. из упр lesson_004/01_shapes.py
# (код функций скопировать сюда и изменить)
# Запросить у пользователя цвет фигуры посредством выбора из существующих:
#   вывести список всех цветов с номерами и ждать ввода номера желаемого цвета.
# Потом нарисовать все фигуры этим цветом

# Пригодятся функции
# sd.get_point()
# sd.line()
# sd.get_vector()
# и константы COLOR_RED, COLOR_ORANGE, COLOR_YELLOW, COLOR_GREEN, COLOR_CYAN, COLOR_BLUE, COLOR_PURPLE
# Результат решения см lesson_004/results/exercise_02_global_color.jpg

print('Возможные цвета'
      '0 : red'
      '1 : orange'
      '2 : yellow'
      '3 : green'
      '4 : cyan'
      '5 : blue'
      '6 : purple')

colors = {
    0: sd.COLOR_RED,
    1: sd.COLOR_ORANGE,
    2: sd.COLOR_YELLOW,
    3: sd.COLOR_GREEN,
    4: sd.COLOR_CYAN,
    5: sd.COLOR_BLUE,
    6: sd.COLOR_PURPLE
}

print('Выберете цвет фигур')


def triangle(triangle_start, angle, length, color):
    side_a = sd.get_vector(start_point=triangle_start, angle=angle, length=length, color=color)
    side_a.draw()
    side_b = sd.get_vector(start_point=side_a.end_point, angle=angle + 120, length=length, color=color)
    side_b.draw()
    side_c = sd.get_vector(start_point=side_b.end_point, angle=angle + 240, length=length, color=color)
    side_c.draw()


# - квадрата

def quadro(quadro_start, angle, length, color):
    side_a = sd.get_vector(start_point=quadro_start, angle=angle, length=length, color=color)
    side_a.draw()
    side_b = sd.get_vector(start_point=side_a.end_point, angle=angle + 90, length=length, color=color)
    side_b.draw()
    side_c = sd.get_vector(start_point=side_b.end_point, angle=angle + 180, length=length, color=color)
    side_c.draw()
    side_d = sd.get_vector(start_point=side_c.end_point, angle=angle + 270, length=length, color=color)
    side_d.draw()


# - пятиугольника
def pento(pento_start, angle, length, color):
    side_a = sd.get_vector(start_point=pento_start, angle=angle, length=length, color=color)
    side_a.draw()
    side_b = sd.get_vector(start_point=side_a.end_point, angle=angle + 72, length=length, color=color)
    side_b.draw()
    side_c = sd.get_vector(start_point=side_b.end_point, angle=angle + 144, length=length, color=color)
    side_c.draw()
    side_d = sd.get_vector(start_point=side_c.end_point, angle=angle + 216, length=length, color=color)
    side_d.draw()
    side_e = sd.get_vector(start_point=side_d.end_point, angle=angle + 288, length=length, color=color)
    side_e.draw()


# - шестиугольника
def hexagon(hexagon_start, angle, length, color):
    side_a = sd.get_vector(start_point=hexagon_start, angle=angle, length=length, color=color)
    side_a.draw()
    side_b = sd.get_vector(start_point=side_a.end_point, angle=angle + 60, length=length, color=color)
    side_b.draw()
    side_c = sd.get_vector(start_point=side_b.end_point, angle=angle + 120, length=length, color=color)
    side_c.draw()
    side_d = sd.get_vector(start_point=side_c.end_point, angle=angle + 180, length=length, color=color)
    side_d.draw()
    side_e = sd.get_vector(start_point=side_d.end_point, angle=angle + 240, length=length, color=color)
    side_e.draw()
    side_f = sd.get_vector(start_point=side_e.end_point, angle=angle + 300, length=length, color=color)
    side_f.draw()


point_1 = sd.get_point(100, 100)
point_2 = sd.get_point(100, 400)
point_3 = sd.get_point(400, 100)
point_4 = sd.get_point(400, 400)
triangle(triangle_start=point_1, angle=321, length=100)
quadro(quadro_start=point_2, angle=10, length=100)
pento(pento_start=point_3, angle=22, length=100)

sd.pause()
