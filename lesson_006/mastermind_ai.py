from random import randint

from termcolor import cprint
from lesson_006.mastermind_engine import make_secret_num, secret_num, value_check

make_secret_num()  # TODO эту команду стоит добавить в ai_mech()
start_num = []
exclude_buffer = []
bull_buffer = [-1, -1, -1, -1]
res = {}
_try_counter = 0


# TODO здесь и далее - хорошенько подумать над названиями, о чём говорилось в прошлой проверке
# TODO функции - глаголы, отражающий суть выполняемых действий!
def end_game():
    return res['bulls'] == 4


def make_start_num():
    global _try_counter
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


make_start_num()  # TODO стоит и эти команды добавить в ai_mech()
make_exclude_buffer(start_num)


def test_run(some_num):
    global res, _try_counter, bull_buffer
    sep = ''
    res = value_check(some_num)
    bulls, cows = res['bulls'], res['cows']
    cprint('Попытка № {0}\n\t{1}'.format(_try_counter, sep.join(map(str, some_num))), 'green')
    cprint('Быков: {}'.format(bulls), 'blue')
    cprint('Коров: {}'.format(cows), 'blue')
    _try_counter += 1
    if end_game():
        cprint('Загаданное число: {}'.format(sep.join(map(str, secret_num))), 'blue', attrs=['reverse'])
        new_pick = input("Хотите еще партию? y/n\n")
        if new_pick in ['Y', 'y', 'Yes', 'yes']:
            bull_buffer = [-1, -1, -1, -1]
            make_secret_num()  # TODO тогда здесь они будут не нужны
            make_exclude_buffer(start_num)
            ai_mech()
    return bulls, cows


def cycle_run(in_list):
    global start_num, exclude_buffer, _try_counter
    for num_id in range(len(in_list)):
        # TODO start_num и in_list будут ссылаться на один объект
        # TODO почему здесь и далее используется то start_num, то in_list?
        # TODO тк cycle_run всегда подаётся start_num - думаю можно обойтись без in_list
        in_res = test_run(start_num)
        in_bulls, in_cows = in_res
        if in_bulls + in_cows == 4 and in_bulls != 4:
            cprint('switching stage', 'red', attrs=['bold'])
            spacer = randint(0, 9)
            while spacer in in_list:
                spacer = randint(0, 9)
            swap_index = bull_buffer.index(-1)
            bull_buffer.pop(swap_index)
            bull_buffer.insert(swap_index, spacer)
            switcher = in_list.pop(swap_index)
            in_list.insert(swap_index, spacer)
            exclude_buffer.insert(0, switcher)
            break
        print(exclude_buffer, 'test nums')
        print('testing :', exclude_buffer[0])
        test_list = in_list.copy()
        test_list[num_id] = exclude_buffer[0]
        test_res = test_run(test_list)
        test_bulls, test_cows = test_res  # [0], test_res[1]
        # TODO следующее далее дерево решений работает, что круто.
        # TODO Но, зачастую одно и тоже число проверяется множество раз (например я насчитал 9 на одной из итераций)
        # TODO похоже это происходит из-за того, что в начале каждого цикла вы тестируете start_num
        # TODO хотя изменяется он далеко не на каждой итерации
        if in_bulls < test_bulls:
            if in_cows == test_cows:
                start_num[num_id] = test_list[num_id]
                exclude_buffer.remove(test_list[num_id])
                bull_buffer.pop(num_id)
                bull_buffer.insert(num_id, test_list[num_id])
                print(test_list[num_id], 'is in, at', num_id + 1, 'position\n')
            elif in_cows > test_cows:
                print(test_list[num_id], 'is in, at', num_id + 1, 'position\n',
                      start_num[num_id], 'is a cow - to next check\n')
                exclude_buffer.remove(test_list[num_id])
                exclude_buffer.insert(0, start_num[num_id])
                bull_buffer.pop(num_id)
                bull_buffer.insert(num_id, test_list[num_id])
                start_num[num_id] = test_list[num_id]
        elif in_bulls > test_bulls and in_cows == test_cows:
            bull_buffer.pop(num_id)
            bull_buffer.insert(num_id, start_num[num_id])
            print(start_num[num_id], 'is in, at', num_id + 1, 'position\n',
                  test_list[num_id], ' is not in\n')
            if in_cows > test_cows:  # TODO в условии выше in_cows == test_cows - похоже это условие лишнее
                print(test_list[num_id], 'maybe in')
                continue
            else:  # TODO а это выполняется всегда
                print(test_list[num_id], 'not in\n removed')
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


def ai_mech():
    global start_num, _try_counter
    while True:
        in_res = test_run(start_num)  # TODO в функции cycle_run первым делом запускается test_run
        in_bulls, in_cows = in_res  # TODO который уже внутри содержит условие победы и выход из игры
        if in_bulls == 4:  # TODO зачем нужно запускать его тут?
            print('break in while')
            break
        cycle_run(start_num)


ai_mech()
