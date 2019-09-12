import simple_draw as sd


def draw_tree(start_point, tree_base_angle=90, tree_base_length=100, tree_base_width=5, tree_base_color=(128, 94, 0)):
    if tree_base_length < 3:
        return
    v1 = sd.get_vector(start_point=start_point, angle=tree_base_angle, length=tree_base_length, width=tree_base_width)
    v1.draw(tree_base_color)
    length_delta = sd.random_number(80, 120) / 100
    angle_delta = sd.random_number(60, 140) / 100
    right_angle = tree_base_angle - 30 * angle_delta
    left_angle = tree_base_angle + 30 * angle_delta
    next_point = {right_angle: v1.end_point,
                  left_angle: v1.end_point}
    tree_base_length = tree_base_length * .75 * length_delta
    tree_base_width -= 1
    if tree_base_width < 1:
        tree_base_width = 1
        tree_base_color = sd.COLOR_GREEN
    for angle_switch, point_xy in next_point.items():
        draw_tree(start_point=point_xy, tree_base_angle=angle_switch,
                  tree_base_length=tree_base_length, tree_base_width=tree_base_width,tree_base_color=tree_base_color)



