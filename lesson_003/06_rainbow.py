# -*- coding: utf-8 -*-

# (цикл for)

import simple_draw as sd

rainbow_colors = (sd.COLOR_RED, sd.COLOR_ORANGE, sd.COLOR_YELLOW, sd.COLOR_GREEN,
                  sd.COLOR_CYAN, sd.COLOR_BLUE, sd.COLOR_PURPLE)

# Нарисовать радугу: 7 линий разного цвета толщиной 4 с шагом 5 из точки (50, 50) в точку (350, 450)
width, step, start_point_x, end_point_x = 4, 5, 50, 350

for colors in rainbow_colors:
    point_a = sd.get_point(start_point_x, 50)
    point_b = sd.get_point(end_point_x, 450)
    sd.line(point_a, point_b, color=colors, width=width)
    start_point_x += step
    end_point_x += step


# Усложненное задание, делать по желанию.
# Нарисовать радугу дугами от окружности (cсм sd.circle) за нижним краем экрана,
# поэкспериментировать с параметрами, что бы было красиво
radius, rainbow_step, rainbow_width = 200, 10, 14

for colors in rainbow_colors:
    center = sd.get_point(600, 0)
    sd.circle(center_position=center, radius=radius, color=colors, width=rainbow_width)
    radius -= rainbow_step
sd.pause()
