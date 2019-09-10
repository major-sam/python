# -*- coding: utf-8 -*-

import simple_draw as sd

sd.resolution = (1200, 600)

# На основе кода из практической части реализовать снегопад:
# - создать списки данных для отрисовки N снежинок
# - нарисовать падение этих N снежинок
# - создать список рандомных длинн лучей снежинок (от 10 до 100) и пусть все снежинки будут разные
# TODO использовать списки вместо словаря 3 списка, по 1 на каждый параметр
# N = 20
# snowflake_on_flore_count = 0
# random_snowflake_on_air = {}
# for snow in range(N):
#     snowflake_size = sd.random_number(10, 100)
#     snowflake_y = sd.random_number(500, 600)
#     snowflake_x = sd.random_number(100, 1100)
#     random_snowflake_on_air.update({snow: [snowflake_size, snowflake_x, snowflake_y]})
#
# while True:
#     for snowflake_in_air_id, snowflake_in_air_param in random_snowflake_on_air.items():
#         snowflake_shift_y = sd.random_number(1, 10)
#         buffer_point = sd.get_point(snowflake_in_air_param[1], snowflake_in_air_param[2])
#         point = sd.get_point(snowflake_in_air_param[1], snowflake_in_air_param[2] - snowflake_shift_y)
#         sd.start_drawing()
#         sd.snowflake(center=buffer_point, length=snowflake_in_air_param[0], color=sd.background_color)
#         snowflake_in_air_param[2] -= snowflake_shift_y
#         sd.start_drawing()
#         sd.snowflake(center=point, length=snowflake_in_air_param[0], color=sd.COLOR_WHITE)
#         if snowflake_in_air_param[2] <= snowflake_in_air_param[0]:
#             sd.snowflake(center=point, length=snowflake_in_air_param[0], color=sd.background_color)
#             snowflake_in_air_param[2] = sd.random_number(500, 600)
#             snowflake_in_air_param[1] = sd.random_number(100, 1100)
#             snowflake_in_air_param[0] = sd.random_number(10, 100)
#     sd.finish_drawing()
#     sd.sleep(0.1)
#     if sd.user_want_exit():
#         break
#
# sd.pause()
# Пригодятся функции
# sd.get_point()
# sd.snowflake()
# sd.sleep()
# sd.random_number()
# sd.user_want_exit()


# подсказка! для ускорения отрисовки можно
#  - убрать clear_screen()
#  - в начале рисования всех снежинок вызвать sd.start_drawing()
#  - на старом месте снежинки отрисовать её же, но цветом sd.background_color
#  - сдвинуть снежинку
#  - отрисовать её цветом sd.COLOR_WHITE на новом месте
#  - после отрисовки всех снежинок, перед sleep(), вызвать sd.finish_drawing()


