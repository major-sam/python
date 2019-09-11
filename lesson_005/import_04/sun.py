import simple_draw as sd


def draw_sun(start_point, angle=0, length=60, width=4, color=sd.COLOR_YELLOW):
    for angle in range(angle, 360 + angle, 30):
        v1 = sd.get_vector(start_point=start_point, angle=angle, length=length, width=width)
        v1.draw(color=color)
    sd.circle(start_point, radius=int(length*.7), color=color, width=0)


