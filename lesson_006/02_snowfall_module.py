# -*- coding: utf-8 -*-

import simple_draw as sd
from lesson_006.snowfall import create_snowflakes, draw_snowfall, shift_snowfall, snow_on_flour, remove_snowflake, \
    on_flore_list

# На основе кода из lesson_004/05_snowfall.py
# сделать модуль snowfall.py в котором реализовать следующие функции
#  создать_снежинки(N) - создает N снежинок
#  нарисовать_снежинки_цветом(color) - отрисовывает все снежинки цветом color
#  сдвинуть_снежинки() - сдвигает снежинки на один шаг
#  номера_достигших_низа_экрана() - выдает список номеров снежинок, которые вышли за границу экрана
#  удалить_снежинки(номера) - удаляет снежинки с номерами из списка
#
# В текущем модуле реализовать главный цикл падения снежинок,
# обращаясь ТОЛЬКО к функциям модуля snowfall

# создать_снежинки(N)
create_snowflakes(20)
while True:
    #  нарисовать_снежинки_цветом(color=sd.background_color)
    draw_snowfall(sd.background_color)
    #  сдвинуть_снежинки()
    shift_snowfall()
    #  нарисовать_снежинки_цветом(color)
    draw_snowfall(sd.COLOR_WHITE)
    #  если есть номера_достигших_низа_экрана() то
    if snow_on_flour() is not None:
        #       удалить_снежинки(номера)
        snowflake_on_flour = on_flore_list()
        for remove_id in snowflake_on_flour:
            remove_snowflake(remove_id)
        #       создать_снежинки(count)
        create_snowflakes(len(snowflake_on_flour))

    sd.sleep(0.1)
    if sd.user_want_exit():
        break

sd.pause()
#зачет!