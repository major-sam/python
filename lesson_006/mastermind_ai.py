from random import randint

from termcolor import cprint
from lesson_006.mastermind_engine import make_secret_num, secret_num, value_check

start_num = []
exclude_buffer = []
bull_buffer = []
res = {}

recheck_flag = True
in_bulls, in_cows = 0, 0


def end_game():
    return res['bulls'] == 4


def make_start_num():
    _try_counter = 0
    start_num.clear()
    while len(start_num) < 4:
        new_num = randint(1, 9)
        if start_num.count(new_num) >= 1:
            continue
        else:
            start_num.append(new_num)
    return start_num


def make_exclude_buffer(start_num_list):
    global exclude_buffer
    exclude_buffer.clear()
    for number1 in range(10):
        if number1 in start_num_list:
            continue
        else:
            exclude_buffer.append(number1)
    return list(exclude_buffer)


def number_testing(some_num):
    global res,  bull_buffer
    sep = ''
    res, try_counter = value_check(some_num)
    bulls, cows = res['bulls'], res['cows']
    cprint('Попытка № {0}\n\t{1}'.format(try_counter, sep.join(map(str, some_num))), 'green')
    cprint('Быков: {}'.format(bulls), 'blue')
    cprint('Коров: {}'.format(cows), 'blue')
    if end_game():
        cprint('Загаданное число: {}'.format(sep.join(map(str, secret_num))), 'blue', attrs=['reverse'])
        new_pick = input("Хотите еще партию? y/n\n")
        if new_pick in ['Y', 'y', 'Yes', 'yes']:
            run_game_with_ai()
        else:
            print('good bay')
            exit(0)
    return bulls, cows


def check_number():
    global start_num, exclude_buffer, _try_counter, recheck_flag, in_bulls, in_cows
    for num_id in range(len(start_num)):
        if recheck_flag:
            in_res = number_testing(start_num)
            in_bulls, in_cows = in_res
            recheck_flag = False
        if in_bulls + in_cows == 4 and in_bulls != 4:
            cprint('switching stage', 'red', attrs=['bold'])
            spacer = randint(0, 9)
            while spacer in start_num:
                spacer = randint(0, 9)
            swap_index = bull_buffer.index(-1)
            bull_buffer.pop(swap_index)
            bull_buffer.insert(swap_index, spacer)
            switcher = start_num.pop(swap_index)
            start_num.insert(swap_index, spacer)
            exclude_buffer.insert(0, switcher)
            recheck_flag = True
            break
        print(exclude_buffer, 'test nums')
        print('testing :', exclude_buffer[0])
        test_list = start_num.copy()
        test_list[num_id] = exclude_buffer[0]
        test_res = number_testing(test_list)
        test_bulls, test_cows = test_res
        if in_bulls < test_bulls:
            if in_cows == test_cows:
                start_num[num_id] = test_list[num_id]
                exclude_buffer.remove(test_list[num_id])
                bull_buffer.pop(num_id)
                bull_buffer.insert(num_id, test_list[num_id])
                print(test_list[num_id], 'is in, at', num_id + 1, 'position\n')
                recheck_flag = True
            elif in_cows > test_cows:
                print(test_list[num_id], 'is in, at', num_id + 1, 'position\n',
                      start_num[num_id], 'is a cow - to next check\n')
                exclude_buffer.remove(test_list[num_id])
                exclude_buffer.insert(0, start_num[num_id])
                bull_buffer.pop(num_id)
                bull_buffer.insert(num_id, test_list[num_id])
                start_num[num_id] = test_list[num_id]
                recheck_flag = True
        elif in_bulls > test_bulls and in_cows == test_cows:
            bull_buffer.pop(num_id)
            bull_buffer.insert(num_id, start_num[num_id])
            print(start_num[num_id], 'is in, at', num_id + 1, 'position\n',
                  test_list[num_id], ' is not in\n removed')
            exclude_buffer.remove(test_list[num_id])
        elif in_bulls + in_cows < test_bulls + test_cows:
            print(test_list[num_id], 'is in\n')
            continue
        elif in_bulls + in_cows <= test_bulls + test_cows != 0:
            print(test_list[num_id], 'maybe in\n')
            continue
        elif in_bulls + in_cows > test_bulls + test_cows:
            exclude_buffer.remove(test_list[num_id])
            print(test_list[num_id], 'not in\n removed')
        else:
            exclude_buffer.remove(test_list[num_id])
            print(test_list[num_id], 'not in\n removed')


def run_game_with_ai():
    global _try_counter, bull_buffer, recheck_flag
    make_secret_num()
    make_start_num()
    recheck_flag = True
    make_exclude_buffer(start_num)
    bull_buffer = [-1, -1, -1, -1]
    while True:
        check_number()


run_game_with_ai()
