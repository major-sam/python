# -*- coding: utf-8 -*-
import random

# День сурка
#
# Напишите функцию one_day() которая возвращает количество кармы от 1 до 7
# и может выкидывать исключения:
# - IamGodError
# - DrunkError
# - CarCrashError
# - GluttonyError
# - DepressionError
# - SuicideError
# Одно из этих исключений выбрасывается с вероятностью 1 к 13 каждый день
#
# Функцию оберните в бесконечный цикл, выход из которого возможен только при накоплении
# кармы до уровня ENLIGHTENMENT_CARMA_LEVEL. Исключения обработать и записать в лог.
# При создании собственных исключений максимально использовать функциональность
# базовых встроенных исключений.

ENLIGHTENMENT_CARMA_LEVEL = 777


class IamGodError(Exception):
    pass


class DrunkError(Exception):
    pass


class CarCrashError(Exception):
    pass


class GluttonyError(Exception):
    pass


class DepressionError(Exception):
    pass


class SuicideError(Exception):
    pass


def day():
    random_error = random.randint(1, 13)
    random_carma = 0
    if random_error == 13:
        dice = random.randint(1, 6)
        if dice == 1:
            raise IamGodError('IDDQD')  # Оригинальная отсылка :)
        elif dice == 2:
            raise DrunkError("too drunk")
        elif dice == 3:
            raise CarCrashError("in car crush")
        elif dice == 4:
            raise GluttonyError("eat too much food")
        elif dice == 5:
            raise DepressionError("too sad")
        elif dice == 6:
            raise SuicideError("too dead")
    else:
        random_carma = random.randint(1, 7)
    return random_carma


carma, day_number = 0, 0
while carma < ENLIGHTENMENT_CARMA_LEVEL:
    day_number += 1
    try:
        carma += day()
    except Exception as exc:
        print(f'on day {day_number} i am {exc}, current carma is {carma}')
    else:
        print(f'on day {day_number} i am ok, current carma is {carma}')
# https://goo.gl/JnsDqu
#зачет!