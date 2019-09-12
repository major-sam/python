# -*- coding: utf-8 -*-

import simple_draw as sd


def circle_vector(sides, start_point, additional_angle=0, length=100, color=sd.COLOR_DARK_YELLOW):
    if sides < 3:
        print('3+ sides needed for a figure')
        return
    base_angle = 360 / sides
    buffer_point = start_point
    for side in range(0, sides - 1):
        side_a = sd.get_vector(start_point=buffer_point, angle=additional_angle + base_angle * side, length=length)
        side_a.draw(color=color)
        buffer_point = side_a.end_point
    sd.line(buffer_point, start_point, color=color)


def get_triangle(start_point, additional_angle=0, length=100, color=sd.COLOR_DARK_YELLOW):
    sides = 3
    circle_vector(sides, start_point, additional_angle, length, color)


def get_quadro(start_point, additional_angle=0, length=100, color=sd.COLOR_DARK_YELLOW):
    sides = 4
    circle_vector(sides, start_point, additional_angle, length, color)


def get_pento(start_point, additional_angle=0, length=100, color=sd.COLOR_DARK_YELLOW):
    sides = 5
    circle_vector(sides, start_point, additional_angle, length, color)


def get_hex(start_point, additional_angle=0, length=100, color=sd.COLOR_DARK_YELLOW):
    sides = 6
    circle_vector(sides, start_point, additional_angle, length, color)


# Запросить у пользователя желаемую фигуру посредством выбора из существующих
#   вывести список всех фигур с номерами и ждать ввода номера желаемой фигуры.
# и нарисовать эту фигуру в центре экрана

# Код функций из упр lesson_004/02_global_color.py скопировать сюда
# Результат решения см lesson_004/results/exercise_03_shape_select.jpg
midpoint = sd.get_point(200, 300)
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
shapes = {
    '0':
        {'shape': 'треугольник',
         'func': get_triangle},
    '1':
        {'shape': 'квадрат',
         'func': get_quadro},
    '2':
        {'shape': 'пятиугольник',
         'func': get_pento},
    '3': {'shape': 'шестиугольник',
          'func': get_hex}
}
for shape_id, shape_name in shapes.items():
    print(shape_id, ':', shape_name['shape'])

user_shape = input('Выберете фигуру\n')
while user_shape not in shapes.keys():
    print('Вы ввели некоректный номер', user_shape)
    user_shape = input('Выберете фигуру\n')
func = shapes[user_shape]['func']
func(midpoint, additional_angle=0, length=100, color=user_color)

sd.pause()

#зачет!