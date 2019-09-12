import simple_draw as sd


def draw_rainbow(center, radius, colors_arr, rainbow_width):
    for colors in colors_arr:
        sd.circle(center_position=center, radius=radius, color=colors, width=rainbow_width)
        radius -= rainbow_width


