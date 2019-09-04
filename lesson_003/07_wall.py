# -*- coding: utf-8 -*-

# (цикл for)
import simple_draw as sd

# Нарисовать стену из кирпичей. Размер кирпича - 100х50
# Использовать вложенные циклы for
shift = 0
for y in range(0, 601, 50):
    start_y = sd.get_point(0, y)
    end_y = sd.get_point(601, y)
    sd.line(start_y, end_y, width=2, color=sd.COLOR_DARK_YELLOW)
    for x in range(shift, 601 - shift, 100):
        start_x = sd.get_point(x, y-50)
        end_x = sd.get_point(x, y)
        sd.line(start_x, end_x, width=3, color=sd.COLOR_DARK_YELLOW)
    shift -= 50


sd.pause()
