# -*- coding: utf-8 -*-

import simple_draw as sd

sd.resolution = (1200, 800)

# На основе кода из практической части реализовать снегопад:
# - создать списки данных для отрисовки N снежинок
# - нарисовать падение этих N снежинок
# - создать список рандомных длинн лучей снежинок (от 10 до 100) и пусть все снежинки будут разные
# N = 20
# random_snowflake_on_air_x = []
# random_snowflake_on_air_y = []
# random_snowflake_on_air_size = []
# for snow in range(N):
#     random_snowflake_on_air_size.append(sd.random_number(10, 100))
#     random_snowflake_on_air_y.append(sd.random_number(500, 600))
#     random_snowflake_on_air_x.append(sd.random_number(100, 1100))
# while True:
#     for snowflake_in_air_id in range(N):
#         snowflake_shift_y = sd.random_number(1, 10)
#         buffer_point = sd.get_point(random_snowflake_on_air_x[snowflake_in_air_id],
#                                     random_snowflake_on_air_y[snowflake_in_air_id])
#         sd.start_drawing()
#         sd.snowflake(center=buffer_point,
#                      length=random_snowflake_on_air_size[snowflake_in_air_id],
#                      color=sd.background_color)
#         random_snowflake_on_air_y[snowflake_in_air_id] -= snowflake_shift_y
#         point = sd.get_point(random_snowflake_on_air_x[snowflake_in_air_id],
#                              random_snowflake_on_air_y[snowflake_in_air_id])
#         sd.snowflake(center=point,
#                      length=random_snowflake_on_air_size[snowflake_in_air_id],
#                      color=sd.COLOR_WHITE)
#         if random_snowflake_on_air_y[snowflake_in_air_id] <= random_snowflake_on_air_size[snowflake_in_air_id]:
#             sd.snowflake(center=point,
#                          length=random_snowflake_on_air_size[snowflake_in_air_id],
#                          color=sd.background_color)
#             random_snowflake_on_air_y[snowflake_in_air_id] = sd.random_number(500, 600)
#             random_snowflake_on_air_x[snowflake_in_air_id] = sd.random_number(100, 1100)
#             random_snowflake_on_air_size[snowflake_in_air_id] = sd.random_number(10, 100)
#     sd.finish_drawing()
#     sd.sleep(0.1)
#     if sd.user_want_exit():
#         break
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


N = 20
snowflake_on_flore_count = 0
random_snowflake_on_air_x = []
random_snowflake_on_air_y = []
random_snowflake_on_air_size = []

for snow in range(N):
    random_snowflake_on_air_size.append(sd.random_number(10, 100))
    random_snowflake_on_air_y.append(sd.random_number(500, 800))
    random_snowflake_on_air_x.append(sd.random_number(50, 1150))

while True:
    for snowflake_in_air_id in range(N):
        snowflake_shift_y = sd.random_number(1, 15)
        snowflake_shift_x = sd.random_number(-10, 10)
        buffer_point = sd.get_point(random_snowflake_on_air_x[snowflake_in_air_id],
                                    random_snowflake_on_air_y[snowflake_in_air_id])
        sd.start_drawing()  # TODO вынести наружу списка, тут она не нужна
        sd.snowflake(center=buffer_point,
                     length=random_snowflake_on_air_size[snowflake_in_air_id],
                     color=sd.background_color)
        random_snowflake_on_air_y[snowflake_in_air_id] -= snowflake_shift_y
        random_snowflake_on_air_x[snowflake_in_air_id] -= snowflake_shift_x
        point = sd.get_point(random_snowflake_on_air_x[snowflake_in_air_id],
                             random_snowflake_on_air_y[snowflake_in_air_id])
        sd.snowflake(center=point,
                     length=random_snowflake_on_air_size[snowflake_in_air_id],
                     color=sd.COLOR_WHITE)
        if random_snowflake_on_air_y[snowflake_in_air_id] <= random_snowflake_on_air_size[snowflake_in_air_id]:
            sd.snowflake(center=point,
                         length=random_snowflake_on_air_size[snowflake_in_air_id],
                         color=sd.COLOR_WHITE)
            random_snowflake_on_air_size.append(random_snowflake_on_air_size[snowflake_in_air_id])
            random_snowflake_on_air_y.append(random_snowflake_on_air_y[snowflake_in_air_id])
            random_snowflake_on_air_x.append(random_snowflake_on_air_x[snowflake_in_air_id])
            random_snowflake_on_air_y[snowflake_in_air_id] = sd.random_number(700, 800)
            random_snowflake_on_air_x[snowflake_in_air_id] = sd.random_number(100, 1100)
            random_snowflake_on_air_size[snowflake_in_air_id] = sd.random_number(10, 100)
    sd.finish_drawing()
    sd.sleep(0.1)
    if sd.user_want_exit():
        break
sd.pause()
