from random import randint

secret_num = []
try_counter = 0


def make_secret_num():
    global secret_num, try_counter
    try_counter = 0
    secret_num.clear()
    secret_num.append(randint(1, 9))
    while len(secret_num) < 4:
        new_num = randint(0, 9)
        if secret_num.count(new_num) >= 1:
            continue
        else:
            secret_num.append(new_num)


def value_check(try_input):
    global secret_num, try_counter
    res = {'bulls': 0,
           'cows': 0}
    try_counter += 1
    for num_id in range(len(try_input)):
        if try_input[num_id] == secret_num[num_id]:
            # print('бык', try_input[num_id]) # не по правилам
            res['bulls'] += 1
        elif try_input[num_id] in secret_num:
            # print('корова', try_input[num_id]) # не по правилам
            res['cows'] += 1
    return res, try_counter
#зачет!