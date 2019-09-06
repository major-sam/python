# -*- coding: utf-8 -*-

import simple_draw as sd


def triangle(triangle_start, angle, length, color):
    side_a = sd.get_vector(start_point=triangle_start, angle=angle, length=length)
    side_a.draw(color=color)
    side_b = sd.get_vector(start_point=side_a.end_point, angle=angle + 120, length=length)
    side_b.draw(color=color)
    side_c = sd.get_vector(start_point=side_b.end_point, angle=angle + 240, length=length)
    side_c.draw(color=color)


# - квадрата

def quadro(quadro_start, angle, length, color):
    side_a = sd.get_vector(start_point=quadro_start, angle=angle, length=length)
    side_a.draw(color=color)
    side_b = sd.get_vector(start_point=side_a.end_point, angle=angle + 90, length=length)
    side_b.draw(color=color)
    side_c = sd.get_vector(start_point=side_b.end_point, angle=angle + 180, length=length)
    side_c.draw(color=color)
    side_d = sd.get_vector(start_point=side_c.end_point, angle=angle + 270, length=length)
    side_d.draw(color=color)


# - пятиугольника
def pento(pento_start, angle, length, color):
    side_a = sd.get_vector(start_point=pento_start, angle=angle, length=length)
    side_a.draw(color=color)
    side_b = sd.get_vector(start_point=side_a.end_point, angle=angle + 72, length=length)
    side_b.draw(color=color)
    side_c = sd.get_vector(start_point=side_b.end_point, angle=angle + 144, length=length)
    side_c.draw(color=color)
    side_d = sd.get_vector(start_point=side_c.end_point, angle=angle + 216, length=length)
    side_d.draw(color=color)
    side_e = sd.get_vector(start_point=side_d.end_point, angle=angle + 288, length=length)
    side_e.draw(color=color)


# - шестиугольника
def hexagon(hexagon_start, angle, length, color):
    side_a = sd.get_vector(start_point=hexagon_start, angle=angle, length=length)
    side_a.draw(color=color)
    side_b = sd.get_vector(start_point=side_a.end_point, angle=angle + 60, length=length)
    side_b.draw(color=color)
    side_c = sd.get_vector(start_point=side_b.end_point, angle=angle + 120, length=length)
    side_c.draw(color=color)
    side_d = sd.get_vector(start_point=side_c.end_point, angle=angle + 180, length=length)
    side_d.draw(color=color)
    side_e = sd.get_vector(start_point=side_d.end_point, angle=angle + 240, length=length)
    side_e.draw(color=color)
    side_f = sd.get_vector(start_point=side_e.end_point, angle=angle + 300, length=length)
    side_f.draw(color=color)


# Запросить у пользователя желаемую фигуру посредством выбора из существующих
#   вывести список всех фигур с номерами и ждать ввода номера желаемой фигуры.
# и нарисовать эту фигуру в центре экрана

# Код функций из упр lesson_004/02_global_color.py скопировать сюда
# Результат решения см lesson_004/results/exercise_03_shape_select.jpg

print('Возможные цвета\n'
      '0 : red\n'
      '1 : orange\n'
      '2 : yellow\n'
      '3 : green\n'
      '4 : cyan\n'
      '5 : blue\n'
      '6 : purple\n')

colors = {
    '0': sd.COLOR_RED,
    '1': sd.COLOR_ORANGE,
    '2': sd.COLOR_YELLOW,
    '3': sd.COLOR_GREEN,
    '4': sd.COLOR_CYAN,
    '5': sd.COLOR_BLUE,
    '6': sd.COLOR_PURPLE
}

user_color_input = input('Выберете цвет фигур\n')
while user_color_input not in colors:
    print('Вы ввели некоректный номер', user_color_input)
    user_color_input = input('Выберете цвет фигур\n')
user_color = colors[user_color_input]

print('Возможные фигуры\n'
      '0 : треугольник\n'
      '1 : квадрат\n'
      '2 : пятиугольник\n'
      '3 : шестиугольник\n')
user_figure_input = input('Выберете фигуру\n')
while int(user_figure_input) not in range(4):
    print('Вы ввели некоректный номер', user_figure_input)
    user_figure_input = input('Выберете фигуру\n')
midpoint = sd.get_point(200, 300)
if user_figure_input == '0':
    triangle(triangle_start=midpoint, angle=321, length=100, color=user_color)
    sd.pause()
elif user_figure_input == '1':
    quadro(quadro_start=midpoint, angle=10, length=100, color=user_color)
    sd.pause()
elif user_figure_input == '2':
    pento(pento_start=midpoint, angle=22, length=100, color=user_color)
    sd.pause()
elif user_figure_input == '3':
    hexagon(hexagon_start=midpoint, angle=22, length=100, color=user_color)
    sd.pause()


