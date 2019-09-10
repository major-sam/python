# -*- coding: utf-8 -*-

import simple_draw as sd


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
    if figure_id == '0':
        triangle(start_point, additional_angle, length, color)
        sd.pause()
    elif figure_id == '1':
        quadro(start_point, additional_angle, length, color)
        sd.pause()
    elif figure_id == '2':
        pento(start_point, additional_angle, length, color)
        sd.pause()
    elif figure_id == '3':
        hexagon(start_point, additional_angle, length, color)
        sd.pause()
    else:
        print('wtf or something wrong with choosing_figure')


# Запросить у пользователя желаемую фигуру посредством выбора из существующих
#   вывести список всех фигур с номерами и ждать ввода номера желаемой фигуры.
# и нарисовать эту фигуру в центре экрана

# Код функций из упр lesson_004/02_global_color.py скопировать сюда
# Результат решения см lesson_004/results/exercise_03_shape_select.jpg
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

print('Возможные фигуры\n')
shapes = {  # TODO здесь лучше создать словарь по примеру словаря с цветами
    '0': 'треугольник',  # TODO только вместо цветов добафить функции, рисующие нужную фигуру
    '1': 'квадрат',  # TODO тут вот будет функция для рисования квадрата :)
    '2': 'пятиугольник',
    '3': 'шестиугольник'
}
for shape_id, shape_name in shapes.items():
    print(shape_id, ':', shape_name)

midpoint = sd.get_point(200, 300)
user_shape = input('Выберете фигуру\n')
while user_shape not in shapes.keys():
    print('Вы ввели некоректный номер', user_shape)
    user_shape = input('Выберете фигуру\n')
# TODO хорошо, но нужно будет глянуть на результат с измененной функцией 01
choosing_figure(user_shape, midpoint, 321, 100, color=user_color)
sd.pause()
