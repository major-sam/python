from random import randint

secret_num = []
res = {}
_try_counter = 0


def make_secret_num():
    global secret_num
    secret_num.clear()
    secret_num.append(str(randint(1, 9)))
    while len(secret_num) < 4:
        new_num = str(randint(0, 9))
        if secret_num.count(new_num) >= 1:
            continue
        else:
            secret_num.append(new_num)


def user_try():
    global _try_counter
    try_num = input("введите 4х значное число\n")
    while not try_num.isdigit() or len(try_num) != 4:
        try_num = input("введите верное 4х значное число\n")
    try_list = list(try_num)
    for i in try_list:  # TODO вместо i нужно название поинтереснее
        # TODO протестируйте этот цикл
        if try_list.count(i) > 1:  # TODO это условие срабатывает для каждой повторяющейся цифры
            print('в числе не должно быть одинаковых цифр\n')
            user_try()  # TODO каждая из повторяющихся цифр запускает эту функцию ещё раз, нужно это исправить
            # TODO и это число после нескольких попыток всёравно попадает в game_mech()
    _try_counter += 1
    return list(try_num)


def game_mech(try_input):
    global secret_num, res
    print(try_input)
    res = {'bulls': 0,
           'cows': 0}
    for i in range(4):  # TODO тут тоже нэйминг, я верю в ваше воображение!
        # TODO + лучше пройти циклом по списку
        if try_input[i] == secret_num[i]:
            print('бык', try_input[i])
            res['bulls'] += 1
        elif try_input[i] in secret_num:
            print('корова', try_input[i])
            res['cows'] += 1


def end_game():
    return res['bulls'] == 4


def result():
    return res['bulls'], res['cows'], _try_counter


