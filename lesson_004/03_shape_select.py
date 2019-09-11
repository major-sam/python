# -*- coding: utf-8 -*-

import simple_draw as sd


# 
# def triangle(triangle_start, angle, length, color):
#     buffer = triangle_start
#     side_a = sd.get_vector(start_point=triangle_start, angle=angle, length=length)
#     side_a.draw(color=color)
#     side_b = sd.get_vector(start_point=side_a.end_point, angle=angle + 120, length=length)
#     side_b.draw(color=color)
#     sd.line(buffer, side_b.end_point, color=color)
# 
# 
# # - квадрата
# def quadro(quadro_start, angle, length, color):
#     buffer = quadro_start
#     side_a = sd.get_vector(start_point=quadro_start, angle=angle, length=length)
#     side_a.draw(color=color)
#     side_b = sd.get_vector(start_point=side_a.end_point, angle=angle + 90, length=length)
#     side_b.draw(color=color)
#     side_c = sd.get_vector(start_point=side_b.end_point, angle=angle + 180, length=length)
#     side_c.draw(color=color)
#     sd.line(buffer, side_c.end_point, color=color)
# 
# 
# # - пятиугольника
# def pento(pento_start, angle, length, color):
#     buffer = pento_start
#     side_a = sd.get_vector(start_point=pento_start, angle=angle, length=length)
#     side_a.draw(color=color)
#     side_b = sd.get_vector(start_point=side_a.end_point, angle=angle + 72, length=length)
#     side_b.draw(color=color)
#     side_c = sd.get_vector(start_point=side_b.end_point, angle=angle + 144, length=length)
#     side_c.draw(color=color)
#     side_d = sd.get_vector(start_point=side_c.end_point, angle=angle + 216, length=length)
#     side_d.draw(color=color)
#     sd.line(buffer, side_d.end_point, color=color)
# 
# 
# # - шестиугольника
# def hexagon(hexagon_start, angle, length, color):
#     buffer = hexagon_start
#     side_a = sd.get_vector(start_point=hexagon_start, angle=angle, length=length)
#     side_a.draw(color=color)
#     side_b = sd.get_vector(start_point=side_a.end_point, angle=angle + 60, length=length)
#     side_b.draw(color=color)
#     side_c = sd.get_vector(start_point=side_b.end_point, angle=angle + 120, length=length)
#     side_c.draw(color=color)
#     side_d = sd.get_vector(start_point=side_c.end_point, angle=angle + 180, length=length)
#     side_d.draw(color=color)
#     side_e = sd.get_vector(start_point=side_d.end_point, angle=angle + 240, length=length)
#     side_e.draw(color=color)
#     sd.line(buffer, side_e.end_point, color=color)
# 
# 
# def choosing_figure(figure_id, start_point, additional_angle=0, length=100, color=user_color):
#     if figure_id == '0':
#         triangle(start_point, additional_angle, length, color)
#         sd.pause()
#     elif figure_id == '1':
#         quadro(start_point, additional_angle, length, color)
#         sd.pause()
#     elif figure_id == '2':
#         pento(start_point, additional_angle, length, color)
#         sd.pause()
#     elif figure_id == '3':
#         hexagon(start_point, additional_angle, length, color)
#         sd.pause()
#     else:
#         print('wtf or something wrong with choosing_figure')


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
         'func': get_triangle},  # TODO хранить функции можно таким образом
    '1':
        {'shape': 'квадрат',
         'func': 'get_quadro(midpoint, additional_angle=0, length=100, color=user_color)'},
    '2':
        {'shape': 'пятиугольник',
         'func': 'get_pento(midpoint, additional_angle=0, length=100, color=user_color)'},
    '3': {'shape': 'шестиугольник',
          'func': 'get_hex(midpoint, additional_angle=0, length=100, color=user_color)'}
}
for shape_id, shape_name in shapes.items():
    print(shape_id, ':', shape_name['shape'])

user_shape = input('Выберете фигуру\n')
while user_shape not in shapes.keys():
    print('Вы ввели некоректный номер', user_shape)
    user_shape = input('Выберете фигуру\n')
exec(shapes[user_shape]['func'])  # TODO затем эту функцию с нужными параметрами вызываем здесь
# TODO что-то вроде функция = словарь[адрес]
# TODO функция(параметры)
sd.pause()

# TODO и нужно подчистить лишний код сверху перед зачетом.