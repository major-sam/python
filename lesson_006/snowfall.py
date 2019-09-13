import simple_draw as sd

snowflake_x = []
snowflake_y = []
snowflake_size = []
snowflake_on_flour = []


def create_snowflakes(total):
    global snowflake_size, snowflake_x, snowflake_y, snowflake_on_flour
    for snow in range(total):  # TODO т.к. snow не используется в теле цикла, можно его заменить на "_"
        # TODO так будет корректнее
        snowflake_size.append(sd.random_number(10, 30))
        snowflake_y.append(sd.random_number(500, 590))
        snowflake_x.append(sd.random_number(10, 590))
    snowflake_on_flour.clear()  # TODO лучше будет выполнять эту команду в той же функции,
    # TODO в которой пополняется этот список (очистили список --> заполнили)


def draw_snowfall(color):
    global snowflake_size, snowflake_x, snowflake_y
    sd.start_drawing()
    # TODO при вызове после shift может ли быть такое, что снежинка залетит за границу?
    # TODO нужно подумать как лучше реализовать отрисовку сугроба
    # TODO возможно перенести это в функцию, обрабатывающую список упавших снежинок
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


def snow_on_flour():
    global snowflake_on_flour
    for on_flour_id in range(len(snowflake_y)):
        if 0 > snowflake_y[on_flour_id] - snowflake_size[on_flour_id]:
            snowflake_on_flour.append(on_flour_id)
            snowflake_on_flour.sort(reverse=True)
            return True  # TODO один из return-ов сработает на первой же снежинке, до остальных не дойдёт
        # TODO и они не добавятся в список и не удалятся, улетая в бесконченую мглу космоса
        else:
            return False


def on_flore_list():
    return snowflake_on_flour


def remove_snowflake(id_to_remove):
    snowflake_size.pop(id_to_remove)
    snowflake_x.pop(id_to_remove)
    snowflake_y.pop(id_to_remove)
