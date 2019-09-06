# -*- coding: utf-8 -*-

import simple_draw as sd

sd.resolution = (1200, 600)


# Нарисовать пузырек - три вложенных окружностей с шагом 5 пикселей

# point = sd.get_point(300,300)
# radius = 50
# for step in range(3):
#     sd.circle(center_position=point, radius=radius, width=1)
#     radius -= 5

# Написать функцию рисования пузырька, принммающую 2 (или более) параметра: точка рисовании и шаг
def bubble(point, step, color):
    radius = 50
    for _ in range(3):
        sd.circle(center_position=point, radius=radius, color=color, width=1)
        radius -= step


# Нарисовать 10 пузырьков в ряд

# for x_position in range(100, 1001, 100):
#     point = sd.get_point(x_position, 300)
#     bubble(point=point, step=3, color=sd.COLOR_DARK_CYAN)

# Нарисовать три ряда по 10 пузырьков
# for y_position in range(100, 301, 100):
#     for x_position in range(100, 1001, 100):
#         point = sd.get_point(x_position, y_position)
#         bubble(point=point, step=3, color=sd.COLOR_DARK_CYAN)


# Нарисовать 100 пузырьков в произвольных местах экрана случайными цветами
# def bubble(point, step, color):
#     radius = 50
#     for _ in range(3):
#         sd.circle(center_position=point, radius=radius, color=color, width=1)
#         radius -= step
# for _ in range(100):
#     point = sd.random_point()
#     color = sd.random_color()
#     bubble(point, step=3, color=color)

sd.pause()
#зачет!