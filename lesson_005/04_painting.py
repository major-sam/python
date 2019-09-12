# -*- coding: utf-8 -*-
import simple_draw as sd
from sun import draw_sun
from house import draw_house, draw_window
from tree import draw_tree
from smile import draw_smile
from rainbow import draw_rainbow
from snowfall import draw_snowfall

# Создать пакет, в который скопировать функции отрисовки из предыдущего урока
#  - радуги
#  - стены
#  - дерева
#  - смайлика
#  - снежинок
# Функции по модулям разместить по тематике. Название пакета и модулей - по смыслу.
# Создать модуль с функцией отрисовки кирпичного дома с широким окном и крышей.

# С помощью созданного пакета нарисовать эпохальное полотно "Утро в деревне".
# На картине должны быть:
#  - кирпичный дом, в окошке - смайлик.
#  - слева от дома - сугроб (предположим что это ранняя весна)
#  - справа от дома - дерево (можно несколько)
#  - справа в небе - радуга, слева - солнце (весна же!)
# пример см. lesson_005/results/04_painting.jpg
# Приправить своей фантазией по вкусу (коты? коровы? люди? трактор? что придумается)

sd.resolution = (1200, 800)

sun_point = sd.get_point(200, 700)
sun_color = sd.COLOR_YELLOW
sun_angle = 0
switch = 1
draw_sun(sun_point, color=sun_color, angle=sun_angle)

house_base_x, house_base_y, house_size_x, house_size_y = 450, 50, 300, 400
draw_house(house_base_x, house_base_y, house_size_x, house_size_y, sd.COLOR_YELLOW)
draw_window(house_base_x, house_base_y, house_size_x, house_size_y)
draw_smile(house_base_x, house_base_y, house_size_x, house_size_y, sd.random_color())

rainbow_center = sd.get_point(100, -20)
rainbow_colors = [sd.COLOR_RED, sd.COLOR_ORANGE, sd.COLOR_YELLOW, sd.COLOR_GREEN,
                  sd.COLOR_CYAN, sd.COLOR_BLUE, sd.COLOR_PURPLE]
draw_rainbow(rainbow_center, 1200, rainbow_colors, 8)

tree_point = sd.get_point(house_base_x + house_size_x + 200, house_base_y)
draw_tree(start_point=tree_point, tree_base_angle=90, tree_base_length=100)

total_num = 10
snowflake_shift_y = sd.random_number(1, 15)
snowflake_shift_x = sd.random_number(-10, 10)
random_snowflake_on_air_x = []
random_snowflake_on_air_y = []
random_snowflake_on_air_size = []
for snow in range(total_num):
    random_snowflake_on_air_size.append(sd.random_number(10, 30))
    random_snowflake_on_air_y.append(sd.random_number(300, 500))
    random_snowflake_on_air_x.append(sd.random_number(10, 250))
draw_snowfall(house_base_y, total_num, random_snowflake_on_air_x,
              random_snowflake_on_air_y,
              random_snowflake_on_air_size)
sd.rectangle(sd.get_point(0, 0), sd.get_point(1200, house_base_y), color=(61, 37, 0))
sd.start_drawing()
while True:
    draw_window(house_base_x, house_base_y, house_size_x, house_size_y)
    draw_smile(house_base_x, house_base_y, house_size_x, house_size_y, sd.random_color())
    draw_sun(sun_point, color=sd.background_color, angle=sun_angle)
    sun_angle += 10
    draw_sun(sun_point, color=sun_color, angle=sun_angle)
    s = rainbow_colors.pop(0)
    draw_rainbow(rainbow_center, 1200, rainbow_colors, 8)
    rainbow_colors.append(s)
    draw_snowfall(house_base_y, total_num, random_snowflake_on_air_x,
                  random_snowflake_on_air_y,
                  random_snowflake_on_air_size)
    sd.finish_drawing()
    sd.sleep(0.1)
    if sd.user_want_exit():
        break

# Усложненное задание (делать по желанию)
# Анимировать картину.
# Пусть слева идет снегопад, радуга переливается цветами, смайлик моргает, солнце крутит лучами, етс.
# Задержку в анимировании все равно надо ставить, пусть даже 0.01 сек - так библиотека устойчивей работает.