# 4) Усложненное задание (делать по желанию)
# - сделать рандомные отклонения вправо/влево при каждом шаге
# - сделать сугоб внизу экрана - если снежинка долетает до низа, оставлять её там,
#   и добавлять новую снежинку
# Результат решения см https://youtu.be/XBx0JtxHiLg
# TODO это лишний код? Если он не нужен - надо удалить
# N = 20
# snowflake_on_flore_count = 0
# random_snowflake_on_air = {}
# random_snowflake_on_floor = {}
# for snow in range(N):
#     snowflake_size = sd.random_number(10, 100)
#     snowflake_y = sd.random_number(500, 600)
#     snowflake_x = sd.random_number(100, 1100)
#     random_snowflake_on_air.update({snow: [
#         {'size': snowflake_size,
#          'x': snowflake_x,
#          'y': snowflake_y}
#     ]})
#
# while True:
#     sd.clear_screen()
#     for snowflake_on_flore_id in range(snowflake_on_flore_count):
#         snow_on_floor = random_snowflake_on_floor[snowflake_on_flore_id]
#         for snowflake_on_floor in snow_on_floor:
#             point = sd.get_point(snowflake_on_floor['x'], snowflake_on_floor['y'])
#             sd.snowflake(center=point, length=snowflake_on_floor['size'])
#     for snowflake_in_air_id in range(N):
#         snowflake_shift_y = sd.random_number(1, 10)
#         snowflake_shift_x = sd.random_number(-10, 10)
#         snow_in_air = random_snowflake_on_air[snowflake_in_air_id]
#         for snowflake_in_air in snow_in_air:
#             snowflake_in_air['y'] -= snowflake_shift_y
#             snowflake_in_air['x'] += snowflake_shift_x
#             point = sd.get_point(snowflake_in_air['x'], snowflake_in_air['y'])
#             sd.snowflake(center=point, length=snowflake_in_air['size'])
#             if snowflake_in_air['y'] <= snowflake_in_air['size']:
#                 snowflake_on_floor_size = snowflake_in_air['size']
#                 snowflake_on_floor_y = snowflake_in_air['y'] + 5
#                 snowflake_on_floor_x = snowflake_in_air['x']
#                 random_snowflake_on_floor.update({snowflake_on_flore_count: [
#                     {'size': snowflake_on_floor_size,
#                      'x': snowflake_on_floor_x,
#                      'y': snowflake_on_floor_y}
#                 ]})
#                 snowflake_on_flore_count += 1
#                 snowflake_in_air['y'] = sd.random_number(500, 600)
#                 snowflake_in_air['x'] = sd.random_number(100, 1100)
#                 snowflake_in_air['size'] = sd.random_number(10, 100)
#
#     sd.sleep(0.1)
#     if sd.user_want_exit():
#         break
# sd.pause()

N = 20
snowflake_on_flore_count = 0
random_snowflake_on_air = {}  # TODO вместо словаря 3 списка
for snow in range(N):
    snowflake_size = sd.random_number(10, 100)  # TODO список для этих значений
    snowflake_y = sd.random_number(500, 600)  # TODO список для этих
    snowflake_x = sd.random_number(100, 1100)  # TODO и для этих(значения будут связаны одним индексом)
    random_snowflake_on_air.update({snow: [snowflake_size, snowflake_x, snowflake_y]})

while True:
    for snowflake_in_air_id, snowflake_in_air_param in random_snowflake_on_air.items():
        snowflake_shift_y = sd.random_number(1, 10)
        snowflake_shift_x = sd.random_number(-10, 10)
        buffer_point = sd.get_point(snowflake_in_air_param[1], snowflake_in_air_param[2])
        # TODO если точку point определить после
        # TODO snowflake_in_air_param[1] -= snowflake_shift_x
        # TODO snowflake_in_air_param[2] -= snowflake_shift_y
        # TODO то не нужно будет дублировать эти вычисления
        point = sd.get_point(snowflake_in_air_param[1] - snowflake_shift_x,
                             snowflake_in_air_param[2] - snowflake_shift_y)
        sd.start_drawing()  # TODO это можно вынести перед for
        sd.snowflake(center=buffer_point, length=snowflake_in_air_param[0], color=sd.background_color)
        snowflake_in_air_param[1] -= snowflake_shift_x
        snowflake_in_air_param[2] -= snowflake_shift_y
        sd.start_drawing()  # TODO это лишнее
        sd.snowflake(center=point, length=snowflake_in_air_param[0], color=sd.COLOR_WHITE)
        if snowflake_in_air_param[2] <= snowflake_in_air_param[0]:  # TODO при достижении земли, снежинку
            snowflake_in_air_param[2] = sd.random_number(500, 600)  # TODO надо будет добавить в списки
            snowflake_in_air_param[1] = sd.random_number(100, 1100)
            snowflake_in_air_param[0] = sd.random_number(10, 100)
    sd.finish_drawing()
    sd.sleep(0.1)
    if sd.user_want_exit():
        break

sd.pause()
