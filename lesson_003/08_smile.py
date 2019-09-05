# -*- coding: utf-8 -*-

# (определение функций)
import simple_draw as sd

# Написать функцию отрисовки смайлика в произвольной точке экрана
# Форма рожицы-смайлика на ваше усмотрение
# Параметры функции: кордината X, координата Y, цвет.
# Вывести 10 смайликов в произвольных точках экрана.


def smile(random_center_x, random_center_y, color):
    center_x = random_center_x
    center_y = random_center_y
    center = sd.get_point(center_x, center_y)
    sd.circle(center, radius=60, color=color, width=2)
    mouth_y = center_y - 25
    mouth_x = center_x - 20
    mouth_start = sd.get_point(mouth_x, mouth_y)
    mouth_end = sd.get_point(mouth_x+40, mouth_y)
    sd.line(mouth_start, mouth_end, width=2, color=color)
    left_eye_y = center_y + 15
    left_eye_x = center_x - 10
    left_eye_start = sd.get_point(left_eye_x, left_eye_y)
    left_eye_end = sd.get_point(left_eye_x - 30, left_eye_y)
    sd.line(left_eye_start, left_eye_end, width=2, color=color)
    right_eye_y = center_y + 15
    right_eye_x = center_x + 10
    right_eye_start = sd.get_point(right_eye_x, right_eye_y)
    right_eye_end = sd.get_point(right_eye_x + 30, right_eye_y)
    sd.line(right_eye_start, right_eye_end, width=2, color=color)


for _ in range(10):
    center_a = sd.random_number(100, 500)
    center_b = sd.random_number(100, 500)
    smile(center_a, center_b, sd.random_color())
sd.pause()
# А в целом, отличная работа, в который раз! :)