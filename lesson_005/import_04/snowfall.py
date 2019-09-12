import simple_draw as sd


def draw_snowfall(house_base_y, total_num, random_snowflake_on_air_x, random_snowflake_on_air_y,
                  random_snowflake_on_air_size):
    sd.start_drawing()
    for snowflake_in_air_id in range(total_num):
        snowflake_shift_y = sd.random_number(1, 15)
        snowflake_shift_x = sd.random_number(-10, 10)
        buffer_point = sd.get_point(random_snowflake_on_air_x[snowflake_in_air_id],
                                    random_snowflake_on_air_y[snowflake_in_air_id])
        sd.snowflake(center=buffer_point,
                     length=random_snowflake_on_air_size[snowflake_in_air_id],
                     color=sd.background_color)
        random_snowflake_on_air_y[snowflake_in_air_id] -= snowflake_shift_y
        random_snowflake_on_air_x[snowflake_in_air_id] -= snowflake_shift_x
        point = sd.get_point(random_snowflake_on_air_x[snowflake_in_air_id],
                             random_snowflake_on_air_y[snowflake_in_air_id])
        sd.snowflake(center=point,
                     length=random_snowflake_on_air_size[snowflake_in_air_id],
                     color=sd.COLOR_WHITE)
        if random_snowflake_on_air_y[snowflake_in_air_id] <= random_snowflake_on_air_size[snowflake_in_air_id] + house_base_y:
            sd.snowflake(center=point,
                         length=random_snowflake_on_air_size[snowflake_in_air_id],
                         color=sd.COLOR_WHITE)
            random_snowflake_on_air_size.append(random_snowflake_on_air_size[snowflake_in_air_id])
            random_snowflake_on_air_y.append(random_snowflake_on_air_y[snowflake_in_air_id])
            random_snowflake_on_air_x.append(random_snowflake_on_air_x[snowflake_in_air_id])
            random_snowflake_on_air_y[snowflake_in_air_id] = sd.random_number(500, 600)
            random_snowflake_on_air_x[snowflake_in_air_id] = sd.random_number(10, 250)
            random_snowflake_on_air_size[snowflake_in_air_id] = sd.random_number(10, 30)
