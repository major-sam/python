import simple_draw as sd

snowflake_x = []
snowflake_y = []
snowflake_size = []
snowflake_on_flour = []


def create_snowflakes(total):
    global snowflake_size, snowflake_x, snowflake_y, snowflake_on_flour
    for _ in range(total):
        snowflake_size.append(sd.random_number(10, 30))
        snowflake_y.append(sd.random_number(500, 590))
        snowflake_x.append(sd.random_number(10, 590))


def draw_snowfall(color):
    global snowflake_size, snowflake_x, snowflake_y
    sd.start_drawing()
    for snowflake_id in range(len(snowflake_y)):
        point = sd.get_point(snowflake_x[snowflake_id],
                             snowflake_y[snowflake_id])
        sd.snowflake(center=point,
                     length=snowflake_size[snowflake_id],
                     color=color)
    sd.finish_drawing()


def shift_snowfall():
    for snowflake_id in range(len(snowflake_y)):
        snowflake_shift_y = sd.random_number(1, 15)
        snowflake_shift_x = sd.random_number(-10, 10)
        snowflake_y[snowflake_id] -= snowflake_shift_y
        snowflake_x[snowflake_id] -= snowflake_shift_x
        if snowflake_y[snowflake_id] < snowflake_size[snowflake_id]:
            snowflake_y[snowflake_id] = snowflake_size[snowflake_id]


def snow_on_flour():
    global snowflake_on_flour
    snowflake_on_flour.clear()
    for on_flour_id in range(len(snowflake_y)):
        if 0 >= snowflake_y[on_flour_id] - snowflake_size[on_flour_id]:
            snowflake_on_flour.append(on_flour_id)
            snowflake_on_flour.sort(reverse=True)
    return snowflake_on_flour


def on_flore_list():
    return snowflake_on_flour


def remove_snowflake(id_to_remove):
    snowflake_size.pop(id_to_remove)
    snowflake_x.pop(id_to_remove)
    snowflake_y.pop(id_to_remove)
#зачет!