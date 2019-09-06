# -*- coding: utf-8 -*-

import simple_draw as sd


# 1) Написать функцию draw_branches, которая должна рисовать две ветви дерева из начальной точки
# Функция должна принимать параметры:
# - точка начала рисования,
# - угол рисования,
# - длина ветвей,
# Отклонение ветвей от угла рисования принять 30 градусов,
# def draw_branches(start_point, br_angle, br_length):
#     br_angle = br_angle - 30
#     v1 = sd.get_vector(start_point=start_point, angle=br_angle, length=br_length, width=3)
#     v1.draw()
#     delta_angle = (180 - br_angle)
#     v2 = sd.get_vector(start_point=start_point, angle=delta_angle, length=br_length, width=3)
#     v2.draw()


# 2) Сделать draw_branches рекурсивной
# - добавить проверку на длину ветвей, если длина меньше 10 - не рисовать
# - вызывать саму себя 2 раза из точек-концов нарисованных ветвей,
#   с параметром "угол рисования" равным углу только что нарисованной ветви,
#   и параметром "длинна ветвей" в 0.75 меньшей чем длина только что нарисованной ветви


# def draw_branches(start_point, br_angle, br_length):
#     if br_length < 10:  # лучше будет с 1
#         return
#     v1 = sd.get_vector(start_point=start_point, angle=br_angle , length=br_length, width=1)
#     v1.draw()
# TODO второй вектор будет лишним, начинается из той же точки, на ту же длину
#     v2 = sd.get_vector(start_point=start_point, angle=br_angle, length=br_length, width=1)
#     v2.draw()
#     right_angle = br_angle - 30
#     left_angle = br_angle + 30
#     next_point = {right_angle: v1.end_point,
#                   left_angle: v2.end_point}
#     br_length = br_length * .75
#     for angle_switch, point_xy in next_point.items():
#         draw_branches(start_point=point_xy, br_angle=angle_switch, br_length=br_length)


# 3) первоначальный вызов:

#
# root_point = sd.get_point(300, 30)
# draw_branches(start_point=root_point, br_angle=90, br_length=100)

# Пригодятся функции
# sd.get_point()
# sd.get_vector()
# Возможный результат решения см lesson_004/results/exercise_04_fractal_01.jpg
# это с br_length < 1
# можно поиграть -шрифтами- цветами и углами отклонения


# 4) Усложненное задание (делать по желанию)
# - сделать рандомное отклонение угла ветвей в пределах 40% от 30-ти градусов
# - сделать рандомное отклонение длины ветвей в пределах 20% от коэффициента 0.75
# Возможный результат решения см lesson_004/results/exercise_04_fractal_02.jpg

def draw_branches(start_point, br_angle, br_length):
    if br_length < 10:  # лучше будет с 1 - да, красиво :) а ещё было бы здорово толщину добавить (по желанию)
        return
    v1 = sd.get_vector(start_point=start_point, angle=br_angle, length=br_length, width=1)
    v1.draw()
    # TODO этот вектор уже будет лишним, он ведь начинается из той же точки, с тем же углом
    v2 = sd.get_vector(start_point=start_point, angle=br_angle, length=br_length, width=1)
    v2.draw()
    length_delta = sd.random_number(80, 120)/100    #В обе стороны 20%
    angle_delta = sd.random_number(60, 140)/100     #В обе стороны 40%
    right_angle = br_angle - 30 * angle_delta
    left_angle = br_angle + 30 * angle_delta
    next_point = {right_angle: v1.end_point,
                  left_angle: v2.end_point}
    br_length = br_length * .75 * length_delta

    for angle_switch, point_xy in next_point.items():
        draw_branches(start_point=point_xy, br_angle=angle_switch, br_length=br_length)


root_point = sd.get_point(300, 30)
draw_branches(start_point=root_point, br_angle=90, br_length=100)
# Пригодятся функции
# sd.random_number()

sd.pause()
