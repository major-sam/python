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

# TODO user_try, а именно ввод числа пользователем и проверку этого числа лучше вообще реализовать в 01_mastermind
# TODO в этом же файле оставьте 2 функции - одну, изменяющую глобальную переменную с загаднным числом
# TODO и вторую - принимающую попытку и возвращающую результат.


def user_try():
    global _try_counter
    try_num = input("введите 4х значное число\n")
    while not try_num.isdigit() or len(try_num) != 4:
        try_num = input("введите верное 4х значное число\n")
    try_list = list(try_num)
    wrong_number_counter = 0
    for number in try_list:
        if try_list.count(number) > 1:
            wrong_number_counter += 1
    if wrong_number_counter > 0:
        print('в числе не должно быть одинаковых цифр\n')
        user_try()
    _try_counter += 1
    return list(try_num)


def game_mech(try_input):  # TODO используйте название, которое отражает суть функции (проверку значений)
    global secret_num, res
    res = {'bulls': 0,
           'cows': 0}
    for num_id in range(len(try_input)):
        if try_input[num_id] == secret_num[num_id]:
            # print('бык', try_input[num_id]) # не по правилам
            res['bulls'] += 1
        elif try_input[num_id] in secret_num:
            # print('корова', try_input[num_id]) # не по правилам
            res['cows'] += 1  # TODO результат не обязательно делать глобальным
# TODO он будет использоваться только этой функцией, а обрабатываться в 01
# TODO просто возвращайте его с помощью ретурна


def end_game():  # TODO конец игры тоже вынести из движка
    return res['bulls'] == 4


def result():  # TODO и результат тоже. В движке достаточно оставить изменение числа и проверку
    return res['bulls'], res['cows'], _try_counter


