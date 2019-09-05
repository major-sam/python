# -*- coding: utf-8 -*-

import simple_draw as sd

sd.resolution = (1200, 600)

# Нарисовать пузырек - три вложенных окружностей с шагом 5 пикселей
# TODO нужно выполнить каждое задание ( код можно закомментировать, если мешается )

# Написать функцию рисования пузырька, принммающую 2 (или более) параметра: точка рисовании и шаг
def bubble(point, step, color):
    radius = 50
    for _ in range(3):
        sd.circle(center_position=point, radius=radius, color=color, width=1)
        radius -= step


# Нарисовать 10 пузырьков в ряд
# TODO это тоже нужно выполнить
# Нарисовать три ряда по 10 пузырьков
# TODO и это

# Нарисовать 100 пузырьков в произвольных местах экрана случайными цветами
for _ in range(100):
    point = sd.random_point()
    color = sd.random_color()
    bubble(point, step=3, color=color)

sd.pause()
# TODO последнее задание со 100 пузырьками сделано верно :) хорошая работа, но жду код и остальных частей