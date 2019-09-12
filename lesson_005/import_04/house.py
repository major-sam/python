import simple_draw as sd


def draw_house(base_shift_x, base_shift_y, size_x, size_y, color):
    position_0 = sd.get_point(base_shift_x, base_shift_y)
    position_1 = sd.get_point(base_shift_x + size_x, base_shift_y + size_y)
    sd.rectangle(position_0, position_1, color=color, width=4)
    shift = -1
    for y in range(base_shift_y, size_y + base_shift_y, 50):
        shift = shift * (-1)
        if shift > 0:
            shift_x = 50
        else:
            shift_x = 0
        for x in range(base_shift_x + shift_x, size_x + base_shift_x - shift_x, 100):
            start_x = sd.get_point(x, y)
            end_x = sd.get_point(x + 100, y + 50)
            sd.rectangle(start_x, end_x, width=2)
    roof_1 = sd.get_point(base_shift_x - 25, base_shift_y + size_y)
    roof_2 = sd.get_point(base_shift_x + size_x + 25, base_shift_y + size_y)
    roof_3 = sd.get_point(int(base_shift_x + size_x / 2), size_y + base_shift_y + 100)
    points = (roof_1, roof_2, roof_3)
    sd.polygon(points, color=sd.COLOR_DARK_RED, width=0)


def draw_window(base_shift_x, base_shift_y, size_x, size_y):
    window_1 = sd.get_point(base_shift_x + size_x * .2, base_shift_y + size_y * .3)
    window_2 = sd.get_point(base_shift_x + size_x * .8, base_shift_y + size_y * .8)
    sd.rectangle(window_1, window_2, width=0, color=sd.background_color)
    sd.rectangle(window_1, window_2, width=4, color=sd.COLOR_DARK_RED)
