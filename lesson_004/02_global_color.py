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

def triangle(triangle_start, angle, length, color):
    buffer = triangle_start
    side_a = sd.get_vector(start_point=triangle_start, angle=angle, length=length)
    side_a.draw(color=color)
    side_b = sd.get_vector(start_point=side_a.end_point, angle=angle + 120, length=length)
    side_b.draw(color=color)
    sd.line(buffer, side_b.end_point, color=color)


# - квадрата
def quadro(quadro_start, angle, length, color):
    buffer = quadro_start
    side_a = sd.get_vector(start_point=quadro_start, angle=angle, length=length)
    side_a.draw(color=color)
    side_b = sd.get_vector(start_point=side_a.end_point, angle=angle + 90, length=length)
    side_b.draw(color=color)
    side_c = sd.get_vector(start_point=side_b.end_point, angle=angle + 180, length=length)
    side_c.draw(color=color)
    sd.line(buffer, side_c.end_point, color=color)


# - пятиугольника
def pento(pento_start, angle, length, color):
    buffer = pento_start
    side_a = sd.get_vector(start_point=pento_start, angle=angle, length=length)
    side_a.draw(color=color)
    side_b = sd.get_vector(start_point=side_a.end_point, angle=angle + 72, length=length)
    side_b.draw(color=color)
    side_c = sd.get_vector(start_point=side_b.end_point, angle=angle + 144, length=length)
    side_c.draw(color=color)
    side_d = sd.get_vector(start_point=side_c.end_point, angle=angle + 216, length=length)
    side_d.draw(color=color)
    sd.line(buffer, side_d.end_point, color=color)


# - шестиугольника
def hexagon(hexagon_start, angle, length, color):
    buffer = hexagon_start
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
    sd.line(buffer, side_e.end_point, color=color)


def choosing_figure(figure_id, start_point, additional_angle=0, length=100, color=sd.COLOR_DARK_YELLOW):
    if figure_id == 0:
        triangle(start_point, additional_angle, length, color)
    elif figure_id == 1:
        quadro(start_point, additional_angle, length, color)
    elif figure_id == 2:
        pento(start_point, additional_angle, length, color)
    elif figure_id == 3:
        hexagon(start_point, additional_angle, length, color)


print('Возможные цвета\n')
colors = {
    '0':
        {'color': 'red', 'sd_color': sd.COLOR_RED},
    '1':
        {'color': 'orange', 'sd_color': sd.COLOR_ORANGE},
    '2':
        {'color': 'yellow', 'sd_color': sd.COLOR_YELLOW},
    '3':
        {'color': 'green', 'sd_color': sd.COLOR_GREEN},
    '4':
        {'color': 'cyan', 'sd_color': sd.COLOR_CYAN},
    '5':
        {'color': 'blue', 'sd_color': sd.COLOR_BLUE},
    '6':
        {'color': 'purple', 'sd_color': sd.COLOR_PURPLE}
}
for color_id, color_names in colors.items():
    cat_colors = colors[color_id]
    print(color_id, ':', cat_colors['color'])

user_input = input('Выберете цвет фигур\n')
while user_input not in colors.keys():
    print('Вы ввели некоректный номер', user_input)
    user_input = input('Выберете цвет фигур\n')
user_color = colors[user_input]['sd_color']

point_1 = sd.get_point(100, 100)
point_2 = sd.get_point(100, 400)
point_3 = sd.get_point(400, 100)
point_4 = sd.get_point(400, 400)
choosing_figure(0, point_1, 321, 100, color=user_color)
choosing_figure(1, point_2, 321, 100, color=user_color)
choosing_figure(2, point_3, 321, 100, color=user_color)
choosing_figure(3, point_4, 321, 100, color=user_color)
sd.pause()
