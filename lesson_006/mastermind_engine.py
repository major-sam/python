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
    for i in try_list:
        if try_list.count(i) > 1:
            print('в числе не должно быть одинаковых цифр\n')
            user_try()
    _try_counter += 1
    return list(try_num)


def game_mech(try_input):
    global secret_num, res
    res = {'bulls': 0,
           'cows': 0}
    for i in range(4):
        if try_input[i] == secret_num[i]:
            res['bulls'] += 1
        elif try_input[i] in secret_num:
            res['cows'] += 1


def end_game():
    return res['bulls'] == 4


def result():
    return res['bulls'], res['cows'], _try_counter


