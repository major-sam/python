# -*- coding: utf-8 -*-

# Написать декоратор, который будет логировать (записывать в лог файл)
# ошибки из декорируемой функции и выбрасывать их дальше.
#
# Имя файла лога - function_errors.log
# Формат лога: <имя функции> <параметры вызова> <тип ошибки> <текст ошибки>
# Лог файл открывать каждый раз при ошибке в режиме 'a'
from functools import wraps


def log_errors(out_file):
    def _log_errors(func):
        def wrapper(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
            except BaseException as log_exc:
                log_line = f'=================\nNAME {func.__name__} \n CALL {func.__call__}\n ' \
                           f'TYPE ' f'{type(log_exc).__name__}\n TEXT {str(log_exc)} \n\r'
                write_file(out_file=out_file, line=log_line)
        return wrapper

    return _log_errors


def write_file(out_file, line, write_param='a+'):
    with open(file=out_file, mode=write_param, encoding='utf8') as source_file:
        source_file.write(line)


# log_errors = partial(_log_errors, out_file='function_errors.log')


# Проверить работу на следующих функциях
@log_errors(out_file='perk_function_errors.log')
def perky(*args, **kwargs):
    for num in kwargs.values():
        print(num)
        return num / 0


@log_errors(out_file='function_errors.log')
def check_line(*args, **kwargs):
    for line in args:
        name, email, age = line.split(' ')
        if not name.isalpha():
            raise ValueError("it's not a name")
        if '@' not in email or '.' not in email:
            raise ValueError("it's not a email")
        if not 10 <= int(age) <= 99:
            raise ValueError('Age not in 10..99 range')


lines = [
    'Ярослав bxh@ya.ru 600',
    'Земфира tslzp@mail.ru 52',
    'Тролль nsocnzas.mail.ru 82',
    'Джигурда wqxq@gmail.com 29',
    'Земфира 86',
    'Равшан wmsuuzsxi@mail.ru 35',
]
for line in lines:
    try:
        check_line(line)
    except Exception as exc:
        print(f'Invalid format: {exc}')
perky(param=42)

# Усложненное задание (делать по желанию).
# Написать декоратор с параметром - именем файла
#
# @log_errors('function_errors.log')
# def func():
#     pass
