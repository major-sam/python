import simple_draw as sd


def draw_house(start_h_x, start_h_y, size_x, size_y, color):
    position_0 = sd.get_point(start_h_x, start_h_y)
    position_1 = sd.get_point(start_h_x + size_x, start_h_y + size_y)
    sd.rectangle(position_0, position_1, color=color, width=4)
    shift = -1
    shift_1 = 0
    for y in range(start_h_y, size_y + start_h_y, 50):
        shift = shift * (-1)
        for x in range(start_h_x, size_x + start_h_x+shift_1, 100):
            start_x = sd.get_point(x, y)
            end_x = sd.get_point(x + 100, y + 50)
            # if (start_h_x <= x) | (x <= start_h_x + size_x - 101 & shift < 0):
            sd.rectangle(start_x, end_x, width=2)
        if shift > 0:
            start_h_x += 50
            shift_1 = 0
        else:
            start_h_x -= 50
            shift_1 = -50
    roof_1 = sd.get_point(start_h_x - 25, start_h_y + size_y)
    roof_2 = sd.get_point(start_h_x + size_x + 25, start_h_y + size_y)
    roof_3 = sd.get_point(int(start_h_y + size_x / 2), size_y + start_h_y + 100)
    points = (roof_1, roof_2, roof_3)
    sd.polygon(points, color=sd.COLOR_DARK_RED, width=0)
    window_1 = sd.get_point(start_h_x + size_x * .2, start_h_y + size_x * .3)
    window_2 = sd.get_point(start_h_x + size_x * .8, start_h_y + size_x * .8)
    sd.rectangle(window_1, window_2, width=0, color=sd.background_color)
    sd.rectangle(window_1, window_2, width=4, color=sd.COLOR_DARK_RED)


draw_house(50, 50, 300, 400, sd.COLOR_YELLOW)
sd.pause()
