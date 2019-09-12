import simple_draw as sd


def draw_smile(base_shift_x, base_shift_y, size_x, size_y, color, radius=60):
    center_x = sd.random_number(base_shift_x + size_x * .2 + radius,
                                base_shift_x + size_x * .8 - radius)

    center_y = sd.random_number(base_shift_y + size_y * .3 + radius,
                                base_shift_y + size_y * .8 - radius)
    center = sd.get_point(center_x, center_y)
    sd.circle(center, radius=radius, color=color, width=2)
    mouth_y = center_y - 25
    mouth_x = center_x - 20
    mouth_start = sd.get_point(mouth_x, mouth_y)
    mouth_end = sd.get_point(mouth_x + 40, mouth_y)
    sd.line(mouth_start, mouth_end, width=2, color=color)
    left_eye_y = center_y + 15
    left_eye_x = center_x - 10
    left_eye_start = sd.get_point(left_eye_x, left_eye_y)
    left_eye_end = sd.get_point(left_eye_x - 30, left_eye_y)
    sd.line(left_eye_start, left_eye_end, width=2, color=color)
    right_eye_y = center_y + 15
    right_eye_x = center_x + 10
    right_eye_start = sd.get_point(right_eye_x, right_eye_y)
    right_eye_end = sd.get_point(right_eye_x + 30, right_eye_y)
    sd.line(right_eye_start, right_eye_end, width=2, color=color)

